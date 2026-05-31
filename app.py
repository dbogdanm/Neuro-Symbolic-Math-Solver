"""Flask app for the Neuro-Symbolic Math-OS.

Bring Your Own API Key (BYOK): every request carries the provider / model /
key chosen in the browser. Nothing is stored server-side. The two supported
providers are a local Ollama server (free, no key) and OpenRouter (the user's
own key, 300+ models).
"""

import json
import logging
import os
import queue
import threading
import time

from flask import Flask, Response, render_template, request, stream_with_context
import requests

import llm as llm_layer
from llm import LLMConfig, LLMError
from neuro_symbolic import run_neuro_symbolic_pipeline
from web_search import get_web_hint

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
PORT = int(os.environ.get("PORT", "5000"))


def _sse(payload: dict) -> str:
    """Format a dict as a Server-Sent Events frame."""
    return f"data: {json.dumps(payload)}\n\n"


# --------------------------------------------------------------------------- #
# Pages & meta
# --------------------------------------------------------------------------- #

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return {
        "status": "ok",
        "default_ollama": llm_layer.DEFAULT_OLLAMA_BASE,
        "default_ollama_model": llm_layer.DEFAULT_OLLAMA_MODEL,
        "default_openrouter_model": llm_layer.DEFAULT_OPENROUTER_MODEL,
        "has_server_key": bool(llm_layer.ENV_OPENROUTER_KEY),
    }


@app.route("/api/openrouter/models")
def openrouter_models():
    """Proxy OpenRouter's public model catalogue (no key required).

    Returns a trimmed list for the settings model picker. Degrades gracefully
    to an empty list so the UI can fall back to its built-in suggestions.
    """
    try:
        resp = requests.get(f"{llm_layer.OPENROUTER_BASE}/models", timeout=10)
        resp.raise_for_status()
        models = []
        for m in resp.json().get("data", []):
            pricing = m.get("pricing", {}) or {}
            is_free = str(pricing.get("prompt", "0")) in ("0", "0.0", "0.00")
            models.append({
                "id": m.get("id"),
                "name": m.get("name", m.get("id")),
                "context": m.get("context_length"),
                "free": is_free,
            })
        models.sort(key=lambda x: (not x["free"], x["id"] or ""))
        return {"models": models}
    except Exception as exc:  # noqa: BLE001
        app.logger.warning("OpenRouter models fetch failed: %s", exc)
        return {"models": [], "error": str(exc)}


# --------------------------------------------------------------------------- #
# Direct chat (any provider/model)
# --------------------------------------------------------------------------- #

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required"}, 400

    cfg = LLMConfig.from_request(data)

    def gen():
        start = time.time()
        try:
            for token in llm_layer.stream(cfg, prompt, temperature=0.6, num_ctx=16384):
                if token:
                    yield _sse({"text": token})
            yield _sse({"done": True, "time": round(time.time() - start, 2)})
        except LLMError as exc:
            yield _sse({"error": str(exc), "done": True})
        except Exception as exc:  # noqa: BLE001
            app.logger.error("generate error: %s", exc)
            yield _sse({"error": str(exc), "done": True})

    return Response(stream_with_context(gen()), content_type="text/event-stream")


# --------------------------------------------------------------------------- #
# Web-RAG mode (live search + grounded generation)
# --------------------------------------------------------------------------- #

@app.route("/api/web_rag", methods=["POST"])
def web_rag_endpoint():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required"}, 400

    cfg = LLMConfig.from_request(data)

    def gen():
        start = time.time()
        yield _sse({"step": "LOG: Initiating Web Search..."})
        context = get_web_hint(prompt)
        if context:
            yield _sse({"step": "LOG: Web context retrieved."})
            yield _sse({"step": "PROMPT: " + context})
        else:
            yield _sse({"step": "LOG: No web context found. Relying on base knowledge."})

        current_date = time.strftime("%A, %B %d, %Y")
        augmented_prompt = (
            "<SYSTEM_CONTEXT>\n"
            f"CURRENT_DATE: {current_date}\n"
            "LIVE_SEARCH_DATA:\n"
            f"{context if context else 'No live data returned from the search engine.'}\n\n"
            "INSTRUCTIONS:\n"
            f"- Treat {current_date} as today's date and the live data above as current and accurate.\n"
            "- Do not refuse based on a training cutoff; use the provided data to answer.\n"
            "- If the data is insufficient, say so and give the last known state as historical context.\n"
            "</SYSTEM_CONTEXT>\n\n"
            f"USER_REQUEST: {prompt}"
        )

        try:
            for token in llm_layer.stream(cfg, augmented_prompt, temperature=0.3, num_ctx=16384):
                if token:
                    yield _sse({"text": token})
            yield _sse({"done": True, "time": round(time.time() - start, 2)})
        except LLMError as exc:
            yield _sse({"error": str(exc), "done": True})
        except Exception as exc:  # noqa: BLE001
            app.logger.error("web_rag error: %s", exc)
            yield _sse({"error": str(exc), "done": True})

    return Response(stream_with_context(gen()), content_type="text/event-stream")


# --------------------------------------------------------------------------- #
# Neuro-symbolic pipeline
# --------------------------------------------------------------------------- #

@app.route("/api/neuro_symbolic", methods=["POST"])
def neuro_symbolic_endpoint():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required"}, 400

    cfg = LLMConfig.from_request(data)

    def gen():
        q: "queue.Queue" = queue.Queue()

        def ui_callback(msg):
            q.put(msg)

        def run_pipeline():
            try:
                result = run_neuro_symbolic_pipeline(prompt, llm=cfg, ui_callback=ui_callback)
                q.put(f"FINAL_RESULT:{result}")
            except Exception as e:  # noqa: BLE001
                q.put(f"ERROR:{str(e)}")
            finally:
                q.put(None)

        threading.Thread(target=run_pipeline, daemon=True).start()

        while True:
            msg = q.get()
            if msg is None:
                break
            if msg.startswith("FINAL_RESULT:"):
                yield _sse({"final_answer": msg[len("FINAL_RESULT:"):], "done": True})
            elif msg.startswith("ERROR:"):
                yield _sse({"error": msg[len("ERROR:"):], "done": True})
            else:
                yield _sse({"step": msg})

    return Response(stream_with_context(gen()), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)

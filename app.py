from flask import Flask, render_template, request, Response, stream_with_context, jsonify
import requests
import json
import logging
import time
from neuro_symbolic import run_neuro_symbolic_pipeline
from web_search import get_web_hint

import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


DOCKER_DEFAULT_HOST = "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"

MODEL_8B = os.environ.get("MODEL_8B", "deepseek-r1:8b")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_URL", f"http://{DOCKER_DEFAULT_HOST}:11434")
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
URL_PC = os.environ.get("URL_PC", f"http://{DOCKER_DEFAULT_HOST}:11434/api/generate")

HEADERS_COLAB = {"Bypass-Tunnel-Reminder": "true"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/web_rag", methods=["POST"])
def web_rag_endpoint():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "Prompt is required"}, 400

    def generate_web_rag():
        yield f"data: {json.dumps({'step': 'LOG: Initiating Web Search...'})}\n\n"
        context = get_web_hint(prompt)
        
        if context:
            yield f"data: {json.dumps({'step': 'LOG: Web context retrieved.'})}\n\n"
            yield f"data: {json.dumps({'step': 'PROMPT: ' + context})}\n\n"
        else:
            yield f"data: {json.dumps({'step': 'LOG: No web context found. Relying on base knowledge with current time context.'})}\n\n"

        current_date = time.strftime("%A, %B %d, %Y")
        
        # Super-strict grounding instruction to bypass model's internal cutoff refusal
        augmented_prompt = (
            f"<SYSTEM_OVERRIDE>\n"
            f"ACTUAL_CURRENT_DATE: {current_date}\n"
            f"LIVE_SEARCH_DATA_FROM_2026:\n{context if context else 'STRICT WARNING: NO LIVE DATA RETURNED FROM SEARCH ENGINE.'}\n\n"
            "MANDATORY PROTOCOLS:\n"
            "- YOU ARE OPERATING IN REAL-TIME. Your knowledge is NO LONGER limited to your 2023/2024 training cutoff.\n"
            "- THE DATE ABOVE ({current_date}) IS THE ABSOLUTE TRUTH. If your internal memory says it's 2023, YOU ARE WRONG.\n"
            "- THE LIVE_SEARCH_DATA IS CURRENT AND ACCURATE FOR 2026. Use it to answer the question below.\n"
            "- DO NOT apologize for your 'knowledge cutoff'. DO NOT state you cannot predict the future.\n"
            "- If the search data is available, answer definitively based on it.\n"
            "- If no data is available, admit you cannot find the *2026* status for this query and provide the last known state from 2024 as a historical reference only.\n"
            "</SYSTEM_OVERRIDE>\n\n"
            f"USER_REQUEST: {prompt}"
        )
        
        payload = {
            "model": MODEL_8B,
            "prompt": augmented_prompt,
            "stream": True,
            "options": {"temperature": 0.3, "num_ctx": 16384}
        }
        
        start_time = time.time()
        try:
            with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=400) as resp:
                resp.raise_for_status()
                full_text = ""
                for line in resp.iter_lines():
                    if line:
                        chunk_str = line.decode('utf-8')
                        try:
                            chunk = json.loads(chunk_str)
                            token = chunk.get("response", "")
                            if token:
                                full_text += token
                                yield f"data: {json.dumps({'text': token})}\n\n"
                            if chunk.get("done"):
                                duration = round(time.time() - start_time, 2)
                                yield f"data: {json.dumps({'done': True, 'time': duration})}\n\n"
                                break
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate_web_rag()), content_type="text/event-stream")

@app.route("/api/neuro_symbolic", methods=["POST"])
def neuro_symbolic_endpoint():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "Prompt is required"}, 400

    def generate_ns():
        q = queue.Queue()
        
        def ui_callback(msg):
            q.put(msg)

        def run_pipeline():
            try:
                result = run_neuro_symbolic_pipeline(prompt, model=MODEL_8B, ui_callback=ui_callback)
                q.put(f"FINAL_RESULT:{result}")
            except Exception as e:
                q.put(f"ERROR:{str(e)}")
            finally:
                q.put(None) # End signal

        threading.Thread(target=run_pipeline).start()

        while True:
            msg = q.get()
            if msg is None:
                break
            
            if msg.startswith("FINAL_RESULT:"):
                yield f"data: {json.dumps({'final_answer': msg[13:], 'done': True})}\n\n"
            elif msg.startswith("ERROR:"):
                yield f"data: {json.dumps({'error': msg[6:], 'done': True})}\n\n"
            else:
                yield f"data: {json.dumps({'step': msg})}\n\n"

    return Response(stream_with_context(generate_ns()), content_type="text/event-stream")

import threading
import queue

def generate_stream(url, payload, headers=None):
    import time
    start_time = time.time()
    try:
        kwargs = {"json": payload, "stream": True, "timeout": 400}
        if headers:
            kwargs["headers"] = headers

        with requests.post(url, **kwargs) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        if token:
                            
                            data = json.dumps({"text": token})
                            yield f"data: {data}\n\n"
                        if chunk.get("done"):
                            duration = round(time.time() - start_time, 2)
                            done_data = json.dumps({"done": True, "time": duration})
                            yield f"data: {done_data}\n\n"
                            break
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        app.logger.error(f"Error streaming from {url}: {e}")
        error_msg = json.dumps({"text": f"\n\n[Error]: {str(e)}"})
        yield f"data: {error_msg}\n\n"
        yield f"data: {json.dumps({'done': True, 'time': 0})}\n\n"

@app.route("/api/generate/<model_type>", methods=["POST"])
def generate(model_type):
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return {"error": "Prompt is required"}, 400

    if model_type == "8b":
        payload = {
            "model": MODEL_8B,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.6,
                "num_predict": 8192,
                "num_ctx": 16384,
            }
        }
        return Response(stream_with_context(generate_stream(OLLAMA_URL, payload)), content_type="text/event-stream")
    
    elif model_type == "14b":
        payload = {
            "model": "deepseek-r1:14b",
            "prompt": prompt,
            "stream": True
        }
        return Response(stream_with_context(generate_stream(URL_PC, payload)), content_type="text/event-stream")
    
    else:
        return {"error": "Invalid model type"}, 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)

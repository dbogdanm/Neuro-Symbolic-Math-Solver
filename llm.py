"""Unified LLM provider layer — Bring Your Own API Key (BYOK).

This module is the single place the rest of the app talks to an LLM. It hides
the differences between providers behind two functions, :func:`complete`
(blocking) and :func:`stream` (token generator), plus an :class:`LLMConfig`
that describes *which* model to hit and *with whose* credentials.

Supported providers
--------------------
* ``ollama``     – a local Ollama server. No API key. Free. Default.
* ``openrouter`` – the universal OpenAI-compatible gateway (300+ models behind
                   a single key). The user brings their own key.
* ``gemini``     – native Google Gemini API (AI Studio). User brings their key.
* ``openai``     – native OpenAI API. User brings their key.
* ``anthropic``  – native Anthropic API. User brings their key.

Privacy contract
----------------
API keys are **never persisted server-side**. They arrive on each request
(forwarded from the browser's ``localStorage``) inside the :class:`LLMConfig`
and live only for the duration of that single call. Nothing is logged, cached,
or written to disk.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterator, Optional

import requests

# --------------------------------------------------------------------------- #
# Defaults / environment
# --------------------------------------------------------------------------- #

_IN_DOCKER = os.path.exists("/.dockerenv")
_DEFAULT_HOST = "host.docker.internal" if _IN_DOCKER else "localhost"

# Ollama base (e.g. http://localhost:11434). The /api/generate path is appended.
DEFAULT_OLLAMA_BASE = os.environ.get(
    "OLLAMA_URL", f"http://{_DEFAULT_HOST}:11434"
).rstrip("/")
DEFAULT_OLLAMA_MODEL = os.environ.get("MODEL_8B", "deepseek-r1:8b")

OPENROUTER_BASE = os.environ.get(
    "OPENROUTER_URL", "https://openrouter.ai/api/v1"
).rstrip("/")
DEFAULT_OPENROUTER_MODEL = os.environ.get(
    "OPENROUTER_MODEL", "deepseek/deepseek-r1"
)

GEMINI_BASE = os.environ.get(
    "GEMINI_URL", "https://generativelanguage.googleapis.com/v1beta"
).rstrip("/")
DEFAULT_GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

OPENAI_BASE = os.environ.get("OPENAI_URL", "https://api.openai.com/v1").rstrip("/")
DEFAULT_OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

ANTHROPIC_BASE = os.environ.get("ANTHROPIC_URL", "https://api.anthropic.com/v1").rstrip("/")
DEFAULT_ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")


# Optional server-side fallback key (so a deployer *can* provide a default key
# if they want to). BYOK keys from the request always take precedence.
ENV_OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
ENV_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
ENV_OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
ENV_ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Sent to OpenRouter for attribution / rankings (purely informational).
_REFERER = os.environ.get("OPENROUTER_REFERER", "http://localhost:5000")
_TITLE = "Neuro-Symbolic Math-OS"


class LLMError(RuntimeError):
    """Raised for provider/transport errors with a user-friendly message."""


@dataclass
class LLMConfig:
    """Everything needed to make one LLM call.

    Attributes
    ----------
    provider : "ollama" | "openrouter" | "gemini" | "openai" | "anthropic"
    model    : model identifier for the chosen provider
    api_key  : the user's key (cloud providers only); never stored
    base_url : optional override for the provider base URL
    """

    provider: str = "ollama"
    model: str = DEFAULT_OLLAMA_MODEL
    api_key: Optional[str] = None
    base_url: Optional[str] = None

    # -- construction ------------------------------------------------------- #
    @classmethod
    def from_request(cls, data: Optional[dict]) -> "LLMConfig":
        """Build a config from a JSON request body.

        Recognised keys: ``provider``, ``model``, ``api_key`` (or ``apiKey``),
        ``base_url`` (or ``baseUrl``). Missing values fall back to sane
        provider-specific defaults.
        """
        data = data or {}
        provider = str(data.get("provider") or "ollama").lower().strip()
        if provider not in ("ollama", "openrouter", "gemini", "openai", "anthropic"):
            provider = "ollama"

        model = (data.get("model") or "").strip()
        if not model:
            if provider == "openrouter":
                model = DEFAULT_OPENROUTER_MODEL
            elif provider == "gemini":
                model = DEFAULT_GEMINI_MODEL
            elif provider == "openai":
                model = DEFAULT_OPENAI_MODEL
            elif provider == "anthropic":
                model = DEFAULT_ANTHROPIC_MODEL
            else:
                model = DEFAULT_OLLAMA_MODEL

        api_key = (data.get("api_key") or data.get("apiKey") or "").strip() or None
        if not api_key:
            if provider == "openrouter":
                api_key = ENV_OPENROUTER_KEY  # optional server fallback
            elif provider == "gemini":
                api_key = ENV_GEMINI_KEY
            elif provider == "openai":
                api_key = ENV_OPENAI_KEY
            elif provider == "anthropic":
                api_key = ENV_ANTHROPIC_KEY

        base_url = (data.get("base_url") or data.get("baseUrl") or "").strip() or None
        if base_url:
            base_url = base_url.rstrip("/")

        return cls(provider=provider, model=model, api_key=api_key, base_url=base_url)

    # -- helpers ------------------------------------------------------------ #
    @property
    def label(self) -> str:
        return f"{self.provider}:{self.model}"

    def require_ready(self) -> None:
        """Raise a clear error if the config cannot make a call."""
        if self.provider == "openrouter" and not self.api_key:
            raise LLMError(
                "OpenRouter selected but no API key provided. Add your key in "
                "Settings (it stays in your browser)."
            )
        if self.provider == "gemini" and not self.api_key:
            raise LLMError(
                "Gemini selected but no API key provided. Add your Google AI Studio "
                "key in Settings (it stays in your browser)."
            )
        if self.provider == "openai" and not self.api_key:
            raise LLMError("OpenAI selected but no API key provided. Add it in Settings.")
        if self.provider == "anthropic" and not self.api_key:
            raise LLMError("Anthropic selected but no API key provided. Add it in Settings.")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def complete(
    config: LLMConfig,
    prompt: str,
    *,
    temperature: float = 0.3,
    num_ctx: int = 4096,
    max_tokens: int = 8192,
    json_mode: bool = False,
    timeout: int = 600,
) -> str:
    """Return the full model response as a string (blocking).

    For OpenRouter reasoning models, any ``reasoning`` field is folded into a
    leading ``<think>...</think>`` block so downstream parsing stays uniform.
    """
    config.require_ready()
    if config.provider == "openrouter":
        return _openrouter_complete(
            config, prompt, temperature, max_tokens, json_mode, timeout
        )
    if config.provider == "gemini":
        return _gemini_complete(
            config, prompt, temperature, max_tokens, json_mode, timeout
        )
    if config.provider == "openai":
        return _openai_complete(
            config, prompt, temperature, max_tokens, json_mode, timeout
        )
    if config.provider == "anthropic":
        return _anthropic_complete(
            config, prompt, temperature, max_tokens, json_mode, timeout
        )
    return _ollama_complete(
        config, prompt, temperature, num_ctx, json_mode, timeout
    )


def stream(
    config: LLMConfig,
    prompt: str,
    *,
    temperature: float = 0.3,
    num_ctx: int = 16384,
    max_tokens: int = 8192,
    timeout: int = 400,
) -> Iterator[str]:
    """Yield response tokens as they arrive.

    Reasoning deltas (OpenRouter) are wrapped in synthetic ``<think>``/
    ``</think>`` markers so the frontend's reasoning panel works for every
    provider.
    """
    config.require_ready()
    if config.provider == "openrouter":
        yield from _openrouter_stream(config, prompt, temperature, max_tokens, timeout)
    elif config.provider == "gemini":
        yield from _gemini_stream(config, prompt, temperature, max_tokens, timeout)
    elif config.provider == "openai":
        yield from _openai_stream(config, prompt, temperature, max_tokens, timeout)
    elif config.provider == "anthropic":
        yield from _anthropic_stream(config, prompt, temperature, max_tokens, timeout)
    else:
        yield from _ollama_stream(config, prompt, temperature, num_ctx, timeout)


# --------------------------------------------------------------------------- #
# Ollama transport (/api/generate)
# --------------------------------------------------------------------------- #

def _ollama_url(config: LLMConfig) -> str:
    base = (config.base_url or DEFAULT_OLLAMA_BASE).rstrip("/")
    return f"{base}/api/generate"


def _ollama_complete(config, prompt, temperature, num_ctx, json_mode, timeout) -> str:
    payload = {
        "model": config.model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    if json_mode:
        payload["format"] = "json"
    try:
        resp = requests.post(_ollama_url(config), json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json().get("response", "")
    except requests.exceptions.ConnectionError as exc:
        raise LLMError(
            f"Cannot reach Ollama at {config.base_url or DEFAULT_OLLAMA_BASE}. "
            "Is `ollama serve` running?"
        ) from exc
    except Exception as exc:  # noqa: BLE001 - surface a clean message
        raise LLMError(f"Ollama error: {exc}") from exc


def _ollama_stream(config, prompt, temperature, num_ctx, timeout) -> Iterator[str]:
    payload = {
        "model": config.model,
        "prompt": prompt,
        "stream": True,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    try:
        with requests.post(
            _ollama_url(config), json=payload, stream=True, timeout=timeout
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                token = chunk.get("response", "")
                if token:
                    yield token
                if chunk.get("done"):
                    break
    except requests.exceptions.ConnectionError as exc:
        raise LLMError(
            f"Cannot reach Ollama at {config.base_url or DEFAULT_OLLAMA_BASE}. "
            "Is `ollama serve` running?"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise LLMError(f"Ollama stream error: {exc}") from exc


# --------------------------------------------------------------------------- #
# OpenRouter transport (OpenAI-compatible /chat/completions)
# --------------------------------------------------------------------------- #

def _openrouter_headers(config: LLMConfig) -> dict:
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": _REFERER,
        "X-Title": _TITLE,
    }


def _openrouter_url(config: LLMConfig) -> str:
    base = (config.base_url or OPENROUTER_BASE).rstrip("/")
    return f"{base}/chat/completions"


def _openrouter_payload(config, prompt, temperature, max_tokens, stream, json_mode):
    payload = {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    return payload


def _raise_openrouter(exc: Exception, resp: Optional[requests.Response]) -> None:
    if resp is not None and resp.status_code == 401:
        raise LLMError("OpenRouter rejected the API key (401). Check it in Settings.")
    if resp is not None and resp.status_code == 402:
        raise LLMError("OpenRouter: insufficient credits (402) for this model.")
    if resp is not None and resp.status_code == 429:
        raise LLMError("OpenRouter rate limit hit (429). Slow down or switch model.")
    detail = ""
    if resp is not None:
        try:
            detail = resp.json().get("error", {}).get("message", "")
        except Exception:  # noqa: BLE001
            detail = resp.text[:200] if resp.text else ""
    raise LLMError(f"OpenRouter error: {detail or exc}")


def _openrouter_complete(config, prompt, temperature, max_tokens, json_mode, timeout):
    payload = _openrouter_payload(
        config, prompt, temperature, max_tokens, False, json_mode
    )
    resp = None
    try:
        resp = requests.post(
            _openrouter_url(config),
            headers=_openrouter_headers(config),
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        msg = resp.json()["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning") or ""
        if reasoning and not json_mode:
            return f"<think>{reasoning}</think>{content}"
        return content
    except Exception as exc:  # noqa: BLE001
        _raise_openrouter(exc, resp)


def _openrouter_stream(config, prompt, temperature, max_tokens, timeout):
    payload = _openrouter_payload(config, prompt, temperature, max_tokens, True, False)
    resp = None
    think_open = False
    try:
        with requests.post(
            _openrouter_url(config),
            headers=_openrouter_headers(config),
            json=payload,
            stream=True,
            timeout=timeout,
        ) as resp:
            if resp.status_code >= 400:
                _raise_openrouter(RuntimeError("bad status"), resp)
            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.decode("utf-8").strip()
                if line.startswith(":"):  # keep-alive comment
                    continue
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"]
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

                reasoning = delta.get("reasoning")
                if reasoning:
                    if not think_open:
                        yield "<think>"
                        think_open = True
                    yield reasoning

                token = delta.get("content")
                if token:
                    if think_open:
                        yield "</think>"
                        think_open = False
                    yield token
            if think_open:  # safety: never leave a think block open
                yield "</think>"
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001
        _raise_openrouter(exc, resp)


# --------------------------------------------------------------------------- #
# Gemini transport (Google AI Studio)
# --------------------------------------------------------------------------- #

def _gemini_url(config: LLMConfig, stream: bool = False) -> str:
    base = (config.base_url or GEMINI_BASE).rstrip("/")
    endpoint = "streamGenerateContent" if stream else "generateContent"
    return f"{base}/models/{config.model}:{endpoint}?key={config.api_key}"


def _gemini_payload(prompt: str, temperature: float, max_tokens: int, json_mode: bool) -> dict:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"
    return payload


def _raise_gemini(exc: Exception, resp: Optional[requests.Response]) -> None:
    if resp is not None and resp.status_code == 400:
        raise LLMError(
            "Gemini error: Bad Request (400). The model may not exist or the "
            "payload is malformed."
        )
    if resp is not None and resp.status_code == 403:
        raise LLMError("Gemini rejected the API key (403). Check it in Settings.")
    if resp is not None and resp.status_code == 429:
        raise LLMError("Gemini rate limit hit (429). Slow down.")
    detail = ""
    if resp is not None:
        try:
            detail = resp.json().get("error", {}).get("message", "")
        except Exception:  # noqa: BLE001
            detail = resp.text[:200] if resp.text else ""
    raise LLMError(f"Gemini error: {detail or exc}")


def _gemini_complete(config, prompt, temperature, max_tokens, json_mode, timeout) -> str:
    payload = _gemini_payload(prompt, temperature, max_tokens, json_mode)
    resp = None
    try:
        resp = requests.post(_gemini_url(config, stream=False), json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return ""
    except Exception as exc:  # noqa: BLE001
        _raise_gemini(exc, resp)


def _gemini_stream(config, prompt, temperature, max_tokens, timeout) -> Iterator[str]:
    # streamGenerateContent with alt=sse emits OpenAI-style "data:" SSE frames.
    url = _gemini_url(config, stream=True) + "&alt=sse"
    payload = _gemini_payload(prompt, temperature, max_tokens, False)
    resp = None
    try:
        with requests.post(url, json=payload, stream=True, timeout=timeout) as resp:
            if resp.status_code >= 400:
                _raise_gemini(RuntimeError("bad status"), resp)
            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if not data:
                    continue
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                try:
                    text = chunk["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    continue
                if text:
                    yield text
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001
        _raise_gemini(exc, resp)


# --------------------------------------------------------------------------- #
# OpenAI transport (native /chat/completions)
# --------------------------------------------------------------------------- #

def _openai_url(config: LLMConfig) -> str:
    base = (config.base_url or OPENAI_BASE).rstrip("/")
    return f"{base}/chat/completions"


def _openai_headers(config: LLMConfig) -> dict:
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }


def _openai_complete(config, prompt, temperature, max_tokens, json_mode, timeout):
    # OpenAI shares the OpenAI-compatible payload/error shape with OpenRouter.
    payload = _openrouter_payload(config, prompt, temperature, max_tokens, False, json_mode)
    resp = None
    try:
        resp = requests.post(
            _openai_url(config),
            headers=_openai_headers(config),
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"].get("content", "")
    except Exception as exc:  # noqa: BLE001
        _raise_openrouter(exc, resp)


def _openai_stream(config, prompt, temperature, max_tokens, timeout):
    payload = _openrouter_payload(config, prompt, temperature, max_tokens, True, False)
    resp = None
    try:
        with requests.post(
            _openai_url(config),
            headers=_openai_headers(config),
            json=payload,
            stream=True,
            timeout=timeout,
        ) as resp:
            if resp.status_code >= 400:
                _raise_openrouter(RuntimeError("bad status"), resp)
            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"]
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
                token = delta.get("content")
                if token:
                    yield token
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001
        _raise_openrouter(exc, resp)


# --------------------------------------------------------------------------- #
# Anthropic transport (native /messages)
# --------------------------------------------------------------------------- #

def _anthropic_url(config: LLMConfig) -> str:
    base = (config.base_url or ANTHROPIC_BASE).rstrip("/")
    return f"{base}/messages"


def _anthropic_headers(config: LLMConfig) -> dict:
    return {
        "x-api-key": config.api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }


def _anthropic_payload(config, prompt, temperature, max_tokens, stream):
    return {
        "model": config.model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
    }


def _raise_anthropic(exc: Exception, resp: Optional[requests.Response]) -> None:
    if resp is not None and resp.status_code == 401:
        raise LLMError("Anthropic rejected the API key (401). Check it in Settings.")
    if resp is not None and resp.status_code == 429:
        raise LLMError("Anthropic rate limit hit (429). Slow down.")
    detail = ""
    if resp is not None:
        try:
            detail = resp.json().get("error", {}).get("message", "")
        except Exception:  # noqa: BLE001
            detail = resp.text[:200] if resp.text else ""
    raise LLMError(f"Anthropic error: {detail or exc}")


def _anthropic_complete(config, prompt, temperature, max_tokens, json_mode, timeout):
    payload = _anthropic_payload(config, prompt, temperature, max_tokens, stream=False)
    resp = None
    try:
        resp = requests.post(
            _anthropic_url(config),
            headers=_anthropic_headers(config),
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]
    except Exception as exc:  # noqa: BLE001
        _raise_anthropic(exc, resp)


def _anthropic_stream(config, prompt, temperature, max_tokens, timeout):
    payload = _anthropic_payload(config, prompt, temperature, max_tokens, stream=True)
    resp = None
    try:
        with requests.post(
            _anthropic_url(config),
            headers=_anthropic_headers(config),
            json=payload,
            stream=True,
            timeout=timeout,
        ) as resp:
            if resp.status_code >= 400:
                _raise_anthropic(RuntimeError("bad status"), resp)
            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if not data:
                    continue
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                if chunk.get("type") == "content_block_delta":
                    token = chunk.get("delta", {}).get("text")
                    if token:
                        yield token
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001
        _raise_anthropic(exc, resp)

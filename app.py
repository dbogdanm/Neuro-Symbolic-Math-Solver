from flask import Flask, render_template, request, Response, stream_with_context, jsonify
import requests
import json
import logging
import time
from neuro_symbolic import run_neuro_symbolic_pipeline

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

#OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL_8B = "deepseek-r1:8b"

#URL_PC = "http://100.66.132.85:11434/api/generate"
#URL_COLAB = "api/generate"
HEADERS_COLAB = {"Bypass-Tunnel-Reminder": "true"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/neuro_symbolic", methods=["POST"])
def neuro_symbolic_endpoint():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "Prompt is required"}, 400

    try:
        result = run_neuro_symbolic_pipeline(prompt)
        return jsonify({"final_answer": result})
    except Exception as e:
        app.logger.error(f"Neuro-symbolic error: {e}")
        return jsonify({"error": str(e)}), 500

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
                            # Format for Server-Sent Events (SSE)
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

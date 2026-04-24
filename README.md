<div align="center">

# Neuro-Symbolic Math Solver

![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue?style=flat-square)
![Conference](https://img.shields.io/badge/KES-2026-purple?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat-square)
![Framework](https://img.shields.io/badge/Backend-Flask-black?style=flat-square)
![Math Engine](https://img.shields.io/badge/Engine-SymPy-green?style=flat-square)
![LLM](https://img.shields.io/badge/LLM-Ollama-orange?style=flat-square)
![Dockerized](https://img.shields.io/badge/Deployment-Docker-blue?style=flat-square)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
![Repo Size](https://img.shields.io/github/repo-size/dbogdanm/Neuro-Symbolic-Math-Solver?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/dbogdanm/Neuro-Symbolic-Math-Solver?style=flat-square)

<br/>

</div>

---

This is my most complex GitHub project yet, exploring hybrid reasoning architectures to completely eliminate computational hallucinations in edge-scale models. The performance metrics demonstrated in the charts below highlight the capabilities of the Release v1.0.0 architecture, where wrapping a compact 8B parameter model in this RAG and neuro-symbolic pipeline yielded massive performance surges, allowing it to compete with and even surpass much larger frontier models.


-----

## Overview (Release v2.0.0)

**Neuro-Symbolic Math Solver** is my research-oriented, web-based artificial intelligence system that integrates the generative reasoning capabilities of Large Language Models (LLMs) with the formal rigor of symbolic mathematics via **SymPy**, augmented by real-time Retrieval-Augmented Generation (RAG).

Developed in the context of my **KES 2026 submission**, the system explores hybrid reasoning architectures to offload rigid arithmetic tasks to a deterministic engine and inject missing parametric knowledge via RAG. This framework empowers compact models (e.g., 8B parameters) to achieve competition-level mathematical deductive capabilities.

The platform is implemented using **Flask**, **Docker**, and **Ollama**, featuring a purpose-built *Focus Mode* interface optimized for high-clarity mathematical interaction and explainability.

-----

## Performance Highlights

In my ablation studies evaluated on frontier mathematical benchmarks, wrapping edge-scale models in this neuro-symbolic pipeline yielded significant performance improvements compared to raw baseline executions:

<div align="center">
  <img src="Charts/Chart1.png" alt="Accuracy Comparison on Top 20 GSM8K Dataset" width="85%" />
  <br><br>
  <img src="Charts/Chart2.png" alt="Precision Accuracy Comparison: MATH500 Top 31 Problems" width="85%" />
  <br><br>
  <img src="Charts/Chart3.png" alt="Precision Accuracy Comparison: GSM8K Top 21 Problems" width="85%" />
</div>
<br/>

* **AIME 2025 Dataset:** Reached **66.6% accuracy** (20 problems solved out of 30) using an 8B model (compared to a 0% baseline without RAG and symbolic execution).
* **MATH 500 Dataset:** Achieved **93.0% accuracy** on the first 100 problems of this dataset, demonstrating extreme robustness in complex theorem application.
* **Zero Arithmetic Hallucinations:** The execution layer securely handles all mathematical operations, completely eliminating LLM calculation errors.
-----

## Key Contributions

  * **Neuro-Symbolic Reasoning Pipeline**
    1.  **Semantic Parsing** – Extraction of variables, constraints, and objectives.
    2.  **Program-of-Thought (PoT) Generation** – LLM-generated symbolic Python scripts.
    3.  **Deterministic Execution** – Secure, isolated evaluation using `SymPy`.
    4.  **Validation & Result Extraction** – Ensuring strict mathematical correctness.
  * **Hybrid Retrieval-Augmented Generation (RAG)**
      * Local knowledge retrieval via **ChromaDB**.
      * Live web search (DuckDuckGo) to mitigate epistemic constraints and knowledge cutoffs.
  * **Explainable AI Interface ("Focus Mode")**
      * Real-time pipeline streaming and execution logs.
      * High-fidelity LaTeX rendering via MathJax.
      * Expandable reasoning traces for complete error traceability.
  * **Containerized Research Environment**
      * Fully reproducible edge architecture via Docker and `docker-compose`.

-----

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Flask (Python 3.11) |
| **Frontend** | Vanilla JavaScript, CSS3 (Glassmorphism), MathJax, Marked |
| **Math Engine** | SymPy (Python Runtime) |
| **LLM Runtime** | Ollama (DeepSeek-R1 or any LLM you like) |
| **Vector Store** | ChromaDB |
| **Web Retrieval** | DuckDuckGo Search API |

-----

## Quick Start (Docker)

Ensure [Ollama](https://ollama.com/) is installed and running locally on your machine. Pull your preferred edge model:

```bash
ollama pull deepseek-r1:8b
```

### 1\. Clone the Repository

```bash
git clone https://github.com/dbogdanm/Neuro-Symbolic-Math-Solver.git
cd Neuro-Symbolic-Math-Solver
```

### 2\. Build and Launch

```bash
docker-compose up --build
```

### 3\. Access the Application

Open your browser and navigate to:

```text
http://localhost:5000
```

-----

## Manual Setup (Without Docker)

### 1\. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3\. Run the Application

```bash
python app.py
```

-----

## Neuro-Symbolic Pipeline Architecture

My system follows a strict deterministic and interpretable reasoning loop to bridge the gap between neural flexibility and symbolic precision:

1.  **Retrieval Phase:** Queries ChromaDB and external web sources to formulate the governing equations.
2.  **Semantic Structuring:** Converts natural language problem statements into strict, structured JSON formats.
3.  **Symbolic Program Synthesis:** Generates executable SymPy code via LLM reasoning based on retrieved context.
4.  **Execution & Verification:** Runs the generated code in an isolated environment, validates outputs, and falls back to natural language reasoning if unrecoverable logic errors occur.

-----

## Requirements

  * Docker & Docker Compose *(recommended for isolation)*
  * Ollama running locally (mapped to `host.docker.internal:11434` in Docker)
  * **Recommended Models:**
      * `deepseek-r1:8b` (default)
      * `llama3:8b-instruct`

-----

## License

**Copyright (c) 2026 DINU BOGDAN**

This project is licensed under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

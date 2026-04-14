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

## Overview

**Neuro-Symbolic Math Solver** is a research-oriented, web-based artificial intelligence system that integrates the generative reasoning capabilities of Large Language Models (LLMs) with the formal rigor of symbolic mathematics via **SymPy**, augmented by real-time Retrieval-Augmented Generation (RAG).

Developed in the context of a **KES 2026 submission**, the system explores hybrid reasoning architectures for mathematically precise and explainable problem solving.

The platform is implemented using **Flask**, **Docker**, and **Ollama**, and features a purpose-built *Focus Mode* interface optimized for high-clarity mathematical interaction.

![Math-OS Web UI](static/style.css) *(Placeholder for UI illustration)*

---

## Key Contributions

- **Neuro-Symbolic Reasoning Pipeline**
  1. **Semantic Parsing** – Extraction of variables, constraints, and objectives
  2. **Program-of-Thought (PoT) Generation** – LLM-generated symbolic programs
  3. **Deterministic Execution** – Secure evaluation using `SymPy`
  4. **Validation & Result Extraction** – Ensuring mathematical correctness

- **Hybrid Retrieval-Augmented Generation (RAG)**
  - Local knowledge via **ChromaDB**
  - Live web search (DuckDuckGo) to mitigate knowledge cutoffs

- **Explainable AI Interface ("Focus Mode")**
  - Real-time pipeline streaming
  - LaTeX rendering via MathJax
  - Expandable reasoning traces

- **Containerized Research Environment**
  - Fully reproducible with Docker and `docker-compose`

---

## Technology Stack

| Layer        | Technology |
|--------------|-----------|
| Backend      | Flask (Python 3.11) |
| Frontend     | Vanilla JavaScript, CSS3 (Glassmorphism), MathJax, Marked.js |
| Math Engine  | SymPy |
| LLM Runtime  | Ollama (DeepSeek-R1, LLaMA 3, etc.) |
| Vector Store | ChromaDB |
| Web Retrieval| DuckDuckGo Search API |

---

## Quick Start (Docker)

Ensure [Ollama](https://ollama.com/) is installed and running locally with:

```bash
ollama pull deepseek-r1:8b
```

### 1. Clone the Repository

```bash
git clone https://github.com/dbogdanm/Neuro-Symbolic-Math-Solver.git
cd Neuro-Symbolic-Math-Solver
```

### 2. Build and Launch

```bash
docker-compose up --build
```

### 3. Access the Application

Open:

```
http://localhost:5000
```

---

## Manual Setup (Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
python app.py
```

---

## Neuro-Symbolic Pipeline Architecture

The system follows a deterministic and interpretable reasoning loop:

1. **Retrieval Phase**
   - Queries ChromaDB and external web sources

2. **Semantic Structuring**
   - Converts natural language into structured JSON

3. **Symbolic Program Synthesis**
   - Generates executable SymPy code via LLM reasoning

4. **Execution & Verification**
   - Runs in isolation and validates outputs
   - Falls back to direct reasoning if needed

---

## Requirements

- Docker & Docker Compose *(recommended)*
- Ollama running locally (`host.docker.internal:11434`)
- Models:
  - `deepseek-r1:8b` (default)
  - Configurable via environment variables

---

## Citation

If you use this work in academic research, please cite the corresponding **KES 2026 paper** (details to be added upon publication).

---

## License

This project is licensed under the MIT License.

---

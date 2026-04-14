# Neuro-Symbolic Math Solver (Math-OS) 🚀

A premium, web-based AI application that combines the creative reasoning of Large Language Models (LLMs) with the rigorous precision of Symbolic Mathematics (SymPy) and real-time Retrieval-Augmented Generation (RAG).

Built with **Flask**, **Docker**, and **Ollama**, this solver features a "Focus Mode" UI designed for high-clarity mathematical exploration.

![Math-OS Web UI](static/style.css) *(Placeholder for UI description)*

## 🌟 Key Features

-   **Neuro-Symbolic Pipeline**: A multi-stage solver that:
    1.  **Semantically Parses** the problem into variables and goals.
    2.  **Generates Programs-of-Thought (PoT)** using LLMs.
    3.  **Executes Code** in a secure, isolated Python environment using `SymPy`.
    4.  **Validates** and extracts the final mathematical result.
-   **Web-RAG (Live Search)**: Bypasses model knowledge cutoffs by performing real-time web searches via DuckDuckGo to find latest formulas, constants, or context.
-   **Premium "Focus Mode" UI**: A sleek, dark-themed ChatGPT-style interface with:
    -   **Live Pipeline Streaming**: Watch the AI "think" through logs, RAG retrieval, and code generation.
    -   **LaTeX Rendering**: Beautiful mathematical formulas via MathJax.
    -   **Collapsible Reasoning**: Expandable blocks for internal LLM thought processes.
-   **Dockerized Architecture**: Fully containerized for easy deployment, with a pre-configured `docker-compose` setup to connect to local Ollama instances.

## 🛠️ Technology Stack

-   **Backend**: Flask (Python 3.11)
-   **Frontend**: Vanilla JS, CSS3 (Modern Glassmorphism), MathJax, Marked.js
-   **Math Engine**: SymPy (Symbolic Mathematics)
-   **LLM Integration**: Ollama (Supporting DeepSeek-R1, Llama 3, etc.)
-   **RAG Database**: ChromaDB (Vector store for mathematical rules)
-   **Search**: DuckDuckGo Search API

## 🚀 Quick Start (Docker)

Ensure you have [Ollama](https://ollama.com/) installed and running on your host machine with the `deepseek-r1:8b` model pulled.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/dbogdanm/Neuro-Symbolic-Math-Solver.git
    cd Neuro-Symbolic-Math-Solver
    ```

2.  **Build and Run with Docker**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the App**:
    Open your browser and navigate to [http://localhost:5000](http://localhost:5000).

## 🔧 Manual Setup (No Docker)

1.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask Server**:
    ```bash
    python app.py
    ```

## 🧠 How the Neuro-Symbolic Pipeline Works

Math-OS doesn't just "guess" the answer. It follows a rigorous logical flow:

1.  **Retrieval**: The system searches the local `ChromaDB` ruleset and the Web for relevant mathematical hints.
2.  **Semantic Parsing**: The LLM extracts the core logic (variables, constraints) into a structured JSON.
3.  **PoT Generation**: The model writes a Python script using `SymPy` to solve the extracted logic.
4.  **Execution & Extraction**: The script runs in a separate process. If it succeeds, the precise symbolic result is returned. If it fails, a "Direct Reasoning" fallback is triggered.

## 🛡️ Requirements

-   **Docker & Docker Compose** (Recommended)
-   **Ollama** running on the host machine (`host.docker.internal:11434`)
-   Models: `deepseek-r1:8b` (default), or customize via `app.py` environment variables.

## 📜 License

This project is part of a Licensing Thesis. All rights reserved.

---
Developed with ❤️ by [dbogdanm](https://github.com/dbogdanm)

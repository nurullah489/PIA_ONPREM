# PIA_ONPREM

Personal Intelligent Assistant — Fully On-Premise

---

## Overview

PIA_ONPREM is a basic fully on-premise personal intelligent assistant that supports:

- Local document ingestion
- Web-based knowledge collection
- Local LLM inference
- Vector database retrieval

The assistant can be extended by adding additional data sources such as:

- Websites
- TXT documents
- PDF documents

All processing runs locally on your machine.

---

# Project Structure

```text
PIA_ONPREM/
│
├── data/
│   └── raw_docs/
│
├── model/
│   ├── EmbedModelfile
│   └── Modelfile
│
├── src/
│   ├── app.py
│   ├── main.py
│   └── tools/
│       ├── scraper.py
│       └── ingest.py
│
├── web/
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1. Create Virtual Environment

Create a virtual environment named `.venv` inside the project directory.

```powershell
python -m venv .venv
```

---

## 2. Activate the Virtual Environment

Activate the environment using PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Required Packages

Install all dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

---

# Configure Project Paths

Update the base directory paths in the following files before running the project:

- `src/main.py`
- `src/tools/ingest.py`
- `src/tools/scraper.py`

Make sure all paths correctly point to your local `PIA_ONPREM` directory.

---

# Download Required Models

Download the following model files and place them inside the `model/` directory.

## LLM Model

```text
llama-3.2-3b-instruct-q4_k_m.gguf
```

## Embedding Model

```text
nomic-embed-text-v1.5.Q5_K_M.gguf
```

---

# Data Preparation

## 1. Collect Web Data

Run the scraper to collect raw data for the vector database.

```powershell
python src/tools/scraper.py
```

---

## 2. Add Local Documents

Place all `.txt` and `.pdf` files inside:

```text
PIA_ONPREM/data/raw_docs/
```

---

## 3. Populate the Vector Database

Run the ingestion script to process documents and populate the vector database.

```powershell
python src/tools/ingest.py
```

---

# Run the Application

Start the assistant application:

```powershell
python src/app.py
```

---

# Web Interface

The project also includes a simple frontend interface:

```text
web/index.html
```

You can open this file directly in your browser if needed.

---

# Notes

- Ensure model paths are configured correctly before running the application.
- Model files are not included in the repository.
- Response quality depends on the quality and amount of ingested data.
- The project is designed to run fully on-premise without external cloud dependencies.

---

# Future Improvements

- Multi-agent architecture
- Voice interaction
- Persistent memory
- Real-time web search
- Better UI/UX
- Streaming responses
- API integrations
- Advanced RAG pipelines

---

# License

This project is intended for personal and educational purposes.

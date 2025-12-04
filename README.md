---

# Local-First RAG Prototype

A simple offline Retrieval-Augmented Generation (RAG) prototype that stores notes locally, embeds them, and retrieves relevant text using semantic search. This version performs retrieval and augmentation; it does not generate final LLM answers.

---
## Features

* Runs fully offline
* Uses SQLite for text storage
* Uses MiniLM for embedding
* Uses FAISS for vector similarity search
* Works on low-end machines (4–8 GB RAM)
* LLM-agnostic (works with GPT, Llama, DeepSeek, etc.)
* Minimal and easy to extend

## How It Works

1. Text is split into small chunks (300–500 characters).
2. Each chunk is stored in SQLite along with an ID and timestamp.
3. Each chunk is converted into an embedding using the all-MiniLM-L6-v2 model.
4. Embeddings are stored in a FAISS vector index.
5. During a query, the question is embedded and searched against FAISS.
6. Matching chunk IDs are used to fetch the original text from SQLite.
7. Retrieved text is returned as context for any LLM.

## Pipeline Overview

Ingest:
text → chunk → embed → store in SQLite → store vector in FAISS

Query:
question → embed → FAISS search → retrieve chunks → return context


## Usage

Install dependencies:

```
pip install -r requirements.txt
```

Run the demo:

```
python main.py
```

## Notes

This prototype performs retrieval only. For a full RAG pipeline, integrate an LLM to generate final answers using the retrieved context.

---



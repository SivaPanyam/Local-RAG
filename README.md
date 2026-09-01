# Local RAG � Retrieval-Augmented Generation

A fully local, open-source Retrieval-Augmented Generation (RAG) prototype built with Python.

This project demonstrates an end-to-end RAG pipeline that loads documents, splits them into chunks, generates embeddings locally, stores them in a persistent vector database, retrieves relevant information, and uses a local LLM through Ollama to generate grounded answers.

---

## Architecture Flow

Documents -> Ingestion -> Chunking -> FastEmbed -> ChromaDB -> Retrieval -> Prompt -> Ollama -> Answer

---

## Quick Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Run indexing:
   python -m tests.test_indexing

3. Launch UI:
   python -m streamlit run app/streamlit_app.py

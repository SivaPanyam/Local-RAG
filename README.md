# Local RAG — Retrieval-Augmented Generation

A fully local, open-source Retrieval-Augmented Generation (RAG) system built with Python, FastEmbed, ChromaDB, Ollama, and Streamlit.

This project implements a complete local RAG pipeline that can ingest documents, split them into meaningful chunks, convert those chunks into vector embeddings, store them in a persistent vector database, retrieve the most relevant information for a user's question, construct a grounded prompt, and generate an answer using a locally running Large Language Model.

The project is designed as a practical RAG engineering project rather than a black-box chatbot.

Every major stage of the RAG pipeline is implemented as a separate Python module so that the system can be understood, tested, modified, and extended.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Project Goals](#project-goals)
- [Core Architecture](#core-architecture)
- [End-to-End Data Flow](#end-to-end-data-flow)
- [Technology Stack](#technology-stack)
- [Current Features](#current-features)
- [Project Structure](#project-structure)
- [RAG Pipeline Components](#rag-pipeline-components)
- [Document Ingestion](#document-ingestion)
- [Document Chunking](#document-chunking)
- [Embedding Generation](#embedding-generation)
- [Vector Database](#vector-database)
- [Retrieval](#retrieval)
- [Prompt Construction](#prompt-construction)
- [Local LLM Generation](#local-llm-generation)
- [End-to-End RAG Pipeline](#end-to-end-rag-pipeline)
- [Streamlit Interface](#streamlit-interface)
- [Installation](#installation)
- [Configuration](#configuration)
- [Using Your Own Documents](#using-your-own-documents)
- [Indexing Documents](#indexing-documents)
- [Asking Questions](#asking-questions)
- [Testing](#testing)
- [Example RAG Flow](#example-rag-flow)
- [Multi-Document Retrieval](#multi-document-retrieval)
- [Current Prototype Results](#current-prototype-results)
- [Design Decisions](#design-decisions)
- [Local and Privacy-First Architecture](#local-and-privacy-first-architecture)
- [Current Limitations](#current-limitations)
- [Future Development](#future-development)
- [RAG Learning Lab](#rag-learning-lab)
- [Future Architecture](#future-architecture)
- [Development Philosophy](#development-philosophy)
- [Project Status](#project-status)
- [License](#license)

---

# Project Overview

Retrieval-Augmented Generation combines two major capabilities:

1. Information retrieval
2. Language generation

Instead of asking a language model to answer a question only from the knowledge stored inside its parameters, a RAG system first retrieves relevant information from an external knowledge source and then provides that information to the language model as context.

This project implements that process locally.

The system takes documents from a local folder, processes them into chunks, generates embeddings for those chunks, stores the embeddings in ChromaDB, retrieves relevant chunks for a user's question, and sends the retrieved context to a local Ollama model.

The basic concept is:

```text
Documents
    ↓
Ingestion
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
User Question
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Chunks
    ↓
Context
    ↓
Prompt
    ↓
Local LLM
    ↓
Answer

```

Project Goals

The first goal of this project is to create a working RAG system without depending on paid cloud APIs.

The second goal is to keep the architecture understandable.

The project therefore avoids hiding the complete RAG process behind a single high-level framework call.

Instead, each major operation has its own module.

For example:

load_documents()
↓
split_documents()
↓
create_embeddings()
↓
store_vectors()
↓
retrieve_documents()
↓
build_prompt()
↓
generate_answer()

This makes it possible to inspect and understand what happens at every stage.

Core Architecture

The current prototype follows this architecture:
LOCAL RAG SYSTEM
│
▼
┌────────────────────┐
│ Document Ingestion │
│ ingestion.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Chunking │
│ chunking.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Embeddings │
│ embeddings.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ ChromaDB │
│ vector_store.py │
└──────────┬─────────┘
│
│
User Question
│
▼
┌────────────────────┐
│ Retrieval │
│ retrieval.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Retrieved Context │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Prompt Builder │
│ prompt.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ RAG Pipeline │
│ rag_pipeline.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Generation │
│ generation.py │
└──────────┬─────────┘
│
▼
┌────────────────────┐
│ Ollama llama3.2 │
└──────────┬─────────┘
│
▼
Answer

End-to-End Data Flow

The complete system can be understood as two connected pipelines.

Indexing Pipeline

The first pipeline prepares documents for retrieval.

Document
↓
Document Loader
↓
LangChain Document
↓
Text Chunk
↓
Embedding Model
↓
Vector
↓
ChromaDB

This pipeline runs when documents are processed.

Query Pipeline

The second pipeline runs when the user asks a question.

User Question
↓
Query Embedding
↓
ChromaDB Similarity Search
↓
Top-K Relevant Chunks
↓
Context Construction
↓
Prompt Construction
↓
Ollama
↓
Generated Answer
↓
Sources

Together:

                 INDEXING
                    │

Documents ─────────┤
↓
ChromaDB
│
│
▼
USER QUESTION
│
↓
RETRIEVAL
│
↓
CONTEXT
│
↓
PROMPT
│
↓
LOCAL LLM
│
↓
ANSWER

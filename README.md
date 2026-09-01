Local RAG
A fully local Retrieval-Augmented Generation (RAG) prototype built with Python, FastEmbed, ChromaDB, Ollama, and Streamlit.

The system processes local documents, creates embeddings, stores them in ChromaDB, retrieves relevant chunks, and generates answers using the local llama3.2 model through Ollama.

No OpenAI API or paid cloud API is required.

Tech Stack
Component	Technology
Language	Python 3.12+
Document Processing	LangChain
Embeddings	FastEmbed
Embedding Model	BAAI/bge-small-en-v1.5
Runtime	ONNX Runtime
Vector Database	ChromaDB
LLM Runtime	Ollama
LLM	llama3.2
Interface	Streamlit
Project Structure
rag/
│
├── app/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── indexing.py
│   ├── ingestion.py
│   ├── prompt.py
│   ├── rag_pipeline.py
│   ├── retrieval.py
│   ├── streamlit_app.py
│   └── vector_store.py
│
├── tests/
│   ├── __init__.py
│   ├── test_generation.py
│   ├── test_indexing.py
│   ├── test_prompt.py
│   ├── test_rag.py
│   └── test_retrieval.py
│
├── watch_folder/
├── chroma_db/
├── requirements.txt
├── run_app.py
├── README.md
└── .gitignore
Note: watch_folder/ is used for local documents, while chroma_db/ contains generated local vector data. Both are excluded from Git.
Installation
1. Clone the Repository
git clone https://github.com/SivaPanyam/Local-RAG.git
cd Local-RAG
2. Create a Virtual Environment
python -m venv .venv
Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1
3. Verify Python
python --version
python -m pip --version
4. Install Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
Ollama Setup
Verify Ollama:

ollama --version
Check installed models:

ollama list
If llama3.2 is not installed:

ollama pull llama3.2
Run the model:

ollama run llama3.2
Ollama should be available locally at:

http://localhost:11434
Verify the local server from PowerShell:

Invoke-WebRequest http://localhost:11434 -UseBasicParsing
Add Documents
Place documents inside:

watch_folder/
Current supported formats:

.pdf
.txt
.md
Example:

watch_folder/
├── document1.pdf
├── document2.pdf
├── notes.txt
└── research.md
Documents inside watch_folder/ are processed locally and are not uploaded to GitHub.

Index Documents
From the project root, run:

python -m tests.test_indexing
The indexing pipeline performs:

Documents
    ↓
Document Loading
    ↓
Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Storage
Example output:

Loading documents...
Documents loaded: 166
Splitting documents...
Chunks created: 533
Creating embeddings...
Embeddings created: 533
Storing vectors...
Vectors stored: 533

==================================================
INDEXING COMPLETE
==================================================
Documents: 166
Chunks:    533
Vectors:   533
Run Retrieval Test
python -m tests.test_retrieval
This tests semantic similarity retrieval from ChromaDB and displays the retrieved chunk, source, chunk ID, and distance.

Run Prompt Test
python -m tests.test_prompt
This verifies that retrieved context and the user's question are correctly combined into the RAG prompt.

Run Generation Test
python -m tests.test_generation
This tests communication with the local Ollama llama3.2 model.

Run End-to-End RAG Test
python -m tests.test_rag
The complete pipeline is:

Question
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
Ollama
    ↓
Answer
Run Streamlit Application
python -m streamlit run app/streamlit_app.py
Open the local application:

http://localhost:8501
The interface provides:

Document processing
Question input
Answer generation
Retrieved source display
Retrieval distance information
Typical Workflow
1. Activate virtual environment
        ↓
2. Start Ollama
        ↓
3. Put documents in watch_folder/
        ↓
4. Run indexing
        ↓
5. Documents are loaded
        ↓
6. Documents are split into chunks
        ↓
7. Embeddings are generated
        ↓
8. Vectors are stored in ChromaDB
        ↓
9. Start Streamlit
        ↓
10. Ask questions
        ↓
11. Relevant chunks are retrieved
        ↓
12. Context is sent to llama3.2
        ↓
13. Answer is generated
Useful Commands
Environment
.venv\Scripts\Activate.ps1
python --version
python -m pip --version
Ollama
ollama --version
ollama list
ollama pull llama3.2
ollama run llama3.2
RAG Tests
python -m tests.test_indexing
python -m tests.test_retrieval
python -m tests.test_prompt
python -m tests.test_generation
python -m tests.test_rag
Streamlit
python -m streamlit run app/streamlit_app.py
GitHub Development
Check repository status:

git status
Stage changes:

git add .
Commit changes:

git commit -m "Update RAG prototype"
Push changes:

git push
Important Git Rules
The following should not be committed:

.venv/
chroma_db/
watch_folder/*.pdf
watch_folder/*.txt
watch_folder/*.md
.env
The project's .gitignore prevents local environments, generated vector data, and personal documents from being uploaded.

Current RAG Pipeline
PDF / TXT / MD
      ↓
Document Loader
      ↓
Text Chunking
      ↓
FastEmbed
BAAI/bge-small-en-v1.5
      ↓
ChromaDB
Persistent Local Storage
      ↓
User Question
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Top-K Relevant Chunks
      ↓
Context Injection
      ↓
Ollama
llama3.2
      ↓
Answer
Current Status
Local document ingestion
PDF support
TXT support
Markdown support
Configurable document chunking
FastEmbed embeddings
BAAI/bge-small-en-v1.5
384-dimensional embeddings
Persistent ChromaDB storage
Semantic similarity retrieval
Context construction
Grounded RAG prompt
Ollama integration
llama3.2 generation
End-to-end RAG pipeline
Multi-document indexing
Streamlit interface
Component-level tests
Current Limitations
The first prototype intentionally keeps the implementation simple.

Current document support is PDF, TXT, and Markdown.
Retrieval currently uses dense vector similarity.
No hybrid BM25 + vector search yet.
No reranking yet.
No advanced query transformation.
No OCR pipeline yet.
No multimodal document processing yet.
No advanced citation system yet.
No retrieval evaluation framework yet.
No generation evaluation framework yet.
No production-scale optimization yet.
Future Development
Future versions will gradually add:

DOCX support
PPT/PPTX support
XLSX and CSV support
HTML/web document ingestion
OCR
Table extraction
Image-aware processing
Semantic chunking
Hybrid search
BM25 retrieval
Query transformation
Reranking
Metadata filtering
Improved citations
Conversational RAG
Guardrails
Retrieval evaluation
Generation evaluation
End-to-end evaluation
Observability and tracing
Performance analysis
Experiment tracking
RAG Learning Lab — Long-Term Goal
The long-term goal is to evolve this prototype into an interactive RAG Learning Lab.

Instead of hiding the RAG process behind a single chatbot interface, the future system will allow learners to inspect what actually happens at every stage.

DOCUMENT
   ↓
PARSING
   ↓
CHUNKING
   ↓
EMBEDDINGS
   ↓
VECTOR DATABASE
   ↓
RETRIEVAL
   ↓
RERANKING
   ↓
CONTEXT
   ↓
PROMPT
   ↓
LLM
   ↓
ANSWER
   ↓
CITATIONS
   ↓
EVALUATION
Future learning modules will include:

Document parsing lessons
Chunking experiments
Chunk visualization
Embedding visualization
Vector database inspection
Dense retrieval lessons
Keyword retrieval
Hybrid search
Query transformation
Reranking experiments
Context management
Prompt experiments
Citation experiments
Conversational RAG
Guardrails
Retrieval evaluation
Generation evaluation
End-to-end evaluation
Observability
Performance analysis
Interactive knowledge checks
Development Philosophy
WORKING > COMPLEX

UNDERSTANDABLE > CLEVER

MODULAR > MONOLITHIC

LOCAL > CLOUD
The project starts with a simple working RAG implementation and will evolve incrementally. Each new capability should be added only after the underlying RAG concept is understood and tested.

Privacy and Local Execution
The core system is designed to operate entirely on the local machine. Documents are processed locally, embeddings are generated locally, ChromaDB is stored locally, and the LLM runs locally through Ollama.

No OpenAI API key or paid cloud API is required for the prototype.

License
This project is intended to be open source. An appropriate open-source license can be added to the repository before distribution.

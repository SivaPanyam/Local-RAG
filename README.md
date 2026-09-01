<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Local RAG - README</title>
<style>
    body {
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.6;
        max-width: 1000px;
        margin: 0 auto;
        padding: 40px 24px;
        color: #222;
        background: #fff;
    }
    h1, h2, h3 { line-height: 1.25; }
    h1 { border-bottom: 2px solid #ddd; padding-bottom: 12px; }
    h2 { margin-top: 36px; border-bottom: 1px solid #ddd; padding-bottom: 6px; }
    code, pre {
        font-family: Consolas, "Courier New", monospace;
    }
    code {
        background: #f2f2f2;
        padding: 2px 5px;
        border-radius: 4px;
    }
    pre {
        background: #f6f8fa;
        padding: 16px;
        overflow-x: auto;
        border-radius: 6px;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 9px 12px;
        text-align: left;
    }
    th { background: #f5f5f5; }
    .note {
        background: #f6f8fa;
        border-left: 4px solid #777;
        padding: 12px 16px;
        margin: 16px 0;
    }
</style>
</head>
<body>

<h1>Local RAG</h1>

<p>
A fully local Retrieval-Augmented Generation (RAG) prototype built with
Python, FastEmbed, ChromaDB, Ollama, and Streamlit.
</p>

<p>
The system processes local documents, creates embeddings, stores them in
ChromaDB, retrieves relevant chunks, and generates answers using the local
<code>llama3.2</code> model through Ollama.
</p>

<p>No OpenAI API or paid cloud API is required.</p>

<h2>Tech Stack</h2>

<table>
<tr><th>Component</th><th>Technology</th></tr>
<tr><td>Language</td><td>Python 3.12+</td></tr>
<tr><td>Document Processing</td><td>LangChain</td></tr>
<tr><td>Embeddings</td><td>FastEmbed</td></tr>
<tr><td>Embedding Model</td><td><code>BAAI/bge-small-en-v1.5</code></td></tr>
<tr><td>Runtime</td><td>ONNX Runtime</td></tr>
<tr><td>Vector Database</td><td>ChromaDB</td></tr>
<tr><td>LLM Runtime</td><td>Ollama</td></tr>
<tr><td>LLM</td><td><code>llama3.2</code></td></tr>
<tr><td>Interface</td><td>Streamlit</td></tr>
</table>

<h2>Project Structure</h2>

<pre>
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
</pre>

<div class="note">
<strong>Note:</strong> <code>watch_folder/</code> is used for local documents,
while <code>chroma_db/</code> contains generated local vector data. Both are
excluded from Git.
</div>

<h2>Installation</h2>

<h3>1. Clone the Repository</h3>

<pre>git clone https://github.com/SivaPanyam/Local-RAG.git
cd Local-RAG</pre>

<h3>2. Create a Virtual Environment</h3>

<pre>python -m venv .venv</pre>

<p>Activate it on Windows PowerShell:</p>

<pre>.venv\Scripts\Activate.ps1</pre>

<h3>3. Verify Python</h3>

<pre>python --version
python -m pip --version</pre>

<h3>4. Install Dependencies</h3>

<pre>python -m pip install --upgrade pip
pip install -r requirements.txt</pre>

<h2>Ollama Setup</h2>

<p>Verify Ollama:</p>

<pre>ollama --version</pre>

<p>Check installed models:</p>

<pre>ollama list</pre>

<p>If <code>llama3.2</code> is not installed:</p>

<pre>ollama pull llama3.2</pre>

<p>Run the model:</p>

<pre>ollama run llama3.2</pre>

<p>Ollama should be available locally at:</p>

<pre>http://localhost:11434</pre>

<p>Verify the local server from PowerShell:</p>

<pre>Invoke-WebRequest http://localhost:11434 -UseBasicParsing</pre>

<h2>Add Documents</h2>

<p>Place documents inside:</p>

<pre>watch_folder/</pre>

<p>Current supported formats:</p>

<pre>.pdf
.txt
.md</pre>

<p>Example:</p>

<pre>watch_folder/
├── document1.pdf
├── document2.pdf
├── notes.txt
└── research.md</pre>

<p>
Documents inside <code>watch_folder/</code> are processed locally and are not
uploaded to GitHub.
</p>

<h2>Index Documents</h2>

<p>From the project root, run:</p>

<pre>python -m tests.test_indexing</pre>

<p>The indexing pipeline performs:</p>

<pre>Documents
    ↓
Document Loading
    ↓
Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Storage</pre>

<p>Example output:</p>

<pre>Loading documents...
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
Vectors:   533</pre>

<h2>Run Retrieval Test</h2>

<pre>python -m tests.test_retrieval</pre>

<p>
This tests semantic similarity retrieval from ChromaDB and displays the
retrieved chunk, source, chunk ID, and distance.
</p>

<h2>Run Prompt Test</h2>

<pre>python -m tests.test_prompt</pre>

<p>
This verifies that retrieved context and the user's question are correctly
combined into the RAG prompt.
</p>

<h2>Run Generation Test</h2>

<pre>python -m tests.test_generation</pre>

<p>
This tests communication with the local Ollama <code>llama3.2</code> model.
</p>

<h2>Run End-to-End RAG Test</h2>

<pre>python -m tests.test_rag</pre>

<p>The complete pipeline is:</p>

<pre>Question
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
Answer</pre>

<h2>Run Streamlit Application</h2>

<pre>python -m streamlit run app/streamlit_app.py</pre>

<p>Open the local application:</p>

<pre>http://localhost:8501</pre>

<p>The interface provides:</p>

<ul>
<li>Document processing</li>
<li>Question input</li>
<li>Answer generation</li>
<li>Retrieved source display</li>
<li>Retrieval distance information</li>
</ul>

<h2>Typical Workflow</h2>

<pre>1. Activate virtual environment
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
13. Answer is generated</pre>

<h2>Useful Commands</h2>

<h3>Environment</h3>

<pre>.venv\Scripts\Activate.ps1
python --version
python -m pip --version</pre>

<h3>Ollama</h3>

<pre>ollama --version
ollama list
ollama pull llama3.2
ollama run llama3.2</pre>

<h3>RAG Tests</h3>

<pre>python -m tests.test_indexing
python -m tests.test_retrieval
python -m tests.test_prompt
python -m tests.test_generation
python -m tests.test_rag</pre>

<h3>Streamlit</h3>

<pre>python -m streamlit run app/streamlit_app.py</pre>

<h2>GitHub Development</h2>

<p>Check repository status:</p>

<pre>git status</pre>

<p>Stage changes:</p>

<pre>git add .</pre>

<p>Commit changes:</p>

<pre>git commit -m "Update RAG prototype"</pre>

<p>Push changes:</p>

<pre>git push</pre>

<h2>Important Git Rules</h2>

<p>The following should not be committed:</p>

<pre>.venv/
chroma_db/
watch_folder/*.pdf
watch_folder/*.txt
watch_folder/*.md
.env</pre>

<p>
The project's <code>.gitignore</code> prevents local environments, generated
vector data, and personal documents from being uploaded.
</p>

<h2>Current RAG Pipeline</h2>

<pre>PDF / TXT / MD
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
Answer</pre>

<h2>Current Status</h2>

<ul>
<li>Local document ingestion</li>
<li>PDF support</li>
<li>TXT support</li>
<li>Markdown support</li>
<li>Configurable document chunking</li>
<li>FastEmbed embeddings</li>
<li><code>BAAI/bge-small-en-v1.5</code></li>
<li>384-dimensional embeddings</li>
<li>Persistent ChromaDB storage</li>
<li>Semantic similarity retrieval</li>
<li>Context construction</li>
<li>Grounded RAG prompt</li>
<li>Ollama integration</li>
<li><code>llama3.2</code> generation</li>
<li>End-to-end RAG pipeline</li>
<li>Multi-document indexing</li>
<li>Streamlit interface</li>
<li>Component-level tests</li>
</ul>

<h2>Current Limitations</h2>

<p>The first prototype intentionally keeps the implementation simple.</p>

<ul>
<li>Current document support is PDF, TXT, and Markdown.</li>
<li>Retrieval currently uses dense vector similarity.</li>
<li>No hybrid BM25 + vector search yet.</li>
<li>No reranking yet.</li>
<li>No advanced query transformation.</li>
<li>No OCR pipeline yet.</li>
<li>No multimodal document processing yet.</li>
<li>No advanced citation system yet.</li>
<li>No retrieval evaluation framework yet.</li>
<li>No generation evaluation framework yet.</li>
<li>No production-scale optimization yet.</li>
</ul>

<h2>Future Development</h2>

<p>Future versions will gradually add:</p>

<ul>
<li>DOCX support</li>
<li>PPT/PPTX support</li>
<li>XLSX and CSV support</li>
<li>HTML/web document ingestion</li>
<li>OCR</li>
<li>Table extraction</li>
<li>Image-aware processing</li>
<li>Semantic chunking</li>
<li>Hybrid search</li>
<li>BM25 retrieval</li>
<li>Query transformation</li>
<li>Reranking</li>
<li>Metadata filtering</li>
<li>Improved citations</li>
<li>Conversational RAG</li>
<li>Guardrails</li>
<li>Retrieval evaluation</li>
<li>Generation evaluation</li>
<li>End-to-end evaluation</li>
<li>Observability and tracing</li>
<li>Performance analysis</li>
<li>Experiment tracking</li>
</ul>

<h2>RAG Learning Lab — Long-Term Goal</h2>

<p>
The long-term goal is to evolve this prototype into an interactive
RAG Learning Lab.
</p>

<p>
Instead of hiding the RAG process behind a single chatbot interface, the
future system will allow learners to inspect what actually happens at every
stage.
</p>

<pre>DOCUMENT
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
EVALUATION</pre>

<p>Future learning modules will include:</p>

<ul>
<li>Document parsing lessons</li>
<li>Chunking experiments</li>
<li>Chunk visualization</li>
<li>Embedding visualization</li>
<li>Vector database inspection</li>
<li>Dense retrieval lessons</li>
<li>Keyword retrieval</li>
<li>Hybrid search</li>
<li>Query transformation</li>
<li>Reranking experiments</li>
<li>Context management</li>
<li>Prompt experiments</li>
<li>Citation experiments</li>
<li>Conversational RAG</li>
<li>Guardrails</li>
<li>Retrieval evaluation</li>
<li>Generation evaluation</li>
<li>End-to-end evaluation</li>
<li>Observability</li>
<li>Performance analysis</li>
<li>Interactive knowledge checks</li>
</ul>

<h2>Development Philosophy</h2>

<pre>WORKING > COMPLEX

UNDERSTANDABLE > CLEVER

MODULAR > MONOLITHIC

LOCAL > CLOUD</pre>

<p>
The project starts with a simple working RAG implementation and will evolve
incrementally. Each new capability should be added only after the underlying
RAG concept is understood and tested.
</p>

<h2>Privacy and Local Execution</h2>

<p>
The core system is designed to operate entirely on the local machine.
Documents are processed locally, embeddings are generated locally,
ChromaDB is stored locally, and the LLM runs locally through Ollama.
</p>

<p>
No OpenAI API key or paid cloud API is required for the prototype.
</p>

<h2>License</h2>

<p>
This project is intended to be open source. An appropriate open-source
license can be added to the repository before distribution.
</p>

</body>
</html>

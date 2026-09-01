from app.vector_store import create_vector_store
from app.retrieval import retrieve_documents
from app.rag_pipeline import build_prompt


collection = create_vector_store()

question = "What does RAG stand for?"

results = retrieve_documents(
    question,
    collection,
    top_k=3,
)

prompt = build_prompt(
    question,
    results,
)

print(prompt)
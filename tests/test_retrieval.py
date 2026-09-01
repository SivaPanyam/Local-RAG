from app.vector_store import create_vector_store
from app.retrieval import retrieve_documents


collection = create_vector_store()

questions = [
    "What does RAG stand for?",
    "How many dimensions does the embedding model produce?",
    "What is the purpose of the vector database?",
]


for question in questions:
    print()
    print("=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    results = retrieve_documents(
        question,
        collection,
        top_k=2,
    )

    for i, result in enumerate(results, start=1):
        print()
        print(f"RESULT {i}")
        print(f"Source: {result['metadata'].get('source')}")
        print(f"Chunk ID: {result['metadata'].get('chunk_id')}")
        print(f"Distance: {result['distance']}")
        print(f"Chunk: {result['chunk'][:500]}")
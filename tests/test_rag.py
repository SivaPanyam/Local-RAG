from app.rag_pipeline import ask_question


question = "What does RAG stand for?"

result = ask_question(
    question,
    top_k=3,
)

print("\nANSWER")
print("=" * 60)
print(result["answer"])

print("\nSOURCES")
print("=" * 60)

for source in result["sources"]:
    print(f"Source: {source['metadata'].get('source')}")
    print(f"Distance: {source['distance']}")
    print(f"Chunk: {source['chunk']}")
    print()
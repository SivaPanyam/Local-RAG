from app.indexing import process_documents


result = process_documents()

print()
print("=" * 50)
print("INDEXING COMPLETE")
print("=" * 50)
print(f"Documents: {result['documents']}")
print(f"Chunks:    {result['chunks']}")
print(f"Vectors:   {result['vectors']}")
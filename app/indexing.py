from .ingestion import load_documents
from .chunking import split_documents
from .embeddings import create_embedding_model, create_embeddings
from .vector_store import reset_vector_store, store_vectors


def process_documents(folder_path="./watch_folder"):
    print("Loading documents...")
    documents = load_documents(folder_path)

    print(f"Documents loaded: {len(documents)}")

    if not documents:
        return {
            "documents": 0,
            "chunks": 0,
            "vectors": 0,
        }

    print("Splitting documents...")
    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    collection = reset_vector_store()

    
    print("Creating embeddings...")
    model = create_embedding_model()

    embeddings = create_embeddings(
        [chunk.page_content for chunk in chunks],
        model,
    )

    print(f"Embeddings created: {len(embeddings)}")

    print("Storing vectors...")

    store_vectors(
        chunks,
        embeddings,
        collection,
    )

    print(f"Vectors stored: {collection.count()}")

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "vectors": len(embeddings),
    }
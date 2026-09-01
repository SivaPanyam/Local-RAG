import chromadb


DB_PATH = "./chroma_db"
COLLECTION_NAME = "rag_documents"


def create_vector_store():
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def reset_vector_store():
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def store_vectors(chunks, embeddings, collection):
    ids = [
        f"{chunk.metadata.get('source', 'unknown')}_chunk_{chunk.metadata.get('chunk_id', i)}"
        for i, chunk in enumerate(chunks)
    ]

    documents = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk.metadata.get("source", "unknown"),
            "chunk_id": str(
                chunk.metadata.get("chunk_id", i)
            ),
            **(
                {"page": chunk.metadata["page"]}
                if "page" in chunk.metadata
                else {}
            ),
        }
        for i, chunk in enumerate(chunks)
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def get_collection():
    return create_vector_store()
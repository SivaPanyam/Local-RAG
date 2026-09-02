from .ingestion import load_documents
from .chunking import split_documents
from .embeddings import create_embedding_model, create_embeddings
from .vector_store import reset_vector_store, store_vectors


def process_documents(folder_path="./watch_folder", progress_callback=None):

    def update(stage, current, total, message):
        if progress_callback:
            progress_callback(stage, current, total, message)

    # --------------------------------------------------
    # 1. Load documents
    # --------------------------------------------------

    update(
        "loading",
        0,
        1,
        "Loading PDFs..."
    )

    documents = load_documents(folder_path)

    print(f"Documents loaded: {len(documents)}")

    update(
        "loading",
        1,
        1,
        f"Loaded {len(documents)} documents"
    )

    if not documents:
        return {
            "documents": 0,
            "chunks": 0,
            "vectors": 0,
        }

    # --------------------------------------------------
    # 2. Create chunks
    # --------------------------------------------------

    update(
        "chunking",
        0,
        1,
        "Creating chunks..."
    )

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    update(
        "chunking",
        1,
        1,
        f"Created {len(chunks)} chunks"
    )

    # --------------------------------------------------
    # 3. Create embeddings
    # --------------------------------------------------

    collection = reset_vector_store()

    print("Creating embeddings...")

    model = create_embedding_model()

    def embedding_progress(current, total):
        update(
            "embedding",
            current,
            total,
            f"Generating embeddings... {current}/{total}"
        )

    embeddings = create_embeddings(
        [chunk.page_content for chunk in chunks],
        model,
        progress_callback=embedding_progress,
    )

    print(f"Embeddings created: {len(embeddings)}")

    # --------------------------------------------------
    # 4. Store vectors
    # --------------------------------------------------

    update(
        "storing",
        0,
        1,
        "Storing vectors in ChromaDB..."
    )

    store_vectors(
        chunks,
        embeddings,
        collection
    )

    vector_count = collection.count()

    print(f"Vectors stored: {vector_count}")

    update(
        "storing",
        1,
        1,
        f"Stored {vector_count} vectors"
    )

    # --------------------------------------------------
    # Return indexing statistics
    # --------------------------------------------------

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "vectors": len(embeddings),
    }
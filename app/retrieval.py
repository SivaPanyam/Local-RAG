from .embeddings import create_embedding_model, create_embeddings

def retrieve_documents(
    question,
    collection,
    top_k=3,
):
    model = create_embedding_model()

    query_embedding = create_embeddings(
        [question],
        model,
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):
        retrieved_documents.append(
            {
                "chunk": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return retrieved_documents
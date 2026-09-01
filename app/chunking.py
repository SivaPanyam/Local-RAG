from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=800, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    document_chunk_counts = {}

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")

        chunk_index = document_chunk_counts.get(source, 0)

        chunk.metadata["chunk_id"] = chunk_index

        document_chunk_counts[source] = chunk_index + 1

    return chunks
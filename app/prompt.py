def build_prompt(question, retrieved_documents):
    context_parts = []

    for i, document in enumerate(retrieved_documents, start=1):
        source = document["metadata"].get("source", "unknown")

        context_parts.append(
            f"[Source {i}: {source}]\n"
            f"{document['chunk']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are answering a question using retrieved documents.

Use the information in the CONTEXT to answer the QUESTION.

Rules:
1. Answer directly and concisely.
2. Use information from the CONTEXT.
3. Do not use outside knowledge.
4. Do not say that information is missing if the CONTEXT contains the answer.
5. If the CONTEXT does not contain the answer, respond exactly:
I don't have enough information in the provided documents.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    return prompt
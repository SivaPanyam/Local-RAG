from .vector_store import create_vector_store
from .retrieval import retrieve_documents
from .prompt import build_prompt
from .generation import generate_answer, classify_question


def ask_question(question, top_k=3):
    """
    Route a question through either normal conversation
    or the RAG pipeline.
    """

    route = classify_question(question)

    # --------------------------------------------------
    # Normal conversation
    # --------------------------------------------------

    if route == "CHAT":

        prompt = f"""You are a helpful local AI assistant.

Respond naturally and briefly to the user's message.

Do not pretend that the message is a document question.

User:
{question}

Answer:"""

        answer = generate_answer(prompt)

        return {
            "answer": answer,
            "sources": [],
            "route": "CHAT",
        }

    # --------------------------------------------------
    # Document question
    # --------------------------------------------------

    collection = create_vector_store()

    retrieved_documents = retrieve_documents(
        question,
        collection,
        top_k=top_k,
    )

    prompt = build_prompt(
        question,
        retrieved_documents,
    )

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": retrieved_documents,
        "route": "DOCUMENT",
    }
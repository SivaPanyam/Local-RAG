from .vector_store import create_vector_store
from .retrieval import retrieve_documents
from .prompt import build_prompt
from .generation import generate_answer


def ask_question(question, top_k=3):
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
    }
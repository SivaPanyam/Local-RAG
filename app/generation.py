import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"


def generate_answer(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


def classify_question(question):
    """
    Use the local Ollama model to determine whether
    a question requires document retrieval.

    Returns:
        "DOCUMENT" or "CHAT"
    """

    prompt = f"""You are a query router for a local RAG system.

Determine whether the user's question requires information
from the user's indexed documents.

Return exactly one word:

DOCUMENT
or
CHAT

Use DOCUMENT when the question asks about information,
facts, explanations, concepts, procedures, or content that
could reasonably require knowledge from the user's documents.

Use CHAT for normal conversation, greetings, small talk,
thanks, opinions, or questions that do not require the
user's documents.

Examples:

User: Hello
CHAT

User: How are you?
CHAT

User: Thanks
CHAT

User: What does RAG stand for?
DOCUMENT

User: Explain the vector database used in the project.
DOCUMENT

User: What is the purpose of chunking?
DOCUMENT

Now classify this question:

User: {question}

Classification:"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    classification = data["response"].strip().upper()

    if "DOCUMENT" in classification:
        return "DOCUMENT"

    return "CHAT"
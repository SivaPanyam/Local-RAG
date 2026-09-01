from app.generation import generate_answer


prompt = """You are a helpful assistant.

Answer this question in one sentence:

What does RAG stand for?

Answer:"""


answer = generate_answer(prompt)

print("Answer:")
print(answer)
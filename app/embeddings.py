import onnxruntime
from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_execution_provider():
    providers = onnxruntime.get_available_providers()

    if "CUDAExecutionProvider" in providers:
        return "CUDAExecutionProvider"

    return "CPUExecutionProvider"


def create_embedding_model():
    provider = get_execution_provider()

    if provider == "CUDAExecutionProvider":
        onnxruntime.preload_dlls(directory="")

    print(f"Embedding execution provider: {provider}")

    return TextEmbedding(
        model_name=MODEL_NAME,
        providers=[provider],
    )


def create_embeddings(texts, model, progress_callback=None):
    embeddings = []

    total = len(texts)

    for index, embedding in enumerate(model.embed(texts), start=1):
        embeddings.append(embedding)

        if progress_callback:
            progress_callback(index, total)

    return embeddings
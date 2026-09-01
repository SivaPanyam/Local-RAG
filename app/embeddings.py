from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def create_embedding_model():
    return TextEmbedding(model_name=MODEL_NAME)


def create_embeddings(texts, model):
    embeddings = list(model.embed(texts))
    return embeddings
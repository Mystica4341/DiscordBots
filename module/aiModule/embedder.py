from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder

def embedderDoc():
    embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/bert-base-nli-mean-tokens")
    embedder.warm_up()
    return embedder

def embedderText():
    embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/bert-base-nli-mean-tokens")
    embedder.warm_up()
    return embedder
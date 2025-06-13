from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from module.aiModule.documentStore import documentStore

def retriever():
    return QdrantEmbeddingRetriever(document_store=documentStore())
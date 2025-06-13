import os
from dotenv import load_dotenv
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.utils import Secret

from module.aiModule.database import get_qdrant_client
from qdrant_client.models import VectorParams, Distance

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

qdrant_Client = get_qdrant_client()

# initialize the QdrantDocumentStore
def documentStore():
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in the environment variables.")

    return QdrantDocumentStore(
        url=QDRANT_URL,
        api_key=Secret.from_token(QDRANT_API_KEY),
        index = "DiscordData",  # Specify your index name
        similarity="cosine",  # Specify the similarity metric
        embedding_dim=768,  # Specify the embedding dimension (768 for BERT-like models, adjust as needed)
    )

# function to create collection in Qdrant if it does not exist
def CreateCollection():
    if not qdrant_Client.collection_exists("DiscordData"):
        qdrant_Client.create_collection(collection_name= "DiscordData",
                                        vectors_config=VectorParams(size=768, distance=Distance.COSINE))
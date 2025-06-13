from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()
QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

def get_qdrant_client():
    if not QDRANT_HOST or not QDRANT_API_KEY:
        raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set in the environment variables.")
    
    return QdrantClient(
        url=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
        port=6333  # Default Qdrant port
    )
    
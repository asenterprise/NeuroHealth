import os
from dotenv import load_dotenv

# Load .env file (only once, желательно делать в main.py)
load_dotenv()

# Qdrant settings
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

# Collection names (optional override)
QDRANT_COLLECTIONS = {
    "headers": os.getenv("QDRANT_COLLECTION_HEADERS", "lectures_headers_en"),
    "fulltext": os.getenv("QDRANT_COLLECTION_FULLTEXT", "lectures_fulltext_en")
}

# Embedding model
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", 384))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

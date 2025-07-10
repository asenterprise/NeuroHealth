from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config.settings import settings
import logging

qdrant = AsyncQdrantClient(
    host=settings.QDRANT_HOST, 
    port=settings.QDRANT_PORT
)

async def recreate_collections():
    for name in settings.QDRANT_COLLECTIONS.values():
        try:
            await qdrant.recreate_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=settings.VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
            logging.info(f"Collection {name} recreated successfully")
        except Exception as e:
            logging.error(f"Error recreating collection {name}: {str(e)}")
            raise
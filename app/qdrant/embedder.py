from sentence_transformers import SentenceTransformer
from app.config.settings import settings
import logging

try:
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
except Exception as e:
    logging.error(f"Failed to load embedding model: {str(e)}")
    raise

def get_vector(text: str) -> list:
    try:
        return model.encode(text.strip() or "").tolist()
    except Exception as e:
        logging.error(f"Error encoding text: {str(e)}")
        return []
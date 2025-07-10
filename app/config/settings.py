import os
from dotenv import load_dotenv
from pathlib import Path

# Загрузка .env файла
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

class Settings:
    # Настройки PostgreSQL
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Настройки Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT"))
    
    # Названия коллекций
    QDRANT_COLLECTIONS = {
        "headers": os.getenv("QDRANT_COLLECTION_HEADERS"),
        "fulltext": os.getenv("QDRANT_COLLECTION_FULLTEXT")
    }
    
    # Настройки модели
    VECTOR_SIZE: int = int(os.getenv("VECTOR_SIZE"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")

settings = Settings()
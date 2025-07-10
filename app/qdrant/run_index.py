from app.qdrant.indexer import reindex
from app.qdrant.client import recreate_collections


if __name__ == "__main__":
    recreate_collections()
    reindex()

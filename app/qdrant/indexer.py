import asyncpg
import logging
from .loader import fetch_sections
from .embedder import get_vector
from .prepare import build_header_text, prepare_payload
from .client import qdrant
from .config import QDRANT_COLLECTIONS

async def reindex():
    sections = await fetch_sections()
    headers, fulltexts = [], []

    for idx, section in enumerate(sections):
        header_text = build_header_text(section)
        full_text = f"{header_text} {section.get('content') or ''}"

        headers.append({
            "id": idx,
            "vector": get_vector(header_text),
            "payload": prepare_payload(section)
        })
        fulltexts.append({
            "id": idx,
            "vector": get_vector(full_text),
            "payload": prepare_payload(section, include_content=True)
        })

    await qdrant.upsert(collection_name=QDRANT_COLLECTIONS["headers"], points=headers)
    await qdrant.upsert(collection_name=QDRANT_COLLECTIONS["fulltext"], points=fulltexts)


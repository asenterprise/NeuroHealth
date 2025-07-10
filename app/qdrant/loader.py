import asyncpg
from app.db.connection import fetch_all

async def fetch_sections():
        return await fetch_all("""
            SELECT id, lecture_id, level_1, level_2, level_3, level_4, content
            FROM sections_en
        """)


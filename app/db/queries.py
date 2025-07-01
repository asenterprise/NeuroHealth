import asyncpg
import os
import  re
import html
from typing import List, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost/neurohealth")

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

async def add_lecture(conn: asyncpg.Connection, title: str, content: str):
    """Saves the lecture to the database after cleaning the text and returns its ID"""

    # Clean HTML characters
    safe_title = html.escape(title).strip()
    safe_content = html.escape(content).strip()

    # Remove the ¶ character
    safe_title = re.sub(r"¶", "", safe_title)
    safe_content = re.sub(r"¶", "", safe_content)

    # Remove extra spaces and newlines
    safe_title = re.sub(r"\s+", " ", safe_title)
    safe_content = re.sub(r"\s+", " ", safe_content)

    # Save the lecture to the database and return its ID
    row = await conn.fetchrow(
        "INSERT INTO lectures_en (title, content) VALUES ($1, $2) RETURNING id",
        title, content
    )
    await conn.close()
    return row["id"]

async def add_sections(conn: asyncpg.Connection, lecture_id: int, sections: List[Dict[str, str]]):
    """
    Adds lecture sections to the 'sections' table.

    :param conn: database connection
    :param lecture_id: ID of the lecture
    :param sections: list of dictionaries containing section data
    """
    query = """
        INSERT INTO sections_en (
            lecture_id, section_number, header, content, level, 
            level_1, level_2, level_3, level_4, section_type_id
        ) VALUES (
            $1, $2, $3, $4, $5, 
            $6, $7, $8, $9, 2
        )
    """

    if not sections:
        raise ValueError("The section list is empty. Cannot add to the database.")

    try:
        async with conn.transaction():  # Wrap in a transaction for reliability
            await conn.executemany(
                query,
                [
                    (
                        lecture_id,
                        section["number"],
                        section["title"],
                        section["content"],
                        section["level"],
                        section["level_1"],
                        section["level_2"],
                        section["level_3"],
                        section["level_4"]
                    )
                    for section in sections
                ]
            )
    except asyncpg.PostgresError as e:
        raise RuntimeError(f"Error while inserting sections into the database: {str(e)}")

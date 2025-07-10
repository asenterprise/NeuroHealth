import os
from dotenv import load_dotenv
import asyncpg
from typing import AsyncGenerator

# Load environment variables from .env file (optional but recommended)
load_dotenv()

# Read PostgreSQL connection details from environment variables
POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123@localhost:5432/neurohealth"
)

# Simple connection getter
async def get_db_connection() -> asyncpg.Connection:
    return await asyncpg.connect(POSTGRES_URL)

# Generator for dependency injection (FastAPI)
async def get_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    conn = await asyncpg.connect(POSTGRES_URL)
    try:
        yield conn
    finally:
        await conn.close()

import asyncpg
from asyncpg.pool import Pool
from app.config.settings import settings
from typing import List, Dict, Any
import logging

_pool: Pool = None

async def create_pool():
    """Создает пул соединений с БД"""
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,
                min_size=1,
                max_size=10
            )
            logging.info("Database pool created successfully")
        except Exception as e:
            logging.error(f"Error creating database pool: {str(e)}")
            raise

async def close_pool():
    """Закрывает пул соединений"""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logging.info("Database pool closed")

async def _ensure_pool_initialized():
    """Проверяет инициализацию пула соединений"""
    if _pool is None:
        logging.warning("Database pool not initialized, creating now...")
        await create_pool()

async def fetch_all(query: str, *args) -> List[Dict[str, Any]]:
    """Выполняет запрос и возвращает все строки как список словарей"""
    await _ensure_pool_initialized()
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    except Exception as e:
        logging.error(f"Error in fetch_all: {str(e)}")
        raise

async def execute_many(query: str, data: List[tuple]):
    """Выполняет массовую вставку данных"""
    await _ensure_pool_initialized()
    try:
        async with _pool.acquire() as conn:
            await conn.executemany(query, data)
            logging.info(f"Executed many: {len(data)} rows affected")
    except Exception as e:
        logging.error(f"Error in execute_many: {str(e)}")
        raise
from .settings import settings

DB_CONFIG = {
    "host": settings.POSTGRES_HOST,
    "port": settings.POSTGRES_PORT,
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
    "database": settings.POSTGRES_DB
}
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Async URL for FastAPI (uses asyncpg)
DATABASE_URL_ASYNC = os.getenv(
    "DATABASE_URL_ASYNC", 
    "postgresql+asyncpg://localhost/gmail_scheduler"
)

# Sync URL for Alembic (uses psycopg2)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://localhost/gmail_scheduler"
)

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync engine (for Alembic migrations)
sync_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db():
    """Synchronous database session for Celery tasks."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/gmail_scheduler")

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()


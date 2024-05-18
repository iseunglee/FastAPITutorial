# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("MY_DB_PASSWORD")

DATABASE_URL = "postgresql+asyncpg://postgres:" + DB_PASSWORD + "@hanslab.org:25432/testdb"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session
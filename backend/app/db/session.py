from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core import config

engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URI,
)

AsyncSessionLocal = sessionmaker(engine, future=True, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

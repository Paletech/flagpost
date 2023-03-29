from typing import Union
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Files, Posts


async def get_all_files(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Files).offset(skip).limit(limit))
    files = result.scalars().all()
    return files


async def get_file(db: AsyncSession, file_id: UUID):
    result = await db.execute(select(Files).filter_by(id=file_id))
    file = result.scalar().first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


async def create_file(db: AsyncSession, post_id: Union[UUID, None], path: str):
    if post_id is not None:
        post = await db.execute(select(Posts).filter_by(id=post_id))
        if not post.scalar().first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_files = Files(
        path=path,
        post_id=post_id,
    )

    db.add(db_files)
    await db.commit()
    await db.refresh(db_files)
    return db_files


async def delete_file(db: AsyncSession, file: UUID):
    file = await get_file(db, file)
    if not file:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    await db.delete(file)
    await db.commit()
    return file

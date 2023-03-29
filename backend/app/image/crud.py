from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.db.models import Images
from app.image.schemas import ImageOut


async def get_all_images(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ImageOut]:
    result = await db.execute(select(Images).offset(skip).limit(limit))
    images = result.scalars().all()
    return images


async def get_image(db: AsyncSession, image_id: UUID):
    result = await db.execute(select(Images).filter_by(id=image_id))
    image = result.scalars().first()
    if not image:
        raise HTTPException(status_code=404, detail="File not found")
    return image


async def create_image(db: AsyncSession, path):
    db_image = models.Images(
        path=path,
    )

    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image


async def delete_image(db: AsyncSession, image: UUID):
    image = await get_image(db, image)
    if not image:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")

    await db.delete(image)
    await db.commit()
    return image

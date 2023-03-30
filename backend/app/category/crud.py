from typing import Collection
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.schemas import CategoryCreate, CategoryEdit, CategoryOut
from app.db.models import Categories, Images


async def get_all_categories(db: AsyncSession, skip: int, limit: int) -> Collection[CategoryOut]:
    result = await db.execute(select(Categories).offset(skip).limit(limit))
    categories = result.scalars().all()
    return categories


async def get_my_category(db: AsyncSession, skip: int, limit: int, user_id: UUID) -> Collection[CategoryOut]:
    result = await db.execute(
        select(Categories)
        .filter_by(user_id=user_id)
        .offset(skip)
        .limit(limit)
    )
    category = result.scalars().all()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def get_category(db: AsyncSession, category_id: UUID):
    result = await db.execute(select(Categories).filter_by(id=category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def create_category(db: AsyncSession, user_id: UUID, category: CategoryCreate):

    if category.image_id is not None:
        image = await db.execute(select(Images).filter_by(id=category.image_id))
        if not image.scalars().first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
    db_category = Categories(
        user_id=user_id,
        name=category.name,
        color=category.color,
        image_id=category.image_id,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


# def choose_category(db: Session, user_id: int, category: schemas.CategoryCreate):
#     db_category = models.Categories(
#         user_id=user_id,
#         name=category.name,
#         color=category.color,
#         image_id=category.image_id,
#     )
#     db.add(db_category)
#     db.commit()
#     db.refresh(db_category)
#     return db_category


async def delete_category(db: AsyncSession, category: UUID):
    category = await get_category(db, category)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    await db.delete(category)
    await db.commit()
    return category


async def edit_category(db: AsyncSession, category_id: UUID, category: CategoryEdit) -> CategoryOut:
    db_category = await get_category(db, category_id)
    if not db_category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    update_data = category.dict(exclude_unset=True)
    if category.image_id and update_data.get("image_id") is not None:
        query = await db.execute(
            select(Categories.id)
            .where(Images.id==update_data.get("image_id"))
        )
        cat_id = query.scalars().first()
        if not cat_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

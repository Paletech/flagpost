from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import literal

from app.db.models import Categories, Files, Posts
from app.post.schemas import PostBase, PostCreate, PostOut


async def get_all_posts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[PostOut]:
    result = await db.execute(select(Posts).offset(skip).limit(limit))
    posts = result.scalars().all()
    return posts


async def get_post(db: AsyncSession, post_id: UUID):
    result = await db.execute(select(Posts).filter_by(id=post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def get_my_post(db: AsyncSession, post_id: UUID, user_id: UUID):
    result = await db.execute(select(Posts).filter_by(user_id=user_id, id=post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def create_post(db: AsyncSession, user_id: UUID, post: PostCreate):
    db_post = Posts(
        user_id=user_id,
        text=post.text,
        type=post.type,
    )

    if post.files and post.files is not None:
        query = await db.execute(select(literal(True)).filter(Files.id == post.files))
        result = query.scalar_one_or_none()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
        else:
            files = await db.get(Files, post.files)
            db_post.files.append(files)

    if post.categories and post.categories is not None:
        query = await db.execute(select(literal(True)).filter(Categories.id == post.categories))
        result = query.scalar_one_or_none()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
        else:
            categories = await db.get(Categories, post.categories)
            # db_post.categories.add(post.categories)
            # categories.id = str(categories.id)
            # db_post.categories.user_id = str(categories.user_id)

            db_post.categories = [categories]

    # files = db.query(models.Files).get(post.files)
    # categories = db.query(models.Categories).get(post.categories)
    # db_post.categories.add(post.categories)
    # db_post.categories = [categories]

    # db_post.files.append(files)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, user_id: UUID, post_id: UUID):
    post = await get_my_post(db, post_id, user_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return post


async def edit_post(db: AsyncSession, user_id: UUID, post_id: UUID, post: PostBase) -> PostOut:
    db_post = await get_my_post(db, post_id, user_id)
    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    update_data = post.dict(exclude_unset=True)
    if update_data.get("files") is not None:
        query = await db.execute(
            select(Posts.id)
            .filter(Files.id==update_data.get('files'))
        )
        result = query.scalars().first()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")

    if update_data.get("categories") is not None:
        query = await db.execute(
            select(Posts.id)
            .filter(Categories.id == update_data["categories"])
        )
        result = query.scalars().first()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

    files = await db.get(Files, update_data.pop("files"))
    categories = await db.get(Categories, update_data.pop("categories"))
    db_post.categories = [categories]
    db_post.files.append(files)

    # files = db.query(models.Files).get(update_data.pop("files"))
    # db_post.files = files
    # update_data.pop("files")

    # db_post.categories = update_data.pop("categories")

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

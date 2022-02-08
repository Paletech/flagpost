from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from sqlalchemy.sql.expression import literal
from . import schemas

from app.db import models


def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.PostOut]:
    return db.query(models.Posts).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: UUID):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_my_post(db: Session, post_id: UUID, user_id: UUID):
    post = db.query(models.Posts).filter(models.Posts.user_id == user_id.id, models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def create_post(db: Session, user_id: UUID, post: schemas.PostCreate):

    db_post = models.Posts(
        user_id=user_id,
        text=post.text,
        type=post.type,
    )

    if post.files and post.files is not None:
        if not db.query(literal(True)).filter(models.Files.id == post.files).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
        else:
            files = db.query(models.Files).get(post.files)
            db_post.files.append(files)

    if post.categories and post.categories is not None:
        if not db.query(literal(True)).filter(models.Categories.id == post.categories).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
        else:
            categories = db.query(models.Categories).get(post.categories)
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
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, user_id: UUID, post_id: UUID):
    post = get_my_post(db, post_id, user_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return post


def edit_post(db: Session, user_id: UUID, post_id: UUID, post: schemas.PostBase) -> schemas.PostOut:
    db_post = get_my_post(db, post_id, user_id)
    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    update_data = post.dict(exclude_unset=True)
    if update_data["files"] is not None:
        if not db.query(models.Posts.id).filter(models.Files.id == update_data["files"]).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")

    if update_data["categories"] is not None:
        if not db.query(models.Posts.id).filter(models.Categories.id == update_data["categories"]).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

    files = db.query(models.Files).get(update_data.pop("files"))
    categories = db.query(models.Categories).get(update_data.pop("categories"))
    db_post.categories = [categories]
    db_post.files.append(files)


    # files = db.query(models.Files).get(update_data.pop("files"))
    # db_post.files = files
    # update_data.pop("files")

    # db_post.categories = update_data.pop("categories")

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post




import typing as t
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import literal
from sqlalchemy.orm import joinedload

from app.db import models
from . import schemas


# TODO joinedload works
def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.PostOut]:
    return db.query(models.Posts).options(joinedload(models.Posts.files), joinedload(models.Posts.categories)).offset(skip).limit(limit).all()


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
        for file in post.files:
            if not db.query(literal(True)).filter(models.Files.id == file).first():
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
            else:
                files = db.query(models.Files).get(file)
                db_post.files.append(files)

    if post.categories and post.categories is not None:
        for category in post.categories:
            if not db.query(literal(True)).filter(models.Categories.id == category).first():
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
            else:
                categories = db.query(models.Categories).get(category)
                db_post.categories.append(categories)

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

    # TODO optimization needed
    if 'files' in update_data and update_data["files"] is not None:
        for file in update_data["files"]:
            if not db.query(models.Posts.id).filter(models.Files.id == file).first():
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
        else:
            db_post.files = []
            kek = update_data.pop("files")
            for i in kek:
                files = db.query(models.Files).get(i)
                db_post.files.append(files)

    # TODO optimization needed
    if 'categories' in update_data and update_data["categories"] is not None:
        for category in update_data["categories"]:
            if not db.query(models.Posts.id).filter(models.Categories.id == category).first():
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
        else:
            db_post.categories = []
            kek = update_data.pop("categories")
            for i in kek:
                categories = db.query(models.Categories).get(i)
                db_post.categories.append(categories)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

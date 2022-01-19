from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models


def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.PostOut]:
    return db.query(models.Posts).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_my_post(db: Session, user_id: int):
    post = db.query(models.Posts).filter(models.Categories.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def create_post(db: Session, user_id: int, post: schemas.PostCreate):
    db_post = models.Posts(
        user_id=user_id,
        text=post.text,
        # categories=post.categories,
        # files=post.files,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post: int):
    post = get_my_post(db, post)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return post


def edit_post(db: Session, post_id: int, post: schemas.PostBase) -> schemas.PostOut:
    db_post = get_my_post(db, post_id)
    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    update_data = post.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.CategoryOut]:
    return db.query(models.Categories).offset(skip).limit(limit).all()


def get_my_category(db: Session, user_id: int):
    category = db.query(models.Categories).filter(models.Categories.user_id == user_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_category(db: Session, user_id: int):
    category = db.query(models.Categories).filter(models.Categories.id == user_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(db: Session, user_id: int, category: schemas.CategoryCreate):
    db_category = models.Categories(
        user_id=user_id,
        name=category.name,
        color=category.color,
        # image_id=category.image_id,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
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


def delete_category(db: Session, category: int):
    category = get_category(db, category)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(category)
    db.commit()
    return category

#fix schemas.JobBase
# def edit_user( db: Session, user_id: int, job: schemas.JobBase) -> schemas.User:
#     db_job = get_jobs(db, user_id)
#     if not db_job:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
#     update_data = job.dict(exclude_unset=True)
#
#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(user.password)
#         del update_data["password"]
#
#     for key, value in update_data.items():
#         setattr(db_user, key, value)
#
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

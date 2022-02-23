from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from sqlalchemy.sql.expression import literal
from . import schemas

from app.db import models


def get_all_categories(db: Session, skip: int, limit: int) -> t.List[schemas.CategoryOut]:
    return db.query(models.Categories).offset(skip).limit(limit).all()


def get_my_categories(db: Session, skip: int, limit: int, user_id: UUID):
    category = db.query(models.Categories).filter(models.Categories.user_id == user_id.id).offset(skip).limit(limit).all()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_my_category(db: Session, category_id: UUID, user_id: UUID):
    category = db.query(models.Categories).filter(models.Categories.user_id == user_id.id, models.Categories.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_admin_category(db: Session, category_id: UUID, user_id: UUID):

    if db.query(models.User.is_superuser).filter_by(id=user_id.id).scalar():

        category = db.query(models.Categories).filter(models.Categories.user_id == user_id.id, models.Categories.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category


def get_category(db: Session, category_id: UUID):
    category = db.query(models.Categories).filter(models.Categories.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(db: Session, user_id: UUID, category: schemas.CategoryCreate):
    if category.image_id is not None:
        if not db.query(literal(True)).filter(models.Images.id == category.image_id).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
    db_category = models.Categories(
        user_id=user_id,
        name=category.name,
        color=category.color,
        image_id=category.image_id,
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


def delete_category(db: Session, category_id: UUID, user_id: UUID):

    category = get_admin_category(db, category_id, user_id)
    if category is None:
        category = get_my_category(db, category_id, user_id)
        if not category:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
    return category


def edit_category(db: Session, category_id: UUID, user_id: UUID, category: schemas.CategoryEdit) -> schemas.CategoryOut:

    db_category = get_admin_category(db, category_id, user_id)
    if db_category is None:
        db_category = get_my_category(db, category_id, user_id)
        if not db_category:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = category.dict(exclude_unset=True)
    if category.image_id and update_data["image_id"] is not None:
        if not db.query(models.Categories.id).filter(models.Images.id == update_data["image_id"]).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models
# from ..core.upload_data import delete_file_from_s3  # TODO


def get_all_images(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.ImageOut]:
    return db.query(models.Images).offset(skip).limit(limit).all()


def get_image(db: Session, image_id: UUID):
    image = db.query(models.Images).filter(models.Images.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="File not found")
    return image


def create_image(db: Session, path):
    db_image = models.Images(
        path=path,
        public_path=path
    )

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image: UUID):
    if not image:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    db.delete(image)
    db.commit()
    return image

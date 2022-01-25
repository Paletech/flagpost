from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models


def get_all_images(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.ImageOut]:
    return db.query(models.Images).offset(skip).limit(limit).all()

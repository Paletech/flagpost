from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models


def get_all_files(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.FileOut]:
    return db.query(models.Files).offset(skip).limit(limit).all()


def get_file(db: Session, file_id: int):
    file = db.query(models.Files).filter(models.Files.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


def create_file(db: Session, file: schemas.FileCreate):
    if file.post_id is not None:
        if not db.query(models.Files.id).filter(models.Posts.id == file.post_id).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_files = models.Files(
        width=file.width,
        height=file.height,
        path=file.path,
        public_path=file.public_path,
        # created_at=file.created_at,
        # updated_at=file.updated_at,
        post_id=file.post_id,
    )

    db.add(db_files)
    db.commit()
    db.refresh(db_files)
    return db_files


def delete_file(db: Session, file: int):
    file = get_file(db, file)
    if not file:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    db.delete(file)
    db.commit()
    return file

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from sqlalchemy.sql.expression import literal


def get_all_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Files).offset(skip).limit(limit).all()


def get_file(db: Session, file_id: UUID):
    file = db.query(models.Files).filter(models.Files.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


def create_file(db: Session, post_id, path):
    if post_id is not None:
        if not db.query(literal(True)).filter(models.Posts.id == post_id).first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_files = models.Files(
        path=path,
        post_id=post_id,
    )

    db.add(db_files)
    db.commit()
    db.refresh(db_files)
    return db_files


def delete_file(db: Session, file: UUID):
    file = get_file(db, file)
    if not file:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    db.delete(file)
    db.commit()
    return file

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import schemas

from app.db import models


def get_job(db: Session, jobs_id: int):
    job = db.query(models.Jobs).filter(models.Jobs.id == jobs_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.JobOut]:
    return db.query(models.Jobs).offset(skip).limit(limit).all()


def create_job(db: Session, user_id: int, job: schemas.JobCreate):
    db_jobs = models.Jobs(
        user_id=user_id,
        title=job.title,
        description=job.description,
        salary_from=job.salary_from,
        salary_to=job.salary_to,
        is_active=job.is_active,

    )
    db.add(db_jobs)
    db.commit()
    db.refresh(db_jobs)
    return db_jobs


def delete_job(db: Session, job: int):
    job = get_jobs(db, job)
    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(job)
    db.commit()
    return job

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

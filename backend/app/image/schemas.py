from pydantic import BaseModel
import typing as t


class JobBase(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True


class JobOut(JobBase):
    pass


class JobCreate(JobBase):
    class Config:
        orm_mode = True


class JobEdit(JobBase):
    id: int

    class Config:
        orm_mode = True


# class User(JobBase):
#     id: int
#
#     class Config:
#         orm_mode = True


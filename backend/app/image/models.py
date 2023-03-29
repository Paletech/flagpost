import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy_utils import ColorType

from app.db.session import Base

# class Images(Base):
#     __tablename__ = "image"
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     category_id = Column(Integer, ForeignKey("category.id"))
#     width = Column(Integer)
#     height = Column(Integer)
#     path = Column(String)
#     public_path = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy_utils import ColorType

from app.db.session import Base

# class Posts(Base):
#     __tablename__ = "post"
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     image_id = Column(Integer, ForeignKey("category.id"))
#     category_id = Column(Integer, ForeignKey("image.id"))
#     type = Column(String)
#     text = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

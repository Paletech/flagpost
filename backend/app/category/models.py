# import datetime
#
# from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy_utils import ColorType
# from app.db.session import Base


# class Categories(Base):
#     __tablename__ = "category"
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     image_id = Column(Integer)
#     category_id = Column(Integer)
#     selected = Column(Integer)
#     name = Column(String)
#     color = Column(ColorType)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#
#

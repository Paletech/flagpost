# import datetime
#
# from sqlalchemy import Column, String, ForeignKey, DateTime
# # from sqlalchemy_utils import ColorType
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
#
# from app.db.session import Base
#
#
# class Posts(Base):
#     __tablename__ = "post"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, unique=True)
#     type = Column(String)
#     text = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
#
#     files = relationship("Files")
#     categories = relationship("Categories", secondary=association_table, back_populates="post")
#

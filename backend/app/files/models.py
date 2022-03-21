# import datetime
# import uuid
#
# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.dialects.postgresql import UUID
#
# from app.db.session import Base
#
#
# def generate_uuid():
#     return str(uuid.uuid4())
#
#
# class Files(Base):
#     __tablename__ = "file"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, unique=True)
#     width = Column(Integer)
#     height = Column(Integer)
#     path = Column(String)
#     public_path = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#
#     post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"))

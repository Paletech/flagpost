import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ColorType
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import backref
from app.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    posts = relationship("Posts")
    categories = relationship("Categories")


association_table = Table('association', Base.metadata,
    Column('category_id', ForeignKey('category.id'), primary_key=True),
    Column('post_id', ForeignKey('post.id'), primary_key=True)
)


class Categories(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    category_id = Column(Integer)
    selected = Column(Integer)
    name = Column(String)
    # color = Column(ColorType)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    image_id = Column(Integer, ForeignKey("image.id"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    image = relationship("Images", backref=backref("category", uselist=False))
    post = relationship("Posts", secondary=association_table, back_populates="categories")


class Images(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    path = Column(String)
    public_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Posts(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    type = Column(String)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id"))

    files = relationship("Files")
    categories = relationship("Categories", secondary=association_table, back_populates="post")


class Files(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    width = Column(Integer)
    height = Column(Integer)
    path = Column(String)
    public_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"))

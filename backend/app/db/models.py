import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ColorType

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
    Column('category_id', ForeignKey('category.id')),
    Column('post_id', ForeignKey('post.id'))
)

class Categories(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    image_id = Column(Integer, ForeignKey("image.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    post = relationship("Posts", secondary=association_table)
    category_id = Column(Integer)
    selected = Column(Integer)
    name = Column(String)
    color = Column(ColorType)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Images(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    path = Column(String)
    public_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    categories = relationship("Categories")


class Posts(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    type = Column(String)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    files = relationship("Files")


class Files(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    width = Column(Integer)
    height = Column(Integer)
    path = Column(String)
    public_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

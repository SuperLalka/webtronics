
from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    username = Column(String(100), default="", unique=True)
    email = Column(String(100), default="")
    password = Column(String(100))

    user_posts = relationship("models.posts.PostOrm", back_populates="author")
    user_ratings = relationship("models.posts.PostRatingOrm", back_populates="user")

    __tablename__ = "users"


user = inspect(UserOrm).local_table

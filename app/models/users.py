
from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    String,
)
from sqlalchemy.orm import backref, relationship

from .base import Base


class UserOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    username = Column(String(100), default="", unique=True)
    email = Column(String(100), default="")
    password = Column(String(100))

    user_posts = relationship("models.posts.PostOrm", back_populates="author")
    user_ratings = relationship("models.posts.PostRatingOrm", backref=backref("user"))

    __tablename__ = "users"


user = inspect(UserOrm).local_table

import collections

from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

from models.users import UserOrm

Base = declarative_base()


class PostOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False, unique=True)
    title = Column(String(100))
    text = Column(Text)

    author_id = Column(Integer, ForeignKey(UserOrm.id), primary_key=True)
    author = relationship("models.users.UserOrm", back_populates="user_posts")

    post_ratings = relationship("models.posts.PostRatingOrm", back_populates="post")

    __tablename__ = "posts"

    @property
    def summary_rating(self):
        return sum(x.value for x in self.post_ratings)

    @property
    def likes_and_dislikes(self):
        values = [x.value for x in self.post_ratings]
        return collections.Counter(values)


class PostRatingOrm(Base):
    value = Column(SmallInteger)

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        primary_key=True,
        nullable=False,
        index=True
    )
    post = relationship(PostOrm, back_populates="post_ratings")

    user_id = Column(
        Integer,
        ForeignKey(UserOrm.id),
        primary_key=True,
        nullable=False,
        index=True
    )
    user = relationship("models.users.UserOrm", back_populates="user_ratings")

    __tablename__ = "posts_rating"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="user_posts_ratings_idx"),
    )

    @validates("value")
    def validate_value(self, key, value):
        if value not in [-1, 1]:
            raise ValueError("Valid values are 1 and -1")
        return value


post = inspect(PostOrm).local_table
post_rating = inspect(PostRatingOrm).local_table

import collections

from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship, validates, backref

from .base import Base


class PostRatingOrm(Base):
    value = Column(SmallInteger)

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        primary_key=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False
    )

    __tablename__ = "posts_rating"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="user_posts_ratings_idx"),
        Index(
            "user_posts_ratings_un",
            "post_id",
            "user_id"
        ),
    )

    @validates("value")
    def validate_value(self, key, value):
        if value not in [-1, 1]:
            raise ValueError("Valid values are 1 and -1")
        return value


class PostOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title = Column(String(100))
    text = Column(Text)

    author_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    author = relationship("models.users.UserOrm", back_populates="user_posts")

    post_ratings = relationship(PostRatingOrm, backref=backref("posts_rating"))

    __tablename__ = "posts"

    @property
    def summary_rating(self):
        return sum(x.value for x in self.post_ratings)

    @property
    def likes_and_dislikes(self):
        values = [x.value for x in self.post_ratings]
        return collections.Counter(values)


post = inspect(PostOrm).local_table
post_rating = inspect(PostRatingOrm).local_table


from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    String,
    Text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PostOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False)
    title = Column(String(100))
    text = Column(Text)

    __tablename__ = "posts"


post = inspect(PostOrm).local_table


from sqlalchemy import (
    inspect,
    BIGINT,
    Column,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserOrm(Base):
    id = Column(BIGINT, primary_key=True, nullable=False)
    username = Column(String(100), default="", unique=True)
    email = Column(String(100), default="")
    password = Column(String(100))

    __tablename__ = "users"


user = inspect(UserOrm).local_table

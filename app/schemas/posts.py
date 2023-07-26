from typing import Optional

from pydantic import BaseModel, validator


class PostSchema(BaseModel):
    title: str
    text: str


class CreatePostSchema(PostSchema):
    author_id: int


class RetrievePostSchema(PostSchema):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UpdatePostSchema(PostSchema):
    pass


class PostRatingSchema(BaseModel):
    value: Optional[int]

    @validator("value", pre=True)
    def validate_value(cls, value):
        if value is None:
            return

        if value not in [-1, 1]:
            raise ValueError("Valid values are 1 and -1")

        return value

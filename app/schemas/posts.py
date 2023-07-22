
from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    text: str


class CreatePostSchema(PostSchema):
    author_id: int


class RetrievePostSchema(PostSchema):
    id: int
    author_id: int


class UpdatePostSchema(PostSchema):
    pass

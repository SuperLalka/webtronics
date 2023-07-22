from typing import List

from fastapi import APIRouter, Body, Request

from app.crud.post import PostManager
from app.routes.utils import forbidden, not_found
from app.schemas.posts import CreatePostSchema, RetrievePostSchema, UpdatePostSchema

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[RetrievePostSchema])
async def get_posts(request: Request):
    return await PostManager(request.state.db_session).get_list()


@router.get("/{post_id}", response_model=RetrievePostSchema)
@router.get(
    "/{post_id}/",
    response_model=RetrievePostSchema,
    include_in_schema=False,
)
async def get_post_by_id(request: Request, post_id: int):
    post = await PostManager(request.state.db_session).get_by_id(post_id)
    if not post:
        return not_found(f"Couldn't find post with id {post_id}")

    return post


@router.post("/", response_model=CreatePostSchema)
async def create_post(
    request: Request,
    post_data: CreatePostSchema = Body(...)
):
    return await PostManager(request.state.db_session).create(post_data.dict())


@router.put("/{post_id}", response_model=UpdatePostSchema)
@router.put(
    "/{post_id}/",
    response_model=UpdatePostSchema,
    include_in_schema=False,
)
async def update_post(
    request: Request,
    post_id: int,
    post_data: UpdatePostSchema = Body(...),
):
    post = await PostManager(request.state.db_session).get_by_id(post_id)
    if not post:
        return not_found(f"Couldn't find post with id {post_id}")

    return await PostManager(request.state.db_session).update(
        post, post_data.dict(exclude_none=True)
    )


@router.delete("/{post_id}")
@router.delete("/{post_id}/", include_in_schema=False)
async def delete_post(request: Request, post_id: int):
    post = await PostManager(request.state.db_session).get_by_id(post_id)
    if not post:
        return not_found(f"Couldn't find post with id {post_id}")

    if request.user.id != post.author_id:
        return forbidden()

    return await PostManager(request.state.db_session).delete(post_id)

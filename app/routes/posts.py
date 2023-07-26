from typing import List

from fastapi import APIRouter, Body, Request
from starlette.responses import JSONResponse

from app.crud.post import PostManager, PostRatingManager
from app.routes.utils import forbidden, not_found
from app.schemas.posts import CreatePostSchema, PostRatingSchema, RetrievePostSchema, UpdatePostSchema

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


@router.post("/", response_model=RetrievePostSchema)
async def create_post(
    request: Request,
    post_data: CreatePostSchema = Body(...)
):
    return await PostManager(request.state.db_session).create(post_data.dict())


@router.put("/{post_id}", response_model=RetrievePostSchema)
@router.put(
    "/{post_id}/",
    response_model=RetrievePostSchema,
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

    await PostManager(request.state.db_session).delete(post_id)
    return JSONResponse(status_code=200, content={"success": True})


@router.post("/{post_id}/like")
@router.post("/{post_id}/like/", include_in_schema=False)
async def post_rating(
        request: Request,
        post_id: int,
        post_rating_data: PostRatingSchema = Body(...)
):
    post = await PostManager(request.state.db_session).get_by_id(post_id)
    if not post:
        return not_found(f"Couldn't find post with id {post_id}")

    if request.user.id == post.author_id:
        return forbidden()

    post_rating_data = post_rating_data.dict()
    post_rating_data["post_id"] = post_id
    post_rating_data["user_id"] = request.user.id

    if post_rating_data["value"] is None:
        await PostRatingManager(request.state.db_session).delete(post_rating_data)
        return JSONResponse(status_code=200, content={"success": True})

    await PostRatingManager(request.state.db_session).create_or_update(post_rating_data)
    return JSONResponse(status_code=200, content={"success": True})

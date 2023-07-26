from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.posts import (
    PostOrm,
    post as post_model,
    PostRatingOrm,
    post_rating as post_rating_model,
)


class PostManager:
    model = post_model

    def __init__(
        self,
        database: AsyncConnection,
    ):
        self.database = database

    @property
    def base_query(self):
        return select(PostOrm)

    async def get_list(self):
        state = await self.database.execute(self.base_query)
        result = state.mappings().unique()
        return (r["PostOrm"] for r in result)

    async def get_by_id(self, item_id: int) -> Optional[PostOrm]:
        query = self.base_query.where(self.model.c.id == item_id)
        state = await self.database.execute(query)
        result = state.mappings().unique().one_or_none()
        return result.get("PostOrm")

    async def create(self, data: dict):
        query = insert(self.model) \
            .returning(self.model) \
            .values(**data)
        state = await self.database.execute(query)
        result = state.mappings().one()
        return result

    async def update(self, item: PostOrm, data: dict):
        query = update(self.model) \
            .returning(self.model) \
            .where(self.model.c.id == item.id) \
            .values(data)
        state = await self.database.execute(query)
        result = state.mappings().one()
        return result

    async def delete(self, item_id: int):
        query = delete(self.model).where(self.model.c.id == item_id)
        return await self.database.execute(query)

    async def is_exists(self, item_id: int) -> bool:
        query = self.base_query.where(self.model.c.id == item_id)
        state = await self.database.execute(query)
        result = state.one_or_none()
        return bool(result)


class PostRatingManager:
    model = post_rating_model

    def __init__(
        self,
        database: AsyncConnection,
    ):
        self.database = database

    @property
    def base_query(self):
        return select(PostRatingOrm)

    async def create_or_update(self, data: dict):
        query = (
            pg_insert(PostRatingOrm)
            .values(**data)
            .on_conflict_do_update(
                constraint="user_posts_ratings_idx",
                set_={"value": data["value"]}
            )
        )

        await self.database.execute(query, data)

    async def delete(self, data: dict):
        query = delete(self.model).where(
            self.model.c.post_id == data["post_id"],
            self.model.c.user_id == data["user_id"],
        )
        return await self.database.execute(query)

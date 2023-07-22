from typing import Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.posts import (
    PostOrm,
    post as post_model,
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
        return select(self.model)

    async def get_list(self):
        state = await self.database.execute(self.base_query)
        result = state.unique()
        return (r["PostOrm"] for r in result)

    async def get_by_id(self, item_id: int) -> Optional[PostOrm]:
        query = self.base_query.where(self.model.c.id == item_id)
        state = await self.database.execute(query)
        result = state.unique().one_or_none()
        if result:
            return result["PostOrm"]
        return result

    async def create(self, data: dict):
        query = insert(PostOrm).values(**data)
        query = query.on_conflict_do_update(index_elements=["username"])
        return await self.database.execute(query)

    async def update(self, item: PostOrm, data: dict) -> PostOrm:
        query = update(self.model).where(self.model.c.id == item.id).values(data)
        await self.database.execute(query)
        await self.database.flush()
        return await self.get_by_id(item.id)

    async def delete(self, item_id: int):
        query = delete(self.model).where(self.model.c.id == item_id)
        return await self.database.execute(query)

from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.users import (
    UserOrm,
    user as user_model,
)


class UserManager:
    model = user_model

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
        return (r["UserOrm"] for r in result)

    async def get_by_id(self, item_id: int) -> Optional[UserOrm]:
        query = self.base_query.where(self.model.c.id == item_id)
        state = await self.database.execute(query)
        result = state.unique().one_or_none()
        if result:
            return result["UserOrm"]
        return result

    async def create(self, data: dict):
        query = insert(UserOrm).values(**data)
        query = query.on_conflict_do_nothing(index_elements=["username"])
        return await self.database.execute(query)

    async def is_exists(self, data: dict) -> bool:
        query = self.base_query.where(
            self.model.c.username == data["username"],
            self.model.c.password == data["password"],
        )
        state = await self.database.execute(query)
        result = state.one_or_none()
        return bool(result)


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware

from config import Config

engine = create_async_engine(Config.DATABASE_URL_ASYNC)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with async_session() as session:
            async with session.begin():
                request.state.db_session = session
                return await call_next(request)

from functools import wraps
from typing import Callable, Any, Coroutine

from sqlalchemy import text

from infrastructure.db.config import new_session


def with_readonly_session(func: Callable[..., Coroutine[Any, Any, Any]]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with new_session() as session:
            await session.execute(text("SET TRANSACTION READ ONLY;"))
            return await func(*args, session=session, **kwargs)

    return wrapper


def with_session(func: Callable[..., Coroutine[Any, Any, Any]]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with new_session() as session:
            async with session.begin():
                return await func(*args, session=session, **kwargs)

    return wrapper

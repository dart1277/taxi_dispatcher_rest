from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

from sqlalchemy import MetaData, BigInteger, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP

from infrastructure.config.settings import settings
from infrastructure.config.logs import log

logger = log.getChild(__name__)

engine = create_async_engine(
    settings.db_conn_string,
    echo=True,
    future=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def new_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(schema="public", naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata


async def init_db():
    logger.info(f"Initiating DB connection {settings.db_conn_string}")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    logger.info(f"Closing DB connection {settings.db_conn_string}")
    await engine.dispose()


# autoincrement=True is chosen for simplicity
bigint_primary_key = Annotated[int, mapped_column(BigInteger, primary_key=True, name="id", autoincrement=True)]


class CommonMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[bigint_primary_key]
    version_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)

    # https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.__init__
    __mapper_args__ = {
        "eager_defaults": True,
        "version_id_col": version_id,
        "version_id_generator": lambda version: version + 1 if version is not None else 0,
    }


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(),
                                                 onupdate=func.now())

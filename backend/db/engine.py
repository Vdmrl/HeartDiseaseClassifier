# import asyncio
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.db.config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

test_async_engine = create_async_engine(
    url=settings.TEST_DATABASE_URL_asyncpg,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)
test_async_session_factory = async_sessionmaker(test_async_engine)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

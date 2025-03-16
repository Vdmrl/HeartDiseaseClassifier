from collections.abc import AsyncGenerator

from sqlalchemy.orm import Mapped
from fastapi_users.db import SQLAlchemyBaseUserTable
from db.engine import Base

class User(Base, SQLAlchemyBaseUserTable[int]):
    age: Mapped[int]
    pass
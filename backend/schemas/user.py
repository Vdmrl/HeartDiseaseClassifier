from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    age: Optional[int] = None
    pass


class UserCreate(schemas.BaseUserCreate):
    age: Optional[int] = None
    pass


class UserUpdate(schemas.BaseUserUpdate):
    age: Optional[int] = None
    pass

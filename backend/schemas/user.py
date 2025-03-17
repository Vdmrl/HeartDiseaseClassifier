from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    age: int
    pass


class UserCreate(schemas.BaseUserCreate):
    age: int
    pass


class UserUpdate(schemas.BaseUserUpdate):
    age: int
    pass

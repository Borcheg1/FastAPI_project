from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[str]):
    id: models.ID
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


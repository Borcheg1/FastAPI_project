from typing import Optional

from fastapi import HTTPException
from fastapi_users import schemas, models
from pydantic import EmailStr, validator


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

    @validator("username")
    def validate_username(cls, v):
        v = v.strip()
        if not v:
            raise HTTPException(status_code=422, detail="Username can't be empty")
        elif not isinstance(v, str):
            raise HTTPException(status_code=422, detail="Username must be a string")
        elif not v.isalnum():
            raise HTTPException(status_code=422, detail="Username must be alphanumeric")
        elif len(v) > 50:
            raise HTTPException(status_code=422, detail="Username must be less than 50 characters")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise HTTPException(status_code=422, detail="Password should be at least 6 characters")
        return v

from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import VERIF_TOKEN, RESET_TOKEN
from src.tasks.tasks import send_verify_email, send_reset_pass_email


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = RESET_TOKEN
    verification_token_secret = VERIF_TOKEN

    async def on_after_login(self, user: User, request: Optional[Request] = None):
        return print(f"User {user.username} logged in")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.username} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_reset_pass_email.delay(user.username, user.email, token)
        print(f"User {user.username} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        send_verify_email.delay(user.username, user.email, token)
        print(f"Verification requested for user {user.username}. Verification token: {token}")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


import asyncio
import httpx
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.auth.models import User
from src.auth.models import Role
from src.auth.auth import get_current_active_user
from src.database import Base
from src.database import get_async_session
from src.config import TEST_DB_HOST, TEST_DB_PORT, TEST_DB_PASS, TEST_DB_USER, TEST_DB_NAME
from src.main import app


TEST_DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
test_async_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

user = User(
    username="user1",
    email="user@example.com",
    hashed_password="aaa",
    role_id=1,
    is_active=True,
    is_verified=True,
    is_superuser=False,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def clean_tables():
    async with test_engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def prepare_tables():
    async with test_engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    async with test_async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="admin", permissions="None")
        await session.execute(stmt)
        await session.commit()
    yield
    async with test_engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="https://test") as ac:
        yield ac

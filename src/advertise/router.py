from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.advertise.schemas import CreateAdvertise
from src.auth.auth import fastapi_users
from src.auth.models import User
from src.database import get_async_session
from src.advertise.models import Advertise

router = APIRouter(
    prefix="/advertise",
    tags=["Advertise"]
)

current_user = fastapi_users.current_user()


@router.get("/")
async def advertise(max_price: int,
                    limit: int = 2,
                    offset: int = 0,
                    session: AsyncSession = Depends(get_async_session)
                    ):
    query = select(Advertise).where(Advertise.price <= max_price).limit(limit).offset(offset)
    result = await session.execute(query)
    rows = [row[0] for row in result.all()]
    if rows:
        return {
            "status": "OK",
            "data": rows,
            "detail": None
        }
    else:
        return {
            "status": "OK",
            "data": "Nothing found",
            "detail": None
        }


@router.post("/")
async def advertise(
        new_advertise: CreateAdvertise,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    try:
        stmt = insert(Advertise).values(**new_advertise.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "OK",
            "data": None,
            "detail": f"added {new_advertise.name}"
        }

    except IntegrityError:
        return {
            "status": "error",
            "data": None,
            "detail": "This id already exists"
        }

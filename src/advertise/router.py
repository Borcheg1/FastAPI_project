from fastapi import APIRouter, Depends
from pydantic.types import Dict
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.adverise.schemas import CreateAdvertise
from src.database import get_async_session
from src.adverise.models import Advertise

router = APIRouter(
    prefix="/advertise",
    tags=["Advertise"]
)


@router.get("/")
async def get_advertise(max_price: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Advertise).where(Advertise.price <= max_price).limit(20)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_advertise(new_advertise: CreateAdvertise, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Advertise).values(**new_advertise.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except IntegrityError as e:
        return f"This id already exists."

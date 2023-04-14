from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.advertise.schemas import CreateAdvertise
from src.database import get_async_session
from src.advertise.models import Advertise

router = APIRouter(
    prefix="/advertise",
    tags=["Advertise"]
)


@router.get("/")
async def get_advertise(max_price: int,
                        limit: int = 2,
                        offset: int = 0,
                        session: AsyncSession = Depends(get_async_session)
                        ):
    query = select(Advertise).where(Advertise.price <= max_price).limit(limit).offset(offset)
    result = await session.execute(query)
    rows = [row[0] for row in result.all()]
    if rows:
        return rows
    else:
        return "Nothing found"


@router.post("/")
async def add_advertise(new_advertise: CreateAdvertise, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Advertise).values(**new_advertise.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except IntegrityError:
        return f"This id already exists."

from datetime import datetime

from sqlalchemy import Integer, String, Numeric, Text, TIMESTAMP

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Advertise(Base):
    __tablename__ = "advertise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=320), nullable=False)
    address: Mapped[str] = mapped_column(String(length=500), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(length=320))

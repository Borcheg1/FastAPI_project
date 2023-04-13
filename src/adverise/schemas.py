from datetime import datetime

from pydantic import BaseModel


class CreateAdvertise(BaseModel):
    id: int
    name: str
    address: str
    price: float
    created_at: datetime
    description: str
    image_url: str
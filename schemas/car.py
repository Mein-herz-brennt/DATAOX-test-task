from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional


class CarBase(BaseModel):
    url: HttpUrl
    title: Optional[str] = None

    price_usd: Optional[int] = None
    odometer: Optional[int] = None

    username: Optional[str] = None
    phone_number: Optional[int] = None

    image_url: Optional[HttpUrl] = None
    images_count: Optional[int] = None

    car_number: Optional[str] = None
    car_vin: Optional[str] = None


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id: int
    datetime_found: datetime

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic

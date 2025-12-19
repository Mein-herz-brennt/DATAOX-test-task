from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional


class CarLinkBase(BaseModel):
    url: HttpUrl


class CarLinkCreate(CarLinkBase):
    pass


class CarLinkRead(CarLinkBase):
    id: int
    is_parsed: bool
    is_failed: bool
    error_message: Optional[str]
    created_at: datetime
    parsed_at: Optional[datetime]

    class Config:
        from_attributes = True

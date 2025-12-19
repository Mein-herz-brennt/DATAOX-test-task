import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String(512), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=True)

    price_usd = Column(Integer, nullable=True)
    odometer = Column(Integer, nullable=True)

    username = Column(String(255), nullable=True)
    phone_number = Column(BigInteger, nullable=True)

    image_url = Column(String(512), nullable=True)
    images_count = Column(Integer, nullable=True)

    car_number = Column(String(32), nullable=True)
    car_vin = Column(String(32), nullable=True, index=True)

    datetime_found = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CarLink(Base):
    __tablename__ = "car_links"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String(512), unique=True, nullable=False, index=True)

    is_parsed = Column(Boolean, default=False, nullable=False)
    is_failed = Column(Boolean, default=False, nullable=False)

    error_message = Column(String(255), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    parsed_at = Column(DateTime, nullable=True)

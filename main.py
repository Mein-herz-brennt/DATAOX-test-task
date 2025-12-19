from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.car import Base, Car
from schemas.car import CarRead
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Parser API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    from tasks import scheduler  # noqa


@app.get("/cars", response_model=List[CarRead])
def get_all_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()


@app.get("/cars/{car_id}", response_model=CarRead)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

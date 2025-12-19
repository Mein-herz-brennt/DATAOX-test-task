import datetime
from database import SessionLocal
from parsers.urls_parser import LinksParser
from parsers.page_parser import CarPageParser
from models.car import Car
from models.car_link import CarLink
from services.links_service import save_new_links


async def daily_job():
    db = SessionLocal()

    links_parser = LinksParser()
    all_links = await links_parser.parse_all_car_links()

    added = save_new_links(db, all_links)
    print(f"Added {added} new links")

    links = db.query(CarLink) \
        .filter(CarLink.is_parsed == False, CarLink.is_failed == False) \
        .limit(30) \
        .all()

    for link in links:
        try:
            parser = CarPageParser(link.url)
            car_data = await parser.parse_all()

            car = Car(**car_data)
            db.add(car)

            link.is_parsed = True
            link.parsed_at = datetime.datetime.utcnow()
            db.commit()

        except Exception as e:
            link.is_failed = True
            link.error_message = str(e)
            db.commit()

    db.close()

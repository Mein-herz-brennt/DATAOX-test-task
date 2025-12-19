from sqlalchemy.orm import Session
from models.car_link import CarLink


def save_new_links(db: Session, links: list[str]) -> int:
    existing = {
        url for (url,) in
        db.query(CarLink.url)
        .filter(CarLink.url.in_(links))
        .all()
    }

    new_links = [
        CarLink(url=link)
        for link in links
        if link not in existing
    ]

    if new_links:
        db.bulk_save_objects(new_links)
        db.commit()

    return len(new_links)

from sqlalchemy.orm import Session

from .models import URL
from .utils import encode_base62


def create_url(db: Session, original_url: str) -> URL:
    """
    Create a URL row and assign a short_code based on its auto-increment ID.
    """
    row = URL(original_url=original_url, click_count=0)
    db.add(row)
    db.flush()
    db.refresh(row)  # ensures row.id is available

    # Generate short_code from the DB-generated id
    row.short_code = encode_base62(row.id)
    
    db.commit()
    db.refresh(row)

    return row


def get_url_by_code(db: Session, short_code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == short_code).first()


def increment_click_count(db: Session, row: URL) -> None:
    db.execute(
        update(URL)
        .where(URL.id == row.id)
        .values(click_count=URL.click_count + 1)
    )
    db.commit()
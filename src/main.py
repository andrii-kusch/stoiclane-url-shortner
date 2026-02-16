from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from .schemas import ShortenRequest, ShortenResponse
from .crud import create_url, get_url_by_code, increment_click_count
from .utils import is_valid_url

app = FastAPI(title="URL Shortener")

# Create tables at startup
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten(payload: ShortenRequest, request: Request, db: Session = Depends(get_db)):
    if not is_valid_url(payload.url):
        raise HTTPException(status_code=400, detail="Invalid URL. Must start with http:// or https://")

    row = create_url(db, payload.url)

    base_url = str(request.base_url).rstrip("/")  # e.g. http://localhost:8000
    short_url = f"{base_url}/{row.short_code}"

    return ShortenResponse(
        short_code=row.short_code,
        short_url=short_url,
        original_url=row.original_url,
    )


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    row = get_url_by_code(db, short_code)
    if not row:
        raise HTTPException(status_code=404, detail="Short code not found")

    increment_click_count(db, row)
    return RedirectResponse(url=row.original_url, status_code=302)
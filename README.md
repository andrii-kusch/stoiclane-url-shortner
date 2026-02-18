A minimal URL shortener service built with FastAPI + SQLite.  
It supports creating short links and redirecting to original URLs, with a click counter.

## Features
- `POST /shorten` creates a short code for a URL
- `GET /{short_code}` redirects (302) to the original URL and increments `click_count`
- SQLite persistence
- Dockerized for reproducible setup
- Unit + integration tests (pytest)

## Tech Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- pytest

## Run (Docker)
```bash
docker compose up --build
```

## References
- https://dev.to/jbrocher/fastapi-testing-a-database-5ao5
- https://www.augustinfotech.com/blogs/fastapi-unit-testing-with-dependency-overrides-a-complete-guide/
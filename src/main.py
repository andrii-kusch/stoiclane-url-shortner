from fastapi import FastAPI

app = FastAPI(title="URL Shortener")

# Create tables at startup
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
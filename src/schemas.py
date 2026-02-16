from pydantic import BaseModel, Field


class ShortenRequest(BaseModel):
    url: str = Field(..., min_length=1)


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str


class ErrorResponse(BaseModel):
    error: str
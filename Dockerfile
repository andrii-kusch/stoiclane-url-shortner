FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app

COPY src src
COPY test test

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
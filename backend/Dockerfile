FROM python:3.13.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

COPY ./migrations /app/migrations
COPY ./alembic.ini /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
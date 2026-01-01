FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY deploy/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY deploy/app/ ./app/
COPY deploy/static/ ./static/
COPY deploy/flag.txt /flag.txt

RUN chmod 400 /flag.txt && \
    chown root:root /flag.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

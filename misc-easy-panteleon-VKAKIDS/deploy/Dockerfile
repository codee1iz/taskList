
FROM python:3.9-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p videos


EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1


CMD ["gunicorn", "main:app", "-w", "4", "-b", "0.0.0.0:5000"]


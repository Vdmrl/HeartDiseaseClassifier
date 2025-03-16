FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The command below is overridden by docker-compose if needed.
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
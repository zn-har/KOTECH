FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

workdir /app
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

copy . /app/

RUN pip install -r requirements.txt

expose 8000


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]



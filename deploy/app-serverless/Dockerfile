FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.3.1 && poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .


RUN poetry install

COPY .. .





RUN python src/manage.py collectstatic --noinput

ENV PORT 8000

CMD uwsgi --ini deploy/app-serverless/uwsgi.ini --http-socket :$PORT --static-map /static=/app/static

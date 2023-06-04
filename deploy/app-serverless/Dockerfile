FROM node:16.15-alpine AS node

WORKDIR /app/src/frontend

COPY src/frontend/package.json .
COPY src/frontend/package-lock.json .
RUN npm ci

COPY src/frontend .
RUN npm run build

FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.3.0 && poetry config virtualenvs.create false

WORKDIR /app



COPY pyproject.toml .
COPY poetry.lock .
COPY .pre-commit-config.yaml .
RUN poetry install

COPY . .

COPY --from=node /app/src/frontend/dist /app/src/frontend/dist


RUN python src/manage.py collectstatic --noinput

ENV PORT 8000

CMD uwsgi --ini deploy/app-serverless/uwsgi.ini --http-socket :$PORT --static-map /static=/app/src/frontend/assets
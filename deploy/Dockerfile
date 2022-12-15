FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN pip install  poetry==1.3.1 && poetry config virtualenvs.create false --local

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .

EXPOSE 8000

CMD python src/manage.py migrate &&  python src/manage.py runserver 0.0.0.0:8000

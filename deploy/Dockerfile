FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.3.1 && poetry config virtualenvs.create false

WORKDIR sites-stat




COPY pyproject.toml .
COPY poetry.lock .


RUN poetry install



COPY . .

RUN python src/manage.py collectstatic --noinput

ENV PORT 8000

#CMD python src/manage.py migrate &&
CMD uwsgi --ini deploy/uwsgi.ini --http-socket :$PORT --static-map /static=/app/static

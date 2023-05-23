from django.conf import settings
from celery import shared_task
from app.clickhouse import create_connection


@shared_task
def groupdb():
    db = create_connection()
    db.raw("OPTIMIZE TABLE viewinday final;")
    db.raw("OPTIMIZE TABLE visitinday final;")
    db.raw("OPTIMIZE TABLE visitorinday final;")

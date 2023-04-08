from django.conf import settings
from celery import shared_task
from app.clickhouse import create_connection


@shared_task
def groupdb():
    db = create_connection()
    print(db.raw("select * from viewinday limit 1"))
    db.raw("OPTIMIZE TABLE viewinday final;")
    db.raw("OPTIMIZE table visitinday final;")
    db.raw("OPTIMIZE table visitorinday final;")

from django.conf import settings
from celery import shared_task
from app.clickhouse import create_connection
# TODO нет разрывов в импорте

@shared_task
def groupdb():
    db = create_connection()
    # TODO сделать сервис, вынести это туда. И сделать консольную команду, которая делат то же самое (может быть 
    # ситуация, когда потребуется это сделать в определнный момент)
    db.raw("OPTIMIZE TABLE viewinday final;")
    db.raw("OPTIMIZE table visitinday final;") # TODO сделать TABLE в верхнем регистре во всех случаях
    db.raw("OPTIMIZE table visitorinday final;")

from django.conf import settings
from celery import shared_task




@shared_task
def groupdb():
    print('произошла группировка')
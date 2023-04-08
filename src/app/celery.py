from django.conf import settings

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "groupdb": {
        "task": "web.tasks.groupdb",
        "schedule": 60.0,  # crontab(minute=0, hour=0)
    }
}

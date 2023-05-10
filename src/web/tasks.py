from celery import shared_task

from web.services import group_clickhouse_tables


@shared_task
def group_db():
    group_clickhouse_tables()

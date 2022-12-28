from django.conf import settings
from infi.clickhouse_orm import Database


def create_connection():
    return Database(**settings.CLICKHOUSE_DATABASE)

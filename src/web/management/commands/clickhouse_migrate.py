from django.core.management.base import BaseCommand

from app.clickhouse import create_connection
from web.clickhouse_models import Views


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        db.create_table(Views)
        print("tables created")

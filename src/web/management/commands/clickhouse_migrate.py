from django.core.management.base import BaseCommand

from app.clickhouse import create_connection
from web.clickhouse_models import Views, VisitsInDay


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        db.create_table(Views)
        db.create_table(VisitsInDay)
        print("tables created")

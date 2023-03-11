from django.core.management.base import BaseCommand

from app.clickhouse import create_connection
from web.clickhouse_models import Views, VisitorInDay, ViewInDay


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        db.create_table(Views)
        db.create_table(VisitorInDay)
        db.create_table(ViewInDay)
        db.create_table(VisitInDay)
        print("tables created")

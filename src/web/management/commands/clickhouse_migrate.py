from django.core.management.base import BaseCommand

from app.clickhouse import create_connection
from web.clickhouse_models import Views, VisitorInDay, ViewInDay, VisitInDay, UniqueVisits, UniqueVisitors


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        db.create_table(Views)
        db.create_table(UniqueVisits)
        db.create_table(UniqueVisitors)
        db.create_table(ViewInDay)
        db.create_table(VisitInDay)
        db.create_table(VisitorInDay)
        print("tables created")

from django.core.management.base import BaseCommand

from web.services import group_clickhouse_tables


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_clickhouse_tables()
        print("The command is completed")

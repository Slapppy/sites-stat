from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError


from app.clickhouse import create_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        try:
            db.raw(
                "CREATE MATERIALIZED VIEW visits_in_day_mv TO visitsinday AS SELECT counter_id, "
                "count(visitor_unique_key) as count_visit, toDate(created_at) as created_at FROM views "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO visitsinday SELECT counter_id, count(visitor_unique_key) as count_visit, "
                "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            )
        except ServerError:
            pass
        print("command completed successfully")

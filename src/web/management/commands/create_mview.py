from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError


from app.clickhouse import create_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        try:

            db.raw(
                "CREATE MATERIALIZED VIEW visitor_in_day_mv TO visitorinday AS SELECT counter_id, "
                "count(visitor_unique_key) as count_visitor, toDate(created_at) as created_at FROM views "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO visitorinday SELECT counter_id, count(visitor_unique_key) as count_visitor, "
                "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            )
            db.raw(
                "CREATE MATERIALIZED VIEW view_in_day_mv TO viewinday AS SELECT counter_id, "
                "count(view_id) as count_visits, toDate(created_at) as created_at FROM views "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO viewinday SELECT counter_id, count(view_id) as count_visits, "
                "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            )
            print("Command completed successfully")

        except ServerError:
            print("View creation error")

from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError


from app.clickhouse import create_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        try:

            def views():
                db.raw(
                    "CREATE MATERIALIZED VIEW view_in_day_mv TO viewinday AS SELECT counter_id, "
                    "count(view_id) as count_views, toDate(created_at) as created_at FROM views "
                    "GROUP BY counter_id, created_at;"
                )
                db.raw(
                    "INSERT INTO viewinday SELECT counter_id, count(view_id) as count_views, "
                    "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
                )

            def visits():
                db.raw(
                    "CREATE MATERIALIZED VIEW visit_in_day_mv TO visitinday AS SELECT counter_id, "
                    "count(DISTINCT visit_id) as count_visits, toDate(created_at) as created_at FROM views "
                    "GROUP BY counter_id, created_at;"
                )
                db.raw(
                    "INSERT INTO visitinday SELECT counter_id, count(DISTINCT visit_id) as count_visit, "
                    "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
                )

            def visitors():
                db.raw(
                    "CREATE MATERIALIZED VIEW visitor_in_day_mv TO visitorinday AS SELECT counter_id, "
                    "count(DISTINCT visitor_unique_key) as count_visitors, toDate(created_at) as created_at FROM views "
                    "GROUP BY counter_id, created_at;"
                )
                db.raw(
                    "INSERT INTO visitorinday SELECT counter_id, count(DISTINCT visitor_unique_key) as count_visitor, "
                    "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
                )


            views()
            visits()
            visitors()
            print("Command completed successfully")
        except ServerError:
            print("View creation error")

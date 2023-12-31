from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError


from app.clickhouse import create_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        try:

            db.raw(
                "CREATE MATERIALIZED VIEW view_in_day_mv TO viewinday AS SELECT counter_id, "
                "count(view_id) as count_views, toDate(created_at) as created_at FROM views "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO viewinday SELECT counter_id, count(view_id) as count_views, "
                "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            )

            db.raw(
                "CREATE MATERIALIZED VIEW uniquevisits_mv TO uniquevisits AS "
                "SELECT v.counter_id, v.new_visit as visit_id, date FROM "
                "(select counter_id, visit_id as new_visit, toDate(created_at) as date from views) v "
                "LEFT JOIN (select counter_id, visit_id as old_visit, date from uniquevisits) uv "
                "on v.counter_id = uv.counter_id and v.new_visit = uv.old_visit and v.date = uv.date "
                "where date = today() and old_visit = '00000000-0000-0000-0000-000000000000';"
            )
            db.raw(
                "INSERT INTO uniquevisits SELECT DISTINCT counter_id, visit_id, "
                "toDate(created_at) as date FROM views;"
            )
            db.raw(
                "CREATE MATERIALIZED VIEW visit_in_day_mv TO visitinday AS SELECT counter_id, "
                "count(visit_id) as count_visits, date as created_at FROM uniquevisits "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO visitinday SELECT counter_id, count(visit_id) as count_visits, "
                "date as created_at FROM uniquevisits GROUP BY counter_id, created_at;"
            )

            db.raw(
                "CREATE MATERIALIZED VIEW uniquevisitors_mv TO uniquevisitors AS "
                "SELECT counter_id, new_visitor as visitor_unique_key, date FROM "
                "(select counter_id, visitor_unique_key as new_visitor, toDate(created_at) as date from views) v "
                "LEFT JOIN (select counter_id, visitor_unique_key as old_visitor, date from uniquevisitors) uv "
                "on v.counter_id = uv.counter_id and v.new_visitor = uv.old_visitor and v.date = uv.date "
                "where date = today() and old_visitor = '00000000-0000-0000-0000-000000000000';"
            )
            db.raw(
                "INSERT INTO uniquevisitors SELECT DISTINCT counter_id, visitor_unique_key, "
                "toDate(created_at) as date FROM views;"
            )
            db.raw(
                "CREATE MATERIALIZED VIEW visitor_in_day_mv TO visitorinday AS SELECT counter_id, "
                "count(visitor_unique_key) as count_visitors, date as created_at FROM uniquevisitors "
                "GROUP BY counter_id, created_at;"
            )
            db.raw(
                "INSERT INTO visitorinday SELECT counter_id, count(visitor_unique_key) as count_visitors, "
                "date as created_at FROM uniquevisitors GROUP BY counter_id, created_at;"
            )

            print("Command completed successfully")

        except ServerError as e:
            print(e)
            print("View creation error")

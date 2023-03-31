from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError
import random


from app.clickhouse import create_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = create_connection()
        try:

            def views():
                db.raw(
                    "CREATE MATERIALIZED VIEW view_in_day_mv TO viewinday AS "
                    "select end_data.counter_id, end_data.count_views, end_data.date, "
                    "toDateTime(now()) as created_time, end_data.sign "
                    "from (SELECT  s.counter_id, (s.new_views + s.old_views) as count_views, s.date, "
                    "coalesce(s.sign, 1) as sign FROM "
                    "(select v.counter_id, v.new_views, v.date, view_t.old_views, view_t.sign from "
                    "(select counter_id, count(view_id) as new_views, toDate(views.created_at) as date "
                    "from views GROUP BY counter_id, date) v "
                    "LEFT JOIN (select t.counter_id, t.old_views, t.date, sgn.sign as sign from "
                    "(select counter_id, count_views as old_views, date, "
                    "row_number() over(partition by counter_id, date order by created_time desc, sign desc) "
                    "as rn from viewinday where date=today()) t cross join "
                    "(select case when number = 0 then -1 when number = 1 then 1 end as sign from numbers(2)) sgn"
                    " where rn = 1) view_t "
                    "on view_t.counter_id = v.counter_id and view_t.date = v.date) s) end_data"
                )
                db.raw(
                    "INSERT INTO viewinday SELECT counter_id, count(view_id) as count_views, "
                    "toDate(created_at) as date, now() as created_time, 1 as sign FROM views "
                    "GROUP BY counter_id, date;"
                )

            def visits():
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
                    "CREATE MATERIALIZED VIEW visit_in_day_mv TO visitinday AS "
                    "select end_data.counter_id, end_data.count_visits, end_data.date, "
                    "toDateTime(now()) as created_time, end_data.sign "
                    "from (SELECT  s.counter_id, (s.new_visits + s.old_visits) as count_visits, s.date, "
                    "coalesce(s.sign, 1) as sign FROM "
                    "(select v.counter_id, v.new_visits, v.date, view_t.old_visits, view_t.sign from "
                    "(select counter_id, count(visit_id) as new_visits, date "
                    "from uniquevisits GROUP BY counter_id, date) v "
                    "LEFT JOIN (select t.counter_id, t.old_visits, t.date, sgn.sign as sign from "
                    "(select counter_id, count_visits as old_visits, date, "
                    "row_number() over(partition by counter_id, date order by created_time desc, sign desc) "
                    "as rn from visitinday where date = today()) t cross join "
                    "(select case when number = 0 then -1 when number = 1 then 1 end as sign from numbers(2)) sgn"
                    " where rn = 1) "
                    "view_t on view_t.counter_id = v.counter_id and view_t.date = v.date) s) end_data"
                )
                db.raw(
                    "INSERT INTO visitinday SELECT counter_id, count(visit_id) as count_visits, "
                    "date, now() as created_time, 1 as sign FROM uniquevisits "
                    "GROUP BY counter_id, date;"
                )

            def visitors():
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
                    "CREATE MATERIALIZED VIEW visitor_in_day_mv TO visitorinday AS "
                    "select end_data.counter_id, end_data.count_visitors, end_data.date, "
                    "toDateTime(now()) as created_time, end_data.sign "
                    "from (SELECT  s.counter_id, (s.new_visitors + s.old_visitors) as count_visitors, s.date, "
                    "coalesce(s.sign, 1) as sign FROM "
                    "(select v.counter_id, v.new_visitors, v.date, view_t.old_visitors, view_t.sign from "
                    "(select counter_id, count(visitor_unique_key) as new_visitors, date "
                    "from uniquevisitors GROUP BY counter_id, date) v "
                    "LEFT JOIN (select t.counter_id, t.old_visitors, t.date, sgn.sign as sign from "
                    "(select counter_id, count_visitors as old_visitors, date, "
                    "row_number() over(partition by counter_id, date order by created_time desc, sign desc) "
                    "as rn from visitorinday where date = today()) t cross join "
                    "(select case when number = 0 then -1 when number = 1 then 1 end as sign from numbers(2)) sgn"
                    " where rn = 1) "
                    "view_t on view_t.counter_id = v.counter_id and view_t.date = v.date) s) end_data"
                )
                db.raw(
                    "INSERT INTO visitorinday SELECT counter_id, count(visitor_unique_key) as count_visitors, "
                    "date, now() as created_time, 1 as sign FROM uniquevisitors "
                    "GROUP BY counter_id, date;"
                )

            views()
            visits()
            visitors()
            print("Command completed successfully")
        except ServerError as e:
            print(e)
            print("View creation error")

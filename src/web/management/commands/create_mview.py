from django.core.management.base import BaseCommand
from infi.clickhouse_orm import ServerError


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
                    "row_number() over(partition by date order by created_time desc) as rn from viewinday) t "
                    "cross join "
                    "(select case when number = 0 then -1 when number = 1 then 1 end as sign from numbers(2)) sgn"
                    " where rn = 1) "
                    "view_t on view_t.counter_id = v.counter_id and view_t.date = v.date) s) end_data"
                )
                db.raw(
                    "INSERT INTO viewinday SELECT counter_id, count(view_id) as count_views, "
                    "toDate(created_at) as date, (now() + rand()) as created_time, 1 as sign FROM views "
                    "GROUP BY counter_id, date;"
                )

            # def visits():
            #     db.raw(
            #         "CREATE MATERIALIZED VIEW visit_in_day_mv TO visitinday AS SELECT counter_id, "
            #         "count(DISTINCT visit_id) as count_visits, toDate(created_at) as created_at FROM views "
            #         "GROUP BY counter_id, created_at;"
            #     )
            #     db.raw(
            #         "INSERT INTO visitinday SELECT counter_id, count(DISTINCT visit_id) as count_visit, "
            #         "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            #     )
            #
            # def visitors():
            #     db.raw(
            #         "CREATE MATERIALIZED VIEW visitor_in_day_mv TO visitorinday AS SELECT counter_id, "
            #         "count(DISTINCT visitor_unique_key) as count_visitors, toDate(created_at) as created_at FROM views "
            #         "GROUP BY counter_id, created_at;"
            #     )
            #     db.raw(
            #         "INSERT INTO visitorinday SELECT counter_id, count(DISTINCT visitor_unique_key) as count_visitor, "
            #         "toDate(created_at) as created_at FROM views GROUP BY counter_id, created_at;"
            #     )
            #
            #
            views()
            # visits()
            # visitors()
            print("Command completed successfully")
        except ServerError as e:
            print(e)
            print("View creation error")

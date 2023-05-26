from .clickhouse_models import ViewInDay, VisitInDay, VisitorInDay
from app.clickhouse import create_connection
from .models import Counter


def get_user_list_of_counters(user):
    if not user.is_authenticated:
        return Counter.objects.none()
    return Counter.objects.filter(user=user).order_by("-created_at")


def add_parameters_into_counters(counters):
    """Добавляет количество просмотров, визитов и посетителей к каждому счетчику"""
    counters_id = [counter["id"] for counter in counters.values("id")]

    if not counters_id:
        return

    db = create_connection()
    views = ViewInDay.objects_in(db).filter(ViewInDay.counter_id.isIn(counters_id))
    visits = VisitInDay.objects_in(db).filter(VisitInDay.counter_id.isIn(counters_id))
    visitors = VisitorInDay.objects_in(db).filter(VisitorInDay.counter_id.isIn(counters_id))
    counters_with_params = [
        {"id": counter_id, "count_views": 0, "count_visits": 0, "count_visitors": 0} for counter_id in counters_id
    ]
    if len(counters_with_params) > 0:
        for raw in views:
            counter_with_params = list(filter(lambda x: x["id"] == raw.counter_id, counters_with_params))
            counter_with_params[0]["count_views"] += raw.count_views

        for raw in visits:
            counter_with_params = list(filter(lambda x: x["id"] == raw.counter_id, counters_with_params))
            counter_with_params[0]["count_visits"] += raw.count_visits

        for raw in visitors:
            counter_with_params = list(filter(lambda x: x["id"] == raw.counter_id, counters_with_params))
            counter_with_params[0]["count_visitors"] += raw.count_visitors

        for counter in counters:
            counter_with_params = list(filter(lambda x: x["id"] == counter.id, counters_with_params))[0]
            counter.count_views = counter_with_params["count_views"]
            counter.count_visits = counter_with_params["count_visits"]
            counter.count_visitors = counter_with_params["count_visitors"]


def group_clickhouse_tables():
    db = create_connection()
    db.raw("OPTIMIZE TABLE viewinday FINAL;")
    db.raw("OPTIMIZE TABLE visitinday FINAL;")
    db.raw("OPTIMIZE TABLE visitorinday FINAL;")

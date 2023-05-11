from datetime import datetime

from django.shortcuts import get_object_or_404

from .clickhouse_models import ViewInDay, VisitInDay, VisitorInDay
from api.servises import get_sum_data_for_certain_period
from .models import Counter


def get_user_list_of_counters(user):
    if not user.is_authenticated:
        return Counter.objects.none()
    return Counter.objects.filter(user=user).order_by("-created_at")


def add_parameters_into_counters(counters):
    """Добавляет количество просмотров, визитов и посетителей к каждому счетчику"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    for counter in counters:
        start_date = counter.created_at.strftime("%Y-%m-%d")
        counter.count_views = get_sum_data_for_certain_period(
            ViewInDay, "count_views", counter.id, start_date, end_date
        )
        counter.count_visits = get_sum_data_for_certain_period(
            VisitInDay, "count_visits", counter.id, start_date, end_date
        )
        counter.count_visitors = get_sum_data_for_certain_period(
            VisitorInDay, "count_visitors", counter.id, start_date, end_date
        )


def filter_counters_with_search(counters, search):
    return counters.filter(name__icontains=search)


def get_user_counter(pk, user):
    return get_object_or_404(Counter, pk=pk, user=user)
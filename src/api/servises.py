from django.utils import timezone
from datetime import date, datetime, timedelta
import uuid

from app.clickhouse import create_connection
from web.models import Counter
from web.clickhouse_models import Views


def get_sum_data_for_certain_period(model, field_name, counter_id, start_date, end_date):
    """Возвращает итогогое количество просмотров, визитов или посетителей за определенный срок"""
    db = create_connection()
    queryset = (
        model.objects_in(db)
        .filter(created_at__between=(start_date, end_date), counter_id=counter_id)
        .aggregate("counter_id", sum_stat=f"sum({field_name})")
    )
    if queryset:
        queryset = queryset[0].sum_stat
        return queryset
    return 0


def does_user_has_counters(user_id, counter_id):
    """Проверяет, есть ли у пользователя счетчики"""
    return Counter.objects.filter(user_id=user_id, id=counter_id).count() != 0


def get_validated_period(start_date, end_date, counter_id):
    """Возвращает корректные start_date и end_data"""
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_date = Counter.objects.get(id=counter_id).created_at.strftime("%Y-%m-%d")

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        end_date = datetime.now().strftime("%Y-%m-%d")
    return start_date, end_date


def create_view_into_table(
    counter_id, referer, visit_id, visitor_unique_key, device_type, browser, metadata, os_type, ip_address, language
):
    """Создает новую запись в таблице Views"""
    db = create_connection()
    notes = [
        Views(
            counter_id=counter_id,
            referer=referer,
            view_id=uuid.uuid4(),
            visit_id=visit_id,
            visitor_unique_key=visitor_unique_key,
            device_type=device_type,
            browser_type=browser,
            user_agent=metadata,
            os_type=os_type,
            ip=ip_address,
            language=language,
            created_at=timezone.now(),
        )
    ]

    db.insert(notes)


def get_data_group_by_days(model, field_name, counter_id, start_date, end_date):
    """Возвращает количество просмотров, визитов или посетителей
    за каждый день из периода start_date - end_date"""
    dataset = _get_list_of_data_for_certain_period(model, counter_id, start_date, end_date)
    data = []
    temp_date = start_date
    while temp_date <= end_date:
        data_per_day = list(filter(lambda x: x.created_at == temp_date, dataset))
        data.append(
            {
                "date": temp_date,
                field_name: sum((getattr(d, field_name) for d in data_per_day)) if len(data_per_day) > 0 else 0,
            }
        )
        temp_date += timedelta(days=1)
    return data


def _get_list_of_data_for_certain_period(model, counter_id, start_date, end_date):
    """Возвращает список данных за период start_date - end_date"""
    db = create_connection()
    queryset = model.objects_in(db).filter(created_at__between=(start_date, end_date), counter_id=counter_id)
    return list(queryset)


def get_validated_period_with_filter(date_filter):
    """Возвращает start_date и end_date, формируя его по фильтру"""
    end_date = date.today()
    days = {"threedays": 2, "week": 6, "month": 30, "quarter": 90, "year": 365}
    start_date = end_date - timedelta(days=days[date_filter])
    return start_date, end_date


def check_counter_exists(counter_id):
    """Проверяет, существует ли счетчик с таким id"""
    return len(Counter.objects.filter(id=counter_id)) > 0

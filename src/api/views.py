from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid

from api.permissions import IsCreatorAndReadOnly
from web.clickhouse_models import VisitorInDay, VisitInDay, ViewInDay
from api.servises import (
    does_user_has_counters,
    get_sum_data_for_certain_period,
    get_validated_period,
    create_view_into_table,
    get_validated_period_with_filter,
    get_data_group_by_days,
    check_counter_exists,
)


class StatCounter(APIView):
    model = None
    field_name = None

    def get(self, request):
        counter_id = request.GET.get("id", None)
        start_date, end_date = request.GET.get("start-date", None), request.GET.get("end-date", None)

        if counter_id:
            # Проверка пользователя
            if does_user_has_counters(request.user.id, counter_id) or request.user.is_superuser:
                start_date, end_date = get_validated_period(start_date, end_date, counter_id)
                data = get_sum_data_for_certain_period(self.model, self.field_name, counter_id, start_date, end_date)

                return Response(
                    {
                        "counter_id": int(counter_id),
                        "start-date": start_date,
                        "end-date": end_date,
                        self.field_name: data,
                    }
                )

            return Response(
                {"error": [{"code": 403, "reason": "AccessError"}]},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {"error": [{"code": 400, "reason": "invalidParameter"}]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StatCounterView(StatCounter):
    # пример запроса: http://127.0.0.1:8000/api/view_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31

    model = ViewInDay
    field_name = "count_views"


class StatCounterVisit(StatCounter):
    # http://127.0.0.1:8000/api/visit_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31

    model = VisitInDay
    field_name = "count_visits"


class StatCounterVisitor(StatCounter):
    # http://127.0.0.1:8000/api/visitor_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31

    model = VisitorInDay
    field_name = "count_visitors"


TRANSPARENT_1_PIXEL_GIF = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"


class GetMetaDataView(APIView):
    # пример <img src="http://127.0.0.1:8000/api/getmetadata/15"/>

    def post(self, request, id):
        visitor_unique_key = (
            str(uuid.uuid4()) if not request.data.get("visitor_unique_key") else request.data.get("visitor_unique_key")
        )
        visit_id = str(uuid.uuid4()) if not request.data.get("visit_id") else request.data.get("visit_id")
        metadata = request.data.get("user_agent")
        referer = request.data.get("referer")
        browser = request.data.get("browser_type")
        os_type = request.data.get("os_type")
        device_type = request.data.get("device_type")
        ip_address = request.data.get("ip")
        language = request.data.get("language")

        create_view_into_table(
            id, referer, visit_id, visitor_unique_key, device_type, browser, metadata, os_type, ip_address, language
        )

        response_data = {"unique_key": str(visitor_unique_key), "visit_id": str(visit_id)}
        return Response(response_data, content_type="application/json")


class StatInDay(APIView):
    """
    Параметры у счетчика за определенный промежуток времени
    пример запроса:
    http://127.0.0.1:8000/api/view/data?id=15&filter=quarter

    Methods
    -------
    get(request)
        Обработчик  get запроса
    """

    model = None
    field_name = None
    permission_classes = [IsAuthenticated, IsCreatorAndReadOnly]

    def get(self, request):
        counter_id = request.GET.get("id", None)
        date_filter = request.GET.get("filter", None)

        if date_filter in ["threedays", "week", "month", "quarter", "year"]:
            if check_counter_exists(counter_id):
                start_date, end_date = get_validated_period_with_filter(date_filter)
                data = get_data_group_by_days(self.model, self.field_name, counter_id, start_date, end_date)

                response = {
                    "counter_id": counter_id,
                    "filter": date_filter,
                    "start_date": start_date,
                    "end_date": end_date,
                    "data": data,
                }
                return Response(response)
        return Response(
            {"error": [{"code": 400, "reason": "invalidParameter"}]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StatViewInDay(StatInDay):
    field_name = "count_views"
    model = ViewInDay


class StatVisitInDay(StatInDay):
    field_name = "count_visits"
    model = VisitInDay


class StatVisitorInDay(StatInDay):
    field_name = "count_visitors"
    model = VisitorInDay

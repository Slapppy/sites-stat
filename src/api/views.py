from django.http import HttpResponse
import uuid
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, datetime, timedelta
import httpagentparser
from app.clickhouse import create_connection
from web.clickhouse_models import Views, VisitorInDay, VisitInDay, ViewInDay
from django.db import connection
from infi.clickhouse_orm import funcs
from web.models import Counter


class StatCounterView(APIView):
    # пример запроса: http://127.0.0.1:8000/api/view_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31
    @staticmethod
    def get_data(counter_id, start_date, end_date):
        db = create_connection()
        views = Views.objects_in(db).filter(created_at__between=(start_date, end_date), counter_id=counter_id)
        return views

    def get(self, request):
        counter_id = request.GET.get("id", None)
        date1, date2 = request.GET.get("start-date", None), request.GET.get("end-date", None)

        if counter_id and date1:
            # Проверка пользователя
            if Counter.objects.filter(user_id=request.user.id, id=counter_id).count() != 0 or request.user.is_superuser:
                start_date = datetime.strptime(date1, "%Y-%m-%d")
                if not date2:
                    end_date = datetime.now()
                    date2 = end_date.strftime("%Y-%m-%d")
                else:
                    end_date = datetime.strptime(date2, "%Y-%m-%d") + timedelta(milliseconds=-1)

                views = self.get_data(counter_id, start_date, end_date)
                return Response(
                    {
                        "counter_id": int(counter_id),
                        "start-date": date1,
                        "end-date": date2,
                        "count_views": views.count(),
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


TRANSPARENT_1_PIXEL_GIF = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"


class StatCounterVisit(APIView):
    # http://127.0.0.1:8000/api/visit_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31
    @staticmethod
    def get_data(counter_id, start_date, end_date):
        db = create_connection()
        end_date += timedelta(days=1)
        views = VisitInDay.objects_in(db).filter(created_at__between=(start_date, end_date), counter_id=counter_id)
        return views.count()

    def get(self, request):
        counter_id = request.GET.get("id", None)
        start_date, end_date = request.GET.get("start-date", None), request.GET.get("end-date", None)

        if counter_id:
            # Проверка пользователя
            if Counter.objects.filter(user_id=request.user.id, id=counter_id).count() != 0 or request.user.is_superuser:
                if start_date:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                else:
                    start_date = Counter.objects.get(id=counter_id).created_at
                    print(start_date)

                if end_date:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                else:
                    end_date = datetime.now()

                visits = self.get_data(counter_id, start_date, end_date)
                return Response(
                    {
                        "counter_id": int(counter_id),
                        "start-date": start_date.strftime("%Y-%m-%d"),
                        "end-date": end_date.strftime("%Y-%m-%d"),
                        "count_visits": visits,
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


class StatCounterVisitor(APIView):
    # http://127.0.0.1:8000/api/visitor_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31
    @staticmethod
    def get_data(counter_id, start_date, end_date):
        db = create_connection()
        visitors = (
            VisitorInDay.objects_in(db)
            .filter(created_at__between=(start_date, end_date), counter_id=counter_id)
            .aggregate("counter_id", sum_visitors="sum(count_visitors)")
        )
        if visitors:
            visitors = visitors[0].sum_visitors
            return visitors
        return 0

    def get(self, request):
        counter_id = request.GET.get("id", None)
        start_date, end_date = request.GET.get("start-date", None), request.GET.get("end-date", None)

        if counter_id:
            # Проверка пользователя
            if Counter.objects.filter(user_id=request.user.id, id=counter_id).count() != 0 or request.user.is_superuser:
                if start_date:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                else:
                    start_date = Counter.objects.get(id=counter_id).created_at
                    print(start_date)

                if end_date:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                else:
                    end_date = datetime.now()

                visitors = self.get_data(counter_id, start_date, end_date)
                return Response(
                    {
                        "counter_id": int(counter_id),
                        "start-date": start_date.strftime("%Y-%m-%d"),
                        "end-date": end_date.strftime("%Y-%m-%d"),
                        "count_visitors": visitors,
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


class GetMetaDataView(APIView):
    # пример <img src="http://127.0.0.1:8000/api/getmetadata/15"/>

    def post(self, request, id):
        db = create_connection()
        visitor_unique_key = (
            str(uuid.uuid4()) if not request.data.get("visitor_unique_key") else request.data.get("visitor_unique_key")
        )
        visit_id = str(uuid.uuid4()) if not request.data.get("visit_id") else request.data.get("visit_id")
        # visitor_unique_key = request.data.get("visitor_unique_key", str(uuid.uuid4()))
        print(request.data)
        print(visitor_unique_key)
        print(visit_id)
        metadata = request.headers["User-Agent"]
        data_split = httpagentparser.detect(metadata, "os")
        referer = request.META.get("HTTP_REFERER")
        browser = data_split["browser"]["name"]
        os_type = data_split["platform"]["name"]
        device_type = data_split["os"]["name"]
        ip_address = request.META["REMOTE_ADDR"]
        language = request.META.get("HTTP_ACCEPT_LANGUAGE", "").split(",")[0][:2]

        notes = [
            Views(
                counter_id=id,
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

        response_data = {"unique_key": str(visitor_unique_key), "visit_id": str(visit_id)}
        return Response(response_data, content_type="application/json")


class StatInDay(APIView):
    """
    Параметры у счетчика за определенный промежуток времени
    пример запроса:
    http://127.0.0.1:8000/api/view/data?id=15&filter=month

    Methods
    -------
    get_date(date_filter)
        По значению фильтра определяет начальную и конечную дату

    get_data(counter_id, start_date, end_date)
        Возвращает список объектов из таблицы viewinday

    get(request)
        Обработчик  get запроса
    """

    field_name = None
    model = None

    @staticmethod
    def get_date(date_filter):
        end_date = date.today()
        if date_filter == "threedays":
            start_date = end_date - timedelta(days=2)
        elif date_filter == "week":
            start_date = end_date - timedelta(days=6)
        elif date_filter == "month":
            month, year = (end_date.month - 1, end_date.year) if end_date.month != 1 else (12, end_date.year - 1)
            start_date = end_date.replace(day=end_date.day, month=month, year=year)
        elif date_filter == "quarter":
            month, year = (end_date.month - 3, end_date.year) if end_date.month != 1 else (12, end_date.year - 1)
            start_date = end_date.replace(day=end_date.day, month=month, year=year)
        else:
            start_date = end_date.replace(day=end_date.day, month=end_date.month, year=end_date.year - 1)
        return start_date, end_date

    def get_data(self, counter_id, start_date, end_date):
        db = create_connection()
        views = self.model.objects_in(db).filter(created_at__between=(start_date, end_date), counter_id=counter_id)
        return list(views)

    def get(self, request):
        counter_id = request.GET.get("id", None)
        date_filter = request.GET.get("filter", None)

        filter_lst = ["threedays", "week", "month", "quarter", "year"]

        if Counter.objects.filter(id=counter_id):
            if date_filter in filter_lst:
                start_date, end_date = self.get_date(date_filter)
                dataset = self.get_data(counter_id, start_date, end_date)

                response = {
                    "counter_id": counter_id,
                    "filter": date_filter,
                    "start_date": start_date,
                    "end_date": end_date,
                    "data": [],
                }

                temp_date = start_date
                while temp_date <= end_date:
                    data = list(filter(lambda x: x.created_at == temp_date, dataset))
                    response["data"].append(
                        {
                            "date": temp_date,
                            self.field_name: sum((getattr(d, self.field_name) for d in data)) if len(data) > 0 else 0,
                        }
                    )
                    temp_date += timedelta(days=1)

                return Response(response)
        return Response(
            {"error": [{"code": 400, "reason": "invalidParameter"}]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StatViewInDay(StatInDay, APIView):
    field_name = "count_view"
    model = ViewInDay


class StatVisitInDay(StatInDay, APIView):
    field_name = "count_visit"
    model = VisitInDay


class StatVisitorInDay(StatInDay, APIView):
    field_name = "count_visitor"
    model = VisitorInDay

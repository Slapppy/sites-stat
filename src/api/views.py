from time import timezone
from django.http import HttpResponse
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
import httpagentparser
from app.clickhouse import create_connection
from web.clickhouse_models import Views
from django.db import connection

from web.models import Counter


class StatCounterView(APIView):
    # пример запроса: http://127.0.0.1:8000/api/view_stat/data?id=5&start-date=2022-12-29&end-date=2022-12-31
    @staticmethod
    def get_data(counter_id, start_date, end_date):
        db = create_connection()
        views = Views.objects_in(db).filter(
            created_at__between=(start_date, end_date), counter_id=counter_id
        )
        return views

    def get(self, request):
        counter_id = request.GET.get("id", None)
        date1, date2 = request.GET.get("start-date", None), request.GET.get(
            "end-date", None
        )

        if counter_id and date1:
            # Проверка пользователя
            if (
                    Counter.objects.filter(user_id=request.user.id, id=counter_id).count()
                    != 0
                    or request.user.is_superuser
            ):
                start_date = datetime.strptime(date1, "%Y-%m-%d")
                if not date2:
                    end_date = datetime.now()
                    date2 = end_date.strftime("%Y-%m-%d")
                else:
                    end_date = datetime.strptime(date2, "%Y-%m-%d") + timedelta(
                        milliseconds=-1
                    )

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
        views = (
            Views.objects_in(db)
            .filter(created_at__between=(start_date, end_date), counter_id=counter_id)
            .order_by("visitor_unique_key", "created_at")
        )
        if views.count() == 0:
            return 0
        print("count", views.count())
        count_visits = 0
        visitor = ""
        last_time = ""
        for i in range(views.count() - 1):
            print(views[i].created_at)
            if views[i].visitor_unique_key != visitor:
                visitor = views[i].visitor_unique_key
                last_time = views[i].created_at
                count_visits += 1
            if views[i].visitor_unique_key == visitor and views[i].created_at - last_time > timedelta(minutes=30):
                count_visits += 1
                last_time = views[i].created_at
        return count_visits

    def get(self, request):
        counter_id = request.GET.get("id", None)
        start_date, end_date = request.GET.get("start-date", None), request.GET.get(
            "end-date", None
        )
        print(counter_id)
        print(start_date)
        print(end_date)

        if counter_id:
            # Проверка пользователя
            if (
                    Counter.objects.filter(user_id=request.user.id, id=counter_id).count()
                    != 0
                    or request.user.is_superuser
            ):
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
                        "count_views": visits,
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

        visitor_unique_key = None
        if not request.data['visitor_unique_key']:
            visitor_unique_key = str(uuid.uuid4())
        elif Views.objects_in(db).filter(visitor_unique_key=request.data['visitor_unique_key']):
            visitor_unique_key = request.data['visitor_unique_key']
        else:
            visitor_unique_key = str(uuid.uuid4())





        metadata = request.headers["User-Agent"]
        data_split = httpagentparser.detect(metadata, "os")
        referer = request.META.get("HTTP_REFERER")
        browser = data_split["browser"]["name"]
        os_type = data_split["platform"]["name"]
        device_type = data_split["os"]["name"]
        ip_address = request.META["REMOTE_ADDR"]
        language = request.META.get("HTTP_ACCEPT_LANGUAGE", "").split(",")[0][:2]

        # visitor_unique_key = self.generate_key()

        notes = [
            Views(
                counter_id=id,
                referer=referer,
                view_id=uuid.uuid4(),
                visitor_unique_key=visitor_unique_key,
                device_type=device_type,
                browser_type=browser,
                user_agent=metadata,
                os_type=os_type,
                ip=ip_address,
                language=language,
                created_at=timezone.real,
            )
        ]

        db.insert(notes)

        response_data = {"unique_key": visitor_unique_key}
        return Response(response_data, content_type="application/json")

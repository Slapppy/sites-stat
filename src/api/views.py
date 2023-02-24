from django.http import HttpResponse
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
import httpagentparser
from app.clickhouse import create_connection
from web.clickhouse_models import Views
import requests


# from src.web.models import Counter


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
            if (
                    Counter.objects.all().filter(user_id=request.user.id, id=counter_id).count() != 0
                    or request.user.is_superuser
            ):
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

            return Response({"error": [{"code": 403, "reason": "AccessError"}]}, status=status.HTTP_403_FORBIDDEN)

        return Response({"error": [{"code": 400, "reason": "invalidParameter"}]}, status=status.HTTP_400_BAD_REQUEST)


TRANSPARENT_1_PIXEL_GIF = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"


class GetMetaDataView(APIView):
    # пример <img src="http://127.0.0.1:8000/api/getmetadata/15"/>
    # unique_key = None
    #
    # def generate_key(self, request):
    #     if GetMetaDataView.unique_key is None:
    #         GetMetaDataView.unique_key = uuid.uuid4()
    #     request.META['unique'] = GetMetaDataView.unique_key
    #     # request.META['unique'] = None
    #     # unique_key = request.META('unique')
    #     print(request.META['unique'])
    #     db = create_connection()
    #     print(Views.objects_in(db).filter(visitor_unique_key=request.META['unique']))
    #     if Views.objects_in(db).filter(visitor_unique_key=request.META['unique']):
    #         return request.META['unique']
    #     else:
    #         visitor_key = uuid.uuid4()
    #         GetMetaDataView.unique_key = visitor_key
    #         print(request.META['unique'])
    #         return visitor_key

    # def generate_key(self, request):
    #     # request.META['unique'] = None
    #     visitor_unique_key = request.META('unique')
    #     db = create_connection()
    #     print(request.headers)
    #     if 'unique' in request.headers:
    #         #            if Views.objects_in(db).get(visitor_unique_key=response.headers['unique']):
    #         return response.headers['unique']
    #     else:
    #         visitor_key = uuid.uuid4()
    #         response.headers['unique'] = visitor_key
    #         return visitor_key

    def get(self, request, id):
        db = create_connection()

        visitor_unique_key = request.COOKIES.get('visitor_unique_key', None)
        if not visitor_unique_key:
            visitor_unique_key = str(uuid.uuid4())
            response = Response(content_type='application/json')
            response.set_cookie('visitor_unique_key', visitor_unique_key)
        else:
            response = Response()

        metadata = request.headers["User-Agent"]
        data_split = httpagentparser.detect(metadata, "os")
        referer = request.META.get("HTTP_REFERER")
        browser = data_split["browser"]["name"]
        os_type = data_split["platform"]["name"]
        device_type = data_split["os"]["name"]
        ip_address = request.META["REMOTE_ADDR"]
        language = request.META["HTTP_ACCEPT_LANGUAGE"].split(",")[0][:2]

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
                created_at=datetime.now(),
            )
        ]

        db.insert(notes)

        response_data = {'key': visitor_unique_key}
        response.data = response_data
        return response
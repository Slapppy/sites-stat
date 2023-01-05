from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

from app.clickhouse import create_connection
from web.clickhouse_models import Views

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

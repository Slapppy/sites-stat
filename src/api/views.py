from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

from app.clickhouse import create_connection
from web.clickhouse_models import Views


class StatCounterView(APIView):
    @staticmethod
    def get_data(counter_id, start_date, end_date):
        db = create_connection()
        views = Views.objects_in(db).filter(created_at__between=(start_date, end_date), counter_id=counter_id)
        return views

    def get(self, request):
        counter_id, date = request.GET.get("id", None), request.GET.get("date", None)

        if counter_id and date:
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1, milliseconds=-1)
            views = self.get_data(counter_id, start_date, end_date)
            return Response({"counter_id": int(counter_id), "date": date, "count_views": views.count()})

        return Response({"error": [{"code": 400, "reason": "invalidParameter"}]}, status=status.HTTP_400_BAD_REQUEST)

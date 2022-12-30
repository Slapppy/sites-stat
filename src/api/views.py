from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta

from app.clickhouse import create_connection
from web.clickhouse_models import Views


@api_view()
def status_view(request):
    return Response({"status": "ok"})


@api_view()
def counter_views(request):
    db = create_connection()
    counter_id, date = request.GET["id"], request.GET["date"]
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    views = Views.objects_in(db).filter(
        (Views.counter_id == counter_id) & (Views.created_at >= start_date) & (Views.created_at < end_date)
    )
    return Response({"count_views": views.count()})

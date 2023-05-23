from celery_yandex_serverless.django import worker_view_factory

from api.views import (
    StatCounterView,
    GetMetaDataView,
    StatCounterVisit,
    StatCounterVisitor,
    StatViewInDay,
    StatVisitInDay,
    StatVisitorInDay,
)
from django.urls import path

from app.celery import app

urlpatterns = [
    path("view/data", StatViewInDay.as_view(), name="view_in_day"),
    path("visit/data", StatVisitInDay.as_view(), name="visit_in_day"),
    path("visitor/data", StatVisitorInDay.as_view(), name="visitor_in_day"),
    path("view_stat/data", StatCounterView.as_view(), name="view_stat"),
    path("visit_stat/data", StatCounterVisit.as_view(), name="visit_stat"),
    path("visitor_stat/data", StatCounterVisitor.as_view(), name="visitor_stat"),
    path("getmetadata/<int:id>", GetMetaDataView.as_view(), name="getmetadata"),
    path("worker/<str:key>/", worker_view_factory(app)),
]

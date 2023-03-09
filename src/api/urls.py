from api.views import StatCounterView, GetMetaDataView, StatCounterVisit, StatCounterVisitor, StatViewInDay
from django.urls import path

urlpatterns = [
    path("view/data", StatViewInDay.as_view(), name="view_in_day"),
    path("view_stat/data", StatCounterView.as_view(), name="view_stat"),
    path("visit_stat/data", StatCounterVisit.as_view(), name="visit_stat"),
    path("visitor_stat/data", StatCounterVisitor.as_view(), name="visitor_stat"),
    path("getmetadata/<int:id>", GetMetaDataView.as_view(), name="getmetadata"),
]

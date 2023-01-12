from api.views import StatCounterView, GetMetaDataView
from django.urls import path

urlpatterns = [
    path("view_stat/data", StatCounterView.as_view(), name="view_stat"),
    path("getmetadata/<int:id>", GetMetaDataView.as_view(), name="getmetadata"),
]

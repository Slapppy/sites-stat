from api.views import StatCounterView
from django.urls import path

urlpatterns = [path("view_stat/data", StatCounterView.as_view(), name="view_stat")]

from api.views import status_view, counter_views
from django.urls import path

urlpatterns = [path("", status_view, name="status"), path("view_stat", counter_views, name="view_stat")]

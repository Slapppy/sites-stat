from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import (
    CounterCreate,
    RegistrationView,
    CounterDetailView,
    CounterEditView,
    CounterDeleteView,
    auth_page,
    MainView,
    CountersListView,
    test_func
)


urlpatterns = [
                  path("", MainView.as_view(), name="main"),
                  path("auth", auth_page, name="auth"),
                  path("logout/", LogoutView.as_view(next_page=reverse_lazy("main")), name="logout"),
                  path("registration", RegistrationView.as_view(), name="reg"),
                  path("counters", CountersListView.as_view(), name="counters"),
                  path("counters/add", CounterCreate.as_view(), name="add"),
                  path("counters/<int:pk>", CounterDetailView.as_view(), name="counter"),
                  path("counters/edit/<int:id>", CounterEditView.as_view(), name="edit"),
                  path("counters/delete/<int:pk>", CounterDeleteView.as_view(), name="delete"),
                  path("test/test/", test_func, name="test"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

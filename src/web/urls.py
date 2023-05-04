from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    CounterCreate,
    RegistrationView,
    CounterDetailView,
    CounterEditView,
    CounterDeleteView,
)

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("auth", views.auth_page, name="auth"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("main")), name="logout"),
    path("registration", RegistrationView.as_view(), name="reg"),
    path("counters", login_required(views.CountersListView.as_view()), name="counters"),
    path("counters/add", login_required(CounterCreate.as_view()), name="add"),
    path("counters/<int:pk>", login_required(CounterDetailView.as_view()), name="counter"),
    path("counters/edit/<int:id>", login_required(CounterEditView.as_view()), name="edit"),
    path("counters/delete/<int:pk>", login_required(CounterDeleteView.as_view()), name="delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

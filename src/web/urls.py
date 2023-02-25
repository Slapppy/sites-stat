from django.urls import path, include, reverse_lazy
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
    path("registration", RegistrationView.as_view(), name="reg"),
    path("auth", views.auth_page, name="auth"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("main")), name="logout"),
    path("counters", views.CountersListView.as_view(), name="counters"),
    path("counters/<int:pk>", CounterDetailView.as_view(), name="counter"),
    path("counters/add", CounterCreate.as_view(), name="add"),
    path("counters/edit/<int:id>", CounterEditView.as_view(), name="edit"),
    path("counters/delete/<int:pk>", CounterDeleteView.as_view(), name="delete"),
]

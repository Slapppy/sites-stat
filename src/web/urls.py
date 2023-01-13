from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CounterCreate, RegistrationView, CounterDetailView

urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
    path("add", CounterCreate.as_view(), name="add"),
    path("profile/counter/<int:pk>", CounterDetailView.as_view(), name="counter"),
    path("", views.main_page, name="main"),
]

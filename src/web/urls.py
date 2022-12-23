from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CounterCreate

urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", views.registration_page, name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
    path("add", CounterCreate.as_view(), name = 'add'),
    path("", views.main_page, name="main"),
]

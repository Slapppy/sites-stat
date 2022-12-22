from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CounterCreate

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth", views.auth_page, name="auth"),
    path("registration", views.registration_page, name="registration"),
    path("add", CounterCreate.as_view()),
]

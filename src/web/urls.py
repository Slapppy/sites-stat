from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CounterCreate

<<<<<<< src/web/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth", views.auth_page, name="auth"),
    path("registration", views.registration_page, name="registration"),
    path("add", CounterCreate.as_view()),
=======

urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", views.registration_page, name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
    path("add", CounterCreate.as_view()),
    path("", views.main_page, name="main")
>>>>>>> src/web/urls.py
]

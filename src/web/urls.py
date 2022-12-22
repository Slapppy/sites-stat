from django.urls import path
from . import views


urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", views.registration_page, name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
]

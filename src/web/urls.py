from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CounterCreate, RegistrationView, CounterDetailView, CounterEditView, CounterDelete

urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
    path("add", CounterCreate.as_view(), name="add"),
    path("edit/<int:id>", CounterEditView.as_view(), name="edit"),
    path("profile/counter/<int:pk>", CounterDetailView.as_view(), name="counter"),
    path("counter/<int:pk>/delete/", CounterDelete.as_view(), name="counter_delete"),
    path("", views.main_page, name="main"),
]

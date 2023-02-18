from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views
from .views import CounterCreate, RegistrationView, CounterDetailView, CounterEditView, CounterDeleteView

urlpatterns = [
    path("auth", views.auth_page, name="auth"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", views.CountersListView.as_view(), name="profile"),
    path("add", CounterCreate.as_view(), name="add"),
    path("edit/<int:id>", CounterEditView.as_view(), name="edit"),
    path("profile/counter/<int:pk>", CounterDetailView.as_view(), name="counter"),
    path("counter/<int:pk>/delete/", CounterDeleteView.as_view(), name="counter_delete"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("main")), name="logout"),
    path("", views.main_page, name="main"),
]

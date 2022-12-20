from django.urls import path
from . import views

urlpatterns = [

    #path('', views.main_page, name='main_page'),
    path('auth', views.auth_page, name='auth'),
    path('registration', views.registration_page, name='registration'),



]

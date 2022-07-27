from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login_auth', views.login_auth, name='login_auth'),
]

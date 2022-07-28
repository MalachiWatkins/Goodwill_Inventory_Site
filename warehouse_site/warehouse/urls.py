from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login_auth', views.login_auth, name='login_auth'),
    path('main/<str:user>/<str:auth>/', views.main)
]

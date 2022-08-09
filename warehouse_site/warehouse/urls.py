from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login_auth', views.login_auth, name='login_auth'),
    path('main/<str:user>/<str:auth>/', views.main),
    path('main/truck', views.truck),
    path('home', views.home),
    path('main/process/<str:data>', views.proc),
    path('data/<str:data>/<str:store>/<str:storage>/<str:sub>/<str:id>', views.proc_data),
    path('logout', views.logout),
    path('tools', views.tools),
    path('stats', views.stats),



]

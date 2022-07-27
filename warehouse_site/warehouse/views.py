from django.shortcuts import render
from django.http import HttpResponse
from .forms import Userform
from django.http import HttpResponseRedirect
import os
import jinja2
import cgi
import webbrowser
from datetime import date
from pymongo import MongoClient
import pymongo
import random


warehouse_db = cluster["WAREHOUSE_MANAGEMENT_Test"]  # GOODWILL

user_db = warehouse_db["Truck_Receiver_DB"]
Truck_Receiver_DB = warehouse_db["Truck_Receiver_DB"]

Processor_Review_DB = warehouse_db["Processor_Review_DB"]


Jewelry_DB = warehouse_db["Jewelry_DB"]
Jewelry_Review_DB = warehouse_db["Jewelry_Review_DB"]

Books_Media_DB = warehouse_db["Books_Media_DB"]
Book_Media_Review_DB = warehouse_db["Book_Media_Review_DB"]

Finished_DB = warehouse_db["Finished_DB"]

Finished_Jewlery_DB = warehouse_db["Finished_Jewlery_DB"]
# Create your views here.


def login(request):
    form = Userform(request.POST)
    return render(request, 'login.html', {'form': form})


def login_auth(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            return HttpResponse()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Userform()

    return render(request, 'login_auth.html')


def landing():

    return


def main(request):
    return HttpResponse("Hello")

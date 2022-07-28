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
import hashlib
import bcrypt
import string

warehouse_db = cluster["WAREHOUSE_MANAGEMENT_GOODWILL"]  # GOODWILL

user_db = warehouse_db["User_DB"]
Truck_Receiver_DB = warehouse_db["Truck_Receiver_DB"]

Processor_Review_DB = warehouse_db["Processor_Review_DB"]


Jewelry_DB = warehouse_db["Jewelry_DB"]
Jewelry_Review_DB = warehouse_db["Jewelry_Review_DB"]

Books_Media_DB = warehouse_db["Books_Media_DB"]
Book_Media_Review_DB = warehouse_db["Book_Media_Review_DB"]

Finished_DB = warehouse_db["Finished_DB"]

Finished_Jewlery_DB = warehouse_db["Finished_Jewlery_DB"]


def login(request):
    form = Userform(request.POST)
    return render(request, 'login.html', {'form': form})


def login_auth(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            hashed_pw = hashlib.sha256(password.encode())
            checkpw = hashed_pw.hexdigest()
            try:
                user_query = {'User': user}
                user_docs = user_db.find(user_query)
                User_Document = user_docs[0]
            except:
                User_Document = {'User': 'NOT FOUND',
                                 'Password': 'NOT FOUND', 'auth_token': 'UNAUTH'}
            if user == User_Document['User']:
                if User_Document['password'] == checkpw:
                    auth = User_Document['auth_token']
                    main = 'main/'
                    redir = main + User_Document['User'] + '/' + auth + '/'

                    return HttpResponseRedirect(redir)
                else:
                    return render(request, 'login.html', {'form': form, 'failed': 'yes'})
            else:
                return render(request, 'login.html', {'form': form, 'failed': 'yes'})

    return render(request, 'login_auth.html')


def main(request, user, auth):
    user_query = {'User': user}
    user_docs = user_db.find(user_query)
    if user_docs[0]['auth_token'] == auth:
        return render(request, 'landing.html')
    else:
        return HttpResponse('not auth')

from django.shortcuts import render
from django.http import HttpResponse
from .forms import Userform
from .forms import TruckForm
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
from datetime import date

today = date.today()
date_format = today.strftime("%Y-%m-%d")
date_proc_format = str(date_format)

warehouse_db = cluster["WAREHOUSE_MANAGEMENT_Test"]  # GOODWILL

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
        response = render(request, 'landing.html')
        response.set_cookie('user', auth, max_age=1000)
        response.set_cookie('user_name', user, max_age=1000)
        return response
    else:
        form = Userform(request.POST)
        return render(request, 'login.html', {'form': form, 'UNAUTH': 'yes'})


def home(request):
    value = request.COOKIES.get('user')
    user_name = request.COOKIES.get('user_name')
    if value is None:
        form = Userform(request.POST)
        response = render(request, 'login.html', {
                          'form': form, 'UNAUTH': 'yes'})
        response.delete_cookie('user')
        return response
    else:
        main = 'main/'
        redir = main + user_name + '/' + value + '/'
        return HttpResponseRedirect(redir)


def db_post(post, isJewlery, isBooks, isSGW):  # Receving Document
    if post['Storage_Type'] != '':
        if isJewlery == True and isBooks == False and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Jewelry_DB.insert_one(post)
                x += 1
        elif isJewlery == False and isBooks == True and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Books_Media_DB.insert_one(post)
                x += 1
        else:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                Truck_Receiver_DB.insert_one(post)
                x += 1
    else:
        # DATA NOT SUBMITTED ROUTE GOES HERE
        null = 'null'
    return


def truck(request):
    value = request.COOKIES.get('user')
    if value is None:
        form = Userform(request.POST)
        response = render(request, 'login.html', {
                          'form': form, 'UNAUTH': 'yes'})
        response.delete_cookie('user')

        return response
    else:
        # form = TruckForm(request.POST)
        if request.method == 'POST':
            form_data = TruckForm(request.POST)
            if form_data.is_valid():
                QUANTITY = form_data.cleaned_data['Quant']
                STORAGE_TYPE = form_data.cleaned_data['storage']
                STORE_NUMBER = form_data.cleaned_data['store_number']
                ITEM_CONTENTS = form_data.cleaned_data['item_contents']
                PROBLEM_FORM = form_data.cleaned_data['problems']
                data_post = {
                    '_id': random.random(),
                    'Quantity': QUANTITY,
                    'Storage_Type': STORAGE_TYPE,
                    'Date_Received': date_format,
                    'Store_Number': STORE_NUMBER,
                    'Contents': ITEM_CONTENTS,
                    'Problems': PROBLEM_FORM,
                }
                if ITEM_CONTENTS == 'Jewelry':
                    db_post(post=data_post, isJewlery=True,
                            isBooks=False, isSGW=False)
                elif ITEM_CONTENTS == 'Books':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=True, isSGW=False)
                elif ITEM_CONTENTS == 'Media':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=True, isSGW=False)
                else:
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=True)
            form = TruckForm()
            return render(request, 'truck.html', {'form': form})
        else:
            form = TruckForm(request.POST)
            return render(request, 'truck.html', {'form': form})

        return render(request, 'truck.html')

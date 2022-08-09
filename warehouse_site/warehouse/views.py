from django.shortcuts import render
from django.http import HttpResponse
from .forms import Userform
from .forms import TruckForm
from .forms import ProcForm
from .forms import ProcDataForm
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
# to- do stats and tools page and forms for processing
# then cleanup test before and after cleanup
today = date.today()
date_format = today.strftime("%Y-%m-%d")
date_proc_format = str(date_format)

warehouse_db = cluster["WAREHOUSE_MANAGEMENT_LIVE"]  # GOODWILL

user_db = warehouse_db["User_DB"]
Truck_Receiver_DB = warehouse_db["Truck_Receiver_DB"]

Processor_Review_DB = warehouse_db["Processor_Review_DB"]


Jewelry_DB = warehouse_db["Jewelry_DB"]

Books_Media_DB = warehouse_db["Books_Media_DB"]
Books_DB = warehouse_db["Books"]
Media_DB = warehouse_db["Media"]


Computer_DB = warehouse_db["Computer_DB"]

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
            print(checkpw)
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
        response.set_cookie('user', auth, max_age=10000)
        response.set_cookie('user_name', user, max_age=10000)
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


def db_post(post, isJewlery, isBooks, isSGW, isComputers, isMedia):  # Receving Document
    if post['Storage_Type'] != '':
        if isJewlery == True and isBooks == False and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                post['id'] = random.random()
                Jewelry_DB.insert_one(post)
                x += 1
        elif isJewlery == False and isBooks == True and isSGW == False:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                post['id'] = random.random()
                Books_DB.insert_one(post)
                x += 1
        elif isComputers == True:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                post['id'] = random.random()
                Computer_DB.insert_one(post)
                x += 1
        elif isMedia == True:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                post['id'] = random.random()
                Media_DB.insert_one(post)
                x += 1
        else:
            x = 0
            while x < int(post['Quantity']):
                post['_id'] = random.random()
                post['id'] = random.random()
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
                    'id': random.random(),
                    'Quantity': QUANTITY,
                    'Storage_Type': STORAGE_TYPE,
                    'Date_Received': date_format,
                    'Store_Number': STORE_NUMBER,
                    'Contents': ITEM_CONTENTS,
                    'Problems': PROBLEM_FORM,
                }
                if ITEM_CONTENTS == 'Jewelry':
                    db_post(post=data_post, isJewlery=True,
                            isBooks=False, isSGW=False, isComputers=False, isMedia=False)
                elif ITEM_CONTENTS == 'Books':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=True, isSGW=False, isComputers=False, isMedia=False)
                elif ITEM_CONTENTS == 'Media':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=False, isComputers=False, isMedia=True)
                elif ITEM_CONTENTS == 'Computers':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=False, isComputers=True, isMedia=False)
                else:
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=True, isComputers=False, isMedia=False)
            else:
                QUANTITY = form_data.cleaned_data['Quant']
                STORAGE_TYPE = form_data.cleaned_data['storage']
                STORE_NUMBER = form_data.cleaned_data['store_number']
                ITEM_CONTENTS = form_data.cleaned_data['item_contents']
                PROBLEM_FORM = form_data.cleaned_data['problems']
                data_post = {
                    'id': random.random(),
                    'Quantity': QUANTITY,
                    'Storage_Type': STORAGE_TYPE,
                    'Date_Received': date_format,
                    'Store_Number': STORE_NUMBER,
                    'Contents': ITEM_CONTENTS,
                    'Problems': PROBLEM_FORM,
                }
                if ITEM_CONTENTS == 'Jewelry':
                    db_post(post=data_post, isJewlery=True,
                            isBooks=False, isSGW=False, isComputers=False, isMedia=False)
                elif ITEM_CONTENTS == 'Books':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=True, isSGW=False, isComputers=False, isMedia=False)
                elif ITEM_CONTENTS == 'Media':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=False, isComputers=False, isMedia=True)
                elif ITEM_CONTENTS == 'Computers':
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=False, isComputers=True, isMedia=False)
                else:
                    db_post(post=data_post, isJewlery=False,
                            isBooks=False, isSGW=True, isComputers=False, isMedia=False)
            form = TruckForm()
            return render(request, 'truck.html', {'form': form})
        else:
            form = TruckForm(request.POST)
            return render(request, 'truck.html', {'form': form})

        return render(request, 'truck.html')


def proc(request, data):
    value = request.COOKIES.get('user')
    if value is None:
        form = Userform(request.POST)
        response = render(request, 'login.html', {
            'form': form, 'UNAUTH': 'yes'})
        response.delete_cookie('user')

        return response
    if request.method == 'POST':
        form = ProcForm(request.POST)
        if form.is_valid():
            print(data)
        else:
            # main / process / data / <str: data > / < str: store > / < str: storage >
            storage = form.cleaned_data['storage']
            store_number = form.cleaned_data['store_number']
            return HttpResponseRedirect('/data/' + data + '/' + store_number + '/' + storage + '/non_sub/null')

    else:
        empty_proc_form = ProcForm()
        return render(request, 'proc.html', {'form': empty_proc_form, 'data': data})


def proc_data(request, data, store, storage, sub, id):
    value = request.COOKIES.get('user')
    if value is None:
        form = Userform(request.POST)
        response = render(request, 'login.html', {
            'form': form, 'UNAUTH': 'yes'})
        response.delete_cookie('user')
        return response
    else:
        if sub == 'sub':
            form = ProcDataForm(request.POST)
            if form.is_valid():
                STORE_NUMBER = store
                STORAGE = storage
                CONTENTS = data
                MANIFEST_NUMBER = form.cleaned_data['man_number']
                PROBLEMS = form.cleaned_data['problems']
                DATE_PROSESSED = date_proc_format
                SEAL_NUM = form.cleaned_data['seal_num']
                PROCESSED_BY = form.cleaned_data['proc_by']

                proc_query = {'Contents': data,
                              'Storage_Type': storage, 'Store_Number': store}
                db_dict = {
                    'Collectables': Truck_Receiver_DB,
                    'Computers': Computer_DB,
                    'Jewelry': Jewelry_DB,
                    'Books': Books_DB,
                    'Media': Media_DB,
                }
                db_to_search = db_dict[data]
                proc_documents = db_to_search.find(proc_query)

                single_doc = proc_documents[0]
                docid = single_doc['id']
                date_rece = single_doc['Date_Received']
                problems_truck = single_doc['Problems']

                # Delete post
                delquery = {"id": float(docid)}
                db_to_search.delete_one(delquery)
                # add post to rev data
                New_Post = {
                    'id': random.random(),
                    'Storage_Type': STORAGE,
                    'Date_Received': date_rece,  # get
                    'Date_Processed': date_proc_format,
                    'MANIFEST_NUMBER': MANIFEST_NUMBER,
                    'Store_Number': STORE_NUMBER,
                    'Contents': CONTENTS,
                    'Problems_Proc': PROBLEMS,
                    'Problems_Truck': problems_truck,
                    'Processed_By': PROCESSED_BY,
                }
                Finished_DB.insert_one(New_Post)

            else:
                STORE_NUMBER = store
                STORAGE = storage
                CONTENTS = data
                MANIFEST_NUMBER = form.cleaned_data['man_number']
                PROBLEMS = form.cleaned_data['problems']
                DATE_PROSESSED = date_proc_format
                SEAL_NUM = form.cleaned_data['seal_num']
                PROCESSED_BY = form.cleaned_data['proc_by']

                proc_query = {'id': float(id)}
                db_dict = {
                    'Collectables': Truck_Receiver_DB,
                    'Computers': Computer_DB,
                    'Jewelry': Jewelry_DB,
                    'Books': Books_DB,
                    'Media': Media_DB,
                }
                db_to_search = db_dict[data]
                proc_documents = db_to_search.find(proc_query)

                single_doc = proc_documents[0]
                print(single_doc)
                date_rece = single_doc['Date_Received']
                problems_truck = single_doc['Problems']

                # Delete post
                delquery = {"id": float(id)}
                db_to_search.delete_one(delquery)
                # add post to rev data
                New_Post = {
                    'id': random.random(),
                    'Storage_Type': STORAGE,
                    'Date_Received': date_rece,  # get
                    'Date_Processed': date_proc_format,
                    'MANIFEST_NUMBER': MANIFEST_NUMBER,
                    'Store_Number': STORE_NUMBER,
                    'Contents': CONTENTS,
                    'Problems_Proc': PROBLEMS,
                    'Problems_Truck': problems_truck,
                    'Processed_By': PROCESSED_BY,
                }
                Finished_DB.insert_one(New_Post)

        if storage != "null" and store != "null":
            null = '1'
            proc_query = {'Store_Number': store, 'Storage_Type': storage,
                          'Contents': data}
        elif storage != "null" or store != "null":
            if storage != "null":
                null = '1'
                proc_query = {'Contents': data,
                              'Storage_Type': storage}
            else:
                null = '1'
                proc_query = {'Contents': data,
                              'Store_Number': store}
        elif storage == "null" and store == "null":
            null = 'n'
            proc_query = {'Contents': data}

        db_dict = {
            'Collectables': Truck_Receiver_DB,
            'Computers': Computer_DB,
            'Jewelry': Jewelry_DB,
            'Books': Books_DB,
            'Media': Media_DB,
        }
        db_to_search = db_dict[data]
        proc_documents = db_to_search.find(proc_query)
        document_count = db_to_search.count_documents(
            proc_query)
        form_data = ProcDataForm()
        pass_url = '/data/' + data + '/' + store + '/' + storage
        return render(request, 'proc_data.html', {'data': data, 'documents': proc_documents, 'count': document_count, 'form': form_data, 'url': pass_url, 'null': null})


def logout(request):
    # also add regeneration of the auth token hereq
    response = HttpResponseRedirect('/')
    response.delete_cookie('user')
    response.delete_cookie('user_name')
    return response


def stats(request):
    book_query = {"Contents": 'Books'}
    media_query = {"Contents": "Media"}
    sgw_query = {"Contents": "Collectables"}
    jewlery_query = {"Contents": "Jewelry"}

    # Total Left to process
    total_books_gay = Books_DB.count_documents(
        {"Contents": "Books", "Storage_Type": "Gaylord"})
    total_books_tote = Books_DB.count_documents(
        {"Contents": "Books", "Storage_Type": "Tote"})
    total_media_gay = Media_DB.count_documents(
        {"Contents": "Media", "Storage_Type": "Gaylord"})
    total_media_tote = Media_DB.count_documents(
        {"Contents": "Media", "Storage_Type": "Tote"})
    total_sgw_gay = Truck_Receiver_DB.count_documents(
        {"Contents": "Collectables", "Storage_Type": "Gaylord"})
    total_sgw_tote = Truck_Receiver_DB.count_documents(
        {"Contents": "Collectables", "Storage_Type": "Tote"})
    total_jewlery_gay = Jewelry_DB.count_documents(
        {"Contents": "Jewelry", "Storage_Type": "Gaylord"})
    total_jewlery_tote = Jewelry_DB.count_documents(
        {"Contents": "Jewelry", "Storage_Type": "Tote"})
    total_computer = Computer_DB.count_documents(
        {"Contents": "Computers", "Storage_Type": "Gaylord"})

    Total_to_process_gay = total_books_gay + \
        total_media_gay + total_sgw_gay + total_jewlery_gay + total_computer
    Total_to_process_tote = total_books_tote + \
        total_media_tote + total_sgw_tote + total_jewlery_tote
    Total = Total_to_process_gay + Total_to_process_tote
    data = {
        'total_gay': Total_to_process_gay,
        'total_totes': Total_to_process_tote,
        'total': Total,
        'totalsgw': total_sgw_gay + total_sgw_tote,
        'sgw_totes': total_sgw_tote,
        'sgw_gay': total_sgw_gay,
        'totaljewl': total_jewlery_gay + total_jewlery_tote,
        'jewl_gay': total_jewlery_gay,
        'jewl_totes': total_jewlery_tote,
        'totalmedia': total_media_tote + total_media_gay,
        'media_gay': total_media_gay,
        'media_totes': total_media_tote,
        'totalbooks': total_books_tote + total_books_gay,
        'books_gay': total_books_gay,
        'books_totes': total_books_tote,
        'totalcomputers': total_computer

    }
    return render(request, 'stats_main.html', data)


def tools(request):

    return render(request, 'tools.html')

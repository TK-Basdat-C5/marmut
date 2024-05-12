from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection as conn
from django.http import (HttpResponse, HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random
import sqlite3
import uuid


def show_landingpage(request):
    context = {
        "is_logged_in": False
    }
    return render(request, "landing.html", context)

def login(request):
    context = {}
    return render(request, "login.html", context)

@csrf_exempt
def register(request):
    context = {
        "is_logged_in": False
    }
    return render(request, 'register.html')

@csrf_exempt
def register_label(request):
    context = {
        "is_logged_in": False
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        random_id = str(uuid.uuid4())

        with conn.cursor() as cursor:
            cursor.execute('set search_path to marmut')
            cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
            hak_cipta = cursor.fetchall()
            random_hak_cipta = str(random.choice(hak_cipta)[0])
            try: 
                cursor.execute(f"INSERT INTO LABEL(id, nama, email, password, kontak, id_pemilik_hak_cipta) values ('{random_id}', '{nama}', '{email}', '{password}', '{kontak}', '{random_hak_cipta}')")
            except Exception as e:
                msg = str(e).split('\n')[0]
                print(msg)
                return render(request, "register_label.html")

        return redirect('authentication:login')
    
    return render(request, "register_label.html", context)

@csrf_exempt
def register_pengguna(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        if(gender) == ('Laki-laki'):
            no_gender = 1;
        else:
            no_gender = 0;
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')
        if len(roles) == 0:
            verified = False
        else:
            verified = True
        with conn.cursor() as cursor:
            try:
                cursor.execute("set search_path to marmut")
                cursor.execute(f"INSERT INTO AKUN(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) values ('{email}', '{password}', '{nama}', '{no_gender}', '{tempat_lahir}', '{tanggal_lahir}', '{verified}', '{kota_asal}')")
                for i in roles:
                    if i == "Podcaster":
                        cursor.execute(f"INSERT INTO PODCASTER(email) values ('{email}')")
                    elif i == "Artist":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id_random = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO ARTIST(id, email_akun, id_pemilik_hak_cipta) values ('{id_random}', '{email}', '{random_hak_cipta}')")
                    elif i == "Songwriter":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id_random = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO SONGWRITER(id, email_akun, id_pemilik_hak_cipta) values ('{id_random}', '{email}', '{random_hak_cipta}')")
            except Exception as e:
                msg = str(e).split('\n')[0]
                return render(request, "register_pengguna.html")

            context = {
                "is_logged_in": False
            }
            return redirect('authentication:login')

    
    context = {
        "is_logged_in": False
    }
    return render(request, "register_pengguna.html", context)

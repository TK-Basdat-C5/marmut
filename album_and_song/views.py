import time
import datetime
from django.shortcuts import render
from django.contrib import messages
from django.db import connection as conn
from django.http import (HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils.query import query
from authentication.views import get_all_credential
import random
import sqlite3
import uuid

@csrf_exempt
def create_album(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)
    
    if "Artist" not in roles and "Songwriter" not in roles:
        return redirect('authentication:dashboard')
    
    if request.method == "POST":
        judul_album = request.POST.get('judul')
        label_id = request.POST.get('label')
        random_id_album = str(uuid.uuid4())
        
        with conn.cursor() as cursor:
            cursor.execute('set search_path to marmut')
            cursor.execute(f"INSERT INTO ALBUM (id, judul, jumlah_lagu, id_label, total_durasi) values ('{random_id_album}', '{judul_album}', '{0}', '{label_id}', '{0}')")
            cursor.execute('set search_path to public')

        judul_lagu = request.POST.get('judul_lagu')
        artist_id = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriters')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        random_id_konten = str(uuid.uuid4())

        current_date = datetime.datetime.now()
        tahun = current_date.year
        
        with conn.cursor() as cursor:
            cursor.execute('set search_path to marmut')
            cursor.execute(f"INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) values ('{random_id_konten}', '{judul_lagu}', '{current_date}', '{tahun}', '{durasi}')")
            if "Artist" in roles:
                cursor.execute(f"SELECT id FROM ARTIST WHERE email_akun = '{email}'")
                artist_id = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) values ('{random_id_konten}', '{artist_id}', '{random_id_album}', '{0}', '{0}')")
            for genre in genres:
                cursor.execute(f"INSERT INTO GENRE (id_konten, genre) values ('{random_id_konten}', '{genre}')")
            for songwriter_id in songwriters:
                cursor.execute(f"INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) values ('{songwriter_id}', '{random_id_konten}')")
            if "Songwriter" in roles:
                songwriter_id = query(f"SELECT S.id FROM AKUN Ak, SONGWRITER S WHERE email = '{email}' AND S.email_akun = Ak.email")
                cursor.execute('set search_path to marmut')
                cursor.execute(f"INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) values ('{songwriter_id[0][0]}', '{random_id_konten}')")
            cursor.execute('set search_path to public')

        return redirect('album_and_song:detail_album', random_id_album)
    else:
        labels = query("SELECT id, nama FROM LABEL ORDER BY nama ASC")
        artists = query("SELECT Ar.id, Ak.nama FROM ARTIST Ar, AKUN Ak WHERE Ar.email_akun = Ak.email ORDER BY Ak.nama ASC")
        songwriters = query("SELECT S.id, A.nama FROM SONGWRITER S, AKUN A WHERE S.email_akun = A.email")
        genres = query("SELECT DISTINCT genre FROM GENRE ORDER BY genre ASC")
        user_artist = query(f"SELECT Ar.idFROM AKUN Ak, ARTIST Ar WHERE email = '{email}' AND Ar.email_akun = Ak.email")
        user_songwriter = query(f"SELECT S.id FROM AKUN Ak, SONGWRITER S WHERE email = '{email}' AND S.email_akun = Ak.email")

        context = {
            'labels': labels,
            'artists': artists,
            'songwriters': songwriters,
            'genres': genres,
            'roles': roles,
            'user_artist': user_artist,
            'user_songwriter': user_songwriter,
            'is_logged_in': is_logged_in,
            'role': role,
            'is_premium': is_premium
        }

        return render(request, 'create_album.html', context)

def add_song(request, id_album):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if "Artist" not in roles and "Songwriter" not in roles:
        return redirect('authentication:dashboard')
    
    if request.method == "POST":
        judul_lagu = request.POST.get('judul_lagu')
        artist_id = request.POST.get('artist')
        songwriters = request.POST.getlist('songwriters')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        random_id_konten = str(uuid.uuid4())

        current_date = datetime.datetime.now()
        tahun = current_date.year
        
        with conn.cursor() as cursor:
            cursor.execute('set search_path to marmut')
            cursor.execute(f"INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) values ('{random_id_konten}', '{judul_lagu}', '{current_date}', '{tahun}', '{durasi}')")
            cursor.execute(f"INSERT INTO SONG (id_konten, id_artist, id_album, total_play, total_download) values ('{random_id_konten}', '{artist_id}', '{id_album}', '{0}', '{0}')")
            for genre in genres:
                cursor.execute(f"INSERT INTO GENRE (id_konten, genre) values ('{random_id_konten}', '{genre}')")
            for songwriter_id in songwriters:
                cursor.execute(f"INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) values ('{songwriter_id}', '{random_id_konten}')")
            if "Songwriter" in roles:
                songwriter_id = query(f"SELECT S.id FROM AKUN Ak, SONGWRITER S WHERE email = '{email}' AND S.email_akun = Ak.email")
                cursor.execute(f"INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song) values ('{songwriter_id[0][0]}', '{random_id_konten}')")
            cursor.execute('set search_path to public')

        return redirect('album_and_song:detail_album', id_album)
    else:
        artists = query("SELECT Ar.id, Ak.nama FROM ARTIST Ar, AKUN Ak WHERE Ar.email_akun = Ak.email ORDER BY Ak.nama ASC")
        songwriters = query("SELECT S.id, A.nama FROM SONGWRITER S, AKUN A WHERE S.email_akun = A.email")
        genres = query("SELECT DISTINCT genre FROM GENRE ORDER BY genre ASC")
        user_artist = query(f"SELECT Ar.idFROM AKUN Ak, ARTIST Ar WHERE email = '{email}' AND Ar.email_akun = Ak.email")
        user_songwriter = query(f"SELECT S.id FROM AKUN Ak, SONGWRITER S WHERE email = '{email}' AND S.email_akun = Ak.email")

        context = {
            'artists': artists,
            'songwriters': songwriters,
            'genres': genres,
            'roles': roles,
            'user_artist': user_artist,
            'user_songwriter': user_songwriter,
            'is_logged_in': is_logged_in,
            'role': role,
            'is_premium': is_premium,
            'id_album': id_album
        }

        return render(request, 'create_lagu.html', context)
    
def list_album(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if role == "pengguna" and "Artist" not in roles and "Songwriter" not in roles:
        return redirect('authentication:dashboard')
    
    if role == "label":
        albums = query(
        f"""
            SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
            FROM ALBUM A, LABEL L
            WHERE A.id_label = L.id AND L.email = '{email}'
            ORDER BY A.judul ASC
        """
        )
    else:
        album_artist = query(
        f"""
            SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
            FROM ALBUM A, LABEL L, SONG S, ARTIST Ar, AKUN Ak
            WHERE A.id_label = L.id AND A.id = S.id_album AND
                S.id_artist = Ar.id AND Ar.email_akun = Ak.email
                AND Ak.email = '{email}'
            ORDER BY A.judul ASC
        """
        )

        album_songwriter = query(
        f"""
            SELECT A.judul, L.nama AS label, A.jumlah_lagu, A.total_durasi, A.id
            FROM ALBUM A, LABEL L, SONG S, SONGWRITER So, SONGWRITER_WRITE_SONG SW, AKUN Ak
            WHERE A.id_label = L.id AND A.id = S.id_album AND S.id_konten = SW.id_song AND
                SW.id_songwriter = So.id AND So.email_akun = Ak.email
                AND Ak.email = '{email}'
            ORDER BY A.judul ASC
        """
        )
        
        albums = set(album_artist + album_songwriter)

    context = {
            'role': role,
            'roles': roles,
            'is_logged_in': is_logged_in,
            'is_premium': is_premium,
            'albums': albums
        }
    return render(request, 'list_album.html', context)

def detail_album(request, id_album):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if role == "pengguna" and "Artist" not in roles and "Songwriter" not in roles:
        return redirect('authentication:dashboard')

        
    album_details = query(f"SELECT judul FROM ALBUM WHERE id = '{id_album}'")
    songs = query(f"SELECT S.id_konten, K.judul, K.durasi, S.total_play, S.total_download FROM SONG S, KONTEN K WHERE S.id_album = '{id_album}' AND S.id_konten = K.id")

    context = {
        'role': role,
        'roles': roles,
        'is_premium': is_premium,
        'is_logged_in': is_logged_in,
        'judul_album': album_details[0][0],
        'id_album': id_album,
        'songs': songs,
    }

    return render(request, 'detail_album.html', context)

def list_royalty(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if role == "pengguna" and "Artist" not in roles and "Songwriter" not in roles or role == "label":
        return redirect('authentication:dashboard')

    if role == "label":
        royalties = query(
            f"""
            SELECT K.judul AS song_title, A.judul AS album_title, S.total_play, S.total_download, P.rate_royalti * S.total_play AS total_royalty
            FROM KONTEN K, SONG S, ALBUM A, LABEL L, PEMILIK_HAK_CIPTA P
            WHERE K.id = S.id_konten AND S.id_album = A.id AND A.id_label = L.id AND L.id_pemilik_hak_cipta = P.id AND L.email = '{email}'
            """
        )
    else:
        royalties = query(
            f"""
            SELECT K.judul AS song_title, A.judul AS album_title, S.total_play, S.total_download, P.rate_royalti * S.total_play AS total_royalty
            FROM KONTEN K, SONG S, ALBUM A, Artist Ar, PEMILIK_HAK_CIPTA P
            WHERE K.id = S.id_konten AND S.id_artist = Ar.id AND S.id_album = A.id AND Ar.id_pemilik_hak_cipta = P.id AND Ar.email_akun = '{email}'
            UNION
            SELECT K.judul AS song_title, A.judul AS album_title, S.total_play, S.total_download, P.rate_royalti * S.total_play AS total_royalty
            FROM KONTEN K, SONG S, ALBUM A, SONGWRITER So, SONGWRITER_WRITE_SONG SW, PEMILIK_HAK_CIPTA P
            WHERE K.id = S.id_konten AND S.id_album = A.id AND SW.id_songwriter = So.id AND SW.id_song = S.id_konten AND So.id_pemilik_hak_cipta = P.id AND So.email_akun = '{email}'
            """
        )

    context = {
        'role': role,
        'roles': roles,
        'is_premium': is_premium,
        'is_logged_in': is_logged_in,
        'royalties': royalties
    }
    return render(request, 'list_royalty.html', context)

def delete_song(request, id_album, id_song):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if role == "pengguna" and "Artist" not in roles and "Songwriter" not in roles or role == "label":
        return redirect('authentication:dashboard')
    
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"DELETE FROM SONG WHERE id_konten = '{id_song}'")
        cursor.execute(f"DELETE FROM KONTEN WHERE id = '{id_song}'")
        cursor.execute("set search_path to public")

    if query(f"SELECT count(*) FROM SONG S, ALBUM A WHERE S.id_album = A.id AND A.id = '{id_album}'")[0][0] != 0:
        return redirect('album_and_song:detail_album', id_album)
    else:
        return redirect('album_and_song:delete_album', id_album)

def delete_album(request, id_album):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email, role, roles, is_premium, is_logged_in = get_all_credential(request)

    if role == "pengguna" and "Artist" not in roles and "Songwriter" not in roles or role == "label":
        return redirect('authentication:dashboard')
    
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut")
        cursor.execute(f"DELETE FROM ALBUM WHERE id = '{id_album}'")
        cursor.execute("set search_path to public")

    return redirect('album_and_song:list_album')

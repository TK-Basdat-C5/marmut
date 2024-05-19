from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection as conn
from django.http import (HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from authentication.views import *
from utils.query import query
import random
import sqlite3
import uuid
import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.db import DatabaseError

logger = logging.getLogger(__name__)


def index(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    context = {
        'email': email,
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
    }
    
    query_playlists = query(f"SELECT * FROM user_playlist WHERE email_pembuat = '{email}'")
    
    playlists = []  # Initialize an empty list to store playlist data
    for playlist_data in query_playlists:
        id_user_playlist = playlist_data[1]
        judul = playlist_data[2]
        deskripsi = playlist_data[3]
        jumlah_lagu = playlist_data[4]
        tanggal_dibuat = playlist_data[5]
        tanggal_dibuat_formated = tanggal_dibuat.strftime('%d/%m/%y')
        id_playlist = playlist_data[6]
        total_durasi = playlist_data[7]
        
        # Create a dictionary for each playlist
        playlist = {
            'id_user_playlist': id_user_playlist,
            'judul': judul,
            'deskripsi': deskripsi,
            'jumlah_lagu': jumlah_lagu,
            'tanggal_dibuat': tanggal_dibuat_formated,
            'id': id_playlist,
            'total_durasi': total_durasi,
        }
        
        playlists.append(playlist)  
            
        context['playlists'] = playlists    
        
        
    if playlists:
        return render(request, 'kelola_playlist.html', context)
    else:
        return render(request, 'playlist_kosong.html', context)

def playlist_form(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)
    
    context = {
        'email': email,
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
    }
    
    return render(request, 'playlist_form.html', context)

def update_playlist(request, id_user_playlist):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)
    
    context = {
        'email': email,
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
    }
    
    playlist_data = query(f"SELECT * FROM user_playlist WHERE id_user_playlist = '{id_user_playlist}' ")
    
    if not playlist_data:
        return redirect('some_error_page')  # Handle case where playlist is not found

    id_user_playlist = playlist_data[0][1]
    judul = playlist_data[0][2]
    deskripsi = playlist_data[0][3]
    jumlah_lagu = playlist_data[0][4]
    creation_date = playlist_data[0][5]
    tanggal_dibuat_formatted = creation_date.strftime('%d/%m/%y')
    id_playlist = playlist_data[0][6]
    total_durasi = playlist_data[0][7]
    
    playlist = {
        'id_user_playlist': id_user_playlist,
        'judul': judul,
        'deskripsi': deskripsi,
        'jumlah_lagu': jumlah_lagu,
        'tanggal_dibuat': tanggal_dibuat_formatted,
        'id': id_playlist,
        'total_durasi': total_durasi,
    }
    
    context.update(playlist)
    
    return render(request, 'update_playlist.html', context)


def playlist_details(request, id_playlist):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    
    playlist_data = query(f"SELECT * FROM user_playlist WHERE id_playlist = '{id_playlist}' ")
        

    id_user_playlist = playlist_data[0][1]
    judul = playlist_data[0][2]
    deskripsi = playlist_data[0][3]
    jumlah_lagu = playlist_data[0][4]
    creation_date = playlist_data[0][5]
    tanggal_dibuat_formatted = creation_date.strftime('%d/%m/%y')
    id_playlist = playlist_data[0][6]
    total_durasi = playlist_data[0][7]
    
    playlist = {
        'id_user_playlist': id_user_playlist,
        'judul': judul,
        'deskripsi': deskripsi,
        'jumlah_lagu': jumlah_lagu,
        'tanggal_dibuat': tanggal_dibuat_formatted,
        'id': id_playlist,
        'total_durasi': durasi_calcultaor(total_durasi),
    }

    songs = query(f"SELECT id_song FROM playlist_song WHERE id_playlist = '{id_playlist}'")


    konten_data = {}

    for song in songs:
        song_id = song[0]
        artist_details = query(f"SELECT a.nama FROM SONG s JOIN ARTIST ar ON s.id_artist = ar.id JOIN AKUN a ON ar.email_akun = a.email WHERE s.id_konten = '{song_id}'")

        konten_details = query(f"SELECT * FROM KONTEN WHERE id = '{song_id}'")
        
        for konten in konten_details:
            konten_data[song_id] = {
                'id_konten': konten[0],
                'judul_konten': konten[1],
                'tanggal_rilis_konten': konten[2],
                'tahun_konten': konten[3],
                'total_durasi_konten': durasi_calcultaor(konten[4]),
                'nama_artis': artist_details[0][0],
            }
            

    query_nama = query(f"SELECT nama FROM AKUN WHERE email = '{email}'")
    
    context = {
        'nama' : query_nama[0][0],
        'playlist': playlist,
        'konten': konten_data,
        'email': email,
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
    }

    
    # Render HTML template for normal requests
    return render(request, 'playlist_details.html', context)

def durasi_calcultaor(total_durasi):
    hours = total_durasi // 60
    minutes = total_durasi % 60
    
    return(f"{hours} jam {minutes} menit")

def view_add_song(request, id_playlist):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)
        
    query_songs = query(f"SELECT k.id, k.judul, a2.nama "
                    f"FROM SONG s "
                    f"JOIN KONTEN k ON s.id_konten = k.id "
                    f"JOIN ARTIST a ON s.id_artist = a.id "
                    f"JOIN AKUN a2 ON a.email_akun = a2.email")
    
    songs = []
    

    for song in query_songs:
        songs.append({
            'id_konten': song[0], 
            'judul_konten': song[1],
            'nama_artis': song[2],
        })
        
    query_playlist = query(f"SELECT * FROM user_playlist WHERE id_user_playlist = '{id_playlist}'")
    
    id_playlist_add = query_playlist[0][6]
    
    context = {
        'email': email,
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'id_playlist': id_playlist_add,
        'songs': songs,
     }
    
            
    return render(request, 'add_song_playlist.html', context)


def add_song(request, id_playlist):
    if request.method == 'POST':
        id_konten = request.POST.get('id_konten')
        # Execute the SQL query to insert the song into the playlist
        printan = query(f"INSERT INTO playlist_song (id_playlist, id_song) VALUES ('{id_playlist}', '{id_konten}')")
        if isinstance(printan, Exception):
            messages.error(request, f"Error occurred: {printan}")
            return HttpResponse(f"Error: {printan}", status=400) 
    return redirect('playlist:playlist_details', id_playlist=id_playlist)

def delete_song(request):
    if request.method == 'POST':
        id_playlist = request.POST.get('id_playlist')
        id_konten = request.POST.get('id_konten')
        query(f"DELETE FROM playlist_song WHERE id_playlist = '{id_playlist}' AND id_song = '{id_konten}'")    
        response_data = {
            'message': 'Song deleted successfully.'
            }
        return JsonResponse(response_data)

def add_playlist(request):
    if request.method == 'POST':
        email = request.session["email"]
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        id_user_playlist = uuid.uuid4()
        id_playlist = uuid.uuid4()
        query(f"INSERT INTO playlist (id) VALUES ('{id_playlist}')")
        query(f"INSERT INTO user_playlist (id_user_playlist, email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) VALUES ('{id_user_playlist}', '{email}', '{judul}', '{deskripsi}', 0, CURRENT_TIMESTAMP, '{id_playlist}', 0)")
        return redirect('playlist:kelola_playlist')
    
def delete_playlist(request): 
    if request.method == 'POST':
        id_playlist = request.POST.get('id_playlist')
        query(f"DELETE FROM playlist WHERE id = '{id_playlist}'")
        query(f"DELETE FROM user_playlist WHERE id_playlist = '{id_playlist}'")
        query(f"DELETE FROM playlist_song WHERE id_playlist = '{id_playlist}'")
        response_data = {
            'message': 'Playlist deleted successfully.'
            }
        return JsonResponse(response_data)

def ubah_playlist(request, id_playlist):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        query(f"UPDATE user_playlist SET judul = '{judul}', deskripsi = '{deskripsi}' WHERE id_user_playlist = '{id_playlist}'")
        return redirect('playlist:kelola_playlist')
    
def play_user_playlist(request, id_user_playlist):
    id_playlist = None  # Assign a default value
    
    if request.method == 'POST':
        email = request.session.get('email')
        if not email:
            # Handle case where the user is not logged in
            return redirect('login')
        
        playlist_data = query(f"SELECT * FROM user_playlist WHERE id_user_playlist = '{id_user_playlist}'")
    
        id_playlist = playlist_data[0][6]

        with conn.cursor() as cursor:
            # Create entry in AKUN_PLAY_USER_PLAYLIST
            cursor.execute("SET SEARCH_PATH TO 'marmut'")
            cursor.execute("""
                INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu)
                SELECT %s, id_user_playlist, email_pembuat, NOW() AT TIME ZONE 'Asia/Jakarta'
                FROM USER_PLAYLIST
                WHERE id_user_playlist = %s
            """, [email, id_user_playlist])

            # Get all songs in the playlist
            cursor.execute("""
                SELECT id_song
                FROM PLAYLIST_SONG
                WHERE id_playlist = %s
            """, [id_playlist])
            songs = cursor.fetchall()

            # Create entries in AKUN_PLAY_SONG for each song in the playlist
            for song in songs:
                cursor.execute("""
                    INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
                    VALUES (%s, %s, NOW() AT TIME ZONE 'Asia/Jakarta')
                """, [email, song[0]])
            cursor.execute("SET SEARCH_PATH TO 'public'")

    return redirect('playlist:playlist_details', id_playlist=id_playlist)

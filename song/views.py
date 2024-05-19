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


from django.shortcuts import render

def index(request, song_id):
    
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
    
    # Fetch song details from the database
    with conn.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO 'marmut'")
        cursor.execute(f"SELECT * FROM SONG WHERE id_konten = '{song_id}'")
        song_data = cursor.fetchone()

        if song_data:
            # Fetch content details
            cursor.execute(f"SELECT * FROM KONTEN WHERE id = '{song_data[0]}'")
            konten_data = cursor.fetchone()

            if konten_data:
                judul = konten_data[1]
                tanggal_rilis = konten_data[2]
                tahun = konten_data[3]
                durasi = konten_data[4]
                total_play = song_data[3]
                total_download = song_data[4]

                # Fetch artist name
                cursor.execute("SELECT nama FROM akun INNER JOIN artist ON akun.email = artist.email_akun WHERE artist.id = %s", [song_data[1]])
                artist_data = cursor.fetchone()
                artist = artist_data[0] if artist_data else None

                # Fetch album title
                cursor.execute("SELECT judul FROM ALBUM WHERE id = %s", [song_data[2]])
                album_data = cursor.fetchone()
                album = album_data[0] if album_data else None

                # Format tanggal_rilis as 'DD/MM/YY'
                tanggal_rilis_formatted = tanggal_rilis.strftime('%d/%m/%y') if tanggal_rilis else ''
                
                # Fetch songwriter name
                cursor.execute("""
                    SELECT AKUN.nama
                    FROM SONG
                    INNER JOIN SONGWRITER_WRITE_SONG ON SONG.id_konten = SONGWRITER_WRITE_SONG.id_song
                    INNER JOIN SONGWRITER ON SONGWRITER_WRITE_SONG.id_songwriter = SONGWRITER.id
                    INNER JOIN AKUN ON SONGWRITER.email_akun = AKUN.email
                    WHERE SONG.id_konten = %s
                """, [song_data[0]])
                songwriter_data = cursor.fetchone()
                songwriter = [songwriter_data[0]] if songwriter_data else None                                
                # Fetch genres
                cursor.execute("SELECT genre from genre where id_konten = %s", [song_data[0]])
                genre_data = cursor.fetchone()
                genre = genre_data[0] if genre_data else None
                genres_list = genre.split(',') if genre else []

                # Format the details in the desired format
                cursor.execute("SET SEARCH_PATH TO 'public'")
                song_details = {
                    "judul": judul,
                    "genres": genres_list,
                    "songwriters": songwriter,
                    "artist": artist,
                    "durasi": durasi,
                    "tanggal_rilis": tanggal_rilis_formatted,
                    "tahun": tahun,
                    "total_play": total_play,
                    "total_download": total_download,
                    "album": album,
                    "song_id": song_id
                }
                
                playlists = query(f"SELECT * FROM user_playlist WHERE email_pembuat = '{email}'")
                                
                context.update(song_details)
                context.update({"playlists": playlists})

                # Pass the song details to the template
                return render(request, 'song_details.html',context)

    # Handle the case when song_data is None or konten_data is None
    return render(request, 'error.html', {"error_message": "Song details not found."})





def add_to_playlist(request, song_id):
    if request.method == 'POST':
        # Get the playlist id from the form
        playlist_id = request.POST.get('playlist_id')

        # Get the song details
        with conn.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO 'marmut'")
            cursor.execute(f"SELECT * FROM song WHERE id_konten = '{song_id}'")
            song = cursor.fetchone()
            cursor.execute(f"SELECT * FROM SONG WHERE id_konten = '{song_id}'")
            song_data = cursor.fetchone()

            if song_data:
                # Fetch content details
                cursor.execute(f"SELECT * FROM KONTEN WHERE id = '{song_data[0]}'")
                konten_data = cursor.fetchone()

        durasi = konten_data[4]

        
        # Insert the song into the playlist_song table
        query = f"""
        INSERT INTO playlist_song (id_playlist, id_song)
        VALUES ('{playlist_id}', '{song_id}')
        """
        with conn.cursor() as cursor:
            cursor.execute(query)

        # Update the total duration and song count of the user_playlist
        query = f"""
        UPDATE user_playlist
        SET total_durasi = total_durasi + {durasi}, jumlah_lagu = jumlah_lagu + 1
        WHERE id_user_playlist = '{playlist_id}'
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            cursor.execute("SET SEARCH_PATH TO 'public'")
            
        return JsonResponse({'success': True, 'message': 'Song successfully added to playlist'})



@csrf_exempt
def update_total_play(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        progress = int(data.get('progress', 0))
        song_id = data.get('song_id')  
        if progress > 70:
            with conn.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO 'marmut'")
                cursor.execute("UPDATE song SET total_play = total_play + 1 WHERE id_konten = %s", [song_id])
                cursor.execute("SELECT total_play FROM song WHERE id_konten = %s", [song_id])
                new_total_play = cursor.fetchone()[0]

                email_pemain = data.get('email')

                # Insert a new entry to AKUN_PLAY_SONG
                cursor.execute("INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu) VALUES (%s, %s, NOW() AT TIME ZONE 'Asia/Jakarta')", [email_pemain, song_id])

                cursor.execute("SET SEARCH_PATH TO 'public'")
            return JsonResponse({'success': True, 'new_total_play': new_total_play})


@csrf_exempt
def download_song(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        song_id = data.get('song_id')  # assuming the song_id is sent in the POST data

        # Get the user's email from the session
        email = request.session['email']

        # Insert the song into the downloaded_song table
        with conn.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO 'marmut'")
            query = f"""
            INSERT INTO downloaded_song (id_song, email_downloader)
            VALUES ('{song_id}', '{email}')
            """
            cursor.execute(query)
            
            cursor.execute('SET SEARCH_PATH TO public')

        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['POST']) 

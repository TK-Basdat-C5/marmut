from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from authentication.views import check_premium, get_role_pengguna
from subscription.models import DOWNLOADED_SONG, SONG, ARTIST
from utils.query import query


def downloaded_songs(request):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    query_charts = query(f"SELECT * FROM chart")
    all_chart = []
    for i in query_charts:
        chart = []
        for y in i:
            chart.append(str(y))
        all_chart.append(chart)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'charts': all_chart
    }

    judul_downloaded_songs = []
    query_downloaded_songs = query(f"""
        SELECT ds.id_song, k.judul, a.nama
        FROM downloaded_song ds
        JOIN konten k ON ds.id_song = k.id
        JOIN song s ON k.id = s.id_konten
        JOIN artist art ON s.id_artist = art.id
        JOIN akun a ON art.email_akun = a.email
        WHERE ds.email_downloader = '{email}'
    """)

    for song in query_downloaded_songs:
        judul_downloaded_songs.append({
            'id_song': song[0],
            'judul': song[1],
            'nama_artis': song[2]
        })

    context = {'downloaded_songs': judul_downloaded_songs}
    return render(request, 'downloaded_songs.html', context)


def delete_downloaded_song(request, id_song):
    if "email" not in request.session:
        return redirect('authentication:login')
    
    email = request.session["email"]
    role = request.session["role"]
    roles = get_role_pengguna(email)

    query_charts = query(f"SELECT * FROM chart")
    all_chart = []
    for i in query_charts:
        chart = []
        for y in i:
            chart.append(str(y))
        all_chart.append(chart)

    context = {
        'is_logged_in': True,
        'role': role,
        'roles': roles,
        'is_premium': check_premium(email),
        'charts': all_chart
    }

    email = request.user.email  # Asumsikan user sudah login dan email tersedia di request.user.email
    query_song_title = query(f"""
        SELECT k.judul
        FROM konten k
        JOIN song s ON k.id = s.id_konten
        WHERE s.id_konten = '{id_song}'
    """)

    if query_song_title:
        judul_lagu = query_song_title[0][0]
        query(f"""
            DELETE FROM downloaded_song
            WHERE id_song = '{id_song}' AND email_downloader = '{email}'
        """)
        messages.success(request, f'Berhasil menghapus lagu dengan judul "{judul_lagu}"')
    else:
        messages.error(request, 'Lagu tidak ditemukan atau Anda tidak memiliki izin untuk menghapusnya.')

    return redirect(reverse('downloaded_songs'))
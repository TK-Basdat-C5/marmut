from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', landing, name='landing'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/label', register_label, name='register-label'),
    path('register/pengguna', register_pengguna, name='register-pengguna'),
    path('dashboard/', dashboard, name='dashboard'),
    path('podcast/', podcast, name='podcast'),
    path('chart-detail/', detail_chart, name='chart-list'),
    path('chart-list/', daftar_chart, name='chart-list'),
    path('create-episode/', create_episode, name='create-episode'),
    path('create-podcast/', create_podcast, name='create-podcast'),
    path('list-podcast/', daftar_podcast, name='list-podcast'),
    path('daftar-episode/', daftar_episode, name='daftar-episode'),
    path ('add_playlist/', add_playlist, name='add_playlist'),
    path('add_song_playlist/', add_song_playlist, name='add_song_playlist'),
    path('add_song/', add_song, name='add_song'),
    path('new_userplaylist/', new_userplaylist, name='new_userplaylist'),
    path('playlistform/', playlistform, name='playlistform'),
    path('user_playlist_details/' , user_playlist_details, name='user_playlist_details'),
    path('user_playlistDetails/', user_playlistDetails, name='user_playlistDetails'),
    path('play_song/', play_song, name='play_song'),
]

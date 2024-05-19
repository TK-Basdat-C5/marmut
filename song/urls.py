from django.urls import path
from song.views import *

app_name = 'song'

urlpatterns = [
    path('play_song/<uuid:song_id>/', index, name='play_song'),
    path('add_to_playlist/<uuid:song_id>/', add_to_playlist, name='add_to_playlist'),
    path('update_total_play/', update_total_play, name='update_total_play'),
    path('download_song/', download_song, name='download_song'),
]

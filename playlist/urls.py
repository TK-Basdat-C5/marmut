from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('kelola_playlist/', index, name='kelola_playlist'),
    path('playlist_form/', playlist_form, name='playlist_form'),
    path('update_playlist/<uuid:id_user_playlist>/', update_playlist, name='update_playlist'),
    path('playlist_details/<uuid:id_playlist>/', playlist_details, name='playlist_details'),
    path('add_song/<uuid:id_playlist>/', add_song, name='add_song'),
    path('view_add_song/<uuid:id_playlist>/', view_add_song, name='view_song'),
    path('delete_song/', delete_song, name='delete_song'),
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('delete_playlist/', delete_playlist, name='delete_playlist'),
    path('ubah_playlist/<uuid:id_playlist>/', ubah_playlist, name='ubah_playlist'),
    path('play_user_playlist/<uuid:id_user_playlist>/', play_user_playlist, name='play_user_playlist')
]

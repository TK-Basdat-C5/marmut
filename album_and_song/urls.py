from django.urls import path
from album_and_song.views import *

app_name = 'album_and_song'

urlpatterns = [
    path('albums/', list_album, name='list_album'),
    path('album/create/', create_album, name='create_album'),
    path('album/<id_album>/', detail_album , name='detail_album'),
    path('album/<id_album>/add-song/', add_song, name="add_song"),
    path('album/<id_album>/delete', delete_album, name='delete_album'),
    path('album/<id_album>/delete/<id_song>', delete_song, name='delete_song'),
    path('royalties/', list_royalty, name='list_royalty'),
]
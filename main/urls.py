from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path ('add_playlist/', add_playlist, name='add_playlist'),
    path('add_song_playlist/', add_song_playlist, name='add_song_playlist'),
    path('add_song/', add_song, name='add_song'),
    path('new_userplaylist/', new_userplaylist, name='new_userplaylist'),
    path('playlistform/', playlistform, name='playlistform'),
    path('user_playlist_details/' , user_playlist_details, name='user_playlist_details'),
    path('user_playlistDetails/', user_playlistDetails, name='user_playlistDetails'),
    path('play_song/', play_song, name='play_song'),
    path('pembayaran-paket/', pembayaran_paket, name='pembayaran-paket'),
    path('riwayat-transaksi-paket/', riwayat_transaksi_paket, name='riwayat-transaksi-paket'),
    path('downloaded-songs/', downloaded_songs, name= "downloaded-songs"),
    path('langganan-paket/', langganan_paket, name= 'langganan-paket'),
    path('hasil-pencarian/', hasil_pencarian, name= 'hasil-pencarian'), 
]

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
    path('pembayaran-paket/', pembayaran_paket, name='pembayaran-paket'),
    path('riwayat-transaksi-paket/', riwayat_transaksi_paket, name='riwayat-transaksi-paket'),
    path('downloaded-songs/', downloaded_songs, name= "downloaded-songs"),
    path('langganan-paket/', langganan_paket, name= 'langganan-paket'),
    path('hasil-pencarian/', hasil_pencarian, name= 'hasil-pencarian'), 
]
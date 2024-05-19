from django.urls import path
from . import views

app_name = 'downloaded_songs'

urlpatterns = [
    path('', views.downloaded_songs, name='downloaded_songs'),
    path('downloaded_songs/delete/<uuid:id_song>/', views.delete_downloaded_song, name='delete_downloaded_song'),
]

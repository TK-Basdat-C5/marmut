from django.urls import path
from podcast.views import *

app_name = 'podcast'

urlpatterns = [
    path('create-episode/<str:id>/', create_episode, name='create-episode'),
    path('daftar-episode/<str:id>/', daftar_episode, name='daftar-episode'),
    path('podcast/<str:id>/', podcast, name='podcast'),
    path('list-podcast/', daftar_podcast, name='list-podcast'),
    path('delete-podcast/<str:id>/', delete_podcast, name='delete-podcast'),
    path('delete-episode/<str:id>/', delete_episode, name='delete-episode'),
    path('create-podcast/', create_podcast, name='create-podcast'),
    path('get-podcast-list/', get_podcast_list, name='get-podcast-list'),
    path('get-episode-list/<str:id>/', get_episode_list, name='get-episode-list'),
]
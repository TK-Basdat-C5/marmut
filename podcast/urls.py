from django.urls import path
from podcast.views import *

app_name = 'podcast'

urlpatterns = [
    path('', show_landingpage, name='landing-page'),
]
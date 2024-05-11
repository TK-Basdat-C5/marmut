from django.urls import path
from auth.views import *

app_name = 'auth'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/label', register_label, name='register-label'),
    path('register/pengguna', register_pengguna, name='register-pengguna'),
]
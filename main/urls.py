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

]
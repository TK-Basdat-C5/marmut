from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_list, name='subscription_list'),
    path('payment/<str:paket_jenis>/', views.payment, name='payment'), 
    path('transaction-history/', views.transaction_history, name='transaction_history'), 
]
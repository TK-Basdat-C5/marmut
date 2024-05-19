from django.urls import path
from chart.views import *

app_name = 'chart'

urlpatterns = [
    path('chart-detail/<str:id>/<str:tipe>', detail_chart, name='detail-chart'),
    path('chart-list/', daftar_chart, name='chart-list'),
]
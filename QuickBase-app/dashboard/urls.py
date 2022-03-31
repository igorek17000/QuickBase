from django.urls import path
from . import views

urlpatterns = [
    path('overview', views.base, name='overview'),
    path('overview/eur', views.get_dashboard_info_eur, name='overviewEur'),
    path('trades', views.trades, name='trades'),
    path('transactions', views.transactions, name='transactions'),
    path('marche', views.marche, name='marche'),
    path('api/get_total_usd_balance', views.get_total_usd_balance, name='get_total_usd_balance'),
    path('api/get_gain_usd', views.get_gain_usd, name='get_gain_usd'),
    path('api/get_biggest_coin_usd', views.get_biggest_coin_usd, name='get_biggest_coin_usd'),
    path('api/get_smallest_coin_usd', views.get_smallest_coin_usd, name='get_smallest_coin_usd'),
]
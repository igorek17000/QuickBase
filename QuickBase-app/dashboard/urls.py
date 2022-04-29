from django.urls import path
from . import views

urlpatterns = [
    path('overview', views.base, name='overview'),
    path('trades', views.trades, name='trades'),
    path('transactions', views.transactions, name='transactions'),
    path('marche', views.marche, name='marche'),
    path('api/get_total_usd_balance', views.get_total_usd_balance, name='get_total_usd_balance'),
    path('api/get_gain_usd', views.get_gain_usd, name='get_gain_usd'),
    path('api/get_biggest_coin_usd', views.get_biggest_coin_usd, name='get_biggest_coin_usd'),
    path('api/get_smallest_coin_usd', views.get_smallest_coin_usd, name='get_smallest_coin_usd'),
    path('api/get_total_eur_balance', views.get_total_eur_balance, name='get_total_eur_balance'),
    path('api/get_gain_eur', views.get_gain_eur, name='get_gain_eur'),
    path('api/get_biggest_coin_eur', views.get_biggest_coin_eur, name='get_biggest_coin_eur'),
    path('api/get_smallest_coin_eur', views.get_smallest_coin_eur, name='get_smallest_coin_eur'),
    path('api/get_hitorical_balance_usd', views.get_hitorical_balance_usd, name='get_hitorical_balance_usd'),
    path('api/test/<str:value>', views.test_get_data, name='test_get_data'),
    path('api/get_market_history/<str:id>/<str:vs_currency>/<int:days>/<str:interval>', views.get_market_history, name='get_market_history'),
    path('api/get_coins', views.get_coins, name='get_coins'),
    path('api/get_vs_currency/<str:id>', views.get_vs_currency, name='get_vs_currency'),
]
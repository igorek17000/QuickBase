from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='index'),
    path('dashboard/overview', views.base, name='overview'),
    path('dashboard/trades', views.trades, name='trades'),
    path('dashboard/transactions', views.transactions, name='transactions'),
    path('dashboard/marche', views.marche, name='marche'),
]
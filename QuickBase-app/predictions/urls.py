from django.urls import path
from . import views

urlpatterns = [
    path('marches', views.marches, name='marches'),
    path('predict', views.predict, name='predict'),
    path('api/predictData/<str:id>/<str:vs_currency>/<int:days>/<str:interval>/<int:period>/<str:freq>', views.predict_data, name='predict_data'),
    path('api/get_coin_infos/<str:id>/<str:vs_currency>', views.get_coin_infos, name='get_coin_infos'),
]
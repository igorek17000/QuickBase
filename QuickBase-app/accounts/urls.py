from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/myaccount/', views.myaccount, name='myaccount'),
    path('accounts/', include("django.contrib.auth.urls")),
]
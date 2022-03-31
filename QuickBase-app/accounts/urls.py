from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('validation/', views.validation, name='validation'),
    path('recuperation/', views.recuperation, name='recuperation'),
    path('validation/password', views.validationToChangePassword, name='validationToChangePassword'),
    path('changepassword/', views.changePassword, name='changePassword'),
    path('sendcode/', views.sendCode, name='sendcode'),
    path('', include("django.contrib.auth.urls")),
]
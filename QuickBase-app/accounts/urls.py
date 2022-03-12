from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/myaccount/', views.myaccount, name='myaccount'),
    path('accounts/validation/', views.validation, name='validation'),
    path('accounts/recuperation/', views.recuperation, name='recuperation'),
    path('accounts/validationPassword', views.validationToChangePassword, name='validationToChangePassword'),
    path('accounts/changepassword/', views.changePassword, name='changePassword'),
    path('accounts/sendcode/', views.sendCode, name='sendcode'),
    path('accounts/', include("django.contrib.auth.urls")),
]
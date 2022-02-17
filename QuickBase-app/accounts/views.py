from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import logout

def login(request):
    if request.method == 'POST':
        print("in login")
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            print("Logged")
            return redirect('/')
        else:
            print("mdp incorrect")
            return render (request,'registration/login.html', context={'erreur':'Email ou mot de passe incorrect'})
    else:
        return render(request,'registration/login.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email = request.POST['email'])
                return render (request,'registration/signup.html', {'error':'Email déjà utilisée!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username =request.POST['username'],email=request.POST['email'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('/')
        else:
            return render (request,'registration/signup.html', {'error':'Mots de passe différents!'})
    else:
        return render(request,'registration/signup.html')

def myaccount(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'accounts/account.html')
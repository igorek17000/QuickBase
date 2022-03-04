from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import auth
from django.shortcuts import render
from accounts.models import APIKey
from django.contrib.auth.hashers import check_password

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
            return render (request,'registration/login.html', context={'status':0})
    else:
        return render(request,'registration/login.html', context={'status':1})

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email = request.POST['email'])
                return render (request,'registration/signup.html', {'status' : 'Email déjà utilisée!'})
            except User.DoesNotExist:
                try:
                    User.objects.get(username = request.POST['username'])
                    return render (request,'registration/signup.html', {'status':"Nom d'utilisateur déjà utilisé!"})
                except User.DoesNotExist:
                    user = User.objects.create_user(username =request.POST['username'],email=request.POST['email'],password=request.POST['password1'])
                    auth.login(request,user)
                    return redirect('/')
        else:
            return render (request,'registration/signup.html', {'status':'Mots de passe différents!'})
    else:
        return render(request,'registration/signup.html', {'status':0})

def myaccount(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        if request.method == "POST":
            try:
                APIKey.objects.get(user = request.user,exchange = 'FTX')
                APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
                FTXKey = APIFTX[0].apiKey
                FTXSecret = APIFTX[0].apiKeySecret
            except APIKey.DoesNotExist:
                FTXKey = 0
                FTXSecret = 0
            try:
                username= request.user.username
                email= request.user.email
            except:
                username = "nom d'utilisateur"
                email = "Email"

            if check_password(request.POST['password3'], request.user.password):
                try:
                    if request.POST['password1']:
                        if request.POST['password1'] == request.POST['password2']:
                            User.objects.filter(username=request.user.username,email=request.user.email).update(username=request.POST['username'],email = request.POST['email'])
                            U = User.objects.get(username=request.user.username)
                            U.set_password(request.POST['password1'])
                            U.save()
                        else :
                            print("mdp différents")
                            return render (request,'accounts/account.html', {'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Mots de passe différents!','status':1})
                except:
                    return render (request,'accounts/account.html', {'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Impossible de modifier les infos!','status':1})
                
                if request.POST['APIKey'] or request.POST['APISecret']:
                    try:
                        APIKey.objects.get(user = request.user)
                        APIKey.objects.get(exchange = 'FTX')
                        APIKey.objects.filter(user=request.user,exchange = 'FTX').update(apiKey=request.POST['APIKey'],apiKeySecret = request.POST['APISecret'])
                        return render (request,'accounts/account.html', {'success':'Clé API modifiée','status':0})
                    except APIKey.DoesNotExist:
                        try:
                            apiKey = APIKey(exchange = 'FTX',apiKey=request.POST['APIKey'],apiKeySecret = request.POST['APISecret'],user=request.user)
                            apiKey.save()
                            #return redirect('overview')
                            return render (request,'accounts/account.html',{'success':'Clé API ajouté','status':0})
                        except:
                            return render (request, 'accounts/account.html',{'error':'Erreur lors de la clé API','status':1})

                else:
                    return render (request,'accounts/account.html',{'success':'Informations modifées','status':0})
            else:
                return render(request, 'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Mot de passe incorrect','status':1})

        else:
            try:
                APIKey.objects.get(user = request.user,exchange = 'FTX')
                APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
                FTXKey = APIFTX[0].apiKey
                FTXSecret = APIFTX[0].apiKeySecret
            except APIKey.DoesNotExist:
                FTXKey = 0
                FTXSecret = 0

            try:
                username= request.user.username
                email= request.user.email
            except:
                username = "nom d'utilisateur"
                email = "Email"

            return render(request, 'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'status':0})


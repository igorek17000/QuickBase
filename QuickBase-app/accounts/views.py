from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import auth
from django.shortcuts import render
from accounts.models import APIKey
from django.contrib.auth.hashers import check_password
import random

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
                    request.session['username'] = request.POST['username']
                    request.session['email'] = request.POST['email']
                    request.session['password'] = request.POST['password1']
                    request.session['code'] = random.randrange(1000, 9999)
                    mailsent = sendCode(request.session['username'],request.session['email'],request.session['code'])  
                    if mailsent:
                        return render(request,'registration/validation.html', {'status':0})
                    else:
                        return render (request,'registration/signup.html', {'status':"Erreur serveur!"})
        else:
            return render (request,'registration/signup.html', {'status':"Mot de passe différent!"})
    else:
        return render(request,'registration/signup.html', {'status':0})

def validation(request):
    if request.method == "POST": 
         
        if(request.POST['code'] == str(request.session['code'])):
            try:
                user = User.objects.create_user(username =request.session['username'],email=request.session['email'],password=request.session['password'])
                auth.login(request,user)
                return redirect('/')
            except:
                return render(request,'registration/validation.html', {'status':1,'error':'Erreur serveur'})
        else:
            return render(request,'registration/validation.html', {'status':1,'error':'Code invalide'})
    else:
        return render(request,'registration/validation.html', {'status':0})

def validationToChangePassword(request):
    if request.method == "POST": 
         
        if(request.POST['code'] == str(request.session['code'])):
            return render(request,'registration/changePassword.html')
        else:
            return render(request,'registration/validationToChangePassword.html', {'status':1,'error':'Code invalide'})
    else:
        return render(request,'registration/validationToChangePassword.html', {'status':0})
    

def myaccount(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        if request.method == "POST":
            if check_password(request.POST['password3'], request.user.password):
                try:
                    if request.POST['password1']:
                        if request.POST['password1'] == request.POST['password2']:
                            User.objects.filter(username=request.user.username,email=request.user.email).update(username=request.POST['username'],email = request.POST['email'])
                            U = User.objects.get(username=request.user.username)
                            U.set_password(request.POST['password1'])
                            U.save()
                        else :
                            FTXKey,FTXSecret,username,email = ReloadInfo(request)
                     
                            return render (request,'accounts/account.html', {'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Mots de passe différents!','status':1})
                    else:
                        User.objects.filter(username=request.user.username,email=request.user.email).update(username=request.POST['username'],email = request.POST['email'])
                except:
                    FTXKey,FTXSecret,username,email = ReloadInfo(request)
                    return render (request,'accounts/account.html', {'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Impossible de modifier les infos!','status':1})
                
                if request.POST['APIKey'] or request.POST['APISecret']:
                    try:
                        APIKey.objects.get(user = request.user)
                        APIKey.objects.get(exchange = 'FTX')
                        APIKey.objects.filter(user=request.user,exchange = 'FTX').update(apiKey=request.POST['APIKey'],apiKeySecret = request.POST['APISecret'])
                        FTXKey,FTXSecret,username,email = ReloadInfo(request)
                        return render (request,'accounts/account.html', {'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'success':'Clé API modifiée','status':0})
                    except APIKey.DoesNotExist:
                        try:
                            apiKey = APIKey(exchange = 'FTX',apiKey=request.POST['APIKey'],apiKeySecret = request.POST['APISecret'],user=request.user)
                            apiKey.save()

                            FTXKey,FTXSecret,username,email = ReloadInfo(request)
                            return render (request,'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'success':'Clé API ajouté','status':0})
                        except:
                            FTXKey,FTXSecret,username,email = ReloadInfo(request)
                            return render (request, 'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Erreur lors de la clé API','status':1})

                else:
                    FTXKey,FTXSecret,username,email = ReloadInfo(request)
                    return render (request,'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'success':'Informations modifées','status':0})
            else:
                FTXKey,FTXSecret,username,email = ReloadInfo(request)
                return render(request, 'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'error':'Mot de passe incorrect','status':1})

        else:
            FTXKey,FTXSecret,username,email = ReloadInfo(request)
            return render(request, 'accounts/account.html',{'FTXKey':FTXKey,'FTXSecret':FTXSecret,'username':username,'email':email,'status':0})

def ReloadInfo(request):
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

    return FTXKey,FTXSecret,username,email

def recuperation(request):
    if request.method == "POST":
        request.session['email'] = request.POST['email']
        try:
            U = User.objects.get(email = request.POST['email'])
            request.session['code'] = random.randrange(1000, 9999)
        except:
            return render(request,'registration/recuperation.html', {'status':1,'error':'Email introuvable'})
        mailsent = sendCode(U.username,U.email,request.session['code'])
        if mailsent:
            return render(request,'registration/validationToChangePassword.html', {'status':0})
        else:
            return render (request,'registration/recuperation.html', {'status':"Erreur serveur!"})
    else:
        return render(request,'registration/recuperation.html')

def changePassword(request):
    if request.method == "POST": 
        try:
            if request.POST['password1'] == request.POST['password2']:
                U = User.objects.get(email = request.session['email'])
                U.set_password(request.POST['password1'])
                U.save()
                return redirect('/')
            else:
                return render(request,'registration/changePassword.html', {'status':1,'error':'Mot de passe différents'})
        except:
            return render(request,'registration/changePassword.html', {'status':1,'error':'Erreur serveur'})
    else:
        return render(request,'registration/changePassword.html', {'status':0})

def resendCode(request):
    sendCode(request.session['username'],request.session['email'],request.session['code'])

def sendCode(username,email,code):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_content = '''
    Bonjour ''' +username + '''

    Nous avons reçu une demande non reconnue de connexion à votre compte depuis un nouvel emplacement en France.

    Si vous n'avez pas essayé de vous connecter à partir d'un nouvel emplacement en France tout à l'heure, vous devez changer votre mot de passe immédiatement. Veuillez revérifier l'URL pour vous assurer qu'il s'agit de quickbase-app.com et non d'un autre domaine se faisant passer pour QuickBase.

    Vous ne devez en aucun cas copier ou partager le code ci-dessous.

    Si vous venez de vous connecter depuis un nouvel emplacement en France, puis en utilisant l'appareil à partir duquel vous venez d'essayer de vous connecter, veuillez entrer le code ci-dessous pour vous connecter à votre compte QuickBase :
    ''' +str(code) + '''

    Merci de faire confiance à QuickBase.

    --------------------------
    QuickBase: https://quickbase-app.com
    '''
    #The mail addresses and password
    sender_address = 'sup.quickbase.app@gmail.com'
    sender_pass = 'momoleplusbo'
    receiver_address = email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Your QuickBase verification code'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    try : 
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        return True
    except:
        return False
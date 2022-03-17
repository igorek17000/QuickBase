from django.shortcuts import redirect, render
from dashboard.models import FtxClient
from accounts.models import APIKey
from currency_converter import CurrencyConverter

# Create your views here.
def base(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        try:
            APIKey.objects.get(user = request.user,exchange = 'FTX')
            APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
            FTXKey = APIFTX[0].apiKey
            FTXSecret = APIFTX[0].apiKeySecret
        except:
            return render(request,'dashboard/dashboard.html', {'status':1,'error':'Veuillez vérifier vos clés API'})

        try:
            account = FtxClient(FTXKey,FTXSecret)
        except:
            return render(request,'dashboard/dashboard.html', {'status':1,'error':'Impossible de se connecter à FTX','description':'Veuillez vérifier les informations API'})

        #info dashboard
        infos,maxCoin, minCoin = get_dashboard_info_usd(account)

        #info menu
        subaccounts = get_dashboard_menu_info(account)
        return render(request,'dashboard/dashboard.html', {'status':0,'infos':infos,'subaccounts':subaccounts,'maxCoin':maxCoin,'minCoin':minCoin})

def get_dashboard_info_usd(account):
    infos = {}
    infos['devise']='$'
    infos['total_balance'] =round(account.get_total_usd_balance(),2)
    c = CurrencyConverter()
    infos['total_deposit'] = c.convert(account.get_total_eur_deposit(),'EUR','USD')
    infos['total_profit'] = round(infos['total_balance'] - infos['total_deposit'],2)
    maxCoin = account.get_biggest_balance()
    maxCoin['usdValue'] = round(maxCoin['usdValue'],2)
    minCoin = account.get_smallest_balance()
    minCoin['usdValue'] = round(minCoin['usdValue'],2)
    return infos,maxCoin,minCoin

def get_dashboard_menu_info(account):
    subaccounts = account.get_all_subaccount()
    return subaccounts

def convert_USD_to_EUR(infos,maxCoin,minCoin):
    c = CurrencyConverter()

    for info in infos:
        try:
            infos[info] = round(c.convert(infos[info],'USD','EUR'),2)
        except:
            pass
    infos['devise']='€'
    for info in maxCoin:
        try:
            maxCoin[info] = round(c.convert(maxCoin[info],'USD','EUR'),2)
        except:
            pass
    for info in minCoin:
        try:
            minCoin[info] = round(c.convert(minCoin[info],'USD','EUR'),2)
        except:
            pass

    return infos,maxCoin,minCoin

def get_dashboard_info_eur(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        try:
            APIKey.objects.get(user = request.user,exchange = 'FTX')
            APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
            FTXKey = APIFTX[0].apiKey
            FTXSecret = APIFTX[0].apiKeySecret
        except:
            return render(request,'dashboard/dashboard.html', {'status':1,'error':'Veuillez vérifier vos clés API'})

        try:
            account = FtxClient(FTXKey,FTXSecret)
        except:
            return render(request,'dashboard/dashboard.html', {'status':1,'error':'Impossible de se connecter à FTX','description':'Veuillez vérifier les informations API'})
        
        #info dashboard
        infos,maxCoin, minCoin = get_dashboard_info_usd(account)

        #convert
        infos,maxCoin, minCoin = convert_USD_to_EUR(infos,maxCoin,minCoin)

        #info menu
        subaccounts = get_dashboard_menu_info(account)
        return render(request,'dashboard/dashboard.html', {'status':0,'infos':infos,'subaccounts':subaccounts,'maxCoin':maxCoin,'minCoin':minCoin})

def marche(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/marche.html')

def transactions(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/transactions.html')

def trades(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/trades.html')
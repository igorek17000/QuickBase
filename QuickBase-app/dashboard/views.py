from datetime import date, timedelta
import datetime
import time
from urllib import response
from django.http import JsonResponse
from django.shortcuts import redirect, render
from dashboard.models import FtxClient
from accounts.models import APIKey
from currency_converter import CurrencyConverter


# Views
# def base(request):
#     if not request.user.is_authenticated:
#         return redirect('/accounts/login')
#     else :
#         try:
#             keys = get_FTX_key(request)
#             account = get_FTX_account(keys['FTXKey'],keys['FTXSecret'])
#             #info dashboard
#             infos,maxCoin, minCoin = get_dashboard_info_usd(account)

#             #info menu
#             subaccounts = get_dashboard_menu_info(account)
#             return render(request,'dashboard/dashboard.html', {'status':0,'infos':infos,'subaccounts':subaccounts,'maxCoin':maxCoin,'minCoin':minCoin,'keys':keys})
#         except Exception as e:
#             print(e)
#             return render(request,'dashboard/dashboard.html', {'status':1,'error':'Error serveur'})

def base(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request,'dashboard/dashboard.html', {'status':0})

def get_dashboard_info_eur(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        try:
            APIKey.objects.get(user = request.user,exchange = 'FTX')
            APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
            FTXKey = APIFTX[0].apiKey
            FTXSecret = APIFTX[0].apiKeySecret
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
        except:
            return render(request,'dashboard/dashboard.html', {'status':1,'error':'Veuillez vérifier vos clés API'})

        

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


# Utils

def get_FTX_key(request):
    if not request.user.is_authenticated:
        return {'status':1,'error':'not conncted'}
    else :
        try : 
            APIKey.objects.get(user = request.user,exchange = 'FTX')
            APIFTX = APIKey.objects.filter(user = request.user,exchange = 'FTX')
            FTXKey = APIFTX[0].apiKey
            FTXSecret = APIFTX[0].apiKeySecret
            return {'FTXKey':FTXKey,'FTXSecret':FTXSecret}
        except Exception as e:
            return {'status':1,'error':e}

def get_FTX_account(request):
    try:
        keys = get_FTX_key(request)
        account = FtxClient(keys['FTXKey'],keys['FTXSecret'])
        return account
    except Exception as e:
        return {'status':1,'error':e}

def get_FTX_balance_usd(request):
    account = get_FTX_account(request)
    return round(account.get_total_usd_balance(),2)

def get_FTX_deposit_usd(request):
    account = get_FTX_account(request)
    depo = account.get_total_eur_deposit()
    c = CurrencyConverter()
    return round(c.convert(depo,'EUR','USD'),2)

def get_FTX_gain_usd(request):
    depo = get_FTX_deposit_usd(request)
    balance = get_FTX_balance_usd(request)
    return round(balance - depo,2)

def get_FTX_Biggest_coin_usd(request):
    account = get_FTX_account(request)
    big = account.get_biggest_balance()
    return big["coin"],round(big['usdValue'],2)

def get_FTX_Smallest_coin_usd(request):
    account = get_FTX_account(request)
    big = account.get_smallest_balance()
    return big["coin"],round(big['usdValue'],2)

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

# API 

def get_total_usd_balance(request):
    response={"balance":get_FTX_balance_usd(request),"devise":"$"}
    return JsonResponse(response)

def get_total_eur_balance(request):
    c = CurrencyConverter()
    usdBalance = get_FTX_balance_usd(request)
    response={"balance":round(c.convert(usdBalance,'USD','EUR'),2),"devise":"€"}
    return JsonResponse(response)

def get_gain_usd(request):
    response={"gain":get_FTX_gain_usd(request),"devise":"$"}
    return JsonResponse(response)

def get_gain_eur(request):
    c = CurrencyConverter()
    usdBalance = get_FTX_balance_usd(request)
    response={"gain":round(c.convert(usdBalance,'USD','EUR'),2),"devise":"€"}
    return JsonResponse(response)

def get_biggest_coin_usd(request):
    coin,value = get_FTX_Biggest_coin_usd(request)
    response = {"coin":coin,"value":value,"devise":"$"}
    return JsonResponse(response)

def get_biggest_coin_eur(request):
    c = CurrencyConverter()
    coin,value = get_FTX_Biggest_coin_usd(request)
    response = {"coin":coin,"value":round(c.convert(value,'USD','EUR'),2),"devise":"€"}
    return JsonResponse(response)

def get_smallest_coin_usd(request):
    coin,value = get_FTX_Smallest_coin_usd(request)
    response = {"coin":coin,"value":value,"devise":"$"}
    return JsonResponse(response)

def get_smallest_coin_eur(request):
    c = CurrencyConverter()
    coin,value = get_FTX_Smallest_coin_usd(request)
    response = {"coin":coin,"value":round(c.convert(value,'USD','EUR'),2),"devise":"€"}
    return JsonResponse(response)


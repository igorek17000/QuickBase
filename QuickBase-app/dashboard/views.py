from datetime import date, timedelta
import datetime
import time
from django.http import JsonResponse
from django.shortcuts import redirect, render
from dashboard.models import FtxClient,CoinGeckoAPI
from accounts.models import APIKey
from currency_converter import CurrencyConverter
from datetime import datetime

def base(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request,'dashboard/dashboard.html', {'status':0})    

def marche(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request, 'dashboard/marche.html', {'status':0})

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

def get_dashboard_menu_info(account):
    subaccounts = account.get_all_subaccount()
    return subaccounts

def get_FTX_historical_balance(request,id):
    account = get_FTX_account(request)
    response = account.get_historical_balance_id_main(id)
    count = 120
    if (len(response['results'])==0) and (count!=0):
        response = account.get_historical_balance_id_main(id)
        count-=1
        time.sleep(0.5)
    else :
        return response

def get_FTX_historical_balance_id_yesterday(request):
    account = get_FTX_account(request)
    response = account.get_historical_balance()
    yest = date.today()  - timedelta(days = 2)
    for i in response:
        if i['endTime'][:10]==str(yest):
            return i['id']
    account.post_yesterday_historical_balance()
    get_FTX_historical_balance_id_yesterday(request)

def get_FTX_historical_balance_usd(request,resp):
    account = get_FTX_account(request)
    accountValue = 0.0
    yest = date.today()  - timedelta(days = 1)
    timeSt= timeSt = time.mktime(datetime.strptime(str(yest), "%Y-%m-%d").timetuple())
    counter=0
    for i in resp['results']:
        market = str(i['ticker']) + '/USD'
        markets = account.get_historical_prices(market=market,end_time=timeSt,start_time=timeSt)
        accountValue+=resp['results'][counter]['size']*markets[0]['open']
        counter+=1
    return round(accountValue,2)

def test_get_data(request,value):
    return JsonResponse({'msg' : value})
    
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
    usdBalance = get_FTX_gain_usd(request)
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

def get_hitorical_balance_usd(request):
    id = get_FTX_historical_balance_id_yesterday(request)
    resp = get_FTX_historical_balance(request,id)
    value = get_FTX_historical_balance_usd(request,resp)
    return JsonResponse({'oldValue':value,'devise':'$'})

def get_market_history(request,id,vs_currency,days,interval):
    cg = CoinGeckoAPI()
    req=cg.get_coin_market_chart_by_id(id=id,vs_currency=vs_currency,days=days,interval=interval)
    for i in range(len(req['prices'])):
        req['prices'][i][0]=datetime.fromtimestamp(int(str(req['prices'][i][0])[:-3]))
    
    prices = []
    dates = []
    volume = []
    marketcap = []
    for i in range(len(req['prices'])):
        prices.append(req['prices'][i][1])
        dates.append(req['prices'][i][0])
        volume.append(req['total_volumes'][i][1])
        marketcap.append(req['market_caps'][i][1])
    return JsonResponse({'dates':dates,'prices':prices,'marketcap':marketcap,'volume':volume})

def get_coins(request):
    cg = CoinGeckoAPI()
    req=cg.get_coins()
    return JsonResponse({"coins":req})

def get_vs_currency(request,id):
    cg = CoinGeckoAPI()
    req=cg.get_coin_by_id(id)
    keys=[]
    for key in req['market_data']['current_price']:
        keys.append(key)
    return JsonResponse({'vs_currency':keys})

def get_coin_infos(request,id, vs_currency):
    cg = CoinGeckoAPI()
    req=cg.get_coin_by_id(id)
    return JsonResponse({'infos':req,'vs_currency':req['market_data']['current_price'][vs_currency]})


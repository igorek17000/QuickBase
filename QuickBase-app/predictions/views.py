from django.http import JsonResponse
from django.shortcuts import redirect, render
from prophet.serialize import  model_from_json
from dashboard.models import CoinGeckoAPI
from datetime import datetime
import pandas as pd
from prophet import Prophet
# from keras import models


# Create your views here.
def marches(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request,'predictions/marches.html', {'status':0})    

def predict(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    else :
        return render(request,'predictions/predict.html', {'status':0}) 

def load_model(name):
    with open(name, 'r') as fin:
        m = model_from_json(fin.read())  # Load model
    return m

def get_crypto_price(request,id, vs_currency,days,interval):
    cg = CoinGeckoAPI()
    prices=cg.get_coin_market_chart_by_id(id=id, vs_currency=vs_currency, days=days, interval=interval)
    df=pd.DataFrame(prices['prices'],columns = ['dates','prices'])
    for i in df.index:
        df.loc[i,'dates']=datetime.fromtimestamp(int(str(df.loc[i,'dates'])[:-3]))
    df['dates']=pd.to_datetime(df['dates'])
    df = df.rename(columns={"dates":'ds',"prices":'y'})
    return df

def create_model(df):
    m2 = Prophet()
    m2.fit(df)
    return m2

# API
def predict_data(request,id, vs_currency,days,interval,period,freq):
    try:
        df=get_crypto_price(request,id,vs_currency,days,interval)
        m=create_model(df)
        future = m.make_future_dataframe(periods=period,freq=freq)
        forecast = m.predict(future)
        mask=forecast['ds']>=datetime.now()
        forecast=forecast[mask]
        forecast = forecast.reset_index(drop=True)
        return JsonResponse({'dates':forecast['ds'].tolist(),'prices':forecast['yhat'].tolist(),'upper':forecast['yhat_upper'].tolist(),'lower':forecast['yhat_lower'].tolist(),'tomorow_price':forecast['yhat'][0],'tomorow_upper':forecast['yhat_upper'][0],'tomorow_lower':forecast['yhat_lower'][0]})
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)})

def get_coin_infos(request,id, vs_currency):
    cg = CoinGeckoAPI()
    req=cg.get_coin_by_id(id)
    return JsonResponse({'infos':req,'price':req['market_data']['current_price'][vs_currency],'marketcap':req['market_data']['market_cap'][vs_currency],'volume':req['market_data']['total_volume'][vs_currency],'prices_changes':req['market_data']['price_change_percentage_24h'],'market_changes':req['market_data']['market_cap_change_percentage_24h']})


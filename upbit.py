import pandas as pd
import numpy as np
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import json
import datetime

import matplotlib as mpl
import matplotlib.pylab as plt

def balance(access_key, secret_key):
    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY'] = access_key
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY'] = secret_key

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get("https://api.upbit.com/v1/accounts", headers=headers)

    return res.json()

def coin_price(coin_list, min):

    graph_list = []
    for coin_name in coin_list:
        coin = "KRW-" + coin_name

        url = "https://api.upbit.com/v1/candles/minutes/1"
        querystring = {"market": coin, "count": min}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)

        sec = datetime.datetime.today().second
        microsec = datetime.datetime.today().microsecond

        price = pd.DataFrame(json.loads(response.text))
        price = price.sort_values('candle_date_time_kst')
        price['second'] = sec
        price['microsecond'] = microsec
        price['high_low'] = (price['high_price'] - price['low_price']) / price['trade_price']
        price['trade_low'] = (price['trade_price'] - price['low_price']) / price['trade_price']
        price['high_trade'] = (price['high_price'] - price['trade_price']) / price['trade_price']

        graph_list.append(price)

    return graph_list

def price_plt(df):
    fig, axes = plt.subplots(len(df), 1, figsize=(20, 10), facecolor="#c1f1f1")

    #make n graphs(depends on user input)
    for i in range(len(df)):

        #coin name(used to set graph's title)
        coin = df[i]['market'][1][4:]

        data = df[i]
        df[i]['min'] = df[i]['candle_date_time_kst'].str.split('T', expand=True)[1].str.replace(':00', '')

        axes[i].set_title("Price of " + coin, fontsize=16)  #set graph title

        #plot graph(trade price - green, high price - red, low price - blue)
        axes[i].plot(data['min'], data['trade_price'], color='green', marker='o', linestyle='dashed', linewidth=2,
                     markersize=5, label='trade')
        axes[i].plot(data['min'], data['high_price'], color='red', marker='o', linewidth=1.5, markersize=5,
                     label='high')
        axes[i].plot(data['min'], data['low_price'], color='blue', marker='o', linewidth=1.5, markersize=5, label='low')

        axes[i].legend()

    plt.savefig('graph.png')
    plt.show()
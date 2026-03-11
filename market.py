import requests

def btc_price():

    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    data=requests.get(url).json()

    return data["bitcoin"]["usd"]

def eth_price():

    url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    data=requests.get(url).json()

    return data["ethereum"]["usd"]

def market_data():

    url="https://api.coingecko.com/api/v3/global"

    data=requests.get(url).json()

    cap=data["data"]["total_market_cap"]["usd"]

    btc_dom=data["data"]["market_cap_percentage"]["btc"]

    return f"""
加密市场

总市值:
${cap}

BTC占比:
{btc_dom}%
"""
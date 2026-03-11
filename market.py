import requests

def btc_price():

    url="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    r=requests.get(url)

    data=r.json()

    if "price" in data:

        return float(data["price"])

    return None


def eth_price():

    url="https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

    r=requests.get(url)

    data=r.json()

    if "price" in data:

        return float(data["price"])

    return None
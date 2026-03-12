import requests

def get_price(symbol):

    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    r=requests.get(url,timeout=10)

    data=r.json()

    if "price" in data:

        return float(data["price"])

    return None


def btc_price():

    return get_price("BTCUSDT")


def eth_price():

    return get_price("ETHUSDT")
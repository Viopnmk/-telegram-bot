import requests

def levels():

    url="https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=50"

    r=requests.get(url)

    data=r.json()

    close=[float(i[4]) for i in data]

    support=min(close[-20:])

    resistance=max(close[-20:])

    return f"""
关键价位

支撑位: {support}

压力位: {resistance}
"""
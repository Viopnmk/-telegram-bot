import requests

def multi_tf():

    tf=["15m","1h","4h"]

    result="多周期趋势\n\n"

    for t in tf:

        url=f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={t}&limit=20"

        r=requests.get(url)

        data=r.json()

        close=[float(i[4]) for i in data]

        if close[-1]>close[-5]:

            trend="上涨"

        else:

            trend="下跌"

        result+=f"{t}: {trend}\n"

    return result
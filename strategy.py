from market import btc_price

def strategy():

    price=btc_price()

    if price is None:

        return "行情获取失败"

    if price>70000:

        return """
交易策略

趋势: 上涨

操作:
回调做多

支撑: 68000
压力: 72000
"""

    elif price<60000:

        return """
交易策略

趋势: 下跌

操作:
反弹做空

压力: 61000
支撑: 58000
"""

    else:

        return """
交易策略

趋势: 震荡

策略:
区间交易

支撑: 60000
压力: 70000
"""
import hashlib
import hmac
from enum import Enum
import pandas

import requests


class Type(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Interval(Enum):
    MIN_1 = "1m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_10 = "10m"
    MIN_15 = "15m"
    MIN_30 = "30m"

    HOURS_1 = "1h"
    HOURS_2 = "2h"
    HOURS_4 = "4h"
    HOURS_6 = "6h"
    HOURS_8 = "8h"
    HOURS_12 = "12h"

    DAY_1 = "1d"
    DAY_3 = "3d"
    WEAK = "1w"
    MONTH = "1m"


class Limit(Enum):
    INT_5 = "5"
    INT_10 = "10"
    INT_20 = "20"
    INT_50 = "50"
    INT_100 = "100"
    INT_500 = "500"
    INT_1000 = "1000"


class Api(object):
    # 定义Binance的URL常量

    baseurl = "https://api.binance.com"

    # K线数据
    klines = "/api/v3/klines"

    # 订单薄
    depth = "/api/v3/depth"

    # 下单
    trade = "/api/v3/order"

    service_time = "/api/v3/time"

    service_status = "/api/v3/ping"

    wallet = "/sapi/v1/capital/config/getall"

    account = "/fapi/v2/account"
    balance = "/fapi/v2/balance"
    order = "/fapi/v1/order"


# 定义交易所
class BinanceExChange(object):

    def __init__(self, app_key, app_secret, timeout=5):
        self.app_key = app_key
        self.app_secret = app_secret
        self.timeout = timeout

    def get_klines(self, symbol, interval: Interval, limit: Limit = Limit.INT_500):
        params = {"symbol": symbol, "interval": interval.value, "limit": limit.value}
        return requests.get(Api.baseurl + Api.klines, params=params, timeout=self.timeout).json()

    # 订单薄
    def get_depth(self, symbol, limit: Limit):
        params = {"symbol": symbol, "limit": limit.value}
        return requests.get(Api.baseurl + Api.depth, params=params, timeout=self.timeout).json()

    def trade_order(self, symbol, side: Enum, type: Enum):
        params = {"symbol": symbol, "side": side.value, "type": type.value}
        return requests.get(Api.baseurl + Api.trade, params=params, timeout=self.timeout).json()

    def get_service_time(self):
        return requests.get(Api.baseurl + Api.service_time, timeout=self.timeout).json()["serverTime"]

    def get_service_status(self):
        return requests.get(Api.baseurl + Api.service_status, timeout=self.timeout).json()

    def get_wallet(self):
        timestamp = self.get_service_time()
        params = {"timestamp": timestamp}
        headers = {"X-MBX-APIKEY": self.app_key}
        # 签名
        params = self.signature(params)
        return requests.get(Api.baseurl + Api.wallet, headers=headers, params=params, timeout=self.timeout).json()

    def get_account(self):
        timestamp = self.get_service_time()
        headers = {"X-MBX-APIKEY": self.app_key}
        params = {"timestamp": timestamp, "recvWindow": 5000}
        params = self.signature(params)
        return requests.get(Api.baseurl + Api.account, headers=headers, params=params, timeout=self.timeout).json()

    def get_balance(self):
        timestamp = self.get_service_time()
        params = {"timestamp": timestamp, "recvWindow": 5000}
        params = self.signature(params)
        headers = {"X-MBX-APIKEY": self.app_key}
        return requests.get(Api.baseurl + Api.balance, headers=headers, params=params, timeout=self.timeout).json()

    def get_order(self, symbol):
        timestamp = self.get_service_time()
        params = {"timestamp": timestamp, "symbol": symbol}
        params = self.signature(params)
        headers = {"X-MBX-APIKEY": self.app_key}
        return requests.get(Api.baseurl + Api.balance, headers=headers, params=params, timeout=self.timeout).json()

    def signature(self, params):
        query = ""
        for key in params:
            query += f"{key}={params[key]}&"
        query = query[0:-1]
        sign = hmac.new(self.app_secret.encode('utf-8'), msg=query.encode('utf-8'),
                        digestmod=hashlib.sha256).hexdigest()
        params["signature"] = sign
        return params


if __name__ == '__main__':
    binance = BinanceExChange("AA7v7Gv6nvVw9wElb7TiqypUroRBP01MVQ6YqNlLaO2jw2PIRQKouMxuSRn0StRH",
                              "61NoeI3o3yezIvcTEbOb4K5l3SvgxZeVwBKZr4FCSR90abOBz9DmukN3DMqxDVyL")
    # print(binance.get_klines("BTCUSDT",Interval.DAY_1,Limit.INT_1000))
    # print(binance.get_depth("BTCUSDT", Limit.INT_5))
    # print(binance.getServiceTime())
    # print(binance.getWallet())
    # print(binance.get_account())

    # print(binance.get_order("BTCUSDT"))
    data = binance.get_klines("BTCUSDT", Interval.DAY_1, Limit.INT_1000)
    df = pandas.DataFrame(data, columns={
        'open_time': 0,
        'open': 1,
        'high': 2,
        'low': 3,
        'close': 4,
        'volume': 5,
        'close_time': 6,
        'quote_volume': 7,
        'trades': 8,
        'taker_base_volume': 9,
        'taker_quote_volume': 10,
        'ignore': 11,

    })
    df.to_csv('btc_day_klines.csv')

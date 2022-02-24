from enum import Enum

import params as params
import requests
import pandas as pd

class Type(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"

class SIDE(Enum):
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

class LIMIT(Enum):
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
    depth= "/api/v3/depth"

    # 下单
    trade = "/api/v3/order"

    service_time = "/api/v3/time"

    service_status = "/api/v3/ping"

    wallet = "/sapi/v1/capital/config/getall"


# 定义交易所
class BinanceExChange(object):

    def __init__(self,appKey,secret):
        self.appKey = appKey
        self.secret = secret

    def getKlines(self,symbol,interval:Interval,limit:LIMIT):
        params = {"symbol":symbol,"interval":interval.value,"limit":limit.value}
        return requests.get(Api.baseurl + Api.klines ,params=params).json()

    # 订单薄
    def getDepth(self,symbol,limit:LIMIT):
        params = {"symbol":symbol,"limit":limit.value}
        return requests.get(Api.baseurl + Api.depth ,params=params).json()

    def tradeOrder(self,symbol,side:Enum,type:Enum):
        params = {"symbol":symbol,"side":side.value,"type":type.value}
        return requests.get(Api.baseurl + Api.depth ,params=params).json()

    def getServiceTime(self):
        return requests.get(Api.baseurl+Api.service_time).json()["serverTime"]

    def getServiceStatus(self):
        return requests.get(Api.baseurl+Api.service_status).json()

    def getWallet(self):

        timestamp = self.getServiceTime()

        return requests.get(Api.baseurl+Api.wallet,params={"timestamp":timestamp}).json()




if __name__ == '__main__':
    binance = BinanceExChange("AA7v7Gv6nvVw9wElb7TiqypUroRBP01MVQ6YqNlLaO2jw2PIRQKouMxuSRn0StRH","61NoeI3o3yezIvcTEbOb4K5l3SvgxZeVwBKZr4FCSR90abOBz9DmukN3DMqxDVyL")
    # print(binance.getKlines("BTCUSDT",Interval.HOURS_1,LIMIT.INT_5))
    # print(binance.getDepth("BTCUSDT",LIMIT.INT_5))
    # print(binance.getServiceTime())
    print(binance.getWallet())
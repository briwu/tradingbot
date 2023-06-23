import yfinance as yf
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails


data = yf.download("EURUSD=X", start="2023-4-25", end="2023-6-18", interval='15m')
print(data.iloc[:,:])
data.Open.iloc

def sig_generator(data):
    curr_open = data.Open.iloc[-1]
    curr_close = data.Close.iloc[-1]
    prev_open = data.Open.iloc[-2]
    prev_close = data.Open.iloc[-2]

    if curr_open > curr_close and prev_open < prev_close and curr_close < prev_open and curr_open >= prev_close:
        return 1
    
    elif curr_open < curr_close and prev_open > prev_close and curr_close > prev_open and curr_open <= prev_close:
        return 2
    
    else:
        return 0
    
sig = []
sig.append(0)
for i in range(1, len(data)):
    new_data = data[i-1:i+1]
    sig.append(sig_generator(new_data))
data["signal"] = sig
print(data)
print(data.signal.value_counts())

from config import access_token, accountID

def get_candles(n):
    client = CandleClient(access_token, real = False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o)) > 1)

def trade():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])

    i = 0
    for candle in candles:
        dfstream.loc[i, ['Open']] = float(str(candle.bid.o))
        dfstream.loc[i, ['Close']] = float(str(candle.bid.c))
        dfstream.loc[i, ['High']] = float(str(candle.bid.h))
        dfstream.loc[i, ['Low']] = float(str(candle.bid.l))
        i += 1

    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    sig = sig_generator(dfstream.iloc[:-1,:])

    client = API(access_token)

    SLTP = 2.
    prev_candle_range = abs(dfstream['Open'].iloc[-2] - dfstream['Close'].iloc[-2])

    SL_buy = float(str(candle.bid.o)) - prev_candle_range
    SL_sell = float(str(candle.bid.o)) + prev_candle_range

    TP_buy = float(str(candle.bid.o)) + (prev_candle_range * SLTP)
    TP_sell = float(str(candle.bid.o)) - (prev_candle_range * SLTP)

    print(dfstream.iloc[:-1,:])
    print(TP_buy, " ", SL_buy, " ", TP_sell, " ", SL_sell)


    


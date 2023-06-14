import yfinance as yf
import pandas as pd

data = yf.download("EURUSD=X", start="2023-4-20", end="2023-6-10", interval='15m')
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

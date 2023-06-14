import yfinance as yf
import pandas as pd

data = yf.download("EURUSD=X", start="2023-4-30", end="2023-6-10", interval='15m')
print(data.iloc[:,:])
data.Open.iloc

def sig_generator(data):
    curr_open = data.Open.iloc[-1]
    curr_close = data.Close.iloc[-1]
    prev_open = data.Open.iloc[-2]
    prev_close = data.Open.iloc[-2]

    

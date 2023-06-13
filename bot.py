import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2023-4-30", end="2023-6-10", interval='15m')
print(dataF.iloc[:,:])
#dataF.Open.iloc

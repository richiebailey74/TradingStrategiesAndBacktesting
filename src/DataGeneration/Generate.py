import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from io import StringIO
import time
import yfinance as yf


def generateYearOfDataForSymbol(sym, time_increment, years_and_months, year_num):
    count = 0
    dff = None
    for ym in years_and_months:

        # free API key is inserted here, limited to 100 calls per day
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={sym}&interval={time_increment}&month={ym}&outputsize=full&apikey=U2Q8E53V7WWY1H9P'
        try:
            r = requests.get(url)
        except:
            print("Invalid API request, limit has most likely been reached")
            print(f"Currently on month year: {ym}")
        data = r.json()
        try:
            df = pd.DataFrame.from_dict(data[f"Time Series ({time_increment})"], orient='index')
        except:
            print(json.dumps(data, indent=4))
        df.columns = ['open', 'high', 'low', 'close', 'volume']  # Renaming the columns for simplicity
        df = df.sort_index()
        count += 1

        if dff is None:
            dff = df
        else:
            dff = pd.concat([dff, df], ignore_index=False)

        if count == 5:
            time.sleep(75)  # sleep 75 seconds as to not exceed api limit
            count = 0

    dff.to_csv(f'../data/stock_data/{sym}_{year_num}year.csv', index=True)
    time.sleep(75)
    return dff


def generateYearOfDataForSymbol_1y(sym, time_increment):
    years_and_months = ["2022-08",
                        "2022-09",
                        "2022-10",
                        "2022-11",
                        "2022-12"
                        "2023-01",
                        "2023-02",
                        "2023-03",
                        "2023-04",
                        "2023-05",
                        "2023-06",
                        "2023-07"]

    count = 0
    dff = None
    for ym in years_and_months:

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={sym}&interval={time_increment}&month={ym}&outputsize=full&apikey=U2Q8E53V7WWY1H9P'
        try:
            r = requests.get(url)
        except:
            print("Invalid API request, limit has most likely been reached")
            print(f"Currently on month year: {ym}")
        data = r.json()
        try:
            df = pd.DataFrame.from_dict(data[f"Time Series ({time_increment})"], orient='index')
        except:
            print(json.dumps(data, indent=4))
        df.columns = ['open', 'high', 'low', 'close', 'volume']  # Renaming the columns for simplicity
        df = df.sort_index()
        count += 1

        if dff is None:
            dff = df
        else:
            dff = pd.concat([dff, df], ignore_index=False)

        if count == 5:
            time.sleep(75)  # sleep 75 seconds as to not exceed api limit
        if count == 10:
            time.sleep(75)  # sleep 75 seconds as to not exceed api limit

    dff.to_csv(f'../data/stock_data/{sym}_1year.csv', index=True)
    time.sleep(75)
    return dff

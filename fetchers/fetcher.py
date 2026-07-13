import yfinance as yf
import pandas as pd
from fredapi import Fred
from loguru import logger

fred = Fred(api_key="FRED_API_KEY")

def fetch_factor(name: str, source: str, ticker: str):

    if source == "yahoo":
        return fetch_yahoo(name, ticker)

    elif source == "fred":
        return fetch_fred(name,ticker)

    else:
        raise ValueError(f"Unknown source: {source}")


def fetch_yahoo(name:str, ticker: str, start="2010-01-01"):
    logger.info(f"Yahoo: {ticker}")

    df = yf.download(ticker, start=start)

    if df.empty:
        return pd.DataFrame()

    df = df[["Close"]].copy()
    df.columns = [name]
    df.index = pd.to_datetime(df.index)

    return df  

def fetch_fred(name:str, ticker: str, start="2010-01-01"):
    logger.info(f"Fred: {ticker}") 
    try:
        series = fred.get_series(ticker)
        df = pd.DataFrame(series)
        df.columns = [name]
        df.index = pd.to_datetime(df.index)
        df = df[df.index >= start]
        return df
    except Exception as e:
        logger.error(f"Failed to fetch FRED series '{ticker}': {e}")
        return pd.DataFrame()   
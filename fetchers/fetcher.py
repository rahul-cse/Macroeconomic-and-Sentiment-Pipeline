import yfinance as yf
import pandas as pd
#from fredapi import Fred
from loguru import logger


def fetch_factor(name: str, source: str, ticker: str):

    if source == "yahoo":
        return fetch_yahoo(name, ticker)

    # elif source == "fred":
    #     return fetch_fred(ticker)

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
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns

def load_dataset(path):
    logger.info("Loading normalized parquet dataset")
    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index)
    return df

def data_quality_check(df):
    print("\nDataset shape:")
    print(df.shape)

    print("\nDate range:")
    print(df.index.min())
    print(df.index.max())

    latest_date = df.index.max()

    days_old = (pd.Timestamp.today() - latest_date).days
    if days_old > 7:
        logger.warning("WARNING: Dataset is older than 7 days")
    else:
        logger.info("Dataset freshness is OK")


def calculate_omx_returns(df):
    df["omx_return_1d"] = (df["omx"].pct_change(1))

    df["omx_return_5d"] = (df["omx"].pct_change(5))

    df["omx_return_20d"] = (df["omx"].pct_change(20))

    #df["omx_return_30d"] = (df["omx"].pct_change(30))

    df = df.replace([np.inf, -np.inf], np.nan)

    logger.info("Calculated OMX returns")
    return df  


def calculate_correlations(df):
    logger.info("Starting correlations calculation")

    numeric_df = df.select_dtypes(include="number")

    pearson = numeric_df.corr(method="pearson")

    spearman = numeric_df.corr(method="spearman")

    return pearson, spearman


def factor_omx_correlation(df):
    logger.info("Calculating factors OMX correlation")
    factors = [
        c for c in df.columns
        if c not in [
            "omx",
            "omx_return_1d",
            "omx_return_5d",
            "omx_return_20d",
            #"omx_return_30d"
        ]
    ]


    results=[]

    for factor in factors:
        print(np.isinf(df).sum())


        row={

            "factor":factor,

            "omx_return_1d":
                df[factor].corr(
                    df["omx_return_1d"]
                ),

            "omx_return_5d":
                df[factor].corr(
                    df["omx_return_5d"]
                ),

            "omx_return_20d":
                df[factor].corr(
                    df["omx_return_20d"]
                ),

            #"omx_return_30d":df[factor].corr(df["omx_return_30d"])    
        }
        results.append(row)

    logger.info("OMX correlation with factors are finished")
    return pd.DataFrame(results)



def rolling_correlation(df, window):

    factors = [
        c for c in df.columns
        if c not in [
            "omx",
            "omx_return_1d",
            "omx_return_5d",
            "omx_return_20d"
        ]
    ]

    results = {}

    for factor in factors:

        results[f"{factor}_1d"] = (
            df[factor]
            .rolling(window)
            .corr(df["omx_return_1d"])
        )

        results[f"{factor}_5d"] = (
            df[factor]
            .rolling(window)
            .corr(df["omx_return_5d"])
        )

        results[f"{factor}_20d"] = (
            df[factor]
            .rolling(window)
            .corr(df["omx_return_20d"])
        )

    return pd.DataFrame(results)
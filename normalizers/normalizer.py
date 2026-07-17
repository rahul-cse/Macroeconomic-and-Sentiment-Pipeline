import pandas as pd
from loguru import logger


def rolling_min_max(series, window=252):
    rolling_min = series.rolling(window=window,min_periods=1).min()
    rolling_max = series.rolling(window=window,min_periods=1).max()
    normalized = (
        (series - rolling_min)
        /
        (rolling_max - rolling_min)
    )

    return normalized

def normalize_factors(df, window=252):
    logger.info("Starting normalization")

    normalized_df = pd.DataFrame(index=df.index)

    for column in df.columns:

        logger.info(f"Normalizing {column}")

        normalized_df[column] = rolling_min_max(
            df[column],
            window
        )


    return normalized_df
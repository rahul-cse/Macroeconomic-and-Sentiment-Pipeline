import pandas as pd
from loguru import logger

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting data cleaning")
    df = df.copy()

    missing_before = df.isna().sum()
    logger.info(
        f"Missing values before filling:\n{missing_before}"
    )


    df = df.ffill()
    
    before_drop = len(df)
    df = df.dropna()
    removed_rows = before_drop - len(df)
    logger.info(
        f"Removed {removed_rows} rows with remaining missing values"
    )
    
    return df
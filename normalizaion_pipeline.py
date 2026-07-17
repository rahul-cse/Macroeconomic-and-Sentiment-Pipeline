import pandas as pd
from loguru import logger

from normalizers.cleaner import clean_data
from normalizers.normalizer import normalize_factors

def main():

    logger.info("Loading raw factors")

    df = pd.read_parquet(
        "data/processed/factors.parquet"
    )

    logger.info("cleaning raw factors") 
    clean_df = clean_data(df)
    logger.info(f"Cleaned dataset shape: {clean_df.shape}")

    normalized_df = normalize_factors(
        clean_df,
        window=252
    )

    normalized_df.to_parquet(
        "data/processed/factors_normalized.parquet"
    )

    normalized_df.to_csv(
        "data/processed/factors_normalized.csv"
    )

    logger.success("Normalization completed")


if __name__ == "__main__":
    main()   
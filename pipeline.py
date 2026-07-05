import yaml
import pandas as pd
from loguru import logger

from fetchers.fetcher import fetch_factor

def load_config(path="config/factors.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def build_dataset(config):
    factors = config["factors"]

    all_data = []

    for name, details in factors.items():
        source = details["source"]
        ticker = details["ticker"]

        logger.info(f"Processing: {name}")

        df = fetch_factor(name, source, ticker)

        if df.empty:
            logger.warning(f"Skipping {name} (no data)")
            continue

        all_data.append(df)

    logger.info("Merging all factors...")

    final_df = pd.concat(all_data, axis=1)

    final_df.sort_index(inplace=True)

    return final_df
 
    
def main():
    logger.info("Starting pipeline...")

    config = load_config()

    df = build_dataset(config)

    logger.info(f"Final dataset shape: {df.shape}")

    # save output
    output_path = "data/processed/"
    df.to_parquet(output_path + "factors.parquet")
    df.to_csv(output_path + "factors.csv")

    logger.success(f"Saved dataset to {output_path}")



if __name__ == "__main__":
    main()    
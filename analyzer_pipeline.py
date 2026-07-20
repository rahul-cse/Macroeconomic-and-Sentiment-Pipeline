import pandas as pd
from loguru import logger

from analyzers.analyzer import *
from visualizers.visualize import *

def main():
    logger.info("Starting analysis pipeline")

    df = load_dataset("data/processed/factors_normalized.parquet")

    data_quality_check(df)

    pearson, spearman = calculate_correlations(df)

    raw_df = load_dataset("data/processed/factors.parquet")
    raw_df = calculate_omx_returns(raw_df)

    df["omx_return_1d"] = raw_df["omx_return_1d"]
    df["omx_return_5d"] = raw_df["omx_return_5d"]
    df["omx_return_20d"] = raw_df["omx_return_20d"]
    #df["omx_return_30d"] = raw_df["omx_return_30d"]

    factor_corr = factor_omx_correlation(df)

    roll_corr = rolling_correlation(df, 252)

    Path("reports").mkdir(exist_ok=True)

    pearson.to_csv("reports/pearson_matrix.csv")

    spearman.to_csv("reports/spearman_matrix.csv")

    factor_corr.to_csv("reports/factor_vs_omx.csv", index=False)

    roll_corr.to_csv("reports/rolling_coll.csv")

    ## Visualization ##
    Path("reports/plots").mkdir(
        parents=True,
        exist_ok=True
    )
    plot_correlation_heatmap(pearson,"pearson_heatmap")
    plot_correlation_heatmap(spearman,"spearman_heatmap")

    plot_rolling_correlation(roll_corr)


if __name__=="__main__":
    main()    
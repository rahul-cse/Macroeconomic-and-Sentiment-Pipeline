from loguru import logger

from pipeline import main as fetch_main
from normalizaion_pipeline import main as normalize_main
from analyzer_pipeline import main as analyze_main

def main():
    logger.info("=" * 50)
    logger.info("Macroeconomic Sentiment Pipeline Started")
    logger.info("=" * 50)

    fetch_main()

    normalize_main()

    analyze_main()

    logger.success("=" * 50)
    logger.success("Pipeline completed successfully.")
    logger.success("=" * 50)

if __name__ == "__main__":
    main()
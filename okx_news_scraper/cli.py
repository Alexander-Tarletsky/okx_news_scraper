import argparse
import logging
import sys
from datetime import datetime

from okx_news_scraper.scraper import scrape

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("OKX News Scraper")


def main() -> None:

    p = argparse.ArgumentParser(
        description="Scrape OKX announcements between dates and save as JSON."
    )
    p.add_argument(
        "--start", "-s", required=True,
        help="Start date (inclusive), format YYYY-MM-DD"
    )
    p.add_argument(
        "--end", "-e", required=True,
        help="End date (inclusive), format YYYY-MM-DD"
    )
    p.add_argument(
        "--folder", "-f", required=True,
        help="Output folder for JSON files"
    )
    args = p.parse_args()

    try:
        start = datetime.strptime(args.start, "%Y-%m-%d")
        end = datetime.strptime(args.end, "%Y-%m-%d")
    except ValueError as exc:
        logger.error(f"Invalid date format: {exc}")
        sys.exit(1)

    if start > end:
        logger.error("START date must be <= END date.")
        sys.exit(1)

    try:
        logger.info("Starting OKX news scraper...")
        scrape(start, end, args.folder)
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        sys.exit(2)
    else:
        logger.info("Scraping completed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()

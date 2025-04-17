import sys
import argparse
import logging
from datetime import datetime
from okx_news_scraper.scraper import scrape

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr
    )

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
        logging.error(f"Invalid date format: {exc}")
        sys.exit(1)

    if start > end:
        logging.error("START date must be <= END date.")
        sys.exit(1)

    try:
        scrape(start, end, args.folder)
    except Exception as exc:
        logging.error(f"Unexpected error: {exc}", exc_info=True)
        sys.exit(2)

if __name__ == "__main__":
    main()

import logging
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from okx_news_scraper.utils import (
    build_url,
    extract_date,
    write_json_file,
    create_session,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://www.okx.com/"
PATH_TO_PARSE = "/help/section/announcements-new-listings"


def fetch_page(session: requests.Session, page: int = 1) -> BeautifulSoup:
    """Fetch a page of OKX announcements."""
    resp = session.get(
        build_url(BASE_URL, PATH_TO_PARSE, page=page),
        timeout=10,
    )
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_announcement_list(
    soup: BeautifulSoup,
) -> list[tuple[str, str, datetime]]:
    """
    Parse a page of OKX announcements.

    Returns:
        A list of (title, full_url, publication_datetime), sorted newest first.
    """
    items = []

    # 1) Select all <li> elements where class begins with 'index_articleItem__'
    for el in soup.select("li[class^='index_articleItem__']"):

        # 2) Find the anchor with the href
        a = el.find("a", href=True)
        if not a:
            continue

        # 3) Within the <a>, find the title DIV (class 'index_articleTitle__')
        title_el = a.find("div", class_=re.compile(r"index_articleTitle__"))

        # 4) And find the date span (data‑testid="DateDisplay")
        date_el = a.find("span", {"data-testid": "DateDisplay"})
        if not title_el or not date_el:
            continue

        # 5) Extract and clean the text
        title = title_el.get_text(strip=True)

        # 6) Prepend domain to the href
        link = build_url("https://www.okx.com/", a["href"])

        # 7) Extract the date string
        try:
            date_str = extract_date(date_el.get_text(strip=True))
        except Exception as e:
            logger.warning(
                f"Failed to parse date '{date_el.get_text(strip=True)}': {e}."
                f" Skipping this announcement."
            )
            continue

        # Collect the tuple
        items.append((title, link, date_str))

    # Sort by date descending
    return sorted(items, key=lambda x: x[2], reverse=True)


def fetch_detail(session: requests.Session, link: str) -> str:
    """Fetch the detail of an announcement."""
    try:
        resp = session.get(link, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        body_el = soup.select_one('div[class*="index_richTextContent__"]')
    except Exception as e:
        logger.error(f"Failed to fetch detail from {link}: {e}")
        return ""
    return body_el.get_text(separator="\n", strip=True) if body_el else ""


def scrape(start_date: datetime, end_date: datetime, out_folder: str):
    """
    Scrape OKX announcements between two dates and save them as JSON files.
    Args:
        start_date (datetime): Start date (inclusive).
        end_date (datetime): End date (inclusive).
        out_folder (str): Output folder for JSON files.
    """
    session = create_session()
    data = []
    page = 1
    done = False

    while not done:
        logger.info("Processing page %d ...", page)
        try:
            soup = fetch_page(session=session, page=page)
        except Exception as e:
            logger.error(f"Failed to fetch page {page}: {e}")
            break

        # Parse raw list of (title, link, date_str)
        ann = parse_announcement_list(soup)
        if not ann:
            break

        # Process in descending order
        for title, link, pub_date in ann:
            # 1) If the date is before the start date, we're done
            # 2) If the date is after the end date, skip
            # 3) Otherwise, fetch the detail and save it

            # Check if we are within the date range
            if pub_date < start_date:
                done = True
                break
            if pub_date > end_date:
                continue

            # Fetch the detail
            body = fetch_detail(session=session, link=link)
            data.append({
                "title": title,
                "url": link,
                "date": pub_date.isoformat(),
                "body": body,
            })

            # To be polite
            time.sleep(0.5)

        page += 1
        time.sleep(1)

    # Write the data to JSON files
    filename = f"okx_announcements_{start_date.date()}_{end_date.date()}.json"
    write_json_file(data, filename, out_folder)

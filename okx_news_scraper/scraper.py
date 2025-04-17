import os
import re
import time
import logging
from datetime import datetime
from dateutil import parser as dateparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
BASE_URL = "https://www.okx.com/help/category/announcements"

def fetch_page(page: int = 1) -> BeautifulSoup:
    resp = requests.get(f"{BASE_URL}?page={page}", timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_announcement_list(soup: BeautifulSoup):
    """Return list of (title, url, date_str)."""
    items = []
    for el in soup.select("li[class^='index_articleItem__']"):
        a = el.find("a", href=True)
        date_el = el.find("span", class_="date")
        if not a or not date_el:
            continue
        title = a.get_text(strip=True)
        link = "https://www.okx.com" + a["href"]
        date_str = date_el.get_text(strip=True)
        items.append((title, link, date_str))
    return items

def fetch_detail(link: str):
    resp = requests.get(link, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    body_el = soup.select_one("div.article-content")
    return body_el.get_text("\n", strip=True) if body_el else ""

def sanitize_filename(s: str) -> str:
    # slugify-ish: lowercase, replace non-alnum with underscore
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

def scrape(start_date: datetime, end_date: datetime, out_folder: str):
    os.makedirs(out_folder, exist_ok=True)
    page = 1
    done = False

    while not done:
        try:
            soup = fetch_page(page)
        except Exception as e:
            logger.error(f"Failed to fetch page {page}: {e}")
            break

        ann = parse_announcement_list(soup)
        if not ann:
            break

        for title, link, date_str in ann:
            try:
                pub_date = dateparser.parse(date_str)
            except Exception:
                logger.warning(f"Skipping invalid date {date_str}")
                continue

            if pub_date < start_date:
                done = True
                break
            if pub_date > end_date:
                continue

            body = fetch_detail(link)
            data = {
                "title": title,
                "url": link,
                "date": pub_date.isoformat(),
                "body": body,
            }
            fname = f"{pub_date.date()}_{sanitize_filename(title)}.json"
            path = os.path.join(out_folder, fname)
            with open(path, "w", encoding="utf-8") as f:
                import json
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Wrote {path}")
            # be polite
            time.sleep(0.5)

        page += 1
        time.sleep(1)


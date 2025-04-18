import json
import logging
import os
from datetime import datetime
from urllib.parse import urljoin

import requests
from dateutil import parser as dateparser
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger(__name__)
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'  # NOQA
}


def build_url(base_url: str, path: str, page: int = None) -> str:
    """
    Build the URL for the given page number.
    """
    url = urljoin(base_url, path)

    if page:
        url = f"{url}/page/{page}"

    return url


def extract_date(date_str: str) -> datetime:
    """
    Extract the date from the string.
    """
    # Remove the 'Published on ' prefix
    date_str = date_str.replace("Published on ", "")

    # Convert to datetime
    try:
        date_str = dateparser.parse(date_str)
    except Exception as e:
        logger.error(f"Failed to parse date '{date_str}': {e}")
        raise Exception(e)

    return date_str


def write_json_file(
    data: list[dict[str, str]],
    filename: str,
    out_folder: str
) -> None:
    """
    Write the data to a JSON file.
    """
    os.makedirs(out_folder, exist_ok=True)
    path = os.path.join(out_folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved {len(data)} announcements to {path}")


def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=3,                # Max 3 retries
        backoff_factor=1,       # 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],  # Retry only on GET requests
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.headers.update(DEFAULT_HEADERS)
    return session

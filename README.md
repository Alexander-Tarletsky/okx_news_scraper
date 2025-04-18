# OKX News Scraper

**okxnews** is a simple CLI tool to scrape announcements from OKX’s help site
(`https://www.okx.com/help/category/announcements`) between two dates and
save each item as a JSON file.

## Installation in venv (recommended)

```bash
cd okx-news-scraper
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```


## Usage

```bash
okxnews --start 2025-04-01 --end 2025-04-15 --folder ./data
```
This will scrape all announcements between `2025-04-01` and `2025-04-15` and save
them in the `./data` folder. The folder will be created if it does not exist.


## Options
- `--start`: The start date in the format `YYYY-MM-DD`. Default is `2025-04-01`.
- `--end`: The end date in the format `YYYY-MM-DD`. Default is `2025-04-15`.
- `--folder`: The folder to save the JSON files. Default is `./data`.


## Notes
- Does not use any browser automation—pure HTTP scraping.
- Handles network errors and missing HTML gracefully.
- Outputs per‑query JSON named okx_announcement_{start_date}_{end_date}.json.s
- Requires Python 3.7 or later.
- During testing, it was found that `https://www.okx.com/help/category/announcements` endpoint can provide data not sorted by dates. This breaks the search algorithm and makes it impossible to set search boundaries. The current version of the script uses a different endpoint - `https://www.okx.com/help/section/announcements-new-listings`
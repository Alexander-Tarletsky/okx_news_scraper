# OKX News Scraper

**okxnews** is a simple CLI tool to scrape announcements from OKX’s help site
(`https://www.okx.com/help/category/announcements`) between two dates and
save each item as a JSON file.

## Installation

```bash
cd okx-news-scraper
python3 -m pip install .
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
- Outputs per‑announcement JSON named {date}_{slug}.json.
- Uses Python version 3.10 or higher.
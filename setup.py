from setuptools import setup, find_packages

setup(
    name="okx-news-scraper",
    version="0.1.0",
    description="CLI tool to scrape OKX announcements between two dates and save as JSON",
    author="Your Name",
    url="https://github.com/youruser/okx-news-scraper",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
        "beautifulsoup4>=4.6.0",
        "python-dateutil>=2.8.0"
    ],
    entry_points={
        "console_scripts": [
            "okxnews=okx_news_scraper.cli:main"
        ]
    },
    python_requires=">=3.10",
)

import re
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


DEFAULT_BOOKS_URL = "https://books.toscrape.com/catalogue/page-1.html"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def build_page_url(base_url: str, page_number: int) -> str:
    """Replace the page number in a URL so we can crawl multiple pages."""
    if "page-" in base_url:
        return re.sub(r"page-\d+\.html", f"page-{page_number}.html", base_url)
    return base_url


def get_rating_text(article) -> str:
    """Convert the CSS class from the demo website into readable text."""
    rating_classes = article.find("p", class_="star-rating")
    if not rating_classes:
        return "N/A"

    for css_class in rating_classes.get("class", []):
        if css_class in RATING_MAP:
            return f"{RATING_MAP[css_class]}/5 stars"
    return "N/A"


def scrape_books(url: str = DEFAULT_BOOKS_URL, max_pages: int = 2) -> pd.DataFrame:
    """Scrape book data from a simple public practice website."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0 Safari/537.36"
        )
    }

    rows: list[dict] = []

    for page_number in range(1, max_pages + 1):
        page_url = build_page_url(url, page_number)
        response = requests.get(page_url, timeout=15, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        if not products:
            break

        for product in products:
            link_tag = product.select_one("h3 a")
            if link_tag is None:
                continue

            product_name = link_tag.get("title", "Unknown product")
            relative_url = link_tag.get("href", "")
            product_url = urljoin(page_url, relative_url)
            price_text = product.select_one("p.price_color")
            price = price_text.get_text(strip=True) if price_text else "N/A"

            rows.append(
                {
                    "product_name": product_name,
                    "category": "Books",
                    "price": price,
                    "rating": get_rating_text(product),
                    "review_count": "N/A",
                    "product_url": product_url,
                }
            )

    if not rows:
        raise ValueError("Không tìm thấy dữ liệu từ website đã chọn.")

    return pd.DataFrame(rows)

import re
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


DEFAULT_BOOKS_URL = "https://books.toscrape.com/catalogue/page-1.html"
DEFAULT_WEBSCRAPER_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
SUPPORTED_WEBSCRAPER_PATH_PREFIX = "/test-sites/e-commerce/allinone"
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class InvalidScrapeUrlError(ValueError):
    """Được gọi khi người dùng cung cấp một URL nằm ngoài các mục tiêu hỗ trợ."""


def build_page_url(base_url: str, page_number: int) -> str:
    """Thay thế số trang trong URL để có thể quét (crawl) qua nhiều trang."""
    if "page-" in base_url:
        return re.sub(r"page-\d+\.html", f"page-{page_number}.html", base_url)
    return base_url


def detect_source_from_url(url: str) -> str:
    """Trả về khóa nguồn (source key) được hỗ trợ dựa trên tên miền của URL."""
    hostname = (urlparse(url).hostname or "").lower()
    if hostname == "books.toscrape.com":
        return "books_toscrape"
    if hostname == "webscraper.io":
        return "webscraper"
    return "generic"


def get_rating_text(article) -> str:
    """Chuyển đổi lớp CSS từ trang sách mẫu thành văn bản dễ đọc."""
    rating_classes = article.find("p", class_="star-rating")
    if not rating_classes:
        return "N/A"

    for css_class in rating_classes.get("class", []):
        if css_class in RATING_MAP:
            return f"{RATING_MAP[css_class]}/5 stars"
    return "N/A"


def extract_webscraper_rating_text(product_card) -> str:
    """Chuyển đổi tiện ích đánh giá của Web Scraper thành định dạng văn bản dùng chung."""
    rating_block = product_card.select_one(".ratings p[data-rating]")
    if rating_block is None:
        return "N/A"

    rating_value = rating_block.get("data-rating", "").strip()
    if not rating_value.isdigit():
        return "N/A"
    return f"{rating_value}/5 stars"


def validate_webscraper_url(url: str) -> None:
    """Đảm bảo URL trỏ đến một trang danh mục hợp lệ của Web Scraper."""
    parsed = urlparse(url)
    normalized_path = parsed.path.rstrip("/")

    if not normalized_path.startswith(SUPPORTED_WEBSCRAPER_PATH_PREFIX):
        raise InvalidScrapeUrlError(
            "URL webscraper.io chua dung. Hay dung link thuoc "
            "https://webscraper.io/test-sites/e-commerce/allinone/..."
        )

    trailing_path = normalized_path[len(SUPPORTED_WEBSCRAPER_PATH_PREFIX):].strip("/")
    if not trailing_path:
        raise InvalidScrapeUrlError(
            "Hay dan URL category hoac subcategory cua webscraper.io, vi du "
            f"{DEFAULT_WEBSCRAPER_URL}"
        )


def parse_webscraper_products(html: str, page_url: str) -> pd.DataFrame:
    """Phân tích các thẻ sản phẩm từ trang danh mục của Web Scraper."""
    soup = BeautifulSoup(html, "html.parser")
    heading_candidates = [
        heading.get_text(" ", strip=True)
        for heading in soup.select("h1")
        if heading.get_text(" ", strip=True)
    ]
    category_name = heading_candidates[-1] if heading_candidates else "Unknown category"

    rows: list[dict] = []
    for product in soup.select(".card.thumbnail"):
        link_tag = product.select_one("a.title")
        if link_tag is None:
            continue

        price_tag = product.select_one('[itemprop="price"]')
        review_count_tag = product.select_one('[itemprop="reviewCount"]')
        product_name = link_tag.get("title") or link_tag.get_text(strip=True) or "Unknown product"
        relative_url = link_tag.get("href", "")

        rows.append(
            {
                "product_name": product_name,
                "category": category_name,
                "price": price_tag.get_text(strip=True) if price_tag else "N/A",
                "rating": extract_webscraper_rating_text(product),
                "review_count": review_count_tag.get_text(strip=True) if review_count_tag else "N/A",
                "product_url": urljoin(page_url, relative_url),
            }
        )

    if not rows:
        raise ValueError("Khong tim thay san pham tren trang webscraper.io da chon.")
    return pd.DataFrame(rows)


def scrape_books_to_scrape(url: str = DEFAULT_BOOKS_URL, max_pages: int = 2) -> pd.DataFrame:
    """Quét dữ liệu sách từ trang web thực hành books.toscrape.com."""
    rows: list[dict] = []

    for page_number in range(1, max_pages + 1):
        page_url = build_page_url(url, page_number)
        response = requests.get(page_url, timeout=15, headers=REQUEST_HEADERS)
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
        raise ValueError("Khong tim thay du lieu tu website da chon.")

    return pd.DataFrame(rows)


def scrape_webscraper_category(url: str) -> pd.DataFrame:
    """Quét một trang danh mục hoặc danh mục con từ webscraper.io."""
    validate_webscraper_url(url)
    response = requests.get(url, timeout=15, headers=REQUEST_HEADERS)
    response.raise_for_status()
    return parse_webscraper_products(response.text, url)


def scrape_generic_page(url: str) -> pd.DataFrame:
    """Bộ cào dữ liệu đa năng nỗ lực tối đa để quét mọi URL công khai, đáp ứng các yêu cầu thu thập linh hoạt."""
    try:
        response = requests.get(url, timeout=15, headers=REQUEST_HEADERS)
        response.raise_for_status()
    except Exception as e:
        raise InvalidScrapeUrlError(f"Không thể truy cập URL công khai: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    rows = []
    
    # 1. Smarter approach: Find prices first, then find their product cards.
    # This prevents scraping navigation menus that don't have prices.
    price_pattern = re.compile(r'(?:₫|đ|\$|€)?\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*(?:vnđ|vnd|đ|\$|€|usd)', re.IGNORECASE)
    
    processed_containers = set()
    
    # Search for all text nodes matching a price
    for text_node in soup.find_all(string=price_pattern):
        container = text_node.parent
        depth = 0
        
        # Traverse up the DOM tree to find the product card container
        while container and container.name not in ['body', 'html'] and depth < 6:
            if container in processed_containers:
                break # Already extracted a product from this card
                
            if container.name in ['div', 'li', 'article']:
                links = container.find_all('a')
                if links:
                    title = ""
                    href = ""
                    # Find a link with meaningful text for the title
                    for link in links:
                        link_text = link.get_text(strip=True)
                        if len(link_text) > 5:
                            title = link_text
                            href = link.get("href")
                            break
                    
                    # Fallback to image alt text if links are images only
                    if not title:
                        for img in container.find_all('img'):
                            alt = img.get('alt', '').strip()
                            if len(alt) > 5:
                                title = alt
                                href = links[0].get("href")
                                break
                                
                    if title and href:
                        price_match = price_pattern.search(container.get_text(separator=' '))
                        price = price_match.group(0).strip() if price_match else "N/A"
                        
                        rows.append({
                            "product_name": title[:100],
                            "category": "Generic Product",
                            "price": price,
                            "rating": "N/A",
                            "review_count": "N/A",
                            "product_url": urljoin(url, href),
                        })
                        
                        processed_containers.add(container)
                        break # Found a valid product, move to the next text node
                        
            container = container.parent
            depth += 1

    # 2. Fallback: If no prices were found, try finding headings
    if not rows:
        headings = soup.find_all(['h2', 'h3'])
        for h in headings:
            text = h.get_text(strip=True)
            if not text or len(text) < 5: continue
            
            link = h.find('a')
            href = link.get("href") if link else ""
            
            rows.append({
                "product_name": text[:100],
                "category": f"Heading {h.name.upper()}",
                "price": "N/A",
                "rating": "N/A",
                "review_count": "N/A",
                "product_url": urljoin(url, href) if href else url,
            })
            
    # 3. Final fallback: Just the page title
    if not rows:
        title = soup.title.string if soup.title else "Unknown Page"
        rows.append({
            "product_name": title[:100],
            "category": "Generic Page",
            "price": "N/A",
            "rating": "N/A",
            "review_count": "N/A",
            "product_url": url,
        })
        
    return pd.DataFrame(rows[:100])


def scrape_books(url: str = DEFAULT_BOOKS_URL, max_pages: int = 2) -> pd.DataFrame:
    """Quét sản phẩm từ các trang web hỗ trợ."""
    source = detect_source_from_url(url)
    if source == "books_toscrape":
        return scrape_books_to_scrape(url=url, max_pages=max_pages)
    if source == "webscraper":
        return scrape_webscraper_category(url=url)
    if source == "generic":
        return scrape_generic_page(url=url)

    raise InvalidScrapeUrlError("Khong the xac dinh website de crawl.")

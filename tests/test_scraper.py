from textwrap import dedent

import pytest

from scraper import (
    InvalidScrapeUrlError,
    detect_source_from_url,
    parse_webscraper_products,
    scrape_books,
)


WEBSCRAPER_SAMPLE_HTML = dedent(
    """
    <html>
      <body>
        <h1>Computers / Laptops</h1>
        <div class="card thumbnail" itemscope itemtype="https://schema.org/Product">
          <div class="product-wrapper card-body">
            <div class="caption">
              <h4 class="price float-end card-title pull-right" itemprop="offers">
                <span itemprop="price">$679</span>
              </h4>
              <h4>
                <a class="title" href="/test-sites/e-commerce/allinone/product/518" title="Dell Inspiron 15">
                  Dell Inspiron 15
                </a>
              </h4>
            </div>
            <div class="ratings" itemprop="aggregateRating">
              <p class="review-count float-end">
                <span itemprop="reviewCount">7</span> reviews
              </p>
              <p data-rating="4"></p>
            </div>
          </div>
        </div>
        <div class="card thumbnail" itemscope itemtype="https://schema.org/Product">
          <div class="product-wrapper card-body">
            <div class="caption">
              <h4 class="price float-end card-title pull-right" itemprop="offers">
                <span itemprop="price">$745.99</span>
              </h4>
              <h4>
                <a class="title" href="/test-sites/e-commerce/allinone/product/519" title="Inspiron 15">
                  Inspiron 15
                </a>
              </h4>
            </div>
            <div class="ratings" itemprop="aggregateRating">
              <p class="review-count float-end">
                <span itemprop="reviewCount">12</span> reviews
              </p>
              <p data-rating="5"></p>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
).strip()


class DummyResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


def test_detect_source_from_url_supports_books_and_webscraper() -> None:
    assert detect_source_from_url("https://books.toscrape.com/catalogue/page-1.html") == "books_toscrape"
    assert (
        detect_source_from_url("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
        == "webscraper"
    )


def test_parse_webscraper_products_maps_schema() -> None:
    df = parse_webscraper_products(
        WEBSCRAPER_SAMPLE_HTML,
        "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
    )

    assert list(df.columns) == [
        "product_name",
        "category",
        "price",
        "rating",
        "review_count",
        "product_url",
    ]
    assert len(df) == 2
    assert df.iloc[0].to_dict() == {
        "product_name": "Dell Inspiron 15",
        "category": "Computers / Laptops",
        "price": "$679",
        "rating": "4/5 stars",
        "review_count": "7",
        "product_url": "https://webscraper.io/test-sites/e-commerce/allinone/product/518",
    }
    assert df.iloc[1]["rating"] == "5/5 stars"


def test_scrape_books_rejects_webscraper_landing_page() -> None:
    with pytest.raises(InvalidScrapeUrlError):
        scrape_books("https://webscraper.io/test-sites/e-commerce/allinone", max_pages=3)


def test_scrape_books_routes_webscraper_category(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_get(url: str, timeout: int, headers: dict[str, str]) -> DummyResponse:
        calls.append(url)
        assert timeout == 15
        assert "User-Agent" in headers
        return DummyResponse(WEBSCRAPER_SAMPLE_HTML)

    monkeypatch.setattr("scraper.requests.get", fake_get)

    df = scrape_books(
        "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
        max_pages=3,
    )

    assert len(calls) == 1
    assert len(df) == 2

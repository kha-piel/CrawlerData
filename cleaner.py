import re
import unicodedata

import pandas as pd


MISSING_MARKERS = {
    "",
    "n/a",
    "na",
    "none",
    "null",
    "nan",
    "dang cap nhat",
    "lien he",
    "khong ro",
    "not available",
}

RATING_WORD_MAP = {
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0,
}


def remove_accents(text: str) -> str:
    """Remove accents to compare Vietnamese text more easily."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(value):
    """Trim spaces and convert common missing markers to null."""
    if pd.isna(value):
        return pd.NA

    text = re.sub(r"\s+", " ", str(value)).strip()
    plain_text = remove_accents(text.lower())

    if plain_text in MISSING_MARKERS:
        return pd.NA
    return text


def normalize_name(value):
    """Clean product names without changing the meaning too much."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA
    return text


def normalize_category(value):
    """Keep categories readable and consistent."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA
    return text.title()


def parse_price(value):
    """Convert text prices like 12.500.000đ or £51.77 into numbers."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA

    raw_text = str(text)
    lower_text = raw_text.lower()
    is_vnd = any(marker in lower_text for marker in ["đ", "vnd", "vnđ"])

    number_text = re.sub(r"[^\d,\.]", "", raw_text)
    if not number_text:
        return pd.NA

    if is_vnd:
        digits_only = re.sub(r"[^\d]", "", number_text)
        return float(digits_only) if digits_only else pd.NA

    if "," in number_text and "." in number_text:
        if number_text.rfind(".") > number_text.rfind(","):
            normalized = number_text.replace(",", "")
        else:
            normalized = number_text.replace(".", "").replace(",", ".")
    elif "," in number_text:
        parts = number_text.split(",")
        if len(parts[-1]) == 3:
            normalized = "".join(parts)
        else:
            normalized = number_text.replace(",", ".")
    elif "." in number_text:
        parts = number_text.split(".")
        if len(parts) > 1 and all(len(part) == 3 for part in parts[1:]):
            normalized = "".join(parts)
        else:
            normalized = number_text
    else:
        normalized = number_text

    try:
        return float(normalized)
    except ValueError:
        return pd.NA


def parse_rating(value):
    """Convert rating strings such as 4.5/5 sao or Three into numbers."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA

    lower_text = str(text).lower()
    if lower_text in RATING_WORD_MAP:
        return RATING_WORD_MAP[lower_text]

    match = re.search(r"(\d+(?:[.,]\d+)?)", lower_text)
    if not match:
        return pd.NA

    rating_text = match.group(1).replace(",", ".")
    try:
        return float(rating_text)
    except ValueError:
        return pd.NA


def parse_review_count(value):
    """Extract the number of reviews from free-text strings."""
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA

    digits = re.findall(r"\d+", str(text))
    if not digits:
        return pd.NA
    return int("".join(digits))


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply basic data cleaning steps for first-year students."""
    cleaned_df = df.copy()
    rows_before = len(cleaned_df)

    if "product_name" in cleaned_df.columns:
        cleaned_df["product_name"] = cleaned_df["product_name"].apply(normalize_name)

    if "category" in cleaned_df.columns:
        cleaned_df["category"] = cleaned_df["category"].apply(normalize_category)

    if "product_url" in cleaned_df.columns:
        cleaned_df["product_url"] = cleaned_df["product_url"].apply(normalize_text)

    if "price" in cleaned_df.columns:
        cleaned_df["price"] = cleaned_df["price"].apply(parse_price)

    if "rating" in cleaned_df.columns:
        cleaned_df["rating"] = cleaned_df["rating"].apply(parse_rating)

    if "review_count" in cleaned_df.columns:
        cleaned_df["review_count"] = cleaned_df["review_count"].apply(parse_review_count)
        cleaned_df["review_count"] = pd.to_numeric(
            cleaned_df["review_count"], errors="coerce"
        ).astype("Int64")

    duplicate_rows_removed = int(cleaned_df.duplicated().sum())
    cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

    if "price" in cleaned_df.columns:
        cleaned_df["price"] = pd.to_numeric(cleaned_df["price"], errors="coerce")

    if "rating" in cleaned_df.columns:
        cleaned_df["rating"] = pd.to_numeric(cleaned_df["rating"], errors="coerce")

    report = {
        "rows_before": rows_before,
        "rows_after": len(cleaned_df),
        "duplicate_rows_removed": duplicate_rows_removed,
        "missing_rows_after_cleaning": int(cleaned_df.isna().any(axis=1).sum()),
    }
    return cleaned_df, report

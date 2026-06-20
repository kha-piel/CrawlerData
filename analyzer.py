import pandas as pd

from storage import SUMMARY_REPORT_PATH, save_dataframe


def safe_stat(series: pd.Series, function_name: str):
    """Thực thi một phép toán thống kê pandas một cách an toàn, trả về None nếu không có dữ liệu."""
    non_null_series = series.dropna()
    if non_null_series.empty:
        return None
    return getattr(non_null_series, function_name)()


def analyze_data(df: pd.DataFrame) -> dict:
    """Tạo ra các chỉ số tổng quan và các bảng dữ liệu sẵn sàng để vẽ biểu đồ."""
    if df.empty:
        raise ValueError("Dữ liệu sạch đang rỗng, không thể phân tích.")

    stats = {
        "total_records": int(len(df)),
        "total_categories": int(df["category"].nunique(dropna=True)) if "category" in df.columns else 0,
        "missing_rows": int(df.isna().any(axis=1).sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "average_price": safe_stat(df["price"], "mean") if "price" in df.columns else None,
        "max_price": safe_stat(df["price"], "max") if "price" in df.columns else None,
        "min_price": safe_stat(df["price"], "min") if "price" in df.columns else None,
        "average_rating": safe_stat(df["rating"], "mean") if "rating" in df.columns else None,
        "most_expensive_item": None,
        "highest_rated_item": None,
    }

    top_5_by_price = pd.DataFrame()
    if {"product_name", "price"}.issubset(df.columns):
        top_5_by_price = df.sort_values(by="price", ascending=False).head(5)
        valid_price_df = df.dropna(subset=["price"])
        if not valid_price_df.empty:
            stats["most_expensive_item"] = valid_price_df.loc[
                valid_price_df["price"].idxmax(), "product_name"
            ]

    top_5_by_rating = pd.DataFrame()
    if {"product_name", "rating"}.issubset(df.columns):
        top_5_by_rating = df.sort_values(by="rating", ascending=False).head(5)
        valid_rating_df = df.dropna(subset=["rating"])
        if not valid_rating_df.empty:
            stats["highest_rated_item"] = valid_rating_df.loc[
                valid_rating_df["rating"].idxmax(), "product_name"
            ]

    category_counts = pd.DataFrame()
    average_price_by_category = pd.DataFrame()

    if "category" in df.columns:
        category_counts = (
            df["category"]
            .fillna("Chưa phân loại")
            .value_counts()
            .reset_index()
        )
        category_counts.columns = ["category", "count"]

        if "price" in df.columns:
            average_price_by_category = (
                df.dropna(subset=["category", "price"])
                .groupby("category", as_index=False)["price"]
                .mean()
                .rename(columns={"price": "average_price"})
            )

    summary_df = pd.DataFrame(
        [
            {"metric": "Tổng bản ghi", "value": stats["total_records"]},
            {"metric": "Tổng danh mục", "value": stats["total_categories"]},
            {"metric": "Số dòng thiếu dữ liệu", "value": stats["missing_rows"]},
            {"metric": "Số dòng trùng trong dữ liệu sạch", "value": stats["duplicate_rows"]},
            {"metric": "Giá trung bình", "value": stats["average_price"]},
            {"metric": "Giá cao nhất", "value": stats["max_price"]},
            {"metric": "Giá thấp nhất", "value": stats["min_price"]},
            {"metric": "Rating trung bình", "value": stats["average_rating"]},
            {"metric": "Sản phẩm giá cao nhất", "value": stats["most_expensive_item"]},
            {"metric": "Sản phẩm rating cao nhất", "value": stats["highest_rated_item"]},
        ]
    )

    return {
        "stats": stats,
        "top_5_by_price": top_5_by_price,
        "top_5_by_rating": top_5_by_rating,
        "category_counts": category_counts,
        "average_price_by_category": average_price_by_category,
        "summary_df": summary_df,
    }


def save_summary_report(summary_df: pd.DataFrame) -> None:
    """Lưu báo cáo tổng quan vào tệp CSV."""
    save_dataframe(summary_df, SUMMARY_REPORT_PATH)

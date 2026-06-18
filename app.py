from pathlib import Path

import plotly.express as px
import streamlit as st

from analyzer import analyze_data, save_summary_report
from cleaner import clean_dataframe
from sample_data import create_sample_dataframe, save_sample_data
from scraper import DEFAULT_BOOKS_URL, scrape_books
from storage import (
    CLEAN_DATA_PATH,
    RAW_DATA_PATH,
    SAMPLE_DATA_PATH,
    SUMMARY_REPORT_PATH,
    dataframe_to_csv_bytes,
    ensure_directories,
    load_dataframe,
    save_dataframe,
)


st.set_page_config(
    page_title="Data Scraper, Cleaner & Tracker",
    page_icon="📊",
    layout="wide",
)


def initialize_files() -> None:
    """Create folders and sample data on the first run."""
    ensure_directories()
    if not SAMPLE_DATA_PATH.exists():
        save_sample_data()


def initialize_session_state() -> None:
    """Prepare session variables used by the Streamlit app."""
    defaults = {
        "raw_df": None,
        "clean_df": None,
        "analysis": None,
        "cleaning_report": None,
        "source_note": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_after_new_raw_data() -> None:
    """When raw data changes, old clean/analyze results should be cleared."""
    st.session_state["clean_df"] = None
    st.session_state["analysis"] = None
    st.session_state["cleaning_report"] = None


def reset_all_data() -> None:
    """Clear all session state data and delete saved CSV files to start fresh."""
    for key in ["raw_df", "clean_df", "analysis", "cleaning_report"]:
        st.session_state[key] = None
    st.session_state["source_note"] = "Ứng dụng đã được làm mới, dữ liệu trống."
    for path in [RAW_DATA_PATH, CLEAN_DATA_PATH, SUMMARY_REPORT_PATH]:
        if path.exists():
            path.unlink()


def load_sample_data_to_raw() -> None:
    """Use offline sample data and save it as the current raw dataset."""
    sample_df = create_sample_dataframe()
    save_sample_data()
    save_dataframe(sample_df, RAW_DATA_PATH)
    st.session_state["raw_df"] = sample_df
    st.session_state["source_note"] = "Đang dùng dữ liệu mẫu để demo offline."
    reset_after_new_raw_data()


def crawl_data(target_url: str, max_pages: int) -> None:
    """Crawl public data. If the website fails, switch to sample data."""
    try:
        with st.spinner("Đang cào dữ liệu từ trang web, vui lòng chờ..."):
            raw_df = scrape_books(url=target_url, max_pages=max_pages)
        save_dataframe(raw_df, RAW_DATA_PATH)
        st.session_state["raw_df"] = raw_df
        st.session_state["source_note"] = (
            f"Crawl dữ liệu thành công từ {target_url}."
        )
        reset_after_new_raw_data()
        st.success("Đã crawl dữ liệu và lưu vào data/raw_data.csv.")
    except Exception as error:
        load_sample_data_to_raw()
        st.warning(
            "Website không phản hồi hoặc cấu trúc đã thay đổi. "
            "Hệ thống tự chuyển sang dữ liệu mẫu.\n\n"
            f"Chi tiết lỗi: {error}"
        )


def clean_current_data() -> None:
    """Read raw data, clean it, then save clean_data.csv."""
    try:
        raw_df = st.session_state["raw_df"]
        if raw_df is None:
            raw_df = load_dataframe(RAW_DATA_PATH)
            st.session_state["raw_df"] = raw_df

        clean_df, cleaning_report = clean_dataframe(raw_df)
        save_dataframe(clean_df, CLEAN_DATA_PATH)

        st.session_state["clean_df"] = clean_df
        st.session_state["cleaning_report"] = cleaning_report
        st.session_state["analysis"] = None

        st.success("Làm sạch dữ liệu thành công và đã lưu vào data/clean_data.csv.")
    except FileNotFoundError:
        st.error("Chưa có raw_data.csv. Hãy bấm 'Crawl Data' hoặc 'Use Sample Data' trước.")
    except Exception as error:
        st.error(f"Không thể làm sạch dữ liệu: {error}")


def analyze_current_data() -> None:
    """Read clean data, compute summary statistics, and save a report."""
    try:
        clean_df = st.session_state["clean_df"]
        if clean_df is None:
            clean_df = load_dataframe(CLEAN_DATA_PATH)
            st.session_state["clean_df"] = clean_df

        analysis = analyze_data(clean_df)
        save_summary_report(analysis["summary_df"])
        st.session_state["analysis"] = analysis

        st.success("Phân tích dữ liệu thành công và đã lưu báo cáo summary_report.csv.")
    except FileNotFoundError:
        st.error("Chưa có clean_data.csv. Hãy bấm 'Clean Data' trước.")
    except Exception as error:
        st.error(f"Không thể phân tích dữ liệu: {error}")


def format_number(value: float | int | None) -> str:
    """Format numbers for metric cards."""
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def render_download_buttons() -> None:
    """Show CSV download buttons in the sidebar."""
    st.sidebar.markdown("### Tải dữ liệu")

    raw_df = st.session_state["raw_df"]
    if raw_df is not None:
        st.sidebar.download_button(
            label="Download raw_data.csv",
            data=dataframe_to_csv_bytes(raw_df),
            file_name="raw_data.csv",
            mime="text/csv",
        )

    clean_df = st.session_state["clean_df"]
    if clean_df is not None:
        st.sidebar.download_button(
            label="Download clean_data.csv",
            data=dataframe_to_csv_bytes(clean_df),
            file_name="clean_data.csv",
            mime="text/csv",
        )

    analysis = st.session_state["analysis"]
    if analysis is not None:
        st.sidebar.download_button(
            label="Download summary_report.csv",
            data=dataframe_to_csv_bytes(analysis["summary_df"]),
            file_name="summary_report.csv",
            mime="text/csv",
        )


def render_cleaning_report() -> None:
    """Display short information about the cleaning step."""
    report = st.session_state["cleaning_report"]
    if not report:
        return

    st.subheader("Báo cáo làm sạch dữ liệu")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Số dòng ban đầu", format_number(report["rows_before"]))
    col2.metric("Số dòng sau làm sạch", format_number(report["rows_after"]))
    col3.metric("Dòng trùng đã xóa", format_number(report["duplicate_rows_removed"]))
    col4.metric("Dòng còn thiếu dữ liệu", format_number(report["missing_rows_after_cleaning"]))


def render_analysis() -> None:
    """Display metric cards and charts from the analysis step."""
    analysis = st.session_state["analysis"]
    if not analysis:
        return

    st.subheader("Thống kê cơ bản")
    stats = analysis["stats"]

    row1 = st.columns(4)
    row1[0].metric("Tổng bản ghi", format_number(stats["total_records"]))
    row1[1].metric("Tổng danh mục", format_number(stats["total_categories"]))
    row1[2].metric("Giá trung bình", format_number(stats["average_price"]))
    row1[3].metric("Rating trung bình", format_number(stats["average_rating"]))

    row2 = st.columns(4)
    row2[0].metric("Giá cao nhất", format_number(stats["max_price"]))
    row2[1].metric("Giá thấp nhất", format_number(stats["min_price"]))
    row2[2].metric("Dòng thiếu dữ liệu", format_number(stats["missing_rows"]))
    row2[3].metric("Dòng trùng trong dữ liệu sạch", format_number(stats["duplicate_rows"]))

    if stats["most_expensive_item"]:
        st.info(f"Sản phẩm có giá cao nhất: {stats['most_expensive_item']}")
    if stats["highest_rated_item"]:
        st.info(f"Sản phẩm có rating cao nhất: {stats['highest_rated_item']}")

    st.subheader("Top 5 sản phẩm theo giá")
    st.dataframe(analysis["top_5_by_price"], use_container_width=True)

    st.subheader("Top 5 sản phẩm theo rating")
    st.dataframe(analysis["top_5_by_rating"], use_container_width=True)

    top_price_df = analysis["top_5_by_price"]
    if not top_price_df.empty:
        fig_price = px.bar(
            top_price_df,
            x="product_name",
            y="price",
            color="category" if "category" in top_price_df.columns else None,
            title="Top 5 sản phẩm theo giá",
        )
        st.plotly_chart(fig_price, use_container_width=True)

    category_count_df = analysis["category_counts"]
    if not category_count_df.empty:
        fig_category = px.bar(
            category_count_df,
            x="category",
            y="count",
            title="Số lượng sản phẩm theo danh mục",
        )
        fig_category.update_xaxes(title_text="")
        st.plotly_chart(fig_category, use_container_width=True)

    average_by_category_df = analysis["average_price_by_category"]
    if not average_by_category_df.empty:
        fig_average = px.bar(
            average_by_category_df,
            x="category",
            y="average_price",
            title="Giá trung bình theo danh mục",
        )
        fig_average.update_xaxes(title_text="")
        st.plotly_chart(fig_average, use_container_width=True)


def main() -> None:
    initialize_files()
    initialize_session_state()

    st.title("Data Scraper, Cleaner & Tracker")
    st.caption(
        "Công cụ tự động hóa thu thập, làm sạch và theo dõi dữ liệu cơ bản "
        "phù hợp cho sinh viên năm nhất ngành Công nghệ thông tin/Data Science."
    )

    st.sidebar.header("Điều khiển")
    st.sidebar.markdown(
        "- Nguồn dữ liệu công khai, hợp pháp\n"
        "- Có dữ liệu mẫu để demo offline\n"
        "- Quy trình: Crawl -> Clean -> Analyze -> Download"
    )

    default_url = st.sidebar.text_input("URL công khai", value=DEFAULT_BOOKS_URL)
    max_pages = st.sidebar.slider("Số trang cần crawl", min_value=1, max_value=3, value=2)

    col1, col2 = st.sidebar.columns(2)
    if col1.button("Crawl Data", use_container_width=True):
        crawl_data(default_url, max_pages)

    if col2.button("Sample Data", use_container_width=True):
        try:
            load_sample_data_to_raw()
            st.success("Đã nạp dữ liệu mẫu và lưu vào data/raw_data.csv.")
        except Exception as error:
            st.error(f"Không thể nạp dữ liệu mẫu: {error}")

    if st.sidebar.button("Clean Data", use_container_width=True):
        clean_current_data()

    if st.sidebar.button("Analyze Data", use_container_width=True):
        analyze_current_data()

    render_download_buttons()

    st.sidebar.markdown("---")
    if st.sidebar.button("Làm mới ứng dụng", type="primary", use_container_width=True):
        reset_all_data()
        st.rerun()

    if st.session_state["source_note"]:
        st.info(st.session_state["source_note"])

    raw_df = st.session_state["raw_df"]
    if raw_df is None and RAW_DATA_PATH.exists():
        raw_df = load_dataframe(RAW_DATA_PATH)
        st.session_state["raw_df"] = raw_df

    clean_df = st.session_state["clean_df"]
    if clean_df is None and CLEAN_DATA_PATH.exists():
        clean_df = load_dataframe(CLEAN_DATA_PATH)
        st.session_state["clean_df"] = clean_df

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Dữ liệu thô")
        if raw_df is not None:
            st.dataframe(raw_df, use_container_width=True, height=360)
        else:
            st.info("Chưa có dữ liệu thô. Hãy crawl dữ liệu hoặc dùng dữ liệu mẫu.")

    with right_column:
        st.subheader("Dữ liệu sau làm sạch")
        if clean_df is not None:
            st.dataframe(clean_df, use_container_width=True, height=360)
        else:
            st.info("Chưa có dữ liệu sạch. Hãy bấm 'Clean Data' sau khi có raw data.")

    render_cleaning_report()
    render_analysis()

    st.markdown("---")
    st.markdown(
        "Nhóm thực hiện: Trần Đức Bá Linh và Nguyễn Phú Kha | Môn học: Python| Năm học: 2026"
    )
    st.markdown(
        f"Tài liệu tham khảo trong repo: "
        f"`{Path('docs/project_report_vi.md')}`, "
        f"`{Path('docs/demo_script_vi.md')}`, "
        f"`{Path('docs/slides_outline_vi.md')}`"
    )


if __name__ == "__main__":
    main()

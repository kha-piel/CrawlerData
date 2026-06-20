import plotly.express as px
import streamlit as st
import importlib
import textwrap

import scraper as scraper_module
importlib.reload(scraper_module)

from analyzer import analyze_data, save_summary_report
from cleaner import clean_dataframe
from sample_data import create_sample_dataframe, save_sample_data
from storage import CLEAN_DATA_PATH, RAW_DATA_PATH, SAMPLE_DATA_PATH, SUMMARY_REPORT_PATH, dataframe_to_csv_bytes, ensure_directories, load_dataframe, save_dataframe


DEFAULT_BOOKS_URL = scraper_module.DEFAULT_BOOKS_URL
DEFAULT_WEBSCRAPER_URL = getattr(
    scraper_module,
    "DEFAULT_WEBSCRAPER_URL",
    "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
)
SCRAPE_URL_ERROR = getattr(scraper_module, "InvalidScrapeUrlError", ValueError)
scrape_books = scraper_module.scrape_books


st.set_page_config(
    page_title="Crawler Data Studio",
    page_icon="📊",
    layout="wide",
)


def inject_styles() -> None:
    """Áp dụng hệ thống giao diện tùy chỉnh cho bảng điều khiển Streamlit."""
    st.markdown(
        textwrap.dedent("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            :root {
                --bg: #f8fafc;
                --surface: #ffffff;
                --surface-strong: #ffffff;
                --ink: #0f172a;
                --muted: #64748b;
                --line: #e2e8f0;
                --accent: #2563eb;
                --accent-deep: #1e3a8a;
                --success: #059669;
                --warning: #d97706;
                --danger: #dc2626;
                --radius-md: 12px;
                --radius-lg: 16px;
                --radius-xl: 24px;
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }

            .stApp {
                background-color: var(--bg);
                color: var(--ink);
                font-family: "Inter", sans-serif;
            }

            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1280px;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: "Inter", sans-serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em;
                color: var(--ink) !important;
            }

            p, div, span, li {
                font-family: "Inter", sans-serif;
            }
            
            /* Fix the silly fonts issue inside Streamlit components */
            .stMarkdown, .stText {
                font-family: "Inter", sans-serif !important;
            }

            [data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid var(--line);
            }

            [data-testid="stSidebar"] hr {
                border-color: var(--line);
                margin: 1.5rem 0;
            }

            .hero-panel {
                padding: 2.5rem;
                border: 1px solid var(--line);
                border-radius: var(--radius-xl);
                background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
                box-shadow: var(--shadow-md);
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
            }

            .hero-panel::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, var(--accent), #60a5fa);
            }

            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.1em;
                font-size: 0.875rem;
                font-weight: 700;
                color: var(--accent);
                margin-bottom: 1rem;
            }

            .hero-title {
                font-size: clamp(1.75rem, 3vw, 2.5rem);
                line-height: 1.2;
                font-weight: 800;
                margin: 0;
                color: var(--ink);
            }

            .hero-body {
                max-width: 800px;
                margin-top: 1rem;
                font-size: 1.125rem;
                line-height: 1.6;
                color: var(--muted);
            }

            .pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-top: 1.5rem;
            }

            .pill {
                padding: 0.5rem 1rem;
                border-radius: 9999px;
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                font-size: 0.875rem;
                color: var(--accent-deep);
                font-weight: 600;
            }

            .section-card {
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                box-shadow: var(--shadow-sm);
                margin-bottom: 1.5rem;
            }

            .kpi-card {
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: var(--radius-lg);
                padding: 1.25rem;
                min-height: 130px;
                box-shadow: var(--shadow-sm);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .kpi-card:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-md);
                border-color: #cbd5e1;
            }

            .kpi-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-weight: 600;
                color: var(--muted);
                margin-bottom: 0.5rem;
            }

            .kpi-value {
                font-size: 2rem;
                font-weight: 700;
                line-height: 1.2;
                color: var(--ink);
                margin-bottom: 0.5rem;
            }

            .kpi-note {
                color: var(--muted);
                font-size: 0.875rem;
                line-height: 1.4;
            }

            .stage-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }

            .stage-card {
                padding: 1.25rem;
                border-radius: var(--radius-md);
                background: var(--bg);
                border: 1px solid var(--line);
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .stage-name {
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--muted);
            }

            .stage-status {
                margin-top: 0.5rem;
                font-size: 1.125rem;
                font-weight: 700;
                color: var(--ink);
            }

            .stage-detail {
                margin-top: 0.25rem;
                color: var(--muted);
                font-size: 0.875rem;
            }

            .micro-title {
                font-size: 1rem;
                font-weight: 600;
                color: var(--ink);
                margin-bottom: 1rem;
                margin-top: 0.5rem;
            }

            .insight-banner {
                border-left: 4px solid var(--accent);
                padding: 1rem 1.25rem;
                border-radius: 0 var(--radius-md) var(--radius-md) 0;
                background: #eff6ff;
                margin-bottom: 1.5rem;
                color: var(--accent-deep);
                font-size: 0.95rem;
                line-height: 1.5;
            }

            .export-card {
                border-radius: var(--radius-lg);
                background: var(--surface);
                border: 1px solid var(--line);
                padding: 1.25rem;
                min-height: 120px;
                box-shadow: var(--shadow-sm);
                margin-bottom: 1rem;
            }

            div[data-testid="stDataFrame"],
            div[data-testid="stPlotlyChart"] {
                border-radius: var(--radius-md);
                border: 1px solid var(--line);
                overflow: hidden;
                background: var(--surface);
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 1rem;
                border-bottom: 1px solid var(--line);
                padding-bottom: 0px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 0.75rem 0.5rem;
                border: none;
                background: transparent;
                color: var(--muted);
                font-weight: 500;
            }

            .stTabs [aria-selected="true"] {
                color: var(--accent) !important;
                border-bottom: 2px solid var(--accent) !important;
                background: transparent !important;
            }

            .stButton > button {
                border-radius: var(--radius-md);
                border: 1px solid var(--line);
                padding: 0.5rem 1rem;
                font-weight: 600;
                background: #ffffff;
                color: var(--ink);
                transition: all 0.2s ease;
                box-shadow: var(--shadow-sm);
            }

            .stButton > button:hover {
                border-color: var(--accent);
                color: var(--accent);
                background: #f8fafc;
            }

            /* Primary action button style (can be applied to specific buttons using columns if needed) */
            .stButton > button[kind="primary"] {
                background: var(--accent);
                color: white;
                border: none;
            }
            
            .stButton > button[kind="primary"]:hover {
                background: var(--accent-deep);
                color: white;
            }

            .stDownloadButton > button {
                border-radius: var(--radius-md);
                border: none;
                padding: 0.6rem 1rem;
                font-weight: 600;
                background: var(--accent);
                color: white;
                width: 100%;
                transition: background 0.2s ease;
            }

            .stDownloadButton > button:hover {
                background: var(--accent-deep);
                color: white;
            }

            .footer-note {
                margin-top: 3rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--line);
                color: var(--muted);
                font-size: 0.875rem;
                text-align: center;
            }
            </style>
        """),
        unsafe_allow_html=True,
    )


def initialize_files() -> None:
    """Tạo thư mục và dữ liệu mẫu trong lần chạy đầu tiên."""
    ensure_directories()
    if not SAMPLE_DATA_PATH.exists():
        save_sample_data()


def initialize_session_state() -> None:
    """Chuẩn bị các biến phiên (session) được dùng bởi ứng dụng Streamlit."""
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
    """Khi dữ liệu thô thay đổi, các kết quả làm sạch/phân tích cũ phải được xóa bỏ."""
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
    """Sử dụng dữ liệu mẫu offline và lưu nó làm tập dữ liệu thô hiện tại."""
    sample_df = create_sample_dataframe()
    save_sample_data()
    save_dataframe(sample_df, RAW_DATA_PATH)
    st.session_state["raw_df"] = sample_df
    st.session_state["source_note"] = "Đang dùng dữ liệu mẫu để demo offline."
    reset_after_new_raw_data()


def crawl_data(target_url: str, max_pages: int) -> None:
    """Cào dữ liệu công khai. Hiện lỗi với URL không hợp lệ; dùng dữ liệu mẫu nếu trang web lỗi."""
    try:
        with st.spinner("Đang cào dữ liệu từ trang web, vui lòng chờ..."):
            raw_df = scrape_books(url=target_url, max_pages=max_pages)
        save_dataframe(raw_df, RAW_DATA_PATH)
        st.session_state["raw_df"] = raw_df
        st.session_state["source_note"] = f"Crawl dữ liệu thành công từ {target_url}."
        reset_after_new_raw_data()
        st.success("Đã crawl dữ liệu và lưu vào data/raw_data.csv.")
    except SCRAPE_URL_ERROR as error:
        st.error(str(error))
    except Exception as error:
        load_sample_data_to_raw()
        st.warning(
            "Website không phản hồi hoặc cấu trúc đã thay đổi. "
            "Hệ thống tự chuyển sang dữ liệu mẫu.\n\n"
            f"Chi tiết lỗi: {error}"
        )


def clean_current_data() -> None:
    """Đọc dữ liệu thô, làm sạch nó, sau đó lưu thành clean_data.csv."""
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
    """Đọc dữ liệu sạch, tính toán các chỉ số thống kê và lưu báo cáo."""
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
    """Định dạng số để hiển thị trên các thẻ (cards)."""
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def stage_card(title: str, active: bool, detail: str) -> str:
    """Hiển thị một thẻ trạng thái của pipeline."""
    status = "Sẵn sàng" if active else "Chưa có dữ liệu"
    return textwrap.dedent(f"""
        <div class="stage-card">
          <div class="stage-name">{title}</div>
          <div class="stage-status">{status}</div>
          <div class="stage-detail">{detail}</div>
        </div>
    """)


def render_hero() -> None:
    """Hiển thị phần giới thiệu (hero) ở đầu trang."""
    st.markdown(
        textwrap.dedent("""
            <div class="hero-panel">
              <div class="hero-kicker">Crawler Data Studio</div>
              <h1 class="hero-title">Biến quy trình crawl, làm sạch và phân tích thành một dashboard đủ tự tin để demo.</h1>
              <div class="hero-body">
                Dùng một giao diện rõ ràng hơn để chạy toàn bộ pipeline từ dữ liệu công khai sang insight trực quan.
                App hiện hỗ trợ cả <strong>books.toscrape.com</strong> và <strong>webscraper.io</strong>, kèm dữ liệu mẫu để trình bày offline.
              </div>
              <div class="pill-row">
                <div class="pill">Nguồn dữ liệu công khai</div>
                <div class="pill">Offline fallback</div>
                <div class="pill">CSV export</div>
                <div class="pill">Charts + KPI</div>
              </div>
            </div>
        """),
        unsafe_allow_html=True,
    )


def render_action_bar(default_url: str, max_pages: int) -> None:
    """Hiển thị các nút thao tác chính trên màn hình."""
    st.markdown('<div class="micro-title">Thao tác nhanh</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Crawl Public Data", use_container_width=True, type="primary"):
            crawl_data(default_url, max_pages)
    with col2:
        if st.button("Use Sample Data", use_container_width=True):
            try:
                load_sample_data_to_raw()
                st.success("Đã nạp dữ liệu mẫu và lưu vào data/raw_data.csv.")
            except Exception as error:
                st.error(f"Không thể nạp dữ liệu mẫu: {error}")
    with col3:
        if st.button("Clean Data", use_container_width=True):
            clean_current_data()
    with col4:
        if st.button("Analyze Data", use_container_width=True):
            analyze_current_data()


def render_pipeline_summary(raw_df, clean_df) -> None:
    """Hiển thị tổng quan nhanh về trạng thái pipeline hiện tại."""
    raw_rows = len(raw_df) if raw_df is not None else 0
    clean_rows = len(clean_df) if clean_df is not None else 0
    analysis_ready = st.session_state["analysis"] is not None

    st.markdown('<div class="section-card"><div class="micro-title">Trạng thái pipeline</div><div class="stage-grid">'
                + stage_card("Raw", raw_df is not None, f"{raw_rows} dòng hiện có")
                + stage_card("Clean", clean_df is not None, f"{clean_rows} dòng sau chuẩn hóa")
                + stage_card("Analysis", analysis_ready, "KPI và charts đã sẵn sàng" if analysis_ready else "Chưa phân tích")
                + stage_card("Export", raw_df is not None or clean_df is not None or analysis_ready, "CSV luôn sẵn để tải xuống")
                + "</div></div>", unsafe_allow_html=True)


def render_source_banner() -> None:
    """Hiển thị thông tin nguồn dữ liệu hiện tại khi có sẵn."""
    if st.session_state["source_note"]:
        st.markdown(
            f'<div class="insight-banner"><strong>Nguồn dữ liệu hiện tại</strong><br>{st.session_state["source_note"]}</div>',
            unsafe_allow_html=True,
        )


def render_cleaning_report() -> None:
    """Hiển thị thông tin ngắn gọn về bước làm sạch dữ liệu."""
    report = st.session_state["cleaning_report"]
    if not report:
        st.info("Chưa có báo cáo làm sạch. Hãy chạy bước Clean Data sau khi có dữ liệu thô.")
        return

    st.markdown('<div class="micro-title">Báo cáo làm sạch</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    items = [
        ("Số dòng ban đầu", format_number(report["rows_before"]), "Tập dữ liệu trước khi chuẩn hóa"),
        ("Số dòng sau làm sạch", format_number(report["rows_after"]), "Kết quả cuối cùng dùng để phân tích"),
        ("Dòng trùng đã xóa", format_number(report["duplicate_rows_removed"]), "Loại bỏ bản ghi lặp"),
        ("Dòng còn thiếu dữ liệu", format_number(report["missing_rows_after_cleaning"]), "Cần lưu ý khi diễn giải"),
    ]
    for column, (label, value, note) in zip(cols, items):
        column.markdown(
            textwrap.dedent(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value">{value}</div>
                  <div class="kpi-note">{note}</div>
                </div>
            """),
            unsafe_allow_html=True,
        )


def render_analysis() -> None:
    """Hiển thị thẻ chỉ số và biểu đồ từ bước phân tích."""
    analysis = st.session_state["analysis"]
    if not analysis:
        st.info("Chưa có kết quả phân tích. Hãy chạy bước Analyze Data để mở khóa KPI, bảng xếp hạng và biểu đồ.")
        return

    stats = analysis["stats"]
    st.markdown('<div class="micro-title">Bảng điều khiển phân tích</div>', unsafe_allow_html=True)

    top_row = st.columns(4)
    top_metrics = [
        ("Tổng bản ghi", format_number(stats["total_records"]), "Kích thước dữ liệu sẵn sàng phân tích"),
        ("Tổng danh mục", format_number(stats["total_categories"]), "Độ đa dạng của dữ liệu"),
        ("Giá trung bình", format_number(stats["average_price"]), "Mean price trên dữ liệu sạch"),
        ("Rating trung bình", format_number(stats["average_rating"]), "Điểm đánh giá trung bình"),
    ]
    for column, (label, value, note) in zip(top_row, top_metrics):
        column.markdown(
            textwrap.dedent(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value">{value}</div>
                  <div class="kpi-note">{note}</div>
                </div>
            """),
            unsafe_allow_html=True,
        )

    secondary_row = st.columns(4)
    secondary_metrics = [
        ("Giá cao nhất", format_number(stats["max_price"]), stats["most_expensive_item"] or "Chưa xác định sản phẩm"),
        ("Giá thấp nhất", format_number(stats["min_price"]), "Mốc giá thấp nhất hiện có"),
        ("Dòng thiếu dữ liệu", format_number(stats["missing_rows"]), "Số bản ghi còn giá trị thiếu"),
        ("Dòng trùng", format_number(stats["duplicate_rows"]), "Trùng lặp trong dữ liệu sạch"),
    ]
    for column, (label, value, note) in zip(secondary_row, secondary_metrics):
        column.markdown(
            textwrap.dedent(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value">{value}</div>
                  <div class="kpi-note">{note}</div>
                </div>
            """),
            unsafe_allow_html=True,
        )

    highlight_messages = []
    if stats["most_expensive_item"]:
        highlight_messages.append(f"Sản phẩm giá cao nhất: {stats['most_expensive_item']}")
    if stats["highest_rated_item"]:
        highlight_messages.append(f"Sản phẩm rating cao nhất: {stats['highest_rated_item']}")
    if highlight_messages:
        st.markdown(
            '<div class="insight-banner"><strong>Insight nổi bật</strong><br>'
            + "<br>".join(highlight_messages)
            + "</div>",
            unsafe_allow_html=True,
        )

    table_col, chart_col = st.columns((1.05, 1.35))
    with table_col:
        with st.container(border=True):
            st.markdown("#### Top 5 sản phẩm theo giá")
            st.dataframe(analysis["top_5_by_price"], use_container_width=True, height=260)
            st.markdown("#### Top 5 sản phẩm theo rating")
            st.dataframe(analysis["top_5_by_rating"], use_container_width=True, height=260)

    with chart_col:
        top_price_df = analysis["top_5_by_price"].copy()
        category_count_df = analysis["category_counts"].copy()
        average_by_category_df = analysis["average_price_by_category"].copy()

        if not top_price_df.empty:
            top_price_df["short_name"] = top_price_df["product_name"].apply(lambda x: x[:40] + '...' if len(x) > 40 else x)
            top_price_df = top_price_df.sort_values(by="price", ascending=True)
            
            fig_price = px.bar(
                top_price_df,
                y="short_name",
                x="price",
                orientation='h',
                color="category" if "category" in top_price_df.columns else None,
                title="Top 5 sản phẩm có giá cao nhất",
                color_discrete_sequence=["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"],
                text_auto='.3s'
            )
            fig_price.update_traces(textposition='outside', marker_line_width=0, width=0.5 if len(top_price_df) <= 3 else None)
            fig_price.update_layout(
                margin=dict(l=10, r=50, t=50, b=10),
                template="plotly_white",
                xaxis_title="Mức giá",
                yaxis_title="",
                showlegend=(top_price_df['category'].nunique() > 1 if 'category' in top_price_df else False),
                hovermode="y unified"
            )
            st.plotly_chart(fig_price, use_container_width=True)

        chart_row = st.columns(2)
        if not category_count_df.empty:
            num_cat = len(category_count_df)
            fig_category = px.bar(
                category_count_df,
                x="category",
                y="count",
                title="Số lượng sản phẩm theo danh mục",
                color_discrete_sequence=["#3b82f6"],
                text_auto=True
            )
            fig_category.update_traces(textposition='outside', width=0.4 if num_cat == 1 else None)
            fig_category.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                template="plotly_white",
                xaxis_title="",
                yaxis_title="Số lượng",
                showlegend=False
            )
            chart_row[0].plotly_chart(fig_category, use_container_width=True)

        if not average_by_category_df.empty:
            num_cat = len(average_by_category_df)
            fig_average = px.bar(
                average_by_category_df,
                x="category",
                y="average_price",
                title="Giá trung bình theo danh mục",
                color_discrete_sequence=["#0ea5e9"],
                text_auto='.3s'
            )
            fig_average.update_traces(textposition='outside', width=0.4 if num_cat == 1 else None)
            fig_average.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                template="plotly_white",
                xaxis_title="",
                yaxis_title="Mức giá",
                showlegend=False
            )
            chart_row[1].plotly_chart(fig_average, use_container_width=True)


def render_dataset_views(raw_df, clean_df) -> None:
    """Hiển thị tập dữ liệu thô và tập dữ liệu đã làm sạch cạnh nhau."""
    left_column, right_column = st.columns(2)

    with left_column:
        with st.container(border=True):
            st.markdown("#### Dữ liệu thô")
            if raw_df is not None:
                st.dataframe(raw_df, use_container_width=True, height=420)
            else:
                st.info("Chưa có dữ liệu thô. Hãy crawl dữ liệu hoặc dùng dữ liệu mẫu.")

    with right_column:
        with st.container(border=True):
            st.markdown("#### Dữ liệu sau làm sạch")
            if clean_df is not None:
                st.dataframe(clean_df, use_container_width=True, height=420)
            else:
                st.info("Chưa có dữ liệu sạch. Hãy bấm Clean Data sau khi có raw data.")


def render_export_center(raw_df, clean_df) -> None:
    """Hiển thị các tùy chọn tải xuống trong một tab riêng."""
    st.markdown('<div class="micro-title">Trung tâm xuất dữ liệu</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            textwrap.dedent("""
                <div class="export-card">
                  <div class="kpi-label">RAW CSV</div>
                  <div class="kpi-note">Tải dữ liệu vừa crawl về để lưu hồ sơ đầu vào hoặc trình bày quy trình.</div>
                </div>
            """),
            unsafe_allow_html=True,
        )
        if raw_df is not None:
            st.download_button(
                label="Download raw_data.csv",
                data=dataframe_to_csv_bytes(raw_df),
                file_name="raw_data.csv",
                mime="text/csv",
                use_container_width=True,
            )

    with col2:
        st.markdown(
            textwrap.dedent("""
                <div class="export-card">
                  <div class="kpi-label">CLEAN CSV</div>
                  <div class="kpi-note">Dùng cho báo cáo phân tích hoặc minh họa bước chuẩn hóa dữ liệu.</div>
                </div>
            """),
            unsafe_allow_html=True,
        )
        if clean_df is not None:
            st.download_button(
                label="Download clean_data.csv",
                data=dataframe_to_csv_bytes(clean_df),
                file_name="clean_data.csv",
                mime="text/csv",
                use_container_width=True,
            )

    with col3:
        st.markdown(
            textwrap.dedent("""
                <div class="export-card">
                  <div class="kpi-label">SUMMARY CSV</div>
                  <div class="kpi-note">Xuất bảng KPI cuối cùng để gắn vào slide, báo cáo hoặc demo script.</div>
                </div>
            """),
            unsafe_allow_html=True,
        )
        analysis = st.session_state["analysis"]
        if analysis is not None:
            st.download_button(
                label="Download summary_report.csv",
                data=dataframe_to_csv_bytes(analysis["summary_df"]),
                file_name="summary_report.csv",
                mime="text/csv",
                use_container_width=True,
            )


def render_sidebar(raw_df, clean_df) -> tuple[str, int]:
    """Hiển thị menu điều khiển ở thanh bên và trả về các tham số cào dữ liệu."""
    st.sidebar.header("Control Center")
    st.sidebar.markdown(
        """
        Cấu hình nguồn dữ liệu ngay tại đây, sau đó dùng các nút ở phần chính để chạy pipeline.

        **Nguồn hỗ trợ**
        - `books.toscrape.com` (Hỗ trợ phân trang)
        - `webscraper.io/...` (Theo category)
        - **Bất kỳ URL công khai nào** (Cào tự động bằng Generic Scraper)
        """
    )

    default_url = st.sidebar.text_input("URL công khai", value=DEFAULT_BOOKS_URL)
    max_pages = st.sidebar.slider("Số trang cần crawl", min_value=1, max_value=3, value=2)
    st.sidebar.caption(
        "Ví dụ: "
        f"`{DEFAULT_BOOKS_URL}` hoặc bất kỳ link trang báo, sản phẩm nào. "
        "Với website lạ, hệ thống sẽ tự động quét các thẻ tiêu đề và liên kết."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Snapshot")
    st.sidebar.write(f"Dòng thô: `{len(raw_df) if raw_df is not None else 0}`")
    st.sidebar.write(f"Dòng sạch: `{len(clean_df) if clean_df is not None else 0}`")
    st.sidebar.write(f"Phân tích: `{'Sẵn sàng' if st.session_state['analysis'] is not None else 'Đang chờ'}`")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Tài liệu đi kèm")
    st.sidebar.markdown(
        "- `docs/project_report_vi.md`\n"
        "- `docs/demo_script_vi.md`\n"
        "- `docs/slides_outline_vi.md`\n"
        "- `docs/team_work_vi.md`"
    )
    return default_url, max_pages


def main() -> None:
    inject_styles()
    initialize_files()
    initialize_session_state()

    raw_df = st.session_state["raw_df"]
    if raw_df is None and RAW_DATA_PATH.exists():
        raw_df = load_dataframe(RAW_DATA_PATH)
        st.session_state["raw_df"] = raw_df

    clean_df = st.session_state["clean_df"]
    if clean_df is None and CLEAN_DATA_PATH.exists():
        clean_df = load_dataframe(CLEAN_DATA_PATH)
        st.session_state["clean_df"] = clean_df

    default_url, max_pages = render_sidebar(raw_df, clean_df)

    render_hero()
    render_action_bar(default_url, max_pages)
    render_source_banner()
    render_pipeline_summary(raw_df, clean_df)

    overview_tab, datasets_tab, analysis_tab, export_tab = st.tabs(
        ["Tổng quan", "Dữ liệu", "Phân tích", "Xuất file"]
    )

    with overview_tab:
        intro_col, status_col = st.columns((1.3, 1))
        with intro_col:
            with st.container(border=True):
                st.markdown("### Góc nhìn vận hành")
                st.write(
                    "Bố cục mới tập trung vào 3 việc khi demo: cho thấy nguồn dữ liệu đang dùng, "
                    "biết pipeline đang ở bước nào, và có thể xuất file kết quả ngay khi cần."
                )
                st.write(
                    "Nếu bạn đang chuẩn bị cho buổi thuyết trình, tab này là nơi tốt nhất để giải thích "
                    "toàn bộ luồng `Crawl → Clean → Analyze → Export` chỉ trong vài phút."
                )
        with status_col:
            with st.container(border=True):
                st.markdown("### Tình trạng hiện tại")
                st.write(f"Raw dataset: **{'Có dữ liệu' if raw_df is not None else 'Chưa có'}**")
                st.write(f"Clean dataset: **{'Có dữ liệu' if clean_df is not None else 'Chưa có'}**")
                st.write(
                    f"Analysis report: **{'Sẵn sàng' if st.session_state['analysis'] is not None else 'Chưa chạy'}**"
                )

        render_cleaning_report()

    with datasets_tab:
        render_dataset_views(raw_df, clean_df)

    with analysis_tab:
        render_analysis()

    with export_tab:
        render_export_center(raw_df, clean_df)

    st.markdown(
        """
        <div class="footer-note">
          Nhóm thực hiện: Nhóm 3 · Môn học: Nhập môn Khoa học dữ liệu · Năm học: 2026
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

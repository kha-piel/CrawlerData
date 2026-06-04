from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

RAW_DATA_PATH = DATA_DIR / "raw_data.csv"
CLEAN_DATA_PATH = DATA_DIR / "clean_data.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_data.csv"
SUMMARY_REPORT_PATH = REPORTS_DIR / "summary_report.csv"


def ensure_directories() -> None:
    """Create folders used by the project if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV with UTF-8 encoding."""
    ensure_directories()
    df.to_csv(file_path, index=False, encoding="utf-8-sig")


def load_dataframe(file_path: Path) -> pd.DataFrame:
    """Load a CSV file and raise a helpful error if it does not exist."""
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    return pd.read_csv(file_path)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to bytes so Streamlit can download it."""
    csv_text = df.to_csv(index=False)
    return csv_text.encode("utf-8-sig")

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
CSV_ENCODING = "utf-8-sig"

RAW_DATA_PATH = DATA_DIR / "raw_data.csv"
CLEAN_DATA_PATH = DATA_DIR / "clean_data.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_data.csv"
SUMMARY_REPORT_PATH = REPORTS_DIR / "summary_report.csv"


def ensure_directories() -> None:
    """Tạo các thư mục cấp cao nhất dùng cho dự án."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_parent_directory(file_path: Path) -> None:
    """Tạo thư mục cha cho một đường dẫn tệp khi cần thiết."""
    file_path.parent.mkdir(parents=True, exist_ok=True)


def save_dataframe(
    df: pd.DataFrame,
    file_path: Path,
    *,
    index: bool = False,
) -> None:
    """Lưu DataFrame thành tệp CSV bằng phương pháp ghi đè an toàn (atomic replace)."""
    ensure_directories()
    ensure_parent_directory(file_path)

    with NamedTemporaryFile(
        mode="w",
        encoding=CSV_ENCODING,
        newline="",
        delete=False,
        dir=file_path.parent,
        suffix=".tmp",
    ) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        df.to_csv(temp_path, index=index, encoding=CSV_ENCODING)
        temp_path.replace(file_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def load_dataframe(file_path: Path, **read_csv_kwargs: Any) -> pd.DataFrame:
    """Tải tệp CSV với các bước kiểm tra hợp lệ và mặc định mã hóa nhất quán."""
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"Đường dẫn không phải là tệp CSV: {file_path}")
    if file_path.stat().st_size == 0:
        raise ValueError(f"Tệp CSV đang rỗng: {file_path}")

    csv_kwargs = {"encoding": CSV_ENCODING}
    csv_kwargs.update(read_csv_kwargs)
    return pd.read_csv(file_path, **csv_kwargs)


def dataframe_to_csv_bytes(
    df: pd.DataFrame,
    *,
    index: bool = False,
) -> bytes:
    """Chuyển đổi DataFrame thành chuỗi byte dạng CSV để có thể tải xuống."""
    csv_text = df.to_csv(index=index)
    return csv_text.encode(CSV_ENCODING)

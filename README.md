# Data Scraper, Cleaner & Tracker

## 1. Tổng quan ý tưởng project


`Raw Data -> Clean Data -> Analysis -> Dashboard`

Ứng dụng giúp người học:

- Thu thập dữ liệu công khai từ một website đơn giản.
- Tự động chuyển sang dữ liệu mẫu khi website không truy cập được.
- Làm sạch dữ liệu bằng các thao tác pandas dễ hiểu.
- Phân tích số liệu cơ bản và hiển thị biểu đồ trên Streamlit.
- Tải xuống các file CSV để phục vụ báo cáo và demo.

Project ưu tiên:

- Code dễ đọc, có comment ngắn gọn.
- Không dùng kỹ thuật quá phức tạp.
- Không thu thập dữ liệu cá nhân.


## 2. Cấu trúc thư mục

```text
data-scraper-cleaner-tracker/
|
|-- app.py
|-- scraper.py
|-- cleaner.py
|-- analyzer.py
|-- storage.py
|-- sample_data.py
|-- requirements.txt
|-- README.md
|
|-- data/
|   |-- raw_data.csv
|   |-- clean_data.csv
|   `-- sample_data.csv
|
|-- reports/
|   `-- summary_report.csv
|
`-- docs/
    |-- project_report_vi.md
    |-- demo_script_vi.md
    |-- team_work_vi.md
    `-- slides_outline_vi.md
```

## 3. Giải thích từng module

- `app.py`: Giao diện Streamlit chính, xử lý nút bấm, hiển thị bảng dữ liệu, metric card và biểu đồ.
- `scraper.py`: Thu thập dữ liệu công khai từ trang demo `books.toscrape.com`.
- `cleaner.py`: Làm sạch dữ liệu như xóa khoảng trắng thừa, đổi giá và rating sang số, xử lý giá trị thiếu.
- `analyzer.py`: Tính thống kê cơ bản, tạo bảng top 5 và dữ liệu cho biểu đồ.
- `storage.py`: Tạo thư mục, đọc file CSV, ghi file CSV.
- `sample_data.py`: Tạo dữ liệu mẫu có lỗi chủ động để demo bước làm sạch.

## 4. Công nghệ sử dụng

- Python
- requests
- BeautifulSoup4
- pandas
- plotly
- Streamlit
- CSV

## 5. Hướng dẫn cài đặt

### Bước 1: Tạo môi trường ảo

```bash
python -m venv .venv
```

### Bước 2: Kích hoạt môi trường

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

### Bước 3: Cài thư viện

```bash
pip install -r requirements.txt
```

## 6. Hướng dẫn chạy project

Chạy ứng dụng bằng lệnh:

```bash
streamlit run app.py
```

Sau khi mở giao diện:

1. Bấm `Crawl Data` để lấy dữ liệu từ website công khai.
2. Hoặc bấm `Use Sample Data` để demo offline.
3. Bấm `Clean Data` để làm sạch dữ liệu.
4. Bấm `Analyze Data` để tính thống kê và xem biểu đồ.
5. Bấm các nút `Download CSV` để tải dữ liệu về máy.

## 7. Luồng hoạt động của hệ thống

```text
Input URL / Sample Data
        |
        v
     Scraper
        |
        v
    Raw Data
        |
        v
     Cleaner
        |
        v
   Clean Data
        |
        v
    Analyzer
        |
        v
 Dashboard / Report
```

## 8. Dữ liệu mẫu

Dữ liệu mẫu nằm ở `data/sample_data.csv` với khoảng 20 dòng. Dữ liệu này cố tình có lỗi để minh họa bước làm sạch:

- Tên sản phẩm có khoảng trắng thừa.
- Giá ở dạng chuỗi như `12.500.000đ`, `19,990,000 VND`, `Liên hệ`.
- Rating ở dạng chuỗi như `4.5/5 sao`, `N/A`.
- Một số dòng thiếu `price`, `rating`, `review_count`.
- Có dữ liệu trùng lặp.
## 9 .

## 10. Ưu điểm, nhược điểm, rủi ro và cách khắc phục

### Ưu điểm

- Dễ học, dễ demo, phù hợp sinh viên năm nhất.
- Có đủ quy trình từ thu thập đến trực quan hóa.
- Có dữ liệu mẫu để chạy cả khi mất mạng.
- Cấu trúc project rõ ràng, dễ mở rộng.

### Nhược điểm

- Website crawl mẫu khá đơn giản.
- Chưa hỗ trợ lịch chạy tự động.
- Chưa dùng cơ sở dữ liệu mạnh như MySQL/PostgreSQL.

### Rủi ro và cách khắc phục

- Website thay đổi cấu trúc: hệ thống sẽ chuyển sang dữ liệu mẫu.
- Mạng yếu hoặc website lỗi: dùng `Use Sample Data`.
- Dữ liệu thiếu hoặc sai định dạng: xử lý trong `cleaner.py`.
- Người mới khó hiểu luồng code: đã chia nhỏ thành nhiều module và có comment.

## 11. Hướng phát triển tương lai

- Thêm SQLite để lưu lịch sử dữ liệu.
- Tự động crawl theo lịch.
- Gửi cảnh báo khi dữ liệu thay đổi.
- Xuất báo cáo Excel hoặc PDF.
- Hỗ trợ thêm nhiều nguồn dữ liệu công khai khác.
- Triển khai ứng dụng lên Streamlit Cloud hoặc Render.

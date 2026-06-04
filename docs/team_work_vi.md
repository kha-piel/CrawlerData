# Phân chia công việc nhóm 3 người

## Người 1: Phụ trách Scraper

Nhiệm vụ chính:

- Tìm nguồn dữ liệu công khai, hợp pháp và dễ crawl.
- Viết module `scraper.py`.
- Gửi request và lấy dữ liệu HTML.
- Dùng BeautifulSoup để trích xuất trường dữ liệu.
- Lưu dữ liệu thô vào `data/raw_data.csv`.

Nhiệm vụ trình bày:

- Giải thích lý do chọn đề tài.
- Giới thiệu nguồn dữ liệu.
- Mô tả cách hệ thống thu thập dữ liệu.

## Người 2: Phụ trách Cleaner

Nhiệm vụ chính:

- Viết module `cleaner.py`.
- Xử lý khoảng trắng thừa.
- Chuẩn hóa giá trị thiếu như `Liên hệ`, `Đang cập nhật`, `N/A`.
- Chuyển `price` và `rating` từ chuỗi sang số.
- Loại bỏ dữ liệu trùng.
- Lưu dữ liệu sạch vào `data/clean_data.csv`.

Nhiệm vụ trình bày:

- Giải thích vì sao dữ liệu thô cần làm sạch.
- Trình bày các bước làm sạch dữ liệu.
- So sánh dữ liệu trước và sau xử lý.

## Người 3: Phụ trách Analyzer và Dashboard

Nhiệm vụ chính:

- Viết module `analyzer.py`.
- Tính thống kê cơ bản.
- Tạo bảng top 5 và nhóm theo danh mục.
- Xây dựng giao diện `app.py` bằng Streamlit.
- Hiển thị metric card, bảng dữ liệu, biểu đồ.
- Tạo file `reports/summary_report.csv`.

Nhiệm vụ trình bày:

- Thực hiện demo trực tiếp.
- Giải thích các thống kê và biểu đồ.
- Trình bày ưu điểm, nhược điểm và hướng phát triển.

## Mô tả phối hợp giữa các thành viên

- Người 1 hoàn thành phần dữ liệu đầu vào.
- Người 2 nhận dữ liệu thô từ Người 1 để xử lý.
- Người 3 nhận dữ liệu sạch từ Người 2 để phân tích và trực quan hóa.
- Cả nhóm cùng kiểm thử, hoàn thiện báo cáo và luyện tập phần demo.

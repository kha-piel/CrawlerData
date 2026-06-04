# Đề xuất nội dung slide thuyết trình

## Slide 1: Tên đề tài và thành viên nhóm

Nội dung bullet:

- Data Scraper, Cleaner & Tracker
- Công cụ thu thập, làm sạch và phân tích dữ liệu cơ bản
- Danh sách thành viên nhóm

Lời thuyết trình gợi ý:

"Đây là đề tài của nhóm em về xây dựng công cụ thu thập, làm sạch và phân tích dữ liệu cơ bản bằng Python và Streamlit."

## Slide 2: Lý do chọn đề tài

Nội dung bullet:

- Dữ liệu thô thường lộn xộn
- Cần xử lý trước khi phân tích
- Liên hệ trực tiếp với Data Science

Lời thuyết trình gợi ý:

"Nhóm chọn đề tài này vì trong thực tế dữ liệu hiếm khi sạch sẵn, nên bước thu thập và làm sạch là rất quan trọng trước khi phân tích."

## Slide 3: Mục tiêu đề tài

Nội dung bullet:

- Thu thập dữ liệu công khai
- Làm sạch dữ liệu
- Phân tích thống kê cơ bản
- Hiển thị kết quả trực quan

Lời thuyết trình gợi ý:

"Mục tiêu chính là xây dựng một quy trình hoàn chỉnh nhưng đơn giản để sinh viên năm nhất có thể hiểu và thực hiện được."

## Slide 4: Phạm vi và đối tượng dữ liệu

Nội dung bullet:

- Dữ liệu sản phẩm công khai
- Không thu thập dữ liệu cá nhân
- Không vượt qua đăng nhập/captcha
- Có dữ liệu mẫu offline

Lời thuyết trình gợi ý:

"Nhóm chỉ làm việc với dữ liệu công khai, hợp pháp và có dữ liệu mẫu để đảm bảo project luôn demo được."

## Slide 5: Công nghệ sử dụng

Nội dung bullet:

- Python
- requests
- BeautifulSoup4
- pandas
- Streamlit
- plotly

Lời thuyết trình gợi ý:

"Nhóm chọn các công nghệ cơ bản, phổ biến và phù hợp với sinh viên năm nhất để việc học tập dễ tiếp cận hơn."

## Slide 6: Kiến trúc hệ thống

Nội dung bullet:

- Scraper
- Cleaner
- Analyzer
- Storage
- Dashboard

Lời thuyết trình gợi ý:

"Hệ thống được chia thành các module nhỏ để dễ hiểu, dễ kiểm thử và dễ phân chia công việc giữa các thành viên."

## Slide 7: Quy trình xử lý dữ liệu

Nội dung bullet:

- Input URL / Sample Data
- Raw Data
- Clean Data
- Analysis
- Dashboard / Report

Lời thuyết trình gợi ý:

"Đây là luồng hoạt động tổng quát của project, từ lúc nhận dữ liệu đầu vào cho đến khi hiển thị dashboard và xuất báo cáo."

## Slide 8: Demo module Scraper

Nội dung bullet:

- Nhập URL công khai
- Crawl dữ liệu
- Lưu `raw_data.csv`
- Fallback sang dữ liệu mẫu khi lỗi

Lời thuyết trình gợi ý:

"Trong phần này, nhóm trình bày cách hệ thống lấy dữ liệu từ website công khai hoặc tự chuyển sang dữ liệu mẫu nếu website gặp lỗi."

## Slide 9: Demo module Cleaner

Nội dung bullet:

- Xóa khoảng trắng thừa
- Chuẩn hóa giá
- Chuẩn hóa rating
- Xóa dữ liệu trùng

Lời thuyết trình gợi ý:

"Sau khi có dữ liệu thô, hệ thống dùng pandas để làm sạch dữ liệu, giúp dữ liệu đồng nhất và dễ phân tích hơn."

## Slide 10: Demo module Analyzer/Dashboard

Nội dung bullet:

- Metric card
- Top 5 theo giá
- Top 5 theo rating
- Biểu đồ theo danh mục

Lời thuyết trình gợi ý:

"Phần analyzer sẽ tính các thống kê cơ bản, còn dashboard sẽ hiển thị kết quả một cách trực quan bằng bảng và biểu đồ."

## Slide 11: Ưu điểm, nhược điểm và lưu ý

Nội dung bullet:

- Dễ học, dễ demo
- Có dữ liệu mẫu offline
- Chưa crawl website phức tạp
- Cần tôn trọng đạo đức dữ liệu

Lời thuyết trình gợi ý:

"Project có ưu điểm là đơn giản và phù hợp người mới, nhưng vẫn còn giới hạn ở các website dễ crawl và cần tuân thủ đạo đức, pháp lý khi thu thập dữ liệu."

## Slide 12: Hướng phát triển và kết luận

Nội dung bullet:

- Thêm database
- Tự động chạy theo lịch
- Xuất Excel/PDF
- Deploy lên cloud

Lời thuyết trình gợi ý:

"Trong tương lai, nhóm có thể mở rộng project bằng cách thêm database, tự động hóa theo lịch và triển khai lên môi trường online."

# Báo cáo đồ án: Data Scraper, Cleaner & Tracker

## 1. Lý do chọn đề tài

Trong thực tế, dữ liệu thường được thu thập từ nhiều nguồn khác nhau và hiếm khi ở trạng thái sạch ngay từ đầu. Dữ liệu thô thường chứa khoảng trắng thừa, giá trị thiếu, dữ liệu trùng lặp hoặc định dạng không đồng nhất. Nếu đem dữ liệu này đi phân tích trực tiếp thì kết quả dễ sai lệch và khó sử dụng.

Đề tài "Data Scraper, Cleaner & Tracker" giúp sinh viên hiểu được một quy trình rất cơ bản nhưng quan trọng trong Data Science:

- Thu thập dữ liệu.
- Làm sạch dữ liệu.
- Phân tích dữ liệu.
- Trực quan hóa dữ liệu.

Đây là một đề tài phù hợp cho sinh viên năm nhất vì vừa có tính ứng dụng, vừa giúp rèn tư duy xử lý dữ liệu bằng Python mà chưa cần đến các kỹ thuật quá nâng cao.

## 2. Mục tiêu đề tài

Mục tiêu của đề tài là xây dựng một công cụ đơn giản có thể:

- Thu thập dữ liệu công khai từ website dễ crawl hoặc từ dữ liệu mẫu.
- Lưu dữ liệu thô vào file CSV.
- Làm sạch dữ liệu bằng pandas.
- Tính toán các thống kê cơ bản.
- Hiển thị dữ liệu và biểu đồ trên giao diện Streamlit.
- Cho phép tải dữ liệu và báo cáo CSV.

## 3. Đối tượng và phạm vi nghiên cứu

### Đối tượng

- Dữ liệu sản phẩm công khai.
- Dữ liệu mẫu phục vụ học tập và demo.

### Phạm vi

- Không thu thập dữ liệu cá nhân.
- Không crawl dữ liệu sau đăng nhập.
- Không vượt qua captcha hoặc cơ chế chống bot mạnh.
- Chỉ sử dụng website đơn giản và hợp pháp cho mục đích học tập.

## 4. Công nghệ sử dụng

- `Python`: ngôn ngữ lập trình chính.
- `requests`: gửi HTTP request đến website công khai.
- `BeautifulSoup4`: phân tích HTML và trích xuất dữ liệu.
- `pandas`: xử lý và làm sạch dữ liệu.
- `Streamlit`: xây dựng dashboard đơn giản.
- `plotly`: vẽ biểu đồ trực quan.
- `CSV`: lưu trữ dữ liệu ở mức cơ bản, dễ hiểu.

## 5. Phân tích yêu cầu hệ thống

### Yêu cầu chức năng

- Cho phép nhập URL công khai hoặc dùng dữ liệu mẫu.
- Crawl dữ liệu từ website đơn giản.
- Lưu dữ liệu thô vào `raw_data.csv`.
- Làm sạch dữ liệu và lưu vào `clean_data.csv`.
- Phân tích dữ liệu sạch.
- Hiển thị thống kê bằng metric card.
- Hiển thị biểu đồ top 5 và phân bố theo danh mục.
- Tải xuống các file CSV.

### Yêu cầu phi chức năng

- Dễ sử dụng cho sinh viên năm nhất.
- Giao diện rõ ràng, dễ quan sát khi demo.
- Code chia module rõ ràng.
- Có xử lý lỗi và thông báo thân thiện.
- Có thể chạy offline với dữ liệu mẫu.

## 6. Thiết kế hệ thống

Hệ thống được thiết kế theo luồng xử lý:

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

Thiết kế này có ưu điểm là đơn giản, dễ chia nhóm và mỗi module có nhiệm vụ rõ ràng.

## 7. Mô tả các module

### Module Scraper

- Nhận URL công khai.
- Gửi request đến website.
- Phân tích HTML bằng BeautifulSoup.
- Trích xuất các trường như tên sản phẩm, giá, rating, link.
- Lưu vào DataFrame và ghi ra CSV.

### Module Cleaner

- Xóa khoảng trắng thừa.
- Chuẩn hóa `category`.
- Chuyển `price` từ chuỗi sang số.
- Chuyển `rating` từ chuỗi sang số.
- Xử lý các giá trị như `Liên hệ`, `Đang cập nhật`, `N/A`.
- Xóa dữ liệu trùng.

### Module Analyzer

- Tính tổng bản ghi.
- Tính tổng danh mục.
- Tính giá trung bình, lớn nhất, nhỏ nhất.
- Tính rating trung bình.
- Tìm sản phẩm có giá cao nhất và rating cao nhất.
- Lập bảng top 5 theo giá và rating.
- Đếm số lượng sản phẩm theo danh mục.

### Module Storage

- Tạo thư mục `data/` và `reports/`.
- Đọc file CSV.
- Ghi file CSV.

### Module UI

- Hiển thị dữ liệu thô.
- Hiển thị dữ liệu sạch.
- Hiển thị thống kê.
- Hiển thị biểu đồ.
- Tải xuống file CSV.

## 8. Quy trình hoạt động

1. Người dùng mở ứng dụng Streamlit.
2. Người dùng chọn `Crawl Data` hoặc `Use Sample Data`.
3. Hệ thống thu thập dữ liệu và lưu vào `data/raw_data.csv`.
4. Người dùng bấm `Clean Data`.
5. Hệ thống làm sạch dữ liệu và lưu vào `data/clean_data.csv`.
6. Người dùng bấm `Analyze Data`.
7. Hệ thống tính toán thống kê, tạo biểu đồ và lưu `reports/summary_report.csv`.
8. Người dùng tải dữ liệu nếu cần.

## 9. Kết quả đạt được

Project đã đáp ứng các mục tiêu chính:

- Thu thập được dữ liệu công khai từ website demo.
- Có cơ chế tự chuyển sang dữ liệu mẫu khi website lỗi.
- Làm sạch dữ liệu thành công.
- Hiển thị được bảng dữ liệu trước và sau làm sạch.
- Tính được các thống kê cơ bản.
- Vẽ được biểu đồ minh họa.
- Tải được dữ liệu CSV phục vụ báo cáo.

## 10. Ưu điểm

- Phù hợp với trình độ sinh viên năm nhất.
- Luồng xử lý rõ ràng, dễ trình bày.
- Có tính thực tế trong học tập Data Science.
- Dễ mở rộng thêm nguồn dữ liệu khác.
- Có thể demo ngay cả khi không có mạng.

## 11. Nhược điểm

- Phụ thuộc vào cấu trúc HTML của website nguồn.
- Chưa crawl được website phức tạp.
- Chưa có cơ sở dữ liệu mạnh.
- Chưa hỗ trợ chạy theo lịch.
- Chưa có phân tích nâng cao hoặc AI.

## 12. Lưu ý đạo đức và pháp lý

- Chỉ sử dụng dữ liệu công khai.
- Không thu thập thông tin cá nhân.
- Không vượt qua đăng nhập, captcha hoặc chống bot.
- Không gửi quá nhiều request trong thời gian ngắn.
- Tôn trọng `robots.txt` và điều khoản sử dụng của website.

## 13. Ưu điểm, nhược điểm, rủi ro và cách khắc phục

### Rủi ro 1: Website thay đổi cấu trúc

- Ảnh hưởng: scraper không lấy được dữ liệu.
- Cách khắc phục: dùng dữ liệu mẫu và cập nhật lại selector trong `scraper.py`.

### Rủi ro 2: Website không truy cập được

- Ảnh hưởng: demo bị gián đoạn.
- Cách khắc phục: hệ thống tự fallback sang dữ liệu mẫu offline.

### Rủi ro 3: Dữ liệu thiếu hoặc sai định dạng

- Ảnh hưởng: thống kê có thể sai.
- Cách khắc phục: dùng `cleaner.py` để chuẩn hóa giá, rating và loại bỏ dữ liệu trùng.

### Rủi ro 4: Thành viên nhóm chưa quen Python

- Ảnh hưởng: khó giải thích code khi bảo vệ.
- Cách khắc phục: chia project thành module nhỏ, thêm comment, giao đúng phần cho từng người.

## 14. Hướng phát triển tương lai

- Thêm SQLite hoặc MySQL để lưu lịch sử.
- Tự động chạy crawl theo lịch.
- Gửi email cảnh báo khi dữ liệu thay đổi.
- Xuất báo cáo Excel hoặc PDF.
- Bổ sung nhiều website công khai khác.
- Thêm chức năng đăng nhập và quản lý phiên làm việc.
- Triển khai lên cloud để truy cập online.

## 15. Kết luận

Đề tài "Data Scraper, Cleaner & Tracker" giúp sinh viên tiếp cận một quy trình rất quan trọng trong Data Science theo cách đơn giản và dễ hiểu. Qua project này, sinh viên có thể học được:

- Cách thu thập dữ liệu bằng Python.
- Cách làm sạch dữ liệu bằng pandas.
- Cách phân tích thống kê cơ bản.
- Cách trực quan hóa kết quả bằng Streamlit.
- Cách tổ chức một project phần mềm nhỏ theo module.

Project có tính ứng dụng thực tế, dễ triển khai, dễ mở rộng và đặc biệt phù hợp cho sinh viên năm nhất khi bắt đầu làm quen với xử lý dữ liệu.

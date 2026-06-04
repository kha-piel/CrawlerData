import pandas as pd

from storage import SAMPLE_DATA_PATH, save_dataframe


def create_sample_dataframe() -> pd.DataFrame:
    """Create intentionally messy sample data for the cleaning demo."""
    rows = [
        {
            "product_name": "  Laptop Dell Inspiron 15  ",
            "category": " laptop ",
            "price": "12.500.000đ",
            "rating": "4.5/5 sao",
            "review_count": "125 reviews",
            "product_url": "https://example.com/dell-inspiron-15",
        },
        {
            "product_name": "MacBook Air M1",
            "category": "Laptop",
            "price": "19,990,000 VND",
            "rating": "4.8/5 sao",
            "review_count": "210",
            "product_url": "https://example.com/macbook-air-m1",
        },
        {
            "product_name": "  iPhone 13  ",
            "category": "điện thoại",
            "price": "Liên hệ",
            "rating": "4.7/5 sao",
            "review_count": "356 đánh giá",
            "product_url": "https://example.com/iphone-13",
        },
        {
            "product_name": "Samsung Galaxy A54",
            "category": "Điện thoại ",
            "price": "8.490.000đ",
            "rating": "4.4/5 sao",
            "review_count": "180 reviews",
            "product_url": "https://example.com/samsung-a54",
        },
        {
            "product_name": "Tai nghe Sony WH-CH520",
            "category": "phụ kiện",
            "price": "1.290.000đ",
            "rating": "4.6/5 sao",
            "review_count": "96",
            "product_url": "https://example.com/sony-wh-ch520",
        },
        {
            "product_name": " Chuột Logitech M331 ",
            "category": "phụ kiện",
            "price": " 420.000đ ",
            "rating": "4.3/5 sao",
            "review_count": "72",
            "product_url": "https://example.com/logitech-m331",
        },
        {
            "product_name": "Bàn phím cơ AKKO 3087",
            "category": "phụ kiện",
            "price": "Đang cập nhật",
            "rating": "4.5/5 sao",
            "review_count": "N/A",
            "product_url": "https://example.com/akko-3087",
        },
        {
            "product_name": "  Màn hình LG 24MP400  ",
            "category": "màn hình",
            "price": "2.990.000đ",
            "rating": "4.2/5 sao",
            "review_count": "54",
            "product_url": "https://example.com/lg-24mp400",
        },
        {
            "product_name": "Màn hình LG 24MP400",
            "category": "Màn Hình",
            "price": "2.990.000đ",
            "rating": "4.2/5 sao",
            "review_count": "54",
            "product_url": "https://example.com/lg-24mp400",
        },
        {
            "product_name": "Loa Bluetooth JBL Go 3",
            "category": "âm thanh",
            "price": "890.000đ",
            "rating": "4.1/5 sao",
            "review_count": "65",
            "product_url": "https://example.com/jbl-go-3",
        },
        {
            "product_name": "Máy in Canon LBP2900",
            "category": "văn phòng",
            "price": "3.150.000đ",
            "rating": "4.0/5 sao",
            "review_count": "41",
            "product_url": "https://example.com/canon-lbp2900",
        },
        {
            "product_name": "  Webcam Rapoo C260 ",
            "category": "phụ kiện ",
            "price": "590.000đ",
            "rating": "N/A",
            "review_count": "18",
            "product_url": "https://example.com/rapoo-c260",
        },
        {
            "product_name": "Ổ cứng SSD Kingston 500GB",
            "category": "Lưu trữ",
            "price": "1,350,000 VND",
            "rating": "4.7/5 sao",
            "review_count": "134",
            "product_url": "https://example.com/ssd-kingston-500gb",
        },
        {
            "product_name": "USB SanDisk 64GB",
            "category": " lưu trữ ",
            "price": "",
            "rating": "4.0/5 sao",
            "review_count": "50",
            "product_url": "https://example.com/usb-sandisk-64gb",
        },
        {
            "product_name": "Ghế công thái học Sihoo M57",
            "category": "nội thất",
            "price": "5.990.000đ",
            "rating": "4.6/5 sao",
            "review_count": "29",
            "product_url": "https://example.com/sihoo-m57",
        },
        {
            "product_name": "Bàn làm việc gỗ MDF",
            "category": "nội thất",
            "price": "2.150.000đ",
            "rating": "4.1/5 sao",
            "review_count": "22",
            "product_url": "https://example.com/ban-mdf",
        },
        {
            "product_name": "Laptop ASUS Vivobook 15",
            "category": "Laptop",
            "price": "14.200.000đ",
            "rating": "4.4/5 sao",
            "review_count": "145",
            "product_url": "https://example.com/asus-vivobook-15",
        },
        {
            "product_name": "Router TP-Link Archer C64",
            "category": "mạng",
            "price": "790.000đ",
            "rating": "4.3/5 sao",
            "review_count": "64",
            "product_url": "https://example.com/tplink-c64",
        },
        {
            "product_name": "  Đồng hồ thông minh Amazfit Bip 5 ",
            "category": "thiết bị đeo",
            "price": "1.990.000đ",
            "rating": "4.5/5 sao",
            "review_count": "88",
            "product_url": "https://example.com/amazfit-bip-5",
        },
        {
            "product_name": "Pin dự phòng Anker 10000mAh",
            "category": "phụ kiện",
            "price": "690.000đ",
            "rating": "4.7/5 sao",
            "review_count": None,
            "product_url": "https://example.com/anker-10000",
        },
    ]
    return pd.DataFrame(rows)


def save_sample_data() -> pd.DataFrame:
    """Save sample data to CSV so the project can run offline."""
    sample_df = create_sample_dataframe()
    save_dataframe(sample_df, SAMPLE_DATA_PATH)
    return sample_df

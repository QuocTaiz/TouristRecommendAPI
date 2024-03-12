import pandas as pd
import sqlite3

# Thông tin kết nối đến cơ sở dữ liệu SQLite
db_path = "D:/Python project/TouristRecommendAPI/tour_recomm_api/db.sqlite3"
table_name = "api_tourist"

# Đọc dữ liệu từ file CSV
csv_file_path = "D:\TaiLieu\DATT\data.csv"
data = pd.read_csv(csv_file_path)

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Chèn dữ liệu vào cơ sở dữ liệu
data.to_sql(table_name, conn, if_exists='replace', index=False)

# Đóng kết nối
conn.close()

print(f"Dữ liệu đã được chèn vào bảng {table_name} của cơ sở dữ liệu {db_path}.")

import pandas as pd

def filter_and_create_list(csv_file_path, area_column):
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv(csv_file_path)

    # Lọc và tạo danh sách các giá trị duy nhất trong cột "area"
    unique_areas = data[area_column].unique().tolist()

    return unique_areas



# Thay đổi đường dẫn đến file CSV và tên cột "area" của bạn
csv_file_path = "D:\TaiLieu\DATT\data_processed.csv"
area_column = "special"

result = filter_and_create_list(csv_file_path, area_column)
print(result)

result_dict = {index + 1: value for index, value in enumerate(result)}

print(result_dict)

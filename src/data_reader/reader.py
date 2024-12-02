import pandas as pd
import os
import logging

class DataReader:
    def __init__(self, api_key, folder_path):
        if not api_key:
            raise ValueError("API KEY không tìm thấy!")
        self.api_key = api_key
        self.folder_path = folder_path
        self.data_frames = []
        self.file_names = [
            "Internation_students_Canada.csv",
            "Internation_students_Province_Canada.csv",
            "International_Students_Study_level.csv"
        ]

    def read_data(self):
        try:
            for file_name in self.file_names:
                file_path = os.path.join(self.folder_path, file_name)
                if not os.path.exists(file_path):
                    logging.warning(f"File '{file_name}' không tồn tại trong thư mục.")
                    continue

                logging.info(f"Đang đọc file: {file_path}")
                data = pd.read_csv(file_path, encoding='utf-8')
                # Loại bỏ khoảng trắng dư thừa ở đầu và cuối tên cột
                data.columns = data.columns.str.strip()
                self.data_frames.append(data)
        except pd.errors.EmptyDataError:
            logging.error("File rỗng không thể đọc.")
        except pd.errors.ParserError:
            logging.error("Lỗi khi phân tích cú pháp file CSV.")
        except Exception as e:
            logging.error(f"Lỗi khi đọc file: {e}")

    def display_data_frames(self):
        """Hiển thị thông tin các DataFrame đã đọc."""
        for i, df in enumerate(self.data_frames):
            print(f"--- DataFrame {i + 1} ---")
            print(df.head())

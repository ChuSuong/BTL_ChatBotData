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

    def get_data_frame(self, file_name):
        """
        Trả về DataFrame tương ứng với file_name.

        Parameters:
            file_name (str): Tên file CSV.

        Returns:
            pd.DataFrame: DataFrame của file tương ứng hoặc None nếu không tìm thấy.
        """
        return self.data_frames.get(file_name, None)

    def process_file(self, file_path, index_columns):
        """
        Xử lý một file cụ thể bằng cách chỉ định các cột làm chỉ mục.

        Parameters:
            file_path (str): Đường dẫn đến file cần xử lý.
            index_columns (list): Danh sách các cột cần đặt làm chỉ mục.

        Returns:
            pd.DataFrame: DataFrame đã xử lý hoặc None nếu xảy ra lỗi.
        """
        try:
            if not os.path.exists(file_path):
                logging.error(f"File '{file_path}' không tồn tại.")
                return None

            logging.info(f"Đang xử lý file: {file_path}")
            data = pd.read_csv(file_path, encoding="utf-8")
            data.columns = data.columns.str.strip()

            # Kiểm tra và đặt các cột làm chỉ mục
            if all(col in data.columns for col in index_columns):
                data.set_index(index_columns, inplace=True)
                logging.info(f"Đã đặt các cột {index_columns} làm chỉ mục.")
            else:
                missing_columns = [col for col in index_columns if col not in data.columns]
                logging.warning(f"Các cột sau không tồn tại trong file '{file_path}': {missing_columns}")

            return data

        except pd.errors.EmptyDataError:
            logging.error(f"File '{file_path}' rỗng không thể xử lý.")
            return None
        except pd.errors.ParserError:
            logging.error(f"Lỗi phân tích cú pháp file '{file_path}'.")
            return None
        except Exception as e:
            logging.error(f"Lỗi không xác định khi xử lý file '{file_path}': {e}")
            return None


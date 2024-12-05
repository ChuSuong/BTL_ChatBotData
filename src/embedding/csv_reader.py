import os
import pandas as pd

class CSVReader:
    def __init__(self, folder_path):
        """
        Khởi tạo đối tượng CSVReader với đường dẫn tới thư mục chứa file CSV.
        :param folder_path: str - Đường dẫn tới thư mục chứa file CSV.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Thư mục '{folder_path}' không tồn tại.")
        self.folder_path = folder_path

    def read_files(self):
        """
        Đọc tất cả các file CSV trong thư mục.
        :return: Generator - Trả về nội dung từng file dưới dạng DataFrame cùng tên file.
        """
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.folder_path, file_name)

                yield pd.read_csv(file_path), file_name
        print("Đã đọc các file .csv")
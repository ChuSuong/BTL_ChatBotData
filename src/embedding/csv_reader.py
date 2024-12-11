import os
import pandas as pd

class CSVReader:
    def __init__(self, output_file):
        """
        Khởi tạo đối tượng CSVReader với đường dẫn tới thư mục chứa file CSV.
        :param chunked_folder: str - Đường dẫn tới thư mục chứa file CSV được chunk.
        """
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Thư mục '{output_file}' không tồn tại.")
        self.output_file = output_file

    def read_files(self):
        """
        Đọc tất cả các file CSV trong thư mục.
        :return: Generator - Trả về nội dung từng file dưới dạng DataFrame cùng tên file.
        """
        for file_name in os.listdir(self.output_file):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.output_file, file_name)

                yield pd.read_csv(file_path), file_name
        print("Đã đọc các file .csv")
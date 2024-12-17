import pandas as pd #Thư viện để xử lý dữ liệu dạng bảng (DataFrame)
import os # Thư viện hỗ trợ thao tác với file và thư mục
import logging # Thư viện ghi log thông tin, cảnh báo, hoặc lỗi

class DataReader:
    def __init__(self, api_key, folder_path):
        if not api_key:
            raise ValueError("API KEY không tìm thấy!")
        self.api_key = api_key
        self.folder_path = folder_path
        self.data_frames = [] # Danh sách chứa các DataFrame đã đọc từ file
        self.file_names = [  # Danh sách các file cần đọc
            "Students.csv",
            "Province.csv",
            "Studylevel.csv"
        ]

    def read_data(self): #Đọc dữ liệu từ danh sách file CSV trong folder_path và lưu vào data_frames
        try:
            for file_name in self.file_names:  # Lặp qua từng tên file trong danh sách file_names
                file_path = os.path.join(self.folder_path, file_name)  # Tạo đường dẫn đầy đủ của file
                if not os.path.exists(file_path):# Kiểm tra file có tồn tại không
                    logging.warning(f"File '{file_name}' không tồn tại trong thư mục.")
                    continue # Bỏ qua file này và tiếp tục

                logging.info(f"Đang đọc file: {file_path}")  # Ghi thông tin về việc đang đọc file
                data = pd.read_csv(file_path, encoding='utf-8') # Đọc file CSV thành DataFrame

                data.columns = data.columns.str.strip() # Loại bỏ khoảng trắng dư thừa ở đầu và cuối tên cột
                self.data_frames.append(data) # Thêm DataFrame đã đọc vào danh sách data_frames
        except pd.errors.EmptyDataError:
            logging.error("File rỗng không thể đọc.") # Ghi lỗi nếu file rỗng
        except pd.errors.ParserError:
            logging.error("Lỗi khi phân tích cú pháp file CSV.") # Ghi lỗi nếu có vấn đề khi phân tích cú pháp file CSV
        except Exception as e:
            logging.error(f"Lỗi khi đọc file: {e}") # Ghi lỗi cho các lỗi không xác định khác

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


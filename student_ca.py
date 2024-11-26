# import openai
import os
from importlib.metadata import files

from dotenv import load_dotenv
import json
import pandas as pd
import requests

class DataReader:

    def __init__(self, api_key, folder_path):
        if not api_key:
            raise ValueError("API KEY không tìm thấy!")
        self.api_key = api_key
        self.folder_path = folder_path
        self.data_frames = []

    def read_data(self):
        try:
            files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]

            for file_name in files:
                file_path = os.path.join(self.folder_path, file_name)
                print(f"Đang đọc file: {file_path}")
                data = pd.read_csv(file_path, encoding='utf-8')
                # Loại bỏ khoảng trắng dư thừa ở đầu và cuối tên cột
                data.columns = data.columns.str.strip()

                self.data_frames.append(data)
        except Exception as e:
            print(f"Lỗi khi duyệt thư mục hoặc đọc file: {e}")

    #Chunking theo alpha
    def chunk_by_alpha(self, text_column1, text_column2, text_column3):
        if not self.data_frames:
            print("Chưa có dữ liệu để phân mảnh.")
            return

        # Duyệt qua từng dataframe trong danh sách data_frames
        for idx, df in enumerate(self.data_frames):
            print(f"Đang phân mảnh dữ liệu từ file {idx + 1} theo chữ cái đầu tiên của cột {text_column1}, {text_column2} và {text_column3} ")
            if text_column1  not in df.columns or text_column2 not in df.columns or text_column3 not in df.columns:
                print(f"Cột '{text_column1}' hoặc '{text_column2}' hoặc '{text_column3}' không tồn tại trong file {idx + 1}")
                continue

            # Tạo cột mới chứa chữ cái đầu tiên của giá trị trong text_column 1 và 2
            df['first_letter_1'] = df[text_column1].apply(lambda x: str(x)[0].upper() if isinstance(x, str) else '')
            df['first_letter_2'] = df[text_column2].apply(lambda x: str(x)[0].upper() if isinstance(x, str) else '')
            df['first_letter_3'] = df[text_column3].apply(lambda x: str(x)[0].upper() if isinstance(x, str) else '')


            # Nhóm theo chữ cái đầu tiên
            grouped_1 = df.groupby('first_letter_1')
            grouped_2 = df.groupby('first_letter_2')
            grouped_3 = df.groupby('first_letter_3')

            # Lưu kết quả nhóm vào các file riêng biệt
            for group_name, group_df in grouped_1:
                output_file1 = f"chunk_{group_name}_{text_column1}_{idx + 1}.csv"
                group_df.to_csv(output_file1, index=False)
                print(f"Đã lưu chunk '{group_name}' vào {output_file1}")

            for group_name, group_df in grouped_2:
                output_file2 = f"chunk_{group_name}_{text_column2}_{idx + 1}.csv"
                group_df.to_csv(output_file2, index=False)
                print(f"Đã lưu chunk '{group_name}' vào {output_file2}")

            for group_name, group_df in grouped_3:
                output_file3 = f"chunk_{group_name}_{text_column3}_{idx + 1}.csv"
                group_df.to_csv(output_file3, index=False)
                print(f"Đã lưu chunk '{group_name}' vào {output_file3}")


    def display_data_frames(self):
        if not self.data_frames:
            print("Chưa có dữ liệu để hiển thị. Hãy chắc chắn rằng bạn đã gọi read_data_from_folder trước.")
            return

        for idx, df in enumerate(self.data_frames):
            print(f"Thông tin file {idx + 1}:")
            print(df.head(), "\n")

if __name__ == "__main__":
    #load environment vảiable
    load_dotenv()
    API_KEY = os.getenv("SECRET_API_KEY")

    #Define folder path
    archive_folder = "archive"

    #Create an instance of DataReader
    data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)

    #Read and display data
    data_reader.read_data()
    data_reader.display_data_frames()
    data_reader.chunk_by_alpha(text_column1="Country of Citizenship", text_column2="Province/territory", text_column3="Province/Territory" )





#
# def get_gemini_embedding(text):
#     headers = {"Authorization": f"Bearer {API_KEY}"}
#     payload = {"input": text}
#     response = requests.post(API_URL, json=payload, headers=headers)
#
#     if response.status_code == 200:
#         try:
#             response_json = response.json()
#             print(response_json)
#             return response_json.get("content", "No content")
#         except json.JSONDecoderError as e:
#             print("Lỗi phân tích cú pháp JSON:", e)
#             return None
#     else:
#         print(f"Lỗi: {response.status_code}, {response.text}")
#         return None
#
# def create_embedding(data, text_column):
#     if text_column not in data.columns:
#         raise  ValueError(f"Không tìm thấy cột '{text_column}' trong dữ liệu.")
#     print("Đang tạo embeddings từ Gemini Flash. Vui lòng chờ...")
#
#     data['embedding'] = data[text_column].apply(lambda x: get_gemini_embedding(x))
#     output_file = "gemini_embedded_data.csv"
#     data.to_csv(output_file, index=False)
#     print(f"Embeddings đã được lưu tại: {output_file}")




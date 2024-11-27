import os
import logging
from dotenv import load_dotenv
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Chunker:
    def __init__(self, data_frames, folder_path):
        self.data_frames = data_frames
        self.folder_path = folder_path

    def chunk_by_alpha(self, text_column, file_name):
        if not self.data_frames:
            logging.warning("Chưa có dữ liệu để phân mảnh.")
            return

        df = self.data_frames[0]  # Giả sử file 1 là file đầu tiên
        if text_column not in df.columns:
            logging.error(f"Cột '{text_column}' không tồn tại trong file 1.")
            return

        logging.info(f"Đang phân mảnh dữ liệu từ file '{file_name}' theo chữ cái đầu tiên của cột '{text_column}'")
        df['first_letter'] = df[text_column].apply(lambda x: str(x)[0].upper() if isinstance(x, str) else '')
        grouped = df.groupby('first_letter')

        for group_name, group_df in grouped:
            output_file = os.path.join(self.folder_path, f"chunk_{group_name}_{file_name}")
            group_df.to_csv(output_file, index=False)
            logging.info(f"Đã lưu chunk '{group_name}' vào {output_file}")

    def chunk_by_rows(self, file_name, chunk_size=5, file_index=1):
        if file_index >= len(self.data_frames):
            logging.error(f"Không tìm thấy dữ liệu cho file thứ {file_index + 1}.")
            return

        df = self.data_frames[file_index]
        logging.info(f"Đang phân mảnh dữ liệu từ file '{file_name}' thành các chunk {chunk_size} hàng.")
        for i in range(0, len(df), chunk_size):
            chunk_df = df.iloc[i:i + chunk_size]
            output_file = os.path.join(self.folder_path, f"chunk_{file_name}_{i // chunk_size + 1}.csv")
            chunk_df.to_csv(output_file, index=False)
            logging.info(f"Đã lưu chunk vào {output_file}")


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

    def chunk_data(self):
        chunker = Chunker(self.data_frames, self.folder_path)

        # File 1: Chunk theo chữ cái đầu tiên của cột "Country of Citizens"
        chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name=self.file_names[0])

        # File 2: Chunk theo số hàng
        chunker.chunk_by_rows(file_name=self.file_names[1], chunk_size=5, file_index=1)

        # File 3: Chunk theo số hàng (giống File 2)
        chunker.chunk_by_rows(file_name=self.file_names[2], chunk_size=5, file_index=2)

    def display_data_frames(self):
        if not self.data_frames:
            logging.warning("Chưa có dữ liệu để hiển thị. Hãy chắc chắn rằng bạn đã gọi read_data trước.")
            return

        for idx, df in enumerate(self.data_frames):
            logging.info(f"Thông tin file {idx + 1} - {self.file_names[idx]}:")


if __name__ == "__main__":
    # Load environment variable
    load_dotenv()
    API_KEY = os.getenv("SECRET_API_KEY")

    # Define folder path
    archive_folder = "archive"

    # Create an instance of DataReader
    data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)

    # Read and display data
    data_reader.read_data()
    data_reader.display_data_frames()

    # Call the chunk_data method to perform chunking
    data_reader.chunk_data()




#
#
# #
# # def get_gemini_embedding(text):
# #     headers = {"Authorization": f"Bearer {API_KEY}"}
# #     payload = {"input": text}
# #     response = requests.post(API_URL, json=payload, headers=headers)
# #
# #     if response.status_code == 200:
# #         try:
# #             response_json = response.json()
# #             print(response_json)
# #             return response_json.get("content", "No content")
# #         except json.JSONDecoderError as e:
# #             print("Lỗi phân tích cú pháp JSON:", e)
# #             return None
# #     else:
# #         print(f"Lỗi: {response.status_code}, {response.text}")
# #         return None
# #
# # def create_embedding(data, text_column):
# #     if text_column not in data.columns:
# #         raise  ValueError(f"Không tìm thấy cột '{text_column}' trong dữ liệu.")
# #     print("Đang tạo embeddings từ Gemini Flash. Vui lòng chờ...")
# #
# #     data['embedding'] = data[text_column].apply(lambda x: get_gemini_embedding(x))
# #     output_file = "gemini_embedded_data.csv"
# #     data.to_csv(output_file, index=False)
# #     print(f"Embeddings đã được lưu tại: {output_file}")
#
#
#
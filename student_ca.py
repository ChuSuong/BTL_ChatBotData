import os
import logging
from dotenv import load_dotenv
import pandas as pd
from langchain_openai import ChatOpenAI
import json



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Chunker:
    def __init__(self, data_frames, folder_path):
        self.data_frames = data_frames
        self.folder_path = folder_path

    #Phân chia dữ liệu thành các phần nhỏ với số hàng cố định
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

    #Phân chia dữ liệu thành các phần nhỏ với số hàng cố định
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

class EmbeddingHandler:

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API KEY không tìm thấy!")
        self.api_key = api_key
        openai.api_key = self.api_key

     # Tạo và lưu các embedding từ văn bản bằng OpenAI API.
    def generate_embeddings(self, texts):
        embeddings = []
        for text in texts:
            try:
                # Sử dụng openai.Embeddings.create
                response = openai.Embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                embeddings.append({
                    "text": text,
                    "embedding": response['data'][0]['embedding']
                })
            except Exception as e:
                logging.error(f"Lỗi khi tạo embedding cho văn bản '{text}': {e}")
        return embeddings

    #Lưu danh sách embedding vào file JSON.
    def save_embeddings_to_json(self, embeddings, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings, f, ensure_ascii=False, indent=4)
        logging.info(f"Đã lưu embeddings vào {output_file}")

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
    GPT_API_KEY = os.getenv("GPT_API_KEY")

    # Define folder path
    archive_folder = "archive"

    # Create an instance of DataReader
    data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)

    # Read and display data
    data_reader.read_data()
    data_reader.display_data_frames()

    # Call the chunk_data method to perform chunking
    data_reader.chunk_data()

    # Initialize EmbeddingHandler
    if API_KEY:  # Đảm bảo API Key tồn tại
        embedding_handler = EmbeddingHandler(api_key=API_KEY)

        # Generate embeddings for a specific column in the first DataFrame
        if data_reader.data_frames:
            df = data_reader.data_frames[0]  # Chọn DataFrame đầu tiên
            text_column = "Country of Citizenship"

            if text_column in df.columns:
                texts = df[text_column].dropna().unique().tolist()  # Lấy danh sách văn bản không trùng lặp
                embeddings = embedding_handler.generate_embeddings(texts)

                # Save embeddings to JSON
                output_file = os.path.join(archive_folder, "embeddings.json")
                embedding_handler.save_embeddings_to_json(embeddings, output_file)
            else:
                logging.warning(f"Cột '{text_column}' không tồn tại trong DataFrame đầu tiên.")
        else:
            logging.warning("Không có dữ liệu nào để tạo embeddings.")
    else:
        logging.error("API Key không được cung cấp. Không thể khởi tạo EmbeddingHandler.")
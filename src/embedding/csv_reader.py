# from sentence_transformers import SentenceTransformer
#
#
# class TextEmbedder:
#     def __init__(self, model_name="all-MiniLM-L6-v2"):
#         """
#         Khởi tạo mô hình embedding.
#         """
#         self.model = SentenceTransformer(model_name)
#
#     def encode_text(self, texts):
#         """
#         Mã hóa danh sách văn bản thành các vector.
#         :param texts: List[str] - Danh sách văn bản cần mã hóa.
#         :return: List[np.ndarray] - Danh sách các vector embedding.
#         """
#         if not isinstance(texts, list):
#             raise ValueError("Input phải là một danh sách các văn bản.")
#
#         # Mã hóa văn bản
#         embeddings = self.model.encode(texts)
#         return embeddings
#
#
# # Ví dụ sử dụng
# if __name__ == "__main__":
#     texts = [
#         "This is a simple text embedding example.",
#         "Text embeddings help machines understand semantic meaning.",
#         "Sentence Transformers are powerful for semantic search."
#     ]
#
#     embedder = TextEmbedder()
#     embeddings = embedder.encode_text(texts)
#
#     # In vector embedding đầu tiên
#     print(f"Embedding đầu tiên: {embeddings[0]}")
#     print(f"Kích thước vector: {len(embeddings[0])}")

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
                print(f"Đang đọc file: {file_name}")
                yield pd.read_csv(file_path), file_name

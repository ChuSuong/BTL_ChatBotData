from sentence_transformers import SentenceTransformer
import numpy as np

class TextEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Khởi tạo mô hình embedding.

        :param model_name: Tên mô hình SentenceTransformer để tạo embeddings (mặc định là 'all-MiniLM-L6-v2').
        """
        self.model = SentenceTransformer(model_name)

    def encode_text(self, texts):
        """
        Mã hóa danh sách văn bản thành các vector embedding.

        :param texts: List[str] - Danh sách các văn bản cần mã hóa.
        :return: List[np.ndarray] - Danh sách các vector embedding tương ứng với mỗi văn bản.
        """
        if not isinstance(texts, list):
            raise ValueError("Input phải là một danh sách các văn bản.")

        if not all(isinstance(text, str) for text in texts):
            raise ValueError("Tất cả các phần tử trong danh sách phải là chuỗi văn bản.")

        # Mã hóa văn bản thành các vector embedding
        embeddings = self.model.encode(texts)
        return embeddings






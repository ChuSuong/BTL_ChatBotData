import json
import numpy as np
import os

class VectorSearch:
    def __init__(self, embeddings_path):
        """
        Khởi tạo lớp tìm kiếm vector và tự động tải dữ liệu từ file JSON.
        :param embeddings_path: Đường dẫn tới file JSON lưu các vector embedding.
        """
        self.embeddings = self._load_embeddings(embeddings_path)

    def _load_embeddings(self, embeddings_path):
        """
        Tải và xử lý các vector embedding từ file JSON.
        :param embeddings_path: Đường dẫn tới file JSON.
        :return: Danh sách các vector embedding.
        """
        if not os.path.exists(embeddings_path):
            raise FileNotFoundError(f"Không tìm thấy file embedding: {embeddings_path}")

        try:
            with open(embeddings_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Đảm bảo định dạng JSON là đúng
            if "texts" not in data or "embeddings" not in data:
                raise ValueError("Định dạng file JSON không hợp lệ. Cần có các trường 'texts' và 'embeddings'.")

            texts = data["texts"]
            embeddings = np.array(data["embeddings"])

            if len(texts) != len(embeddings):
                raise ValueError("Số lượng văn bản và vector không khớp trong file JSON.")

            return [{"text": text, "embedding": embedding} for text, embedding in zip(texts, embeddings)]

        except json.JSONDecodeError as e:
            raise ValueError(f"Lỗi khi đọc file JSON: {e}")

    def search(self, query_embedding):
        """
        Tìm kiếm các văn bản có độ tương đồng cao nhất với query embedding.
        :param query_embedding: Vector embedding của truy vấn.
        :return: Danh sách các kết quả (văn bản, điểm tương đồng).
        """
        results = []
        for item in self.embeddings:
            text = item["text"]
            embedding = np.array(item["embedding"])
            similarity = self._cosine_similarity(query_embedding, embedding)
            results.append((text, similarity))

        # Sắp xếp theo điểm tương đồng giảm dần và lấy top_k
        results = sorted(results, key=lambda x: x[1], reverse=True)
        return results


    @staticmethod
    def _cosine_similarity(vec1, vec2):
        """
        Tính cosine similarity giữa hai vector.
        :param vec1: Vector thứ nhất.
        :param vec2: Vector thứ hai.
        :return: Điểm tương đồng cosine.
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0


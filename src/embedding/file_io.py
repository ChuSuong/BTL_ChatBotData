import json
import os


class FileIO:
    @staticmethod
    def save_embeddings_to_json(file_path, texts, embeddings):
        """
        Lưu danh sách văn bản và vector embedding tương ứng vào file JSON.
        :param file_path: str - Đường dẫn file JSON để lưu.
        :param texts: List[str] - Danh sách văn bản gốc.
        :param embeddings: List[List[float]] - Danh sách các vector embedding.
        """
        # if not os.path.exists(os.path.dirname(file_path)):
        #     os.makedirs(os.path.dirname(file_path))  # Tạo thư mục nếu chưa tồn tại
        if len(texts) != len(embeddings):
            raise ValueError("Số lượng văn bản và embeddings không khớp.")

        # Chuẩn bị dữ liệu để lưu
        data = {
            "texts": texts,
            "embeddings": embeddings
        }

        # Ghi dữ liệu vào file JSON
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Đã lưu embeddings vào file: {file_path}")
        except Exception as e:
            print(f"Lỗi khi lưu embeddings vào file: {e}")
        # with open(file_path, "w", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)
        #
        # print(f"Dữ liệu đã được lưu thành công tại: {file_path}")

    @staticmethod
    def load_embeddings_from_json(file_path):
        """
        Đọc dữ liệu embedding từ file JSON.
        :param file_path: str - Đường dẫn file JSON cần đọc.
        :return: List[dict] - Danh sách các văn bản và embedding.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' không tồn tại.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"Dữ liệu đã được đọc thành công từ: {file_path}")
        return data

    @staticmethod
    def save_text_to_file(file_path, text):
        """
        Lưu văn bản vào file.
        :param file_path: str - Đường dẫn file để lưu.
        :param text: str - Nội dung văn bản cần lưu.
        """
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))  # Tạo thư mục nếu chưa tồn tại

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Văn bản đã được lưu tại: {file_path}")

    @staticmethod
    def read_text_from_file(file_path):
        """
        Đọc văn bản từ file.
        :param file_path: str - Đường dẫn file cần đọc.
        :return: str - Nội dung văn bản.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' không tồn tại.")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Đã đọc thành công văn bản từ: {file_path}")
        return text

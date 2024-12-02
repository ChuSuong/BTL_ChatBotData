
import os
from dotenv import load_dotenv
from data_reader import DataReader
import logging
from chunking.chunk_data import Chunker
from embedding.csv_reader import CSVReader
from embedding.file_io import FileIO
from embedding.embedder import TextEmbedder
from embedding.vector_search import VectorSearch
from prompt import AIChatAssistant

def main():
    # Load environment variables
    load_dotenv()
    API_KEY = os.getenv("GPT_API_KEY")
    if not API_KEY:
        logging.error("API KEY không tồn tại trong biến môi trường!")
        exit()

    # DataReader: Load và hiển thị dữ liệu ban đầu
    archive_folder = "archive"
    data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)
    data_reader.read_data()
    data_reader.display_data_frames()

    # Chunking: Phân mảnh dữ liệu thành các file CSV nhỏ hơn
    if data_reader.data_frames:
        chunker = Chunker(data_reader.data_frames, archive_folder)

        # Phân mảnh theo chữ cái đầu tiên
        chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name="Internation_students_Canada.csv")

        # Phân mảnh theo số hàng (File 2 & 3)
        chunker.chunk_by_rows(file_name="Internation_students_Province_Canada.csv", chunk_size=5, file_index=1)
        chunker.chunk_by_rows(file_name="International_Students_Study_level.csv", chunk_size=5, file_index=2)

    # Embedding: Đọc các file CSV đã chunk và tạo vector embedding
    csv_reader = CSVReader(archive_folder)  # Tạo đối tượng CSVReader để đọc file CSV
    embedder = TextEmbedder()  # Tạo đối tượng TextEmbedder để mã hóa văn bản
    embeddings_output_path = "vector/embeddings.json"

    # Danh sách lưu kết quả embedding
    all_embeddings = []

    for df, file_name in csv_reader.read_files():
        # Kết hợp các cột dữ liệu thành một chuỗi văn bản
        texts = df.astype(str).apply(" ".join, axis=1).tolist()

        # Mã hóa các văn bản thành vector
        embeddings = embedder.encode_text(texts)

        # Lưu kết quả
        for text, embedding in zip(texts, embeddings):
            all_embeddings.append({
                "file": file_name,
                "text": text,
                "embedding": embedding.tolist()  # Chuyển np.ndarray thành list
            })

    # Lưu embedding vào file JSON
    FileIO.save_embeddings_to_json(
        file_path=embeddings_output_path,
        texts=[item['text'] for item in all_embeddings],
        embeddings=[item['embedding'] for item in all_embeddings]
    )

    print(f"Embedding đã được lưu vào file: {embeddings_output_path}")

    # Tạo đối tượng VectorSearch để tìm kiếm trong vector DB
    try:
        vector_search = VectorSearch(embeddings_path=embeddings_output_path)
    except Exception as e:
        logging.error(f"Lỗi khi tải vector DB: {e}")
        exit()

    # Khởi tạo AIChatAssistant
    chat_assistant = AIChatAssistant()  # Tạo đối tượng AIChatAssistant để xử lý phản hồi từ AI

    # Lấy truy vấn từ người dùng
    query = input("Nhập câu hỏi hoặc truy vấn của bạn: ").strip()

    if not query:
        print("Truy vấn không hợp lệ. Vui lòng thử lại.")
        return

    # Mã hóa truy vấn thành vector embedding
    try:
        query_embedding = embedder.encode_text([query])[0]
    except Exception as e:
        print(f"Lỗi khi mã hóa truy vấn: {e}")
        return

    # Tìm kiếm các văn bản tương đồng
    try:
        results = vector_search.search(query_embedding)
    except Exception as e:
        print(f"Lỗi khi tìm kiếm trong vector DB: {e}")
        return

    # Hiển thị kết quả tìm kiếm văn bản tương đồng
    print("\nCác kết quả tương đồng nhất:")
    for i, (text, score) in enumerate(results, start=1):
        print(f"{i}. Văn bản: {text}\n   Điểm tương đồng: {score:.4f}")

    context = "\n".join(
        [f"{i}. {text}" for i, (text, _) in enumerate(results, start=1)])  # Tạo ngữ cảnh từ các văn bản tìm được
    ai_query = f"Câu hỏi của người dùng: {query}\nDữ liệu tham chiếu:\n{context}\nVui lòng trả lời câu hỏi dựa trên dữ liệu tham chiếu."

    # Sử dụng AI để trả lời
    ai_response = chat_assistant.get_response(ai_query)
    print("\nPhản hồi từ AI Chat Assistant:")
    print(ai_response)


if __name__ == "__main__":
    main()



import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .data_reader import DataReader
from .chunking import Chunker
from .embedding import CSVReader
from .embedding import FileIO
from .embedding import TextEmbedder
from .embedding import VectorSearch
from dotenv import load_dotenv
import logging
from src.prompt import AIChatAssistant

def file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)

def initialize_system():
    load_dotenv()
    API_KEY = os.getenv("GPT_API_KEY")
    if not API_KEY:
        logging.error("API KEY không tồn tại trong biến môi trường!")
        exit()

    #Đường dẫn tới các file embedding
    archive_folder = "archive"
    chunked_folder = "chunked_folder"
    embeddings_output_path = "vector/embeddings.json"

    # Kiểm tra nếu embeddings đã tồn tại
    if os.path.exists(embeddings_output_path):
        logging.info("Embeddings đã tồn tại. Tải dữ liệu...")
        vector_search = VectorSearch(embeddings_path=embeddings_output_path)
    else:
        logging.info("Embeddings chưa tồn tại. Tiến hành xử lý dữ liệu...")
        # Đọc và xử lý dữ liệu từ file gốc
        data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)
        data_reader.read_data()

        if data_reader.data_frames:
            chunker = Chunker(data_reader.data_frames, archive_folder, chunked_folder)
            chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name="Students.csv")
            chunker.chunk_by_rows(file_name="Province.csv", chunk_size=5, file_index=1)
            chunker.chunk_by_rows(file_name="Studylevel.csv", chunk_size=5, file_index=2)

            # Tạo embeddings và lưu lại
            csv_reader = CSVReader(output_file=chunked_folder)
            embedder = TextEmbedder()
            embeddings_per_file = []

            for df, file_name in csv_reader.read_files():
                texts = df.astype(str).apply(" ".join, axis=1).tolist()
                embeddings = embedder.encode_text(texts)
                for text, embedding in zip(texts, embeddings):
                    embeddings_per_file.append({
                        "file": file_name,
                        "text": text,
                        "embedding": embedding.tolist()
                    })

            FileIO.save_embeddings_to_json(
                file_path=embeddings_output_path,
                texts=[item['text'] for item in embeddings_per_file],
                embeddings=[item['embedding'] for item in embeddings_per_file]
            )
            logging.info(f"Embedding đã được lưu vào file: {embeddings_output_path}")

        vector_search = VectorSearch(embeddings_path=embeddings_output_path)

    #Khởi tạo Chat Assistant
    chat_assistant = AIChatAssistant()
    return TextEmbedder(), vector_search, chat_assistant

#Hàm hỏi/đáp với AI
def chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history):
    try:
        #Tạo embedding cho câu truy vấn
        query_embedding = embedder.encode_text([user_query])[0]
        #Kết quả tìm kiếm liên quan
        results = vector_search.search(query_embedding)

        # Lấy thông tin từ kết quả tìm kiếm
        relevant_data = []
        for result in results:
            # Kiểm tra cấu trúc thực tế của từng phần tử
            if len(result) == 2:  # Nếu phần tử là tuple chứa (text, score)
                text, score = result
                file_name = "Unknown"  # Nếu không có file_name
                embedding = []  # Nếu không có embedding
            elif len(result) == 4:  # Nếu phần tử là tuple chứa (file_name, text, score, embedding)
                file_name, text, score, embedding = result
            else:
                raise ValueError(f"Cấu trúc không xác định: {result}")

            # Thêm vào danh sách dữ liệu tham chiếu
            relevant_data.append({
                "file": file_name,
                "text": text,
                "score": score,
                "embedding": embedding
            })

        # Tính điểm lệch chuẩn của kết quả tìm kiếm
        scores = [item["score"] for item in relevant_data]
        mean_score = sum(scores) / len(scores) if scores else 0
        std_deviation = (sum((x - mean_score) ** 2 for x in scores) / len(scores)) ** 0.5 if scores else 0
    except Exception as e:
        return {"error": f"Lỗi xử lý truy vấn: {e}"}

    references = "\n".join(
        f"- File: {item['file']}\n  Text: {item['text']}\n  Score: {item['score']:.4f}\n"
        for item in relevant_data
    )
    ai_query = (
        f"Câu hỏi của người dùng: {user_query}\n\n"
        f"Dữ liệu tham chiếu (hãy trả lời dựa trên dữ liệu này):\n{references}\n\n"
        "Vui lòng trả lời câu hỏi bằng cách trích dẫn cụ thể dữ liệu liên quan."
    )

    # Gọi AI để lấy phản hồi
    ai_response = chat_assistant.get_response(ai_query)
    # Thêm câu hỏi và phản hồi của AI vào lịch sử trò chuyện
    conversation_history.append(f"Câu hỏi: {user_query}")
    conversation_history.append(f"\nAI trả lời: {ai_response}")

    # Tạo phản hồi chi tiết
    detailed_response = {
        "response": ai_response,
        "references": relevant_data,
        "std_deviation": std_deviation,
        "history": conversation_history
    }
    return detailed_response

def run_cli(embedder, vector_search, chat_assistant):
    conversation_history = []
    print("\nHệ thống đã sẵn sàng. Nhập 'exit' để thoát.")
    while True:
        user_query = input("\nNhập câu hỏi hoặc truy vấn của bạn: ").strip()
        if user_query.lower() == "exit":
            print("\nKết thúc cuộc trò chuyện.")
            break

        result = chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history)
        if "error" in result:
            print(result["error"])
        else:
            print(f"\nAI trả lời: {result['response']}")
            # for ref in result["references"]:
            #     print(f"  - File: {ref['file']}")
            #     print(f"    Text: {ref['text']}")
            #     print(f"    Score: {ref['score']:.4f}")
            #     print(f"    Embedding: {ref['embedding'][:5]}...")
            # print(f"\nĐiểm lệch chuẩn: {result['std_deviation']:.4f}")
            conversation_history = result["history"]

if __name__ == "__main__":
    embedder, vector_search, chat_assistant = initialize_system()
    run_cli(embedder, vector_search, chat_assistant)
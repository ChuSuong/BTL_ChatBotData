import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_reader import DataReader
from chunking import Chunker
from embedding import CSVReader
from embedding import FileIO
from embedding import TextEmbedder
from embedding import VectorSearch
from dotenv import load_dotenv
import logging
from src.prompt import AIChatAssistant

# Khởi tạo các đối tượng toàn cục
def initialize_system():
    load_dotenv()
    API_KEY = os.getenv("GPT_API_KEY")
    if not API_KEY:
        logging.error("API KEY không tồn tại trong biến môi trường!")
        exit()

    archive_folder = "archive"
    data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)
    data_reader.read_data()
    data_reader.display_data_frames()

    if data_reader.data_frames:
        chunker = Chunker(data_reader.data_frames, archive_folder)
        chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name="Internation_students_Canada.csv")
        chunker.chunk_by_rows(file_name="Internation_students_Province_Canada.csv", chunk_size=5, file_index=1)
        chunker.chunk_by_rows(file_name="International_Students_Study_level.csv", chunk_size=5, file_index=2)

    csv_reader = CSVReader(archive_folder)
    embedder = TextEmbedder()
    embeddings_output_path = "vector/embeddings.json"
    all_embeddings = []

    for df, file_name in csv_reader.read_files():
        texts = df.astype(str).apply(" ".join, axis=1).tolist()
        embeddings = embedder.encode_text(texts)
        for text, embedding in zip(texts, embeddings):
            all_embeddings.append({"file": file_name, "text": text, "embedding": embedding.tolist()})

    FileIO.save_embeddings_to_json(
        file_path=embeddings_output_path,
        texts=[item['text'] for item in all_embeddings],
        embeddings=[item['embedding'] for item in all_embeddings]
    )
    print(f"Embedding đã được lưu vào file: {embeddings_output_path}")

    try:
        vector_search = VectorSearch(embeddings_path=embeddings_output_path)
    except Exception as e:
        logging.error(f"Lỗi khi tải vector DB: {e}")
        exit()

    chat_assistant = AIChatAssistant()

    return embedder, vector_search, chat_assistant


# Hàm hỏi/đáp với AI
def chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history):
    try:
        query_embedding = embedder.encode_text([user_query])[0]
        results = vector_search.search(query_embedding)
    except Exception as e:
        return {"error": f"Lỗi xử lý truy vấn: {e}"}

    context = "\n".join([f"{i}. {turn}" for i, turn in enumerate(conversation_history, start=1)])
    ai_query = f"Câu hỏi của người dùng: {user_query}\nDữ liệu tham chiếu:\n{context}\nVui lòng trả lời câu hỏi dựa trên dữ liệu tham chiếu."

    ai_response = chat_assistant.get_response(ai_query)
    conversation_history.append(f"Câu hỏi: {user_query}")
    conversation_history.append(f"AI trả lời: {ai_response}")

    return {"response": ai_response, "history": conversation_history}

def run_cli(embedder, vector_search, chat_assistant):
    """
    Chạy giao diện CLI để hỏi/đáp với AI.
    """
    conversation_history = []
    print("Hệ thống đã sẵn sàng. Nhập 'exit' để thoát.")
    while True:
        user_query = input("Nhập câu hỏi hoặc truy vấn của bạn: ").strip()
        if user_query.lower() == "exit":
            print("Kết thúc cuộc trò chuyện.")
            break

        # Gọi hàm xử lý truy vấn
        result = chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history)
        if "error" in result:
            print(result["error"])
        else:
            print(f"AI trả lời: {result['response']}")
            conversation_history = result["history"]


if __name__ == "__main__":
    # Khởi tạo hệ thống
    embedder, vector_search, chat_assistant = initialize_system()

    # Chạy giao diện CLI
    run_cli(embedder, vector_search, chat_assistant)
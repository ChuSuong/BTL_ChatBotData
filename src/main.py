# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# from .data_reader import DataReader
# from .chunking import Chunker
# from .embedding import CSVReader
# from .embedding import FileIO
# from .embedding import TextEmbedder
# from .embedding import VectorSearch
# from dotenv import load_dotenv
# import logging
# from src.prompt import AIChatAssistant
#
# #Kiểm tra sự tồn tại của file
# def file_exists(file_path):
#     return os.path.exists(file_path) and os.isfile(file_path)
#
# # Khởi tạo các đối tượng toàn cục
# def initialize_system():
#     load_dotenv()
#     API_KEY = os.getenv("GPT_API_KEY")
#     if not API_KEY:
#         logging.error("API KEY không tồn tại trong biến môi trường!")
#         exit()
#
#     archive_folder = "archive"
#     data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)
#     data_reader.read_data()
#     data_reader.display_data_frames()
#
#     if data_reader.data_frames:
#         chunker = Chunker(data_reader.data_frames, archive_folder)
#         chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name="Internation_students_Canada.csv")
#         chunker.chunk_by_rows(file_name="Internation_students_Province_Canada.csv", chunk_size=5, file_index=1)
#         chunker.chunk_by_rows(file_name="International_Students_Study_level.csv", chunk_size=5, file_index=2)
#
#     csv_reader = CSVReader(archive_folder)
#     embedder = TextEmbedder()
#     embeddings_output_path = "vector/embeddings.json"
#     all_embeddings = []
#
#     for df, file_name in csv_reader.read_files():
#         texts = df.astype(str).apply(" ".join, axis=1).tolist()
#         embeddings = embedder.encode_text(texts)
#         for text, embedding in zip(texts, embeddings):
#             all_embeddings.append({"file": file_name, "text": text, "embedding": embedding.tolist()})
#
#     FileIO.save_embeddings_to_json(
#         file_path=embeddings_output_path,
#         texts=[item['text'] for item in all_embeddings],
#         embeddings=[item['embedding'] for item in all_embeddings]
#     )
#     print(f"Embedding đã được lưu vào file: {embeddings_output_path}")
#
#     try:
#         vector_search = VectorSearch(embeddings_path=embeddings_output_path)
#     except Exception as e:
#         logging.error(f"Lỗi khi tải vector DB: {e}")
#         exit()
#
#     chat_assistant = AIChatAssistant()
#
#     return embedder, vector_search, chat_assistant
#
#
# # Hàm hỏi/đáp với AI
# def chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history):
#     try:
#         query_embedding = embedder.encode_text([user_query])[0]
#         results = vector_search.search(query_embedding)
#     except Exception as e:
#         return {"error": f"Lỗi xử lý truy vấn: {e}"}
#
#     context = "\n".join([f"{i}. {turn}" for i, turn in enumerate(conversation_history, start=1)])
#     ai_query = f"Câu hỏi của người dùng: {user_query}\nDữ liệu tham chiếu:\n{context}\nVui lòng trả lời câu hỏi dựa trên dữ liệu tham chiếu."
#
#     ai_response = chat_assistant.get_response(ai_query)
#     conversation_history.append(f"Câu hỏi: {user_query}")
#     conversation_history.append(f"AI trả lời: {ai_response}")
#
#     return {"response": ai_response, "history": conversation_history}
#
# def run_cli(embedder, vector_search, chat_assistant):
#     """
#     Chạy giao diện CLI để hỏi/đáp với AI.
#     """
#     conversation_history = []
#     print("Hệ thống đã sẵn sàng. Nhập 'exit' để thoát.")
#     while True:
#         user_query = input("Nhập câu hỏi hoặc truy vấn của bạn: ").strip()
#         if user_query.lower() == "exit":
#             print("Kết thúc cuộc trò chuyện.")
#             break
#
#         # Gọi hàm xử lý truy vấn
#         result = chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history)
#         if "error" in result:
#             print(result["error"])
#         else:
#             print(f"AI trả lời: {result['response']}")
#             conversation_history = result["history"]
#
#
# if __name__ == "__main__":
#     # Khởi tạo hệ thống
#     embedder, vector_search, chat_assistant = initialize_system()
#
#     # Chạy giao diện CLI
#     run_cli(embedder, vector_search, chat_assistant)

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# from data_reader import DataReader
# from chunking import Chunker
# from embedding import CSVReader
# from embedding import FileIO
# from embedding import TextEmbedder
# from embedding import VectorSearch
# from dotenv import load_dotenv
# import logging
# from src.prompt import AIChatAssistant
#
# # Kiểm tra sự tồn tại của file
# def file_exists(file_path):
#     return os.path.exists(file_path) and os.path.isfile(file_path)
#
# # Khởi tạo các đối tượng toàn cục
# def initialize_system():
#     load_dotenv()
#     API_KEY = os.getenv("GPT_API_KEY")
#     if not API_KEY:
#         logging.error("API KEY không tồn tại trong biến môi trường!")
#         exit()
#
#     archive_folder = "archive"
#     embeddings_output_path = "vector/embeddings.json"
#
#     # Kiểm tra sự tồn tại của các file cần thiết
#     need_to_process_data = not file_exists(embeddings_output_path)
#
#     if need_to_process_data:
#         logging.info("Các file dữ liệu cần thiết chưa tồn tại. Tiến hành xử lý...")
#
#         # Bước 1: Đọc dữ liệu
#         data_reader = DataReader(api_key=API_KEY, folder_path=archive_folder)
#         data_reader.read_data()
#         data_reader.display_data_frames()
#
#         if data_reader.data_frames:
#             # Bước 2: Chunking dữ liệu
#             chunker = Chunker(data_reader.data_frames, archive_folder)
#             chunker.chunk_by_alpha(text_column="Country of Citizenship", file_name="Internation_students_Canada.csv")
#             chunker.chunk_by_rows(file_name="Internation_students_Province_Canada.csv", chunk_size=5, file_index=1)
#             chunker.chunk_by_rows(file_name="International_Students_Study_level.csv", chunk_size=5, file_index=2)
#
#         # Bước 3: Tạo embedding
#         csv_reader = CSVReader(archive_folder)
#         embedder = TextEmbedder()
#         all_embeddings = []
#
#         for df, file_name in csv_reader.read_files():
#             texts = df.astype(str).apply(" ".join, axis=1).tolist()
#             embeddings = embedder.encode_text(texts)
#             for text, embedding in zip(texts, embeddings):
#                 all_embeddings.append({"file": file_name, "text": text, "embedding": embedding.tolist()})
#
#         FileIO.save_embeddings_to_json(
#             file_path=embeddings_output_path,
#             texts=[item['text'] for item in all_embeddings],
#             embeddings=[item['embedding'] for item in all_embeddings]
#         )
#         logging.info(f"Embedding đã được lưu vào file: {embeddings_output_path}")
#     else:
#         logging.info("Các file dữ liệu đã tồn tại. Bỏ qua bước xử lý dữ liệu.")
#
#     # Khởi tạo VectorSearch và AIChatAssistant
#     try:
#         vector_search = VectorSearch(embeddings_path=embeddings_output_path)
#     except Exception as e:
#         logging.error(f"Lỗi khi tải vector DB: {e}")
#         exit()
#
#     chat_assistant = AIChatAssistant()
#
#     return TextEmbedder(), vector_search, chat_assistant
#
#
# # Hàm hỏi/đáp với AI
# def chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history):
#     try:
#         #Tạo embedding cho câu truy vấn
#         query_embedding = embedder.encode_text([user_query])[0]
#         #Kết quả tìm kiếm liên quan
#         results = vector_search.search(query_embedding)
#
#         # Lấy thông tin từ kết quả tìm kiếm
#         relevant_data = []
#         for result in results:
#             # Kiểm tra cấu trúc thực tế của từng phần tử
#             if len(result) == 2:  # Nếu phần tử là tuple chứa (text, score)
#                 text, score = result
#                 file_name = "Unknown"  # Nếu không có file_name
#                 embedding = []  # Nếu không có embedding
#             elif len(result) == 4:  # Nếu phần tử là tuple chứa (file_name, text, score, embedding)
#                 file_name, text, score, embedding = result
#             else:
#                 raise ValueError(f"Cấu trúc không xác định: {result}")
#
#             # Thêm vào danh sách dữ liệu tham chiếu
#             relevant_data.append({
#                 "file": file_name,
#                 "text": text,
#                 "score": score,
#                 "embedding": embedding
#             })
#
#         # Tính điểm lệch chuẩn của kết quả tìm kiếm
#         scores = [item["score"] for item in relevant_data]
#         mean_score = sum(scores) / len(scores) if scores else 0
#         std_deviation = (sum((x - mean_score) ** 2 for x in scores) / len(scores)) ** 0.5 if scores else 0
#     except Exception as e:
#         return {"error": f"Lỗi xử lý truy vấn: {e}"}
#
#     references = "\n".join(
#         f"- File: {item['file']}\n  Text: {item['text']}\n  Score: {item['score']:.4f}\n"
#         for item in relevant_data
#     )
#     ai_query = (
#         f"Câu hỏi của người dùng: {user_query}\n\n"
#         f"Dữ liệu tham chiếu (hãy trả lời dựa trên dữ liệu này):\n{references}\n\n"
#         "Vui lòng trả lời câu hỏi bằng cách trích dẫn cụ thể dữ liệu liên quan."
#     )
#
#     # Gọi AI để lấy phản hồi
#     ai_response = chat_assistant.get_response(ai_query)
#     # Thêm câu hỏi và phản hồi của AI vào lịch sử trò chuyện
#     conversation_history.append(f"Câu hỏi: {user_query}")
#     conversation_history.append(f"\nAI trả lời: {ai_response}")
#
#     # Tạo phản hồi chi tiết
#     detailed_response = {
#         "response": ai_response,
#         "references": relevant_data,
#         "std_deviation": std_deviation,
#         "history": conversation_history
#     }
#     return detailed_response
#
# # Chạy giao diện CLI
# def run_cli(embedder, vector_search, chat_assistant):
#
#     #Chạy giao diện CLI để hỏi/đáp với AI.
#     conversation_history = []
#     print("\nHệ thống đã sẵn sàng. Nhập 'exit' để thoát.")
#     while True:
#         user_query = input("\nNhập câu hỏi hoặc truy vấn của bạn: ").strip()
#         if user_query.lower() == "exit":
#             print("\nKết thúc cuộc trò chuyện.")
#             break
#
#         # Gọi hàm xử lý truy vấn
#         result = chat_with_ai(embedder, vector_search, chat_assistant, user_query, conversation_history)
#         if "error" in result:
#             print(result["error"])
#         else:
#             print(f"\nAI trả lời: {result['response']}")
#             print("\nDữ liệu tham chiếu:")
#             for ref in result["references"]:
#                 print(f"  - File: {ref['file']}")
#                 print(f"    Text: {ref['text']}")
#                 print(f"    Score: {ref['score']:.4f}")
#                 print(f"    Embedding: {ref['embedding'][:5]}...")  # Hiển thị một phần embedding
#             print(f"\nĐiểm lệch chuẩn: {result['std_deviation']:.4f}")
#             conversation_history = result["history"]
#
#
# if __name__ == "__main__":
#     # Khởi tạo hệ thống
#     embedder, vector_search, chat_assistant = initialize_system()
#
#     # Chạy giao diện CLI
#     run_cli(embedder, vector_search, chat_assistant)

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

    archive_folder = "archive"
    embeddings_output_path = "vector/embeddings.json"
    need_to_process_data = not file_exists(embeddings_output_path)

    if need_to_process_data:
        logging.info("Các file dữ liệu cần thiết chưa tồn tại. Tiến hành xử lý...")
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
        logging.info(f"Embedding đã được lưu vào file: {embeddings_output_path}")
    else:
        logging.info("Các file dữ liệu đã tồn tại. Bỏ qua bước xử lý dữ liệu.")

    try:
        vector_search = VectorSearch(embeddings_path=embeddings_output_path)
    except Exception as e:
        logging.error(f"Lỗi khi tải vector DB: {e}")
        exit()

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
            for ref in result["references"]:
                print(f"  - File: {ref['file']}")
                print(f"    Text: {ref['text']}")
                print(f"    Score: {ref['score']:.4f}")
                print(f"    Embedding: {ref['embedding'][:5]}...")
            print(f"\nĐiểm lệch chuẩn: {result['std_deviation']:.4f}")
            conversation_history = result["history"]

if __name__ == "__main__":
    embedder, vector_search, chat_assistant = initialize_system()
    run_cli(embedder, vector_search, chat_assistant)

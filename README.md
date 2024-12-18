# Ứng dụng Chatbot Hỏi Đáp Cơ Bản trên Dữ Liệu Cố Định

## Giới thiệu: 
Ứng dụng Chatbot Hỏi Đáp được xây dựng để cung cấp các câu trả lời dựa trên một tập dữ liệu cố định.Chatbot này có thể: 
- Trả lời câu hỏi dựa trên tập dữ liệu cố định.
- Sử dụng mô hình SentenceTransformer để tạo embeddings cho văn bản.
- Tìm kiếm câu trả lời bằng cách sử dụng Cosine Similarity trên các vector.
Ứng dụng phù hợp để làm ví dụ học tập hoặc triển khai chatbot cơ bản cho các tập dữ liệu cố định như FAQ, tài liệu công ty, hoặc cơ sở tri thức nhỏ.

## Tính năng
- Xử lý và phân tích câu hỏi từ người dùng.
- Tìm câu trả lời tương tự nhất từ dữ liệu đã được cung cấp.
- Hoạt động offline mà không cần kết nối tới API bên ngoài.

## Yêu cầu
- Python 3.7 trở lên
- SentenceTransformer
- NumPy: Xử lý và tính toán các vector.
- JSON: Quản lý dữ liệu đầu vào/đầu ra.
- Python-dotenv #Tải các biến môi trường từ file .env
- Langchain_openai  #Kết nối AI
- Streamlit #Chạy giao diện ChatBot
  
## Cài đặt
1. **Clone repository**:
   ```bash
      https://github.com/ChuSuong/BTL_Python.git
   ```

2. **Cài đặt môi trường ảo**:
    ```bash
     python -m venv venv
     source venv/bin/activate  # Trên macOS/Linux
     venv\Scripts\activate     # Trên Window
   ```
3. **Cài đặt thư viện**:
   ```bash
    pip install -r requirements.txt
   ```

3. **Tải mô hình Chatbot**:
   - Tải mô hình chatbot data dựa vào thư mục front_end và tên file là 'chatbot.py'.

## Cấu trúc thư mục
```bash
BTL_Python/
├── archive/ #Thư mục lưu dữ liệu đầu vào
│   ├── Province.csv
│   ├── Students.csv
│   └── Studylevel.csv
├── chunked_folder #Thư mục lưu các file có dữ liệu sau khi chunking
├── front_end/ #Thư mục chứa giao diện Chatbot Data
│   ├── __init__.py
│   └── chatbot.py
├── src/ #Thư mục gốc chứa mã nguồn chính
│   ├── chunking/ #Thư mục xử lý việc chia nhỏ dữ liệu lớn thành các phần
│   │   ├── __init__.py
│   │   └── chunk_data.py
│   ├── data_reader/ #Thư mục đọc và xử lý dữ liệu từ các nguồn đầu vào
│   │   ├── __init__.py
│   │   └── reader.py
│   ├── embedding/ #Thư mục xử lý và lưu trữ embedding
│   │   ├── __init__.py
│   │   ├── csv_reader.py
│   │   ├── embedder.py
│   │   ├── file_io.py
│   │   └── vector_search.py #File tính độ tương đồng giữa các vector
│   ├── __init__.py
│   ├── main.py #File gốc chạy chương trình
│   └── prompt.py # File xử lý prompt cho mô hình AI.
├── vector/ #Thư mục lưu các vector DB
│   └── embeddings.json
├── .env #Môi trường ảo lưu trữ thông tin API
├── .gitignore
├── README.md
└── requirements.txt

```

## Cách sử dụng
1. **Khởi động ứng dụng**:
   - Chạy file `main.py`:
   ```bash
   python -m src.main
   ```

2. **Sử dụng giao diện**:
    - Chạy file `chatbot.py`:
   ```bash
   streamlit run .\front_end\chatbot.py
   ```

## Ghi chú


## Tài liệu tham khảo


## Giấy phép

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from .embedding import TextEmbedder
from .embedding import VectorSearch

class AIChatAssistant:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.5, max_tokens=1000):
        load_dotenv()  # Load biến môi trường từ tệp .env

        # Lấy API Key từ biến môi trường
        self.api_key = os.getenv('GPT_API_KEY')
        if not self.api_key:
            raise EnvironmentError("API Key không được tìm thấy trong biến môi trường.")

        # Khởi tạo mô hình
        self.model = ChatOpenAI(
            api_key=self.api_key,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Tạo prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Bạn là một nhà phân tích dữ liệu thông minh. Nhiệm vụ của bạn là cung cấp câu trả lời chính xác và chi tiết dựa trên số liệu từ file archive. "
                "Khi trả lời, hãy ưu tiên sử dụng thông tin cụ thể từ các văn bản được cung cấp. Nếu cần thiết, giải thích cách dữ liệu hỗ trợ câu trả lời."
            )),
            ("human", "{input}"),
            (
                "assistant",
                "Dưới đây là các văn bản có liên quan mà bạn có thể tham khảo:\n{texts}\n"
                "Hãy trả lời câu hỏi dựa trên các văn bản trên và chỉ cung cấp thông tin có thể suy ra từ chúng. Nếu thông tin không đủ, hãy nói rõ điều này."
            )
        ])

        # Tạo output parser
        self.output_parser = StrOutputParser()

        # Tạo chuỗi xử lý
        self.chain = self.prompt | self.model | self.output_parser

        # Khởi tạo các công cụ cho việc mã hóa văn bản và tìm kiếm vector
        self.embedder = TextEmbedder()
        self.vector_search = VectorSearch(embeddings_path="vector/embeddings.json")

    def get_response(self, query):
        """
        Lấy phản hồi từ AI dựa trên truy vấn đầu vào và các văn bản liên quan.
        """
        if not query.strip():
            return "Vui lòng cung cấp một truy vấn hợp lệ."

        try:
            # Mã hóa truy vấn thành vector embedding
            query_embedding = self.embedder.encode_text([query])[0]

            # Tìm kiếm các văn bản tương đồng trong vector database
            results = self.vector_search.search(query_embedding)

            # Lấy các văn bản tương đồng
            texts = [text for text, _ in results]

            # Tạo prompt với các văn bản tương đồng và câu truy vấn của người dùng
            prompt = self.prompt | self.model | self.output_parser

            # Gửi truy vấn và các văn bản liên quan vào mô hình để nhận câu trả lời
            response = prompt.invoke({"input": query, "texts": texts})
            return response

        except Exception as e:
            return f"Đã xảy ra lỗi khi xử lý truy vấn: {e}"



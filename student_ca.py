# import openai
import json
import pandas as pd
import matplotlib.pyplot as plt
import requests


API_KEY = "AIzaSyAeHhDebqy-9CIf8eRLF0vAAdSasyoYCBM"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyAeHhDebqy-9CIf8eRLF0vAAdSasyoYCBM"
def read_data(path):
    with open(path, mode='r', encoding='utf8') as file:
        data_student = pd.read_csv(file)
    return data_student

def display(data_student):
    data_student = data_student.dropna() #Loại bỏ hàng bị thiếu
    print("First 5 rows of the data:")
    print(data_student.head())
    print("\n")
    print("Data Information:")
    data_student.info()
    print("\n")
from urllib.parse import splittag

def get_gemini_embedding(text):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"input": text}
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            response_json = response.json()
            print(response_json)
            return response_json.get("content", "No content")
        except json.JSONDecoderError as e:
            print("Lỗi phân tích cú pháp JSON:", e)
            return None
    else:
        print(f"Lỗi: {response.status_code}, {response.text}")
        return None

def create_embedding(data, text_column):
    if text_column not in data.columns:
        raise  ValueError(f"Không tìm thấy cột '{text_column}' trong dữ liệu.")
    print("Đang tạo embeddings từ Gemini Flash. Vui lòng chờ...")

    data['embedding'] = data[text_column].apply(lambda x: get_gemini_embedding(x))
    output_file = "gemini_embedded_data.csv"
    data.to_csv(output_file, index=False)
    print(f"Embeddings đã được lưu tại: {output_file}")

# def student_year(data_student):
#     #Số lượng sinh viên quốc tế thay đổi từ 2015 - 2013 (9 năm)
#     student_per_year = data_student.iloc[:, 1:].sum().head(9)
#
#     #Convert index(năm) thành kiểu int
#     student_per_year.index = student_per_year.index.astype(int)
#     print(student_per_year.head())  #Hiển thị tổng số sinh viên
#
#     #Lưu kqua tổng sv vào vector (danh sách)
#     student_vector = student_per_year.tolist()
#
#     #Lưu vào file Json
#     with open('student_embedding.json', 'w') as json_file:
#         json.dump(student_vector, json_file)
#
#     #Vẽ:
#     plt.figure(figsize=(10, 6))
#     student_per_year.plot(kind='line', marker = 'o', color = 'skyblue')
#
#     plt.title("Annual Growth Trends of International Students in Canada (2015-2023)")
#     plt.xlabel('Year')
#     plt.ylabel('The total number of students')
#     # plt.xticks(rotations=45)
#
#     #Dựng đường thẳng cho thời điểm Covid-19 (năm 2020)
#     plt.axvline(x=2020, color='r', linestyle='--', label='COVID-19')
#     plt.legend()
#     plt.show()

#Đọc dữ liệu và hiển thị từ file CSV
if __name__ == "__main__":
    # Đường dẫn đến file CSV
    file_path = "Internation_students_Canada.csv"

    # Đọc dữ liệu
    try:
        data_student = read_data(file_path)
        display(data_student)

        # Tạo embeddings
        data_student = create_embedding(data_student,text_column="Country of Citizenship")  # Thay 'Description' bằng cột chứa văn bản thực tế
    except Exception as e:
        print(f"Lỗi: {e}")


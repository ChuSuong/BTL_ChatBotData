import json

import pandas as pd
import matplotlib.pyplot as plt


def read_data(path):
    with open(path, mode='r', encoding='utf8') as file:
        data_student = pd.read_csv(file)
    return data_student

def display(data_student):
    print("First 5 rows of the data:")
    print(data_student.head())
    print("\n")
    print("Data Information:")
    data_student.info()
    print("\n")

def student_year(data_student):
    #Số lượng sinh viên quốc tế thay đổi từ 2015 - 2013 (9 năm)
    student_per_year = data_student.iloc[:, 1:].sum().head(9)

    #Convert index(năm) thành kiểu int
    student_per_year.index = student_per_year.index.astype(int)
    print(student_per_year.head())  #Hiển thị tổng số sinh viên

    #Lưu kqua tổng sv vào vector (danh sách)
    student_vector = student_per_year.tolist()

    #Lưu vào file Json
    with open('student_embedding.json', 'w') as json_file:
        json.dump(student_vector, json_file)

    #Vẽ:
    plt.figure(figsize=(10, 6))
    student_per_year.plot(kind='line', marker = 'o', color = 'skyblue')

    plt.title("Annual Growth Trends of International Students in Canada (2015-2023)")
    plt.xlabel('Year')
    plt.ylabel('The total number of students')
    # plt.xticks(rotations=45)

    #Dựng đường thẳng cho thời điểm Covid-19 (năm 2020)
    plt.axvline(x=2020, color='r', linestyle='--', label='COVID-19')
    plt.legend()
    plt.show()

#Đọc dữ liệu và hiển thị từ file CSV
path = 'D:\docker_images\museum-backend-admin\Python\PROJECT_DATA\BTL_Python\Internation_students_Canada.csv'
data_student = read_data(path)
display(data_student)
student_year(data_student)


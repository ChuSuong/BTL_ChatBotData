import logging
import os

class Chunker:
    def __init__(self, data_frames, folder_path):
        self.data_frames = data_frames
        self.folder_path = folder_path

    def chunk_by_alpha(self, text_column, file_name):
        """Phân chia dữ liệu thành các phần theo chữ cái đầu tiên."""
        if not self.data_frames:
            logging.warning("Chưa có dữ liệu để phân mảnh.")
            return

        df = self.data_frames[0]  # Giả sử xử lý file đầu tiên
        if text_column not in df.columns:
            logging.error(f"Cột '{text_column}' không tồn tại trong file đầu tiên.")
            return

        logging.info(f"Đang phân mảnh dữ liệu từ file '{file_name}' theo chữ cái đầu tiên của cột '{text_column}'.")
        df['first_letter'] = df[text_column].apply(lambda x: str(x)[0].upper() if isinstance(x, str) else '')
        grouped = df.groupby('first_letter')

        for group_name, group_df in grouped:
            output_file = os.path.join(self.folder_path, f"chunk_{group_name}_{file_name}")
            group_df.to_csv(output_file, index=False)
            logging.info(f"Đã lưu chunk '{group_name}' vào {output_file}.")

    def chunk_by_rows(self, file_name, chunk_size=5, file_index=1):
        """Phân chia dữ liệu thành các phần nhỏ với số hàng cố định."""
        if file_index >= len(self.data_frames):
            logging.error(f"Không tìm thấy dữ liệu cho file thứ {file_index + 1}.")
            return

        df = self.data_frames[file_index]
        logging.info(f"Đang phân mảnh dữ liệu từ file '{file_name}' thành các chunk {chunk_size} hàng.")
        for i in range(0, len(df), chunk_size):
            chunk_df = df.iloc[i:i + chunk_size]
            output_file = os.path.join(self.folder_path, f"chunk_{file_name}_{i // chunk_size + 1}.csv")
            chunk_df.to_csv(output_file, index=False)
            logging.info(f"Đã lưu chunk vào {output_file}.")

import math
import random
import pandas
from PyQt5.QtWidgets import QMessageBox

class SeatArranger:
    def __init__(self):
        self.student_list = []  # 学生名单
        self.column_num = 0     # 列数
        self.row_num = 0        # 行数
        self.board = []         # 座位表

    def load_students(self, file_path):
        """加载学生名单文件，返回学生数量或错误信息"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if file_path.endswith(".txt"):
                    self.student_list = [line.strip() for line in f.readlines() if line.strip()]
                elif file_path.endswith(".csv"):
                    df = pandas.read_csv(file_path, encoding='utf-8-sig')
                    self.student_list = df['name'].tolist()
            return len(self.student_list)
        except Exception as e:
            return f"文件加载失败: {str(e)}"

    def set_column_num(self, column_num):
        """设置列数，返回错误信息或 None"""
        try:
            self.column_num = int(column_num)
            if self.column_num <= 0:
                raise ValueError("列数必须为正整数")
            return None
        except ValueError as e:
            return f"列数设置失败: {str(e)}"

    def generate_seating(self):
        """生成随机座位表，返回错误信息或 None"""
        if not self.student_list or self.column_num <= 0:
            return "请先加载学生名单并设置有效列数"
        student_num = len(self.student_list)
        self.row_num = math.ceil(student_num / self.column_num)
        random.shuffle(self.student_list)
        self.board = [self.student_list[i * self.column_num:(i + 1) * self.column_num] 
                      for i in range(self.row_num)]
        # 补齐最后一行的空缺
        while len(self.board[-1]) < self.column_num:
            self.board[-1].append("")
        return None

    def save_seating(self, file_name):
        """保存座位表到 CSV 文件，返回错误信息或 None"""
        if not self.board:
            return "请先生成座位表"
        row_names = [str(row) for row in range(1, self.row_num + 1)]
        column_names = [str(col) for col in range(1, self.column_num + 1)]
        df = pandas.DataFrame(self.board, columns=column_names, index=row_names)
        try:
            df.to_csv(file_name, encoding='utf-8-sig')
            return None
        except Exception as e:
            return f"保存失败: {str(e)}"
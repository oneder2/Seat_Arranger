import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow, QAction, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
import math
import random
import pandas
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # <菜单>-基础信息
        self.setWindowTitle("排座位")
        self.setGeometry(100, 100, 600, 400)
        # 创建菜单栏
        self.menu_bar = self.menuBar()
        # --<文件>-菜单
        file_menu = self.menu_bar.addMenu("文件")
        # 创建退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)  # 连接退出动作到关闭窗口
        file_menu.addAction(exit_action)
        # 创建保存动作
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_file)  # 连接退出动作到关闭窗口
        file_menu.addAction(save_action)

        # --<帮助>-菜单
        help_menu = self.menu_bar.addMenu("帮助")
        # 创建关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)  # 连接关于动作到显示关于信息
        help_menu.addAction(about_action)
        
        # <按钮>-创建表格
        # 创建一个中心小部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # 创建垂直布局
        self.layout = QVBoxLayout(self.central_widget)
        # 创建按钮
        self.add_button = QPushButton("显示表格", self)
        self.add_button.clicked.connect(self.show_table)  # 连接按钮点击事件
        self.layout.addWidget(self.add_button)
        # 初始化表格为 None
        self.table_widget = None

        # <按钮>-选择文件
        # 创建按钮
        self.select_button = QPushButton("选择文件", self)
        self.select_button.clicked.connect(self.open_file_dialog)  # 连接按钮点击事件
        self.layout.addWidget(self.select_button)
        # 创建标签用于显示选择的文件路径
        self.file_label = QLabel("选择的文件路径将显示在这里", self)
        self.layout.addWidget(self.file_label)

        # <列数>-选择文件名称
        # 创建文本框
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("在这里输入排座目标列数：")
        self.layout.addWidget(self.text_input)
        # 创建按钮
        self.button = QPushButton("确认", self)
        self.button.clicked.connect(self.read_text)
        self.layout.addWidget(self.button)
        # 创建标签用于显示读取的文本
        self.column_label = QLabel("", self)
        self.layout.addWidget(self.column_label)


    def show_about(self):
        QMessageBox.information(self, "关于", "这是一个简单的排座位程序。给定一个学生列表，以及你希望生成的座位的>    列数，就可以生成一个完全随机的座位表")


    def show_table(self):
        # 准备数据
        # 一级数据，用于计算数组
        # 列数、行数、学生总数
        with open(self.file_path, "r", encoding="utf-8") as f:
            if ".txt" in self.file_path:
                # 读取学生列表
                student_list = f.read().split("\n")
            elif ".csv" in self.file_path:
                df = pandas.read_csv(self.file_path, encoding='utf-8-sig')
                student_list = df['name'].tolist()
        student_num = len(student_list) # 学生总数
        self.row_num = math.ceil (student_num / self.column_num) # 行数
        
        # 如果表格已经存在，则先删除原有表格再创建新表格
        if self.table_widget is not None:
            self.layout.removeWidget(self.table_widget)  # 从布局中移除表格
            self.table_widget.setParent(None)  # 解除表格与父窗口的关系
            self.table_widget.deleteLater()  # 删除表格对象

        # 创建表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(self.row_num)  # 设置行数
        self.table_widget.setColumnCount(self.column_num)  # 设置列数
#       self.table_widget.setHorizontalHeaderLabels(["列 1", "列 2", "列 3"])  # 设置表头
    
        # 添加表格到布局
        self.layout.addWidget(self.table_widget)

        # 二级数据，得出记载最终的座位次序的2d array，等待渲染
        # 打乱顺序
        random.shuffle(student_list)
        # 切片
        self.board = [student_list[self.column_num * i: self.column_num * (i + 1)] for i in range(self.row_num)]
        flag = False
        # 补齐空缺，格式化
        while len(self.board[self.row_num - 1]) != self.column_num:
            if flag:
                self.board[self.row_num - 1].insert(0, "") # add empty string at beginning
            else:
                self.board[self.row_num - 1].append("") # add empty string at tail
            flag = not flag

        # 但是表格元素会随着点击而更新
        # 向表格中添加一些示例数据
        for row in range(self.row_num):
            for column in range(self.column_num):
                # data
                item = QTableWidgetItem(f"{self.board[row][column]}")
                # change font size
                font = item.font()
                font.setPointSize(20)
                item.setFont(font)
                self.table_widget.setItem(row, column, item)
        
        # 设置表格内，表头的字体为20pt
        font = QFont()
        font.setPointSize(20)  # set header font size
        self.table_widget.horizontalHeader().setFont(font)
        self.table_widget.verticalHeader().setFont(font)

        # 表格长宽自适应
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


    # 读取文件绝对路径
    def open_file_dialog(self):
            # 打开文件选择对话框
            options = QFileDialog.Options()
            self.file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*);;文本文件 (*.txt)", options=options)
            if self.file_path is not None:
                self.file_label.setText(self.file_path)  # 显示选择的文件路径

    # 保存方法
    def save_file(self):
        # 打开文件保存对话框
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "逗号分隔文件（excel可识别） (*.csv)", options=options)

        if file_name:
            row_names = [row for row in range(1, self.row_num + 1)]
            column_names = [column for column in range(1, self.column_num + 1)]
            # 将生成的board保存到文件
            df = pandas.DataFrame(self.board, columns = column_names, index = row_names)
            df.to_csv(f'{time.strftime("%Y-%m-%d")}排序结果.csv', encoding='utf-8-sig')
    
    # 读取文本框
    def read_text(self):
        # 读取文本框中的内容
        input_text = self.text_input.text()
        self.column_label.setText(f"输入的文本: {input_text}")
        try:
            self.column_num = int(input_text)
            self.column_label.setText(f"输入的列数是：{self.column_num}")
        except ValueError as e:
            self.column_label.setText("输入有误，请输入整数")



    # return a board
    def get_board(self):
        return self.board
    

    # print board by line in terminal, for testing
    def print_board_byline(self):
        list(map(print, self.board))

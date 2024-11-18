import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow, QAction, QPushButton
from PyQt5.QtGui import QFont
import math
import random



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("排座位")
        self.setGeometry(100, 100, 600, 400)
        # 创建菜单栏
        self.menu_bar = self.menuBar()
        # 创建文件菜单
        file_menu = self.menu_bar.addMenu("文件")
        # 创建退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)  # 连接退出动作到关闭窗口
        file_menu.addAction(exit_action)
        # 创建帮助菜单
        help_menu = self.menu_bar.addMenu("帮助")
        # 创建关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)  # 连接关于动作到显示关于信息
        help_menu.addAction(about_action)

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


    def show_about(self):
        QMessageBox.information(self, "关于", "这是一个简单的排座位程序。给定一个学生列表，以及你希望生成的座位的>    列数，就可以生成一个完全随机的座位表")


    def show_table(self):
        # 准备数据
        # 一级数据，用于计算数组
        # 列数、行数、学生总数
        column_num = 5 # 列数
        with open("name_list.txt", "r", encoding="utf-8") as f:
            # 读取学生列表
            student_list = f.read().split("\n")
        student_num = len(student_list) # 学生总数
        row_num = math.ceil (student_num / column_num) # 行数
        
        # 如果表格已经存在，则不再创建
        if self.table_widget is None:
            # 创建表格
            self.table_widget = QTableWidget(self)
            self.table_widget.setRowCount(row_num)  # 设置行数
            self.table_widget.setColumnCount(column_num)  # 设置列数
#            self.table_widget.setHorizontalHeaderLabels(["列 1", "列 2", "列 3"])  # 设置表头

            # 添加表格到布局
            self.layout.addWidget(self.table_widget)

        # 二级数据，得出记载最终的座位次序的2d array，等待渲染
        # 打乱顺序
        random.shuffle(student_list)
        # 切片
        self.board = [student_list[column_num * i: column_num * (i + 1)] for i in range(row_num)]
        flag = False
        # 补齐空缺，格式化
        while len(self.board[row_num - 1]) != column_num:
            if flag:
                self.board[row_num - 1].insert(0, "") # add empty string at beginning
            else:
                self.board[row_num - 1].append("") # add empty string at tail
            flag = not flag

        # 但是表格元素会随着点击而更新
        # 向表格中添加一些示例数据
        for row in range(row_num):
            for column in range(column_num):
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



    # return a board
    def get_board(self):
        return self.board
    

    # print board by line in terminal, for testing
    def print_board_byline(self):
        list(map(print, self.board))







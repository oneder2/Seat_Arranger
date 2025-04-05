import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QAction, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from prompt_toolkit import Application
from seat_arranger import SeatArranger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arranger = SeatArranger()
        self.setup_ui()

    def setup_ui(self):
        """初始化 UI 组件"""
        self.setWindowTitle("随机排座")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        
        # 菜单栏
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("文件")
        file_menu.addAction(QAction("保存", self, triggered=self.save_file))
        file_menu.addAction(QAction("退出", self, triggered=self.close))
        help_menu = self.menu_bar.addMenu("帮助")
        help_menu.addAction(QAction("关于", self, triggered=self.show_about))

        # UI 组件
        self.select_button = QPushButton("选择文件")
        self.select_button.clicked.connect(self.open_file_dialog)
        self.file_label = QLabel("选择的文件路径将显示在这里")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("在此输入列数")
        self.column_label = QLabel("")
        self.start_button = QPushButton("启动排序")
        self.start_button.clicked.connect(self.show_table)
        self.table_widget = None

        # 设置固定字体大小
        font = QFont()
        font.setPointSize(15)
        for widget in [self.select_button, self.file_label, self.text_input, self.column_label]:
            widget.setFont(font)
        font.setPointSize(25)
        self.start_button.setFont(font)

        # 添加到布局
        self.layout.addWidget(self.select_button, 1, 1, 1, 14)
        self.layout.addWidget(self.file_label, 3, 1, 3, 14)
        self.layout.addWidget(self.text_input, 6, 1, 6, 6)
        self.layout.addWidget(self.column_label, 6, 9, 6, 14)
        self.layout.addWidget(self.start_button, 1, 16)

    def open_file_dialog(self):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", 
                                                   "所有文件 (*);;文本文件 (*.txt);;CSV 文件 (*.csv)")
        if file_path:
            result = self.arranger.load_students(file_path)
            if isinstance(result, int):
                self.file_label.setText(f"已选择文件: {file_path}，学生数量: {result}")
            else:
                self.file_label.setText(result)

    def show_table(self):
        """生成并显示座位表"""
        # 设置列数
        result = self.arranger.set_column_num(self.text_input.text())
        if result:
            self.column_label.setText(result)
            return
        self.column_label.setText(f"输入的列数是：{self.arranger.column_num}")

        # 生成座位表
        result = self.arranger.generate_seating()
        if result:
            QMessageBox.warning(self, "警告", result)
            return

        # 删除旧表格
        if self.table_widget:
            self.layout.removeWidget(self.table_widget)
            self.table_widget.deleteLater()

        # 创建新表格
        self.table_widget = QTableWidget(self.arranger.row_num, self.arranger.column_num)
        self.layout.addWidget(self.table_widget, 12, 1, 80, 20)
        for row in range(self.arranger.row_num):
            for col in range(self.arranger.column_num):
                item = QTableWidgetItem(self.arranger.board[row][col])
                item.setFont(QFont("", 30))  # 固定表格字体大小为 30
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
                self.table_widget.setItem(row, col, item)

        # 自适应表格大小
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def save_file(self):
        """保存座位表"""
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "CSV 文件 (*.csv)")
        if file_name:
            result = self.arranger.save_seating(file_name)
            if result:
                QMessageBox.warning(self, "警告", result)
            else:
                QMessageBox.information(self, "信息", "文件保存成功")

    def show_about(self):
        """显示关于信息"""
        QMessageBox.information(self, "关于", "这是一个简单的排座位程序。给定学生列表和列数，生成随机座位表。")

if __name__ == "__main__":
    app = Application(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
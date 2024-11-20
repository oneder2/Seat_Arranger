import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建网格布局
        grid_layout = QGridLayout()

        # 创建按钮并添加到网格布局中
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')

        # 将按钮添加到网格布局中
        grid_layout.addWidget(button1, 0, 0)  # 第1行第1列
        grid_layout.addWidget(button2, 0, 1)  # 第1行第2列
        grid_layout.addWidget(button3, 1, 0)  # 第2行第1列
        grid_layout.addWidget(button4, 1, 1)  # 第2行第2列

        # 设置窗口的布局
        self.setLayout(grid_layout)

        # 设置窗口标题
        self.setWindowTitle('QGridLayout Example')

# 主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


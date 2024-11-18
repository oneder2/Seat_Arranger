from PyQt5.QtWidgets import QApplication
from arranger import MainWindow
import sys


column_num = 5

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#my_arranger = Arranger(column_num)

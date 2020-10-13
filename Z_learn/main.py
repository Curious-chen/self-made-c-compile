from PyQt5.QtWidgets import QApplication, QMainWindow

from Z_learn.ui_main import Ui_MainWindow as Main_Ui
from Z_learn.f import Ui_MainWindow as f_ui
import sys


class Mywindow(QMainWindow, Main_Ui):

    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.qt)

    def qt(self):
        self.f = QMainWindow()
        f_ui().setupUi(self.f)
        self.f.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Mywindow()
    w.show()
    sys.exit(app.exec_())

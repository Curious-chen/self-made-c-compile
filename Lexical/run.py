import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QAction,qApp
from Lexical.GUI import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.Button1.clicked.connect(self.push_)
        self.Button2.clicked.connect(self.save_)
        self.Button3.clicked.connect(self.wordRec)
        self.Button4.clicked.connect(self._analysis_Demo)
        self.Button5.clicked.connect(self._semanalysis)
        self.Button6.clicked.connect(self._generation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

import sys,os
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import *
from ui1 import *
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from my_window import Mywindow as W_zgs


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.open_txt.triggered.connect(self.push_)
        self.save.triggered.connect(self.save_)
        self.word.triggered.connect(self.wordRec)
        self.gram.triggered.connect(self.analysis_ll)
        self.opt_anay.triggered.connect(self.new_window_)
        self.sema.triggered.connect(self._semanalysis)
        self.gen.triggered.connect(self._generation)
        self.gen_lr.triggered.connect(self._genetation_lr)
        self.opt.triggered.connect(self.new_window_)
        self.aim.triggered.connect(self._targe_code)
        self.zgs2nfa.triggered.connect(self.new_zgs_windows)
        self.yfs_lr.triggered.connect(self.export_lr_yfs)
        self.yfs_ll.triggered.connect(self.export_ll_yfs)
        self.gram_lr.triggered.connect(self.analysis_lr)
        self.show_token.triggered.connect(self.show_t)
        self.show_action.triggered.connect(self.show_a)
        self.show_fh.triggered.connect(self.show_f)
        self.show_sys.triggered.connect(self.show_s)
        self.show_hb.triggered.connect(self.show_h)

    def new_window_(self):
        self.child = New_window()
        self.child.show()

    def new_zgs_windows(self):
        self.zgs_ui = W_zgs()
        self.zgs_ui.show()


class New_window(QMainWindow, Ui_MainWindow_1):
    def __init__(self, parent=None):
        super(New_window, self).__init__(parent)
        self.setupUi_1(self)
        self.initUI()
        self.open_txt_.triggered.connect(self.push_)
        self.code_op.triggered.connect(self.code_opt_)
        self.opt_vt.triggered.connect(self.opt_table_)
        self.opt_.triggered.connect(self.opt_anay_)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

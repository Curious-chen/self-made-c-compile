from PyQt5.QtGui import QImage, QPixmap

from ui_zgs import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene
from chensong.code.to_dfa import DFA
from chensong.code.model import draw
from chensong.code.to_nfa import NFA
from chensong.code.config import save_dfa, save_min_dfa, save_nfa


class Mywindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self._gen)
        self.before_zgs = 'dgfdrfgdgd'
        self.count = 0
        self.p_paths = []

    def _gen(self):
        try:
            zgs = self.lineEdit.text()
            if zgs and zgs != self.before_zgs:
                self.p_paths = self._photo_addr()
                nfa = NFA(zgs)
                nfa_dict = nfa.to_nfa()
                draw(nfa_dict, self.p_paths[0])
                dfa = DFA(nfa_dict)
                dfa.to_dfa()
                draw(dfa.dfa_dict, self.p_paths[1])
                dfa.to_min_nfa()
                draw(dfa.mini_dfa, self.p_paths[2])
                self.before_zgs = zgs
            self.show_png()
        except Exception as e:
            print(e)

    def _photo_addr(self):
        self.count += 1
        return [self._c_photo(save_nfa), self._c_photo(save_dfa), self._c_photo(save_min_dfa)]

    def _c_photo(self, path):
        num = self.count
        return path+'_{:>02d}_'.format(num)

    def show_png(self):
        import random

        self.label_nfa.setPixmap(QPixmap(self.p_paths[0]))
        self.label_dfa.setPixmap(QPixmap(self.p_paths[1]))
        self.label_m_dfa.setPixmap(QPixmap(self.p_paths[2]))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = Mywindow()
    w.show()
    sys.exit(app.exec_())

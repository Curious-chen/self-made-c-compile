from code.wordUI import Ui_MainWindow
from code.handle import LexicalAnalysis, SyntaxAnalysis
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets as Qwt
import sys
import traceback
import logging
from code.config import *

class Mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.lex_result = []
        # 创建词法分析器
        self.syntax_analysis = SyntaxAnalysis('../data/c_ll.txt')
        # 获得first集
        self.syntax_analysis.get_first()
        # 获得follow集
        self.syntax_analysis.get_follow()
        self.setupUi(self)
        # 设置其字符超出后也不能转行
        self.pt_error.setLineWrapMode(Qwt.QPlainTextEdit.NoWrap)
        self.pt_Analysis.setLineWrapMode(Qwt.QPlainTextEdit.NoWrap)
        self.initUI()

    def initUI(self):
        mbar = Qwt.QMenuBar(self)
        fileMenu = mbar.addMenu("文件")
        newAct = Qwt.QAction('新建', self)
        impAct = Qwt.QAction('导入', self)
        fileMenu.addAction(newAct)
        fileMenu.addAction(impAct)
        fileMenu.triggered[Qwt.QAction].connect(self.file_process)

        workMenu = mbar.addMenu("run")
        word_analysis = Qwt.QAction("词法分析", self)
        grammar_analysis = Qwt.QAction("语法分析", self)
        intermediateCode = Qwt.QAction("中间代码", self)
        workMenu.addAction(word_analysis)
        workMenu.addAction(grammar_analysis)
        workMenu.addAction(intermediateCode)
        workMenu.triggered[Qwt.QAction].connect(self.work_process)

        qtMenu = mbar.addMenu('other')
        word_table = Qwt.QAction("词汇表", self)
        fh_table = Qwt.QAction("符号表", self)
        yfs = Qwt.QAction("导出语法树", self)
        qtMenu.addAction(word_table)
        qtMenu.addAction(fh_table)
        qtMenu.addAction(yfs)
        qtMenu.triggered[Qwt.QAction].connect(self.other_process)
        # 默认加载 test.c 文件
        try:
            with open('../data/test.c', 'r', encoding='utf-8') as f:
                code_str = f.read()
            self.pt_filw.setPlainText(code_str)
        except Exception as e:
            print("默认路径加载错误")

    def other_process(self, q):
        # 输出那个Qmenu对象被点击
        print(q.text() + 'is triggeres')
        try:
            if q.text() == '导出语法树':
                self.export_yfs()
            elif q.text() == '词汇表':
                self.pt_Analysis.setPlainText('')
                self.show_word()
            elif q.text() == '符号表':
                self.pt_Analysis.setPlainText('')
                self.show_fh_table()
        except Exception as e:
            traceback.print_exc()

    def file_process(self, q):
        # 输出那个Qmenu对象被点击
        print(q.text() + 'is triggeres')
        if q.text() == '新建':
            pass
        elif q.text() == '导入':
            self.show_content()

    def work_process(self, q):
        # 输出那个Qmenu对象被点击
        choose = q.text()
        if choose == '词法分析':
            try:
                self.lexicalAnalysis()
            except Exception as e:
                traceback.print_exc()
        elif choose == '语法分析':
            # 展示分析
            try:
                self.syntaxAnalysis()
            except Exception as e:
                traceback.print_exc()
            pass

    def lexicalAnalysis(self):
        content = str(self.pt_filw.toPlainText())
        if len(content) > 0:
            # 构建词法分析器
            lex_a = LexicalAnalysis()
            # 词法分析
            lex_a.analysis(content)
            # 将词法分析结果共享
            self.lex_result = lex_a.result_lex.copy()

            # 构建错误信息显示
            result_error = "******************{:^5d}lexError********************\n".format(len(lex_a.result_error))
            if len(lex_a.result_error) > 0:
                for pos, error_word, error_info in lex_a.result_error:
                    result_error += 'pos:({:^5d},{:^5d}) error_word:{{{:^10s}}} error_info:{:30s}\n'.format(pos[0],
                                                                                                            pos[1],
                                                                                                            str(
                                                                                                                error_word),
                                                                                                            error_info)
            # 显示词汇表
            self.show_word()
            # 显示词法错误
            self.pt_error.setPlainText(result_error)

    def show_word(self):
        # 判断是否进行了词法分析

        if self.lex_result:
            # 获得分析面内容
            content = str(self.pt_Analysis.toPlainText())
            # 添加词汇表信息显示前缀
            content += '\n{:^50s}\n'.format('词汇表')
            # 构建词汇表格式
            word_table = '\n'.join(['pos:({:^5d},{:^5d}) {:20s}{:5d}       {:s}'.format(*_) for _ in self.lex_result])
            self.pt_Analysis.setPlainText(content + word_table)
        else:
            logging.info('不能显示词汇表，没有进行词法分析')
            print('不能显示词汇表，没有进行词法分析')

    # 显示代码
    def show_content(self):
        filename_choose, file_type = Qwt.QFileDialog.getOpenFileName(self, '选取文件')
        content = str()
        if filename_choose != '':
            try:
                with open(filename_choose, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(e)
            if content:
                self.pt_filw.setPlainText(content)

    def syntaxAnalysis(self):
        if len(self.lex_result) >= 1:
            word_lsit = self.lex_result.copy()
            # 传入词法分析结果，进行语法分析
            self.tree, self.fh_table, error_list = self.syntax_analysis.analysis(word_lsit, 'translation_unit')
            # 构建语法错误信息
            error_info = "******************{:^5d}syntaxError*****************\n".format(len(error_list))
            for error in error_list:
                error_info += 'pos:({:^5d},{:^5d}) e_word:{{{:^10s}}} e_info:{:30s}\n'.format(error[0], error[1],
                                                                                              error[2], error[-1])

            # 显示错误
            self.pt_error.setPlainText(str(self.pt_error.toPlainText()) + error_info)

    def export_yfs(self):
        try:
            self.tree
        except NameError:
            tree_exist = False
        else:
            tree_exist = True
        if tree_exist:
            from code.model import to_dot
            # 不管正确与否，都导出分析树
            data = to_dot(self.tree)  # 将树转换为dot格式

            # 画出语法树
            import pydotplus as pdp
            print(data)
            graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(data))
            with open(save_syntax_tree_LL1, 'wb') as f:
                f.write(graph.create_png())
            # 打开语法树图片
            import os
            path = os.path.join(os.path.abspath('.'), save_syntax_tree_LL1)
            if os.path.exists(path):
                # 相对路径不能打开
                os.startfile(path, 'open')
        else:
            print('导出语法树失败')

    def show_fh_table(self):
        # 判断是否进行了词法分析
        try:
            self.fh_table
        except NameError:
            fh_exist = False
        else:
            fh_exist = True

        if fh_exist:
            con = self.fh_table['con']
            con_str = '{:^50s}\n'.format('常量表')
            con_str += '{:^10s} {:^10s} {:^10s}\n'.format('name', 'type', 'value')
            for k, v in con.items():
                con_str += '{:^10s} {:^10s} {:^10s}\n'.format(k, v[0], str(v[1][2]))
            var = self.fh_table['var']
            var_str = '{:^50s}\n'.format('变量表')
            var_str += '{:^10s} {:^10s} {:^10s} {:^10s}\n'.format('name', 'sca', 'type', 'value')
            for k, v in var.items():
                for vv in v:
                    vvv = vv[2][2] if vv[2] else vv[2]
                    var_str += '{:^10s} {:^10s} {:^10s} {:^10}\n'.format(k, str(vv[0]), vv[1], str(vvv))
            fun = self.fh_table['fun']
            # 获得分析面内容
            content = str(self.pt_Analysis.toPlainText())
            self.pt_Analysis.setPlainText(content + con_str + var_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Mywindow()

    w.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

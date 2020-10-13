# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog
from Lexical.lex_word import *
from Lexical.QCodeEditor import QCodeEditor
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication, QFileDialog, QMessageBox, QAction, qApp
from Analysis._token import *
from Semantic.Semantic_analysis import *
from Semantic.generation import *
from Targetcode.Aim_Code import *
from chensong.code.config import *
from chensong.code.handle import SyntaxAnalysis
from chensong.code.LR import SLR, get_lex
from chensong.code.model import *
import traceback


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1094, 905)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.textEdit = QCodeEditor(self.centralwidget)  # 文本输入
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 551, 881))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(False)
        self.horizontalLayout.addWidget(self.textEdit)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textEdit_2 = QCodeEditor(self.widget)
        self.textEdit_2.setGeometry(QtCore.QRect(550, 0, 551, 481))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setReadOnly(True)
        self.verticalLayout.addWidget(self.textEdit_2)

        self.textEdit_3 = QtWidgets.QTextBrowser(self.widget)
        self.textEdit_3.setGeometry(QtCore.QRect(550, 480, 551, 401))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setReadOnly(True)
        self.verticalLayout.addWidget(self.textEdit_3)
        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1094, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menubar)
        self.menu_7.setObjectName('menu_7')
        self.menu_8 = QtWidgets.QMenu(self.menubar)
        self.menu_8.setObjectName('menu_8')
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_7.menuAction())
        self.menubar.addAction(self.menu_8.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.flag = True
        self.file_path = ''
        self.strs = ''
        self.fname = ""
        self.filename = ""
        self.token_code = list()
        self.textEdit_3.setFontFamily("黑体")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "编译器"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "词法分析"))
        self.menu_3.setTitle(_translate("MainWindow", "语法分析"))
        self.menu_4.setTitle(_translate("MainWindow", "语义分析"))
        self.menu_5.setTitle(_translate("MainWindow", "中间代码"))
        self.menu_6.setTitle(_translate("MainWindow", "目标代码"))
        self.menu_7.setTitle(_translate("MainWindow", "导出"))
        self.menu_8.setTitle(_translate("MainWindow", "查看"))

    def initUI(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        # 添加事件
        self.open_txt = self.add_action('打开')
        self.save = self.add_action('保存')
        self.menu.addAction(self.open_txt)
        self.menu.addAction(self.save)
        self.menu.addAction(exitAction)
        self.word = self.add_action('词法')
        self.menu_2.addAction(self.word)
        self.zgs2nfa = self.add_action('正规式转NFA')
        self.menu_2.addAction(self.zgs2nfa)
        self.gram = self.add_action('预测分析')
        self.gram_lr = self.add_action('LR分析')
        self.opt_anay = self.add_action('算符优先')
        self.menu_3.addAction(self.gram)
        self.menu_3.addAction(self.gram_lr)
        self.menu_3.addAction(self.opt_anay)
        self.sema = self.add_action('语义')
        self.menu_4.addAction(self.sema)
        self.gen = self.add_action('递归生成')
        self.gen_lr = self.add_action('LR生成')
        self.opt = self.add_action('代码优化')
        self.menu_5.addAction(self.gen)
        self.menu_5.addAction(self.gen_lr)
        self.menu_5.addAction(self.opt)

        self.aim = self.add_action('目标代码')
        self.menu_6.addAction(self.aim)
        self.yfs_lr = self.add_action('LR语法树')
        self.yfs_ll = self.add_action('LL语法树')
        self.menu_7.addAction(self.yfs_ll)
        self.menu_7.addAction(self.yfs_lr)

        self.show_token = self.add_action('词汇表')
        self.show_action = self.add_action('LRA表')
        self.show_fh = self.add_action('符号表')
        self.show_sys = self.add_action('四元式')
        self.show_hb = self.add_action('汇编代码')
        self.menu_8.addAction(self.show_token)
        self.menu_8.addAction(self.show_action)
        self.menu_8.addAction(self.show_fh)
        self.menu_8.addAction(self.show_sys)
        self.menu_8.addAction(self.show_hb)

    def add_action(self, name):
        Action = QAction(name, self)
        return Action

    def push_(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        self.textEdit.clear()
        if len(file_path) != 0:
            self.file_path = file_path
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for index, pre_line in enumerate(lines):
                    self.textEdit.insertPlainText(pre_line)
                self.strs = lines

    def highline(self, err_index):
        print(self.textEdit.toPlainText())
        self.textEdit.clear()
        err_ = [in_[1] for in_ in err_index]
        for index, pre_line in enumerate(self.strs):
            if index in err_:
                self.textEdit.append("<font color='red' size=3>" + str(index) + ': ' + "</font>")
                self.textEdit.insertPlainText(pre_line)
            else:
                self.textEdit.append("<font color='black' size=3>" + str(index) + ': ' + "</font>")
                self.textEdit.insertPlainText(pre_line)

    def wordRec(self):
        self.flag = True
        err_index = []
        temp_list = []
        dic = {'11': '数字格式错误: ', '57': '字符串格式错误: ', '61': '字符格式错误: ', '62': '无法识别的字符错误: ', '68': '头文件错误: '}
        print(self.file_path)
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        T = anayword()
        all_ = T.read_file(self.textEdit.toPlainText())
        self.token_code = T.token(all_)
        self.textEdit_2.insertPlainText('\t' + '行' + '\t' + '单词' + '\t' + 'token\n')
        self.textEdit_2.insertPlainText('-------------------------------------------\n')
        for pre_token in self.token_code:
            if pre_token[1] in [11, 57, 61, 62, 68]:  # 错误信息状态
                err_index.append([pre_token[0], pre_token[2], pre_token[3], pre_token[1]])
            if pre_token[1] != 68:
                self.textEdit_2.insertPlainText(
                    '\t' + str(pre_token[2] + 1) + '\t' + pre_token[0] + '\t' + str(pre_token[1]) + '\n')
        for i in self.token_code:
            if i[1] != 68:
                temp_list.append(i)
        self.token_code = copy.deepcopy(temp_list)
        self.textEdit_3.append(
            "<font color='black' size=4>" + '----------------------词法分析错误信息----------------------' + "</font>")
        if len(err_index) == 0:
            self.textEdit_3.append("<font color='black' size=4>词法分析结束 - 0 error(s)</font>")
        else:
            # self.highline(err_index)
            self.flag = False
            for index, pre in enumerate(err_index):
                self.textEdit_3.append(
                    "<font color='red' size=4>" + '------> error ' + str(index) + ': ' + '第' + str(
                        pre[1] + 1) + '行' + str(
                        pre[2] - (len(pre[0]))) + '列附近存在' + dic.get(str(pre[3])) +
                    pre[0] + "</font>")
            self.textEdit_3.append("<font color='black' size=4>" + "词法分析结束 - " + str(
                len(err_index)) + " error(s)" + "</font>")
        try:
            token_txt = ''
            for tok in self.token_code:
                token_txt += '{:} {:} {:} {:}\n'.format(tok[0], tok[1], str(tok[2]), str(tok[3]))
            with open(save_token_list, 'w', encoding='utf-8') as f:
                f.write(token_txt)
        except Exception as e:
            traceback.print_exc()

    def save_(self):
        # self.textEdit_2.fileSave()
        if self.filename != '':
            with open(file=self.filename + '.txt', mode='w', encoding='utf-8') as file:
                file.write(self.textEdit_2.toPlainText())
                self.filename = ''
        else:
            self.fileSaveAs()

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", self.filename, ".txt")
        print(fn)
        if not fn:
            print("Error saving")
            return False

        self.filename = fn
        self.fname = os.path.splitext(str(fn))[0].split("/")[-1]
        print(self.filename, self.fname)
        return self.save_()

    def analysis_lr(self):
        try:
            # lr分析语法，生成语法树
            t = SyntaxAnalysis(lr_grammar)  # 将lr文法转换成
            t.get_first()
            t.get_follow(t_unit)

            # 读取存放的token串
            lex_result_token = get_lex()

            lr = SLR(t.g_dict, dot, t_unit)
            lr.get_v()
            items = lr.get_items()
            lr.get_lr_table(items)
            sucess, data = lr.analysis(lex_result_token, in_code=False)
            if sucess:
                self.lr_tree = data
                lr.save_action(save_action)
                self.textEdit_3.append("<font color='black' size=4>语法法分析结束 - 0 error(s)</font>")
                self.show_a()
            else:
                self.textEdit_3.append("<font color='red' size=4>" + '------> error ' + str(data) + "</font>")
                self.textEdit_3.append(
                    "<font color='black' size=4>" + "语法分析结束 - 1 error(s)" + "</font>")


        except Exception as e:
            traceback.print_exc()

    def analysis_ll(self):
        try:
            self.flag = True
            t = SyntaxAnalysis(ll1_grammar)
            # print("-------------------first && follow---------------------\n")
            t.get_first()
            t.get_follow()
            t.get_synch()
            # 读取存放的token串
            lex_result_token = get_lex()
            # 获得lr文法分析树
            self.ll_tree, self.fh_table, error_list = t.analysis(lex_result_token, t_unit)
            self.textEdit_3.append(
                "<font color='black' size=4>" + '----------------------语法分析错误信息----------------------' + "</font>")
            if len(error_list) == 0:
                self.textEdit_3.append("<font color='black' size=4>语法法分析结束 - 0 error(s)</font>")
            else:
                self.flag = False
                for index, pre in enumerate(error_list):
                    print(pre)
                    self.textEdit_3.append("<font color='red' size=4>" + '------> error ' + str(pre) + "</font>")
                self.textEdit_3.append(
                    "<font color='black' size=4>" + "语法分析结束 - " + str(len(error_list)) + " error(s)" + "</font>")
        except Exception as e:
            traceback.print_exc()

    def export_ll_yfs(self):
        try:
            try:
                self.ll_tree
            except NameError:
                tree_exist = False
            else:
                tree_exist = True
            if tree_exist:
                # 不管正确与否，都导出分析树
                data = to_dot(self.ll_tree)  # 将树转换为dot格式

                # 画出语法树
                import pydotplus as pdp
                print(data)
                graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(data))
                with open(save_syntax_tree_LL1, 'wb') as f:
                    f.write(graph.create_png())
                default_open(save_syntax_tree_LL1)
            else:
                print('导出语法树失败')
        except Exception as e:
            traceback.print_exc()

    def export_lr_yfs(self):
        try:
            try:
                self.lr_tree
            except NameError:
                tree_exist = False
            else:
                tree_exist = True
            if tree_exist:
                # 不管正确与否，都导出分析树
                data = to_dot(self.lr_tree)  # 将树转换为dot格式

                # 画出语法树
                import pydotplus as pdp
                print(data)
                graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(data))
                with open(save_syntax_tree_LR, 'wb') as f:
                    f.write(graph.create_png())
                default_open(save_syntax_tree_LR)
            else:
                print('导出语法树失败')
        except Exception as e:
            traceback.print_exc()

    def _semanalysis(self):
        print('asedsa')
        try:
            self.flag = True
            S = Semantic_()
            if len(self.token_code) != 0:
                print('save')
                S.access(self.token_code)
                err_list = copy.deepcopy(S.error_list)
                err_list = sorted(err_list, key=lambda x: x.Location['line'])
                self.textEdit_2.clear()
                fh_table = ''
                for pre in S.syn_table.symbolTableInfo:
                    t = pre.strip() + '\n'
                    fh_table += t
                    self.textEdit_2.insertPlainText(t)
                with open(save_fh_table, 'w', encoding='utf-8') as f:
                    f.write(fh_table)
                self.textEdit_3.append(
                    "<font color='black' size=4>" + '----------------------语义分析错误信息----------------------' + "</font>")
                if len(err_list) == 0:
                    self.textEdit_3.append("<font color='black' size=4>语义分析结束 - 0 error(s)</font>")
                else:
                    self.flag = False
                    for index, pre in enumerate(err_list):
                        print(pre)
                        self.textEdit_3.append(
                            "<font color='red' size=3 width=20px>------> error  第{:^5d}行 第{:^5d}列    ErrorType:{:40s}  ErrorMessage:{:}".format(
                                pre.Location['line'], pre.Location['col'], pre.ErrorType,
                                pre.ErrorMessage) + "</font>")
                    self.textEdit_3.append(
                        "<font color='black' size=4>" + "语义分析结束 - " + str(len(err_list)) + " error(s)" + "</font>")

        except Exception as e:
            self.textEdit_3.append(
                "<font color='black' size=4>" + '----------------------语义分析错误信息----------------------' + "</font>")
            self.textEdit_3.append("<font color='black' size=4>" + "语法存在错误，语义分析无法进行" + "</font>")
            print(e.__traceback__.tb_lineno)
            traceback.print_exc()

    def _generation(self):
        try:
            # with open('D:/程序代码/PyProject/编译原理/Targetcode/t.txt', 'w', encoding='utf-8')as f:
            # with open(UI_token_path, 'w', encoding='utf-8')as f:
            #     for i in self.token_code:
            #         f.write(str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(i[3]) + '\n')
            G = Genration_()
            if len(self.token_code) != 0 and self.flag:
                G.Acess_gen(self.token_code)
                self.textEdit_2.clear()
                with open(gen_path, 'w', encoding='utf-8')as f:
                    self.textEdit_2.insertPlainText('四元式:' + '\n')
                    f.write('四元式:' + '\n')
                    for pre in G.out_list:
                        self.textEdit_2.insertPlainText(pre + '\n')
                        f.write(pre + '\n')
            else:
                self.textEdit_3.append("<font color='black' size=4>" + "程序存在错误无法生成四元式" + "</font>")
        except:
            self.textEdit_3.append("<font color='black' size=4>" + "程序存在错误无法生成四元式" + "</font>")
            traceback.print_exc()

    def _genetation_lr(self):
        try:
            t = SyntaxAnalysis(lr_grammar)
            t.get_first()
            t.get_follow(t_unit)
            lex_result_token = get_lex()
            lr = SLR(t.g_dict, dot, t_unit)
            lr.get_v()
            items = lr.get_items()
            lr.get_lr_table(items)
            sucess, tree = lr.analysis(lex_result_token, in_code=True)
            if sucess:
                print(lr.save_())
                # print(lr.save_action(save_action))
                self.show_s()
            else:
                print(tree)
                raise Exception()
        except:
            self.textEdit_3.append("<font color='black' size=4>" + "程序存在错误无法生成四元式" + "</font>")
            traceback.print_exc()

    def _targe_code(self):
        try:
            with open(UI_token_path, 'r', encoding='UTF-8')as f:
                lines_token = f.readlines()
            with open(gen_path, 'r', encoding='UTF-8')as f:
                lines_gen = f.readlines()
            print(lines_token, lines_gen)
            if len(lines_gen) > 0 and len(lines_token) > 0:
                tag = target_Code()
                target_list = tag.access_target()
                self.textEdit_2.clear()
                hbdm = '目标代码:\n'
                self.textEdit_2.insertPlainText('目标代码:' + '\n')
                for i in target_list:
                    self.textEdit_2.insertPlainText(i + '\n')
                    hbdm += i + '\n'
                with open(save_hb_code, 'w', encoding='utf-8') as f:
                    f.write(hbdm)
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            traceback.print_exc()

    # token串
    def show_t(self):
        self.textEdit_2.clear()
        token_list = get_lex()
        self.textEdit_2.insertPlainText('\t' + '行' + '\t' + '单词' + '\t' + 'token\n')
        self.textEdit_2.insertPlainText('-------------------------------------------\n')
        for pre_token in token_list:
            self.textEdit_2.insertPlainText(
                '\t' + str(int(pre_token.cur_line) + 1) + '\t' + pre_token.val + '\t' + str(pre_token.typ) + '\n')

    # action表
    def show_a(self):
        self.textEdit_2.clear()
        with open(save_action, 'r', encoding='utf-8') as f:
            self.textEdit_2.insertPlainText(f.read() + '\n')
        pass

    # 符号表
    def show_f(self):
        self.textEdit_2.clear()
        with open(save_fh_table, 'r', encoding='utf-8') as f:
            self.textEdit_2.insertPlainText(f.read() + '\n')

    # 四元式
    def show_s(self):
        self.textEdit_2.clear()
        with open(save_quaternion_info, 'r', encoding='utf-8') as f:
            self.textEdit_2.insertPlainText(f.read() + '\n')

    # 汇编代码
    def show_h(self):
        self.textEdit_2.clear()
        with open(save_hb_code, 'r', encoding='utf-8') as f:
            self.textEdit_2.insertPlainText(f.read() + '\n')

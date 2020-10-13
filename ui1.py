# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import tkinter as tk
from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from Lexical.QCodeEditor import QCodeEditor
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication, QFileDialog, QMessageBox, QAction, qApp
from Semantic.code_opt_1 import *
from Analysis.opt_analysis import *
import traceback


class Ui_MainWindow_1(object):
    def setupUi_1(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(881, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.textEdit_1 = QCodeEditor(self.groupBox)  # 文本输入
        self.textEdit_1.setGeometry(QtCore.QRect(0, 0, 381, 581))
        self.textEdit_1.setObjectName("textEdit_1")
        self.textEdit_1.setReadOnly(False)
        self.horizontalLayout.addWidget(self.textEdit_1)
        self.horizontalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_2.setGeometry(QtCore.QRect(380, 0, 501, 221))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_2.setReadOnly(True)
        self.verticalLayout.addWidget(self.textBrowser_2)

        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_3.setGeometry(QtCore.QRect(380, 280, 501, 301))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_3.setReadOnly(False)
        self.verticalLayout.addWidget(self.textBrowser_3)

        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_4.setGeometry(QtCore.QRect(380, 220, 501, 61))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_4.setReadOnly(True)
        self.verticalLayout.addWidget(self.textBrowser_4)
        self.verticalLayout.setStretch(0, 9)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 9)
        self.horizontalLayout_2.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 881, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.strs = ''
        self.table, self.Opt = None, None
        self.textBrowser_2.setFontFamily("黑体")
        self.textBrowser_3.setFontFamily("黑体")
        self.textBrowser_4.setFontFamily("黑体")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "算符优先"))
        self.menu_3.setTitle(_translate("MainWindow", "代码优化"))

    def initUI(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        # 添加事件
        self.open_txt_ = self.add_action('打开')
        self.save_ = self.add_action('保存')
        self.menu.addAction(self.open_txt_)
        self.menu.addAction(self.save_)
        self.menu.addAction(exitAction)
        self.opt_vt = self.add_action('Firstvt与lastvt')
        self.opt_ = self.add_action('算符优先')
        self.menu_2.addAction(self.opt_vt)
        self.menu_2.addAction(self.opt_)
        self.code_op = self.add_action('DAG优化')
        self.menu_3.addAction(self.code_op)

    def add_action(self, name):
        Action = QAction(name, self)
        return Action

    def push_(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        self.textEdit_1.clear()
        if len(file_path) != 0:
            self.file_path = file_path
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for index, pre_line in enumerate(lines):
                    self.textEdit_1.insertPlainText(pre_line)
                self.strs = lines

    def opt_table_(self):
        try:
            if len(self.textEdit_1.toPlainText()) != 0:
                self.Opt = Opt_()
                self.Opt.read_file(self.textEdit_1.toPlainText())
                self.Opt.fistrVt()
                self.Opt.lastVt()
                self.table = self.Opt.op_table()
                firstvt, lastvt = self.Opt.first, self.Opt.last
                self.textBrowser_2.clear()
                self.textBrowser_2.insertPlainText('Fistvt:\n')
                for key in firstvt.keys():
                    self.textBrowser_2.insertPlainText('{:<3}:'.format(key))
                    for index, per in enumerate(firstvt[key]):
                        if index == len(firstvt[key]) - 1:
                            self.textBrowser_2.insertPlainText('{:<3}\n'.format(per))
                        else:
                            self.textBrowser_2.insertPlainText('{:<3}'.format(per))
                self.textBrowser_2.insertPlainText('Lastvt:\n')
                for key in lastvt.keys():
                    self.textBrowser_2.insertPlainText('{:<3}:'.format(key))
                    for index, per in enumerate(lastvt[key]):
                        if index == len(lastvt[key]) - 1:
                            self.textBrowser_2.insertPlainText('{:<3}\n'.format(per))
                        else:
                            self.textBrowser_2.insertPlainText('{:<3}'.format(per))
                self.textBrowser_2.insertPlainText('Table:\n')
                for row in self.table:
                    for index, col in enumerate(row):
                        if index == len(row) - 1:
                            self.textBrowser_2.insertPlainText('{:<3}\n'.format(col))
                        else:
                            self.textBrowser_2.insertPlainText('{:<3}'.format(col))
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            traceback.print_exc()

    def opt_anay_(self):
        try:
            if len(self.textBrowser_3.toPlainText()) != 0:
                self.textBrowser_4.clear()
                text = self.textBrowser_3.toPlainText().split(' ')
                text.append('#')
                result,flag = self.Opt.__annalysis__(self.table, text)
                for per in result:
                    self.textBrowser_4.insertPlainText(
                        '{:<10s}{:<10s}{:<10s}\n'.format(''.join(per[0]), ''.join(per[1]), per[2][0] + ' ' + per[2][1]))
                if flag:
                    self.textBrowser_4.insertPlainText('字符串分析成功')
                else:
                    self.textBrowser_4.insertPlainText('字符串分析失败')
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            traceback.print_exc()

    def code_opt_(self):
        try:
            if len(self.strs) != 0:
                self.textEdit_1.clear()
                self.textBrowser_2.clear()
                self.textBrowser_4.clear()
                act_var_dic = dict()
                act_var = self.textBrowser_3.toPlainText()
                # if len(act_var) != 0:
                for per_fun in act_var.split(';'):
                    per_fun_ = per_fun.split(':')
                    if len(per_fun) != 0:
                        list_ = per_fun_[1].split(' ')
                        act_var_dic[per_fun_[0]] = [set(), list_]
                print(act_var_dic)
                O = Optimizathon_(act_var_dic)
                O.Acess_(self.strs)
                block = O.block_dic
                print(block)
                self.textEdit_1.clear()
                for per_block in block:
                    for key in per_block.keys():
                        self.textEdit_1.insertPlainText(key + ':\n')
                        for per in per_block[key]:
                            self.textEdit_1.insertPlainText(
                                "\t( {:<4s} {:<4s} {:<4s} {:<4s} )\n".format(per[0],per[1],per[2],per[3]))
                nodes = O.node_dic
                for node in nodes:
                    for i in node:
                        self.textBrowser_2.insertPlainText(
                            'id:{} val:{} value:{} left:{} right:{}\n'.format(i.id, i.val, i.value, i.leftchild,
                                                                              i.rightchild))
                    self.textBrowser_2.insertPlainText(
                        '-------------------------------------------------------------')
                for i in O.gen_list:
                    self.textBrowser_4.insertPlainText(
                        "{:<3s}: ( {:<4s} {:<4s} {:<4s} {:<4s} )\n".format(str(i.id), str(i.op), str(i.n1),
                                                                           str(i.n2),
                                                                           str(i.res)))
                # else:
                #     raise Exception('活跃变量为空')
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            traceback.print_exc()

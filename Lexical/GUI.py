# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog
from Lexical.lex_word import *
from Lexical.QCodeEditor import QCodeEditor
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication, QFileDialog, QMessageBox
from Analysis._token import *
from Semantic.Semantic_analysis import *
from Semantic.generation import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 914)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button1.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.Button1.setObjectName("Button1")
        self.Button2 = QtWidgets.QPushButton(self.centralwidget)
        self.Button2.setGeometry(QtCore.QRect(70, 0, 71, 31))
        self.Button2.setObjectName("Button2")
        self.Button3 = QtWidgets.QPushButton(self.centralwidget)
        self.Button3.setGeometry(QtCore.QRect(140, 0, 71, 31))
        self.Button3.setObjectName("Button3")
        self.Button4 = QtWidgets.QPushButton(self.centralwidget)
        self.Button4.setGeometry(QtCore.QRect(210, 0, 71, 31))
        self.Button4.setObjectName("Button4")
        self.Button5 = QtWidgets.QPushButton(self.centralwidget)
        self.Button5.setGeometry(QtCore.QRect(280, 0, 71, 31))
        self.Button5.setObjectName("Button5")
        self.Button6 = QtWidgets.QPushButton(self.centralwidget)
        self.Button6.setGeometry(QtCore.QRect(350, 0, 101, 31))
        self.Button6.setObjectName("Button6")
        self.Button7 = QtWidgets.QPushButton(self.centralwidget)
        self.Button7.setGeometry(QtCore.QRect(450, 0, 71, 31))
        self.Button7.setObjectName("Button7")
        self.Button8 = QtWidgets.QPushButton(self.centralwidget)
        self.Button8.setGeometry(QtCore.QRect(520, 0, 71, 31))
        self.Button8.setObjectName("Button8")
        self.textEdit = QCodeEditor(self.centralwidget)  # 文本输入
        self.textEdit.setGeometry(QtCore.QRect(0, 30, 531, 851))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(False)
        self.textEdit_2 = QCodeEditor(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(530, 30, 571, 421))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setReadOnly(True)
        self.textEdit_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(530, 450, 571, 431))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1112, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "词法分析器"))
        self.Button1.setText(_translate("MainWindow", "文件"))
        self.Button2.setText(_translate("MainWindow", "保存"))
        self.Button3.setText(_translate("MainWindow", "词法分析"))
        self.Button4.setText(_translate("MainWindow", "语法分析"))
        self.Button5.setText(_translate("MainWindow", "语义分析"))
        self.Button6.setText(_translate("MainWindow", "中间代码"))
        self.Button7.setText(_translate("MainWindow", "自动生成"))
        self.Button8.setText(_translate("MainWindow", "帮助"))

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

    def _analysis_Demo(self):
        try:
            self.flag = True
            err_list = []
            Sy = Predict_()
            if len(self.token_code) != 0:
                print(self.token_code)
                Sy.Acess_(self.token_code)
                for i in Sy.err_list:
                    if i != None:
                        err_list.append(i)
                Sy.err_list = copy.deepcopy(err_list)
                self.textEdit_3.append(
                    "<font color='black' size=4>" + '----------------------语法分析错误信息----------------------' + "</font>")
                if len(err_list) == 0:
                    self.textEdit_3.append("<font color='black' size=4>语法法分析结束 - 0 error(s)</font>")
                else:
                    self.flag = False
                    for index, pre in enumerate(err_list):
                        self.textEdit_3.append("<font color='red' size=4>" + '------> error ' + str(pre) + "</font>")
                    self.textEdit_3.append(
                        "<font color='black' size=4>" + "语法分析结束 - " + str(len(err_list)) + " error(s)" + "</font>")

        except:
            self.textEdit_3.append(
                "<font color='black' size=4>" + '----------------------语法分析错误信息----------------------' + "</font>")
            self.textEdit_3.append("<font color='black' size=4>" + "存在文法无法推导得符号异常终止" + "</font>")

    def _semanalysis(self):
        try:
            self.flag = True
            S = Semantic_()
            if len(self.token_code) != 0:
                S.access(self.token_code)
                err_list = copy.deepcopy(S.error_list)
                err_list = list(set(err_list))
                self.textEdit_2.clear()
                for pre in S.syn_table.symbolTableInfo:
                    self.textEdit_2.insertPlainText(pre.strip() + '\n')
                self.textEdit_3.append(
                    "<font color='black' size=4>" + '----------------------语义分析错误信息----------------------' + "</font>")
                if len(err_list) == 0:
                    self.textEdit_3.append("<font color='black' size=4>语义分析结束 - 0 error(s)</font>")
                else:
                    self.flag = False
                    for index, pre in enumerate(err_list):
                        self.textEdit_3.append(
                            "<font color='red' size=3 width=20px>" + 'ErrorType:{} {} ErrorMessage:{}'.format(
                                pre.ErrorType, pre.Location,
                                pre.ErrorMessage) + "</font>")
                    self.textEdit_3.append(
                        "<font color='black' size=4>" + "语义分析结束 - " + str(len(err_list)) + " error(s)" + "</font>")

        except:
            self.textEdit_3.append(
                "<font color='black' size=4>" + '----------------------语义分析错误信息----------------------' + "</font>")
            self.textEdit_3.append("<font color='black' size=4>" + "语法存在错误，语义分析无法进行" + "</font>")

    def _generation(self):
        try:
            with open('D:/程序代码/PyProject/编译原理/Semantic/t.txt', 'w', encoding='utf-8')as f:
                for i in self.token_code:
                    f.write(str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(i[3]) + '\n')
            G = Genration_()
            if len(self.token_code) != 0 and self.flag:
                G.Acess_gen(self.token_code)
                self.textEdit_2.clear()
                self.textEdit_2.insertPlainText('四元式:' + '\n')
                for pre in G.out_list:
                    self.textEdit_2.insertPlainText(pre + '\n')
            else:
                self.textEdit_3.append("<font color='black' size=4>" + "程序存在错误无法生成四元式" + "</font>")
        except:
            self.textEdit_3.append("<font color='black' size=4>" + "程序存在错误无法生成四元式" + "</font>")

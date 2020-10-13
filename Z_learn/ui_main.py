# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", ".486   ;指令集\n"
".model flat,stdcall ;模式为flat（平坦）,函数调用方式为stdcall，代表从右到左将函数的参数\n"
";压栈\n"
"option casemap:none ;指明大小写敏感\n"
";inclue,includelib导入要用到的库\n"
"include     user32.inc\n"
"include     windows.inc\n"
"includelib  user32.lib\n"
"include     kernel32.inc\n"
"includelib  kernel32.lib\n"
"include     msvcrt.inc\n"
"includelib  msvcrt.lib\n"
"\n"
".const\n"
"t dd 3\n"
".data\n"
"RETURN dword ?\n"
"stop byte \'pause\', 0\n"
"printf byte \'%d \' ,0\n"
"scanf byte \'%d\',0\n"
"t11 dd ?\n"
"a dd ?\n"
"b dd ?\n"
"cc dd ?\n"
"T0 dd ?\n"
".code\n"
"add_fun proc t1, t2\n"
"MOV EAX, t1\n"
"ADD EAX, t2\n"
"MOV T0, EAX\n"
"MOV RETURN, EAX\n"
"RET\n"
"L4:\n"
"add_fun endp\n"
"Demo proc e, f\n"
"INVOKE add_fun, e, f\n"
"MOV EAX,RETURN\n"
"MOV t11, EAX\n"
"MOV RETURN, EAX\n"
"RET\n"
"L3:\n"
"Demo endp\n"
"main:\n"
"MOV EAX, 1\n"
"MOV a, EAX\n"
"MOV EAX, 2\n"
"MOV b, EAX\n"
"INVOKE Demo, a, b\n"
"MOV EAX,RETURN\n"
"MOV cc, EAX\n"
"L4:\n"
"invoke  crt_printf,offset printf,eax ; printf(‘%d’,a);\n"
"invoke crt_system,offset  stop ;system(‘pause’);\n"
"invoke ExitProcess,1; exit(1)\n"
"end main\n"
""))
        self.pushButton.setText(_translate("MainWindow", "点击"))

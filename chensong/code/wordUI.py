# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wordUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from Experiment_01.model_UI import QCodeEditor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1398, 871)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gb_showFile = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_showFile.setGeometry(QtCore.QRect(20, 20, 741, 761))
        self.gb_showFile.setObjectName("gb_showFile")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gb_showFile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pt_filw = QCodeEditor(self.gb_showFile)
        self.pt_filw.setStyleSheet("font: 14pt \"楷体\";")
        self.pt_filw.setObjectName("pt_filw")
        self.verticalLayout.addWidget(self.pt_filw)
        self.gb_showAnalysis = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_showAnalysis.setGeometry(QtCore.QRect(780, 30, 591, 401))
        self.gb_showAnalysis.setObjectName("gb_showAnalysis")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_showAnalysis)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pt_Analysis = QtWidgets.QPlainTextEdit(self.gb_showAnalysis)
        self.pt_Analysis.setStyleSheet("font: 14pt \"楷体\";")
        self.pt_Analysis.setReadOnly(True)
        self.pt_Analysis.setObjectName("pt_Analysis")
        self.verticalLayout_2.addWidget(self.pt_Analysis)
        self.gb_showError = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_showError.setGeometry(QtCore.QRect(780, 450, 591, 311))
        self.gb_showError.setObjectName("gb_showError")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gb_showError)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pt_error = QtWidgets.QPlainTextEdit(self.gb_showError)
        self.pt_error.setStyleSheet("font: 14pt \"楷体\";")
        self.pt_error.setReadOnly(True)
        self.pt_error.setObjectName("pt_error")
        self.verticalLayout_3.addWidget(self.pt_error)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1398, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gb_showFile.setTitle(_translate("MainWindow", "文件"))
        self.gb_showAnalysis.setTitle(_translate("MainWindow", "分析"))
        self.gb_showError.setTitle(_translate("MainWindow", "错误"))

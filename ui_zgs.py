# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_zgs.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 771)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_nfa = QtWidgets.QLabel(self.groupBox)
        self.label_nfa.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.label_nfa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_nfa.setObjectName("label_nfa")
        self.horizontalLayout.addWidget(self.label_nfa)
        self.label_dfa = QtWidgets.QLabel(self.groupBox)
        self.label_dfa.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.label_dfa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dfa.setObjectName("label_dfa")
        self.horizontalLayout.addWidget(self.label_dfa)
        self.label_m_dfa = QtWidgets.QLabel(self.groupBox)
        self.label_m_dfa.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.label_m_dfa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_m_dfa.setObjectName("label_m_dfa")
        self.horizontalLayout.addWidget(self.label_m_dfa)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "show"))
        self.label_nfa.setText(_translate("MainWindow", "nfa"))
        self.label_dfa.setText(_translate("MainWindow", "dfa"))
        self.label_m_dfa.setText(_translate("MainWindow", "min_dfa"))
        self.groupBox_2.setTitle(_translate("MainWindow", "input_zgs"))
        self.lineEdit.setText(_translate("MainWindow", "(a|b|c)*"))
        self.pushButton.setText(_translate("MainWindow", "生成"))

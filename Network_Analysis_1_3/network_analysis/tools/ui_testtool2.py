# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_Dialogtool2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        font.setFamily("Calibri")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 150, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(150, 40, 121, 22))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 42, 121, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(30, 102, 121, 16))
        self.label2.setFont(font)
        self.label2.setObjectName("label_2")
        self.comboBox2 = QtGui.QComboBox(Dialog)
        self.comboBox2.setGeometry(QtCore.QRect(150, 100, 121, 22))
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox_2")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Start Nodes Field", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "End Nodes Field", None, QtGui.QApplication.UnicodeUTF8))


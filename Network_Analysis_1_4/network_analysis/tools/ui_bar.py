# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_Dialog5(object):
    def setupUi(self, Dialog5):
        Dialog5.setObjectName("Dialog5")
        Dialog5.resize(400, 189)
        self.progressBar = QtGui.QProgressBar(Dialog5)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtGui.QLabel(Dialog5)
        self.label.setGeometry(QtCore.QRect(30, 50, 201, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog5)
        QtCore.QMetaObject.connectSlotsByName(Dialog5)

    def retranslateUi(self, Dialog5):
        Dialog5.setWindowTitle(QtGui.QApplication.translate("Dialog5", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog5", "Progression du calcul", None, QtGui.QApplication.UnicodeUTF8))


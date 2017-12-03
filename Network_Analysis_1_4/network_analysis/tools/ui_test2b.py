# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_Dialog2b(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(472, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog2)
        self.buttonBox.setGeometry(QtCore.QRect(110, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtGui.QComboBox(Dialog2)
        self.comboBox.setGeometry(QtCore.QRect(110, 20, 101, 22))
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog2)
        self.label.setGeometry(QtCore.QRect(20, 18, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Dialog2)
        self.label_2.setGeometry(QtCore.QRect(20, 28, 81, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Dialog2)
        self.label_3.setGeometry(QtCore.QRect(260, 18, 81, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtGui.QComboBox(Dialog2)
        self.comboBox_2.setGeometry(QtCore.QRect(350, 20, 101, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_4 = QtGui.QLabel(Dialog2)
        self.label_4.setGeometry(QtCore.QRect(260, 30, 81, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(Dialog2)
        self.label_5.setGeometry(QtCore.QRect(20, 83, 101, 16))
        self.label_5.setObjectName("label_5")
        self.comboBox_3 = QtGui.QComboBox(Dialog2)
        self.comboBox_3.setGeometry(QtCore.QRect(130, 80, 51, 21))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_4 = QtGui.QComboBox(Dialog2)
        self.comboBox_4.setGeometry(QtCore.QRect(130, 140, 51, 21))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_6 = QtGui.QLabel(Dialog2)
        self.label_6.setGeometry(QtCore.QRect(20, 143, 101, 16))
        self.label_6.setObjectName("label_6")
        self.comboBox_5 = QtGui.QComboBox(Dialog2)
        self.comboBox_5.setGeometry(QtCore.QRect(350, 140, 101, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.label_7 = QtGui.QLabel(Dialog2)
        self.label_7.setGeometry(QtCore.QRect(220, 143, 121, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtGui.QLabel(Dialog2)
        self.label_8.setGeometry(QtCore.QRect(20, 203, 121, 16))
        self.label_8.setObjectName("label_8")
        self.comboBox_6 = QtGui.QComboBox(Dialog2)
        self.comboBox_6.setGeometry(QtCore.QRect(90, 200, 171, 22))
        self.comboBox_6.setObjectName("comboBox_6")

        self.retranslateUi(Dialog2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog2.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog2.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        Dialog2.setWindowTitle(QtGui.QApplication.translate("Dialog2", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog2", "Start nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog2", "field", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog2", "End nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog2", "field", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog2", "Directed network ?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog2", "Weighted network ?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog2", "Weight field (optional)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog2", "Algorithm", None, QtGui.QApplication.UnicodeUTF8))


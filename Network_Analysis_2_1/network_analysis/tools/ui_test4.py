from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog4(object):
    def setupUi(self, Dialog4):
        Dialog4.setObjectName("Dialog4")
        Dialog4.resize(1000, 700)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog4)
        self.textBrowser.setGeometry(QtCore.QRect(15, 11, 961, 671))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog4)
        QtCore.QMetaObject.connectSlotsByName(Dialog4)

    def retranslateUi(self, Dialog4):
        Dialog4.setWindowTitle(QtWidgets.QApplication.translate("Dialog4", "Dialog", None))


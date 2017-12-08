from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog5(object):
    def setupUi(self, Dialog5):
        Dialog5.setObjectName("Dialog5")
        Dialog5.resize(400, 189)
        self.progressBar = QtWidgets.QProgressBar(Dialog5)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Dialog5)
        self.label.setGeometry(QtCore.QRect(30, 50, 201, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog5)
        QtCore.QMetaObject.connectSlotsByName(Dialog5)

    def retranslateUi(self, Dialog5):
        Dialog5.setWindowTitle(QtWidgets.QApplication.translate("Dialog5", "Dialog", None))
        self.label.setText(QtWidgets.QApplication.translate("Dialog5", "Progression du calcul", None))


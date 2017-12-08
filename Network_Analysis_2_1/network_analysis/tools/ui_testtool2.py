from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 150, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(150, 40, 121, 22))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 42, 121, 20))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(30, 102, 121, 16))
        self.label2.setFont(font)
        self.label2.setObjectName("label_2")
        self.comboBox2 = QtWidgets.QComboBox(Dialog)
        self.comboBox2.setGeometry(QtCore.QRect(150, 100, 121, 22))
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox_2")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Start Nodes Field", None))
        self.label2.setText(QtWidgets.QApplication.translate("Dialog", "End Nodes Field", None))


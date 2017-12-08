from PyQt5 import QtCore, QtGui, QtWidgets

import matplotlib.pyplot as plt
try : 
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except :
    "Catch error"

class Ui_Matplot(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 600)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        Dialog.setFont(font)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, Dialog)
        self.bouton1 = QtWidgets.QPushButton("Run", Dialog)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.toolbar,0,0,1,1)
        layout.addWidget(self.canvas,1,0,1,2)
        layout.addWidget(self.comboBox,2,0)
        layout.addWidget(self.bouton1,2,1)
        Dialog.setLayout(layout)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None))


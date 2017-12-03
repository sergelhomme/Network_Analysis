# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
try : 
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
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
        self.bouton1 = QtGui.QPushButton("Run", Dialog)
        self.comboBox = QtGui.QComboBox(Dialog)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,0,1,1)
        layout.addWidget(self.canvas,1,0,1,2)
        layout.addWidget(self.comboBox,2,0)
        layout.addWidget(self.bouton1,2,1)
        Dialog.setLayout(layout)

        self.retranslateUi(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))



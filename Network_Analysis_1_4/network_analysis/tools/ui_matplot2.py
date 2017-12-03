# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
try :
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except :
    "Catch error"

class Ui_Matplot2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 800)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        Dialog.setFont(font)
        self.figure = plt.figure()
        self.figure.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, wspace = 0, hspace = 0)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, Dialog)
        self.bouton1 = QtGui.QPushButton("Run", Dialog)
        self.bouton2 = QtGui.QPushButton("Edit Visualization", Dialog)
        self.comboBox = QtGui.QComboBox(Dialog)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,0,1,1)
        layout.addWidget(self.canvas,1,0,1,2)
        layout.addWidget(self.comboBox,2,0)
        layout.addWidget(self.bouton1,2,1)
        layout.addWidget(self.bouton2,3,0,1,2)
        Dialog.setLayout(layout)

        self.retranslateUi(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))



from PyQt5 import QtCore, QtGui, QtWidgets
from ui_matplot2 import Ui_Matplot2
class testMatplot2(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Matplot2()
    self.ui.setupUi(self)

from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtoolGS import Ui_DialogtesttoolGS
class testDialogtoolGS(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_DialogtesttoolGS()
    self.ui.setupUi(self)





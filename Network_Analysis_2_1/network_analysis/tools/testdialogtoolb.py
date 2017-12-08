from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtoolb import Ui_Dialogtoolb
class testDialogtoolb(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogtoolb()
    self.ui.setupUi(self)





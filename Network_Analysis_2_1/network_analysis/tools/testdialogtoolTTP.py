from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtoolTTP import Ui_DialogtesttoolTTP
class testDialogtoolTTP(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_DialogtesttoolTTP()
    self.ui.setupUi(self)





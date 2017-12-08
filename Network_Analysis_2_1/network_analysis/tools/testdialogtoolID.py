from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtoolID import Ui_DialogtesttoolID
class testDialogtoolID(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_DialogtesttoolID()
    self.ui.setupUi(self)





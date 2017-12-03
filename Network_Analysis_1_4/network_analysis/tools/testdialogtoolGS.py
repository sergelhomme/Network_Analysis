from PyQt4 import QtCore, QtGui
from ui_testtoolGS import Ui_DialogtesttoolGS
class testDialogtoolGS(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.ui = Ui_DialogtesttoolGS()
    self.ui.setupUi(self)





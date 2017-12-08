from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtool2 import Ui_Dialogtool2
class testDialogtool2(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogtool2()
    self.ui.setupUi(self)





from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testdialogdraw2 import Ui_testDialogdraw2
class testDialogdraw2(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_testDialogdraw2()
    self.ui.setupUi(self)





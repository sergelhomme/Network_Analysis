from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testdialogtoollc import Ui_testDialogtoollc
class testDialogtoollc(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_testDialogtoollc()
    self.ui.setupUi(self)





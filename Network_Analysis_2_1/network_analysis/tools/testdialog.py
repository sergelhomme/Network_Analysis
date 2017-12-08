from PyQt5 import QtCore, QtGui, QtWidgets
from ui_test import Ui_Dialog
class testDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)





from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtooldraw import Ui_Dialogtesttooldraw
class testDialogtooldraw(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogtesttooldraw()
    self.ui.setupUi(self)





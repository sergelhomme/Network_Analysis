from PyQt5 import QtCore, QtGui, QtWidgets
from ui_bar import Ui_Dialog5
class testDialog5(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog5()
    self.ui.setupUi(self)





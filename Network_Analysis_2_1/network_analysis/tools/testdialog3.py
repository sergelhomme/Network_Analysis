from PyQt5 import QtCore, QtGui, QtWidgets
from ui_test3 import Ui_Dialog3
class testDialog3(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog3()
    self.ui.setupUi(self)





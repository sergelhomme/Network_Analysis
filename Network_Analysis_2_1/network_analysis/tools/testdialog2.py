from PyQt5 import QtCore, QtGui, QtWidgets
from ui_test2 import Ui_Dialog2
class testDialog2(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog2()
    self.ui.setupUi(self)





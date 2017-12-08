from PyQt5 import QtCore, QtGui, QtWidgets
from ui_test2b import Ui_Dialog2b
class testDialog2b(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog2b()
    self.ui.setupUi(self)





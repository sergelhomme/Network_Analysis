from PyQt5 import QtCore, QtGui, QtWidgets
from ui_test4 import Ui_Dialog4
class testDialog4(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialog4()
    self.ui.setupUi(self)





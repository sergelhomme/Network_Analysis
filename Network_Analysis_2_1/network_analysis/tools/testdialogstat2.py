from PyQt5 import QtCore, QtGui, QtWidgets
from ui_teststat2 import Ui_Dialogstat2
class testDialogstat2(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogstat2()
    self.ui.setupUi(self)





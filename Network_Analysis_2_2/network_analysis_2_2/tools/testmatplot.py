from PyQt5 import QtCore, QtGui, QtWidgets
from ui_matplot import Ui_Matplot
class testMatplot(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Matplot()
    self.ui.setupUi(self)

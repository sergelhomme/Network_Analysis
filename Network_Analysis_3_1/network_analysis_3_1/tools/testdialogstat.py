#from PyQt6 import QtCore, QtGui, QtWidgets
from qgis.PyQt import QtCore, QtGui, QtWidgets
from ui_teststat import Ui_Dialogstat
class testDialogstat(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogstat()
    self.ui.setupUi(self)

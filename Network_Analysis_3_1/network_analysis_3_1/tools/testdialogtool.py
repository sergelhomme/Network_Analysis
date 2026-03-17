#from PyQt6 import QtCore, QtGui, QtWidgets
from qgis.PyQt import QtCore, QtGui, QtWidgets
from ui_testtool import Ui_Dialogtool
class testDialogtool(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = Ui_Dialogtool()
    self.ui.setupUi(self)

from PyQt4 import QtCore, QtGui
from ui_testdialogtoollc import Ui_testDialogtoollc
# create the dialog
class testDialogtoollc(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_testDialogtoollc()
    self.ui.setupUi(self)





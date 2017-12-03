from PyQt4 import QtCore, QtGui
from ui_testdialogdraw2 import Ui_testDialogdraw2
# create the dialog
class testDialogdraw2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_testDialogdraw2()
    self.ui.setupUi(self)





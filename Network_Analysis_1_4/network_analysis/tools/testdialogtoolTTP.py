from PyQt4 import QtCore, QtGui
from ui_testtoolTTP import Ui_DialogtesttoolTTP
# create the dialog
class testDialogtoolTTP(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_DialogtesttoolTTP()
    self.ui.setupUi(self)





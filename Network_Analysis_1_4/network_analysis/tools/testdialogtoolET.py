from PyQt4 import QtCore, QtGui
from ui_testtoolET import Ui_DialogtesttoolET
# create the dialog
class testDialogtoolET(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_DialogtesttoolET()
    self.ui.setupUi(self)





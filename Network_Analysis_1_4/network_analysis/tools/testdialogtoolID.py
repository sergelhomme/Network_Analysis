from PyQt4 import QtCore, QtGui
from ui_testtoolID import Ui_DialogtesttoolID
# create the dialog
class testDialogtoolID(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_DialogtesttoolID()
    self.ui.setupUi(self)





from PyQt4 import QtCore, QtGui
from ui_testtoolb import Ui_Dialogtoolb
# create the dialog
class testDialogtoolb(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogtoolb()
    self.ui.setupUi(self)





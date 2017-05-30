from PyQt4 import QtCore, QtGui
from ui_testtool2 import Ui_Dialogtool2
# create the dialog
class testDialogtool2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogtool2()
    self.ui.setupUi(self)





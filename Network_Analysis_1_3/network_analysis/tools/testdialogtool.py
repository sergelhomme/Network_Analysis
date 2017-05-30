from PyQt4 import QtCore, QtGui
from ui_testtool import Ui_Dialogtool
# create the dialog
class testDialogtool(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogtool()
    self.ui.setupUi(self)





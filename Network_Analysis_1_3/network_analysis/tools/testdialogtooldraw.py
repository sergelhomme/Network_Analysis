from PyQt4 import QtCore, QtGui
from ui_testtooldraw import Ui_Dialogtesttooldraw
# create the dialog
class testDialogtooldraw(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogtesttooldraw()
    self.ui.setupUi(self)





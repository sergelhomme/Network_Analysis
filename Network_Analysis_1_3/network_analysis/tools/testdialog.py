from PyQt4 import QtCore, QtGui
from ui_test import Ui_Dialog
# create the dialog
class testDialog(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)





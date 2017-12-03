from PyQt4 import QtCore, QtGui
from ui_teststat import Ui_Dialogstat
# create the dialog
class testDialogstat(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogstat()
    self.ui.setupUi(self)





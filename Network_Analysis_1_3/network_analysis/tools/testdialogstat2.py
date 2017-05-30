from PyQt4 import QtCore, QtGui
from ui_teststat2 import Ui_Dialogstat2
# create the dialog
class testDialogstat2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialogstat2()
    self.ui.setupUi(self)





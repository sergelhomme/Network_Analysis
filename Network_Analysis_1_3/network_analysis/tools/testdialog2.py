from PyQt4 import QtCore, QtGui
from ui_test2 import Ui_Dialog2
# create the dialog
class testDialog2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog2()
    self.ui.setupUi(self)





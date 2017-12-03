from PyQt4 import QtCore, QtGui
from ui_test3 import Ui_Dialog3
# create the dialog
class testDialog3(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog3()
    self.ui.setupUi(self)





from PyQt4 import QtCore, QtGui
from ui_test2b import Ui_Dialog2b
# create the dialog
class testDialog2b(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog2b()
    self.ui.setupUi(self)





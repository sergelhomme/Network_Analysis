from PyQt4 import QtCore, QtGui
from ui_test4 import Ui_Dialog4
# create the dialog
class testDialog4(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog4()
    self.ui.setupUi(self)





from PyQt4 import QtCore, QtGui
from ui_matplot2 import Ui_Matplot2
# create the dialog
class testMatplot2(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Matplot2()
    self.ui.setupUi(self)

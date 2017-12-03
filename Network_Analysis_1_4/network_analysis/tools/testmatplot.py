from PyQt4 import QtCore, QtGui
from ui_matplot import Ui_Matplot
# create the dialog
class testMatplot(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Matplot()
    self.ui.setupUi(self)

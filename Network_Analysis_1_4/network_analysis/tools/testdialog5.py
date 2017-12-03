from PyQt4 import QtCore, QtGui
from ui_bar import Ui_Dialog5
# create the dialog
class testDialog5(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_Dialog5()
    self.ui.setupUi(self)





from PyQt5 import QtCore, QtGui, QtWidgets
from ui_testtoolET import Ui_DialogtesttoolET
# create the dialog
class testDialogtoolET(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    # Set up the user interface from Designer.
    self.ui = Ui_DialogtesttoolET()
    self.ui.setupUi(self)





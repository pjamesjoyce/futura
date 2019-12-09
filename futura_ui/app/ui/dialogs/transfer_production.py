from PySide2 import QtWidgets, QtGui
from ..utils import load_ui_file
import os


class TransferProductionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TransferProductionDialog, self).__init__(parent)

        ui_path = 'transfer_production.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        validator = QtGui.QDoubleValidator()
        validator.setDecimals(0)

        self.newValueLineEdit.setValidator(validator)

        self.transferLabel.setText('Percentage:')
        self.newValueLineEdit.setInputMask("009%")

        self.percentageRadioButton.clicked.connect(self.radio_button_change)
        self.amountRadioButton.clicked.connect(self.radio_button_change)

    def radio_button_change(self):

        if self.percentageRadioButton.isChecked():
            self.transferLabel.setText('Percentage:')
            self.newValueLineEdit.setInputMask("009%")
        elif self.amountRadioButton.isChecked():
            self.transferLabel.setText('Amount:')
            self.newValueLineEdit.setInputMask(None)

            print('Amount')

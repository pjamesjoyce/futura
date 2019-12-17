from PySide2 import QtWidgets, QtGui
from ..ui_files import Ui_TransferProductionDialog


class TransferProductionDialog(Ui_TransferProductionDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TransferProductionDialog, self).__init__(parent)

        self.setupUi(self)

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

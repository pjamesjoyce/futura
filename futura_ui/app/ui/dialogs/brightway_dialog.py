from PySide2 import QtWidgets
from ..ui_files import Ui_BrightwayDialog


class BrightwayDialog(Ui_BrightwayDialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BrightwayDialog, self).__init__(parent)

        self.setupUi(self)

        self.existingComboBox = QtWidgets.QComboBox()

        self.newLineEdit = QtWidgets.QLineEdit()

        self.input_widgets = [
            self.existingComboBox,
            self.newLineEdit
        ]
        for input_widget in self.input_widgets:
            self.projectChoiceLayout.addWidget(input_widget)

        self.connect_widgets()
        self.check_project_type()

    def connect_widgets(self):
        self.existingRadioButton.toggled.connect(self.check_project_type)
        self.newRadioButton.toggled.connect(self.check_project_type)

    def check_project_type(self):

        if self.existingRadioButton.isChecked():
            self.existingComboBox.show()
            self.newLineEdit.hide()
        elif self.newRadioButton.isChecked():
            self.existingComboBox.hide()
            self.newLineEdit.show()
        else:
            print('something has gone wrong')



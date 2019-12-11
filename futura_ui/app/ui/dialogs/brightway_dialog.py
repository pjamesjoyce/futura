from PySide2 import QtWidgets
from ..utils import load_ui_file
import os


class BrightwayDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BrightwayDialog, self).__init__(parent)

        ui_path = 'brightway_dialog.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.existingComboBox = QtWidgets.QComboBox()

        self.newLineEdit = QtWidgets.QLineEdit()

        self.input_widgets = [
            self.existingComboBox,
            self.newLineEdit
        ]
        for input_widget in self.input_widgets:
            self.projectChoiceLayout.addWidget(input_widget)

        self.connect_widgets()

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



from PySide2 import QtWidgets
from ..utils import load_ui_file
import os
import brightway2 as bw2

class BrightwayOpenDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BrightwayOpenDialog, self).__init__(parent)

        ui_path = 'brightway_open_dialog.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.projectComboBox = QtWidgets.QComboBox()
        self.databaseComboBox = QtWidgets.QComboBox()

        self.projectChoiceLayout.addWidget(self.projectComboBox)
        self.databaseChoiceLayout.addWidget(self.databaseComboBox)

        self.connect_widgets()

    def connect_widgets(self):
        #self.existingRadioButton.toggled.connect(self.check_project_type)
        self.projectComboBox.currentIndexChanged.connect(self.check_project)
        pass

    def check_project(self):

        chosen_project = self.projectComboBox.currentText()
        bw2.projects.set_current(chosen_project)
        databases = list(sorted(bw2.databases))

        self.databaseComboBox.clear()
        self.databaseComboBox.addItems(databases)




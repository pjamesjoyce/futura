from PySide2 import QtWidgets
from futura_ui.app.ui.utils import load_ui_file
from futura_ui.app.ui.tables.projects import ProjectListWidget
import os


class ProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ProjectDialog, self).__init__(parent)

        ui_path = 'project_choice.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        projectList = ProjectListWidget()

        self.verticalLayout.addWidget(projectList)


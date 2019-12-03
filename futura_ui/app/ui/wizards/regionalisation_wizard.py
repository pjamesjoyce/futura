from PySide2 import QtWidgets
import os
from ..utils import load_ui_file
from ..widgets.filter import FilterListerWidget


class RegionalisationWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(RegionalisationWizard, self).__init__(parent)

        ui_path = 'regionalisation_wizard.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)
        self.filter_widget = FilterListerWidget()
        self.filterLayout.addWidget(self.filter_widget)


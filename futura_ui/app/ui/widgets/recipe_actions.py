from PySide2 import QtWidgets
from ..utils import load_ui_file
from ...signals import signals
import os
from functools import partial

emit_0 = partial(signals.start_status_progress.emit, 0)


class RecipeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RecipeWidget, self).__init__(parent)

        ui_path = 'recipe_actions.ui'
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        #self.baseDatabaseButton.pressed.connect(signals.show_load_actions.emit)
        self.baseDatabaseButton.pressed.connect(signals.test_filter.emit)
        self.regionaliseButton.pressed.connect(signals.regionalisation_wizard.emit)
        self.exportButton.pressed.connect(signals.export_recipe.emit)
        self.technologyFileButton.pressed.connect(signals.add_technology_file.emit)
        self.marketsButton.pressed.connect(signals.markets_wizard.emit)


from PySide2 import QtWidgets
from ...signals import signals
from ..ui_files import Ui_ActionsWidget


class ActionWidget(Ui_ActionsWidget, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ActionWidget, self).__init__(parent)

        self.setupUi(self)

        self.recipe_buttons = [
            self.baseDatabaseButton,
            self.regionaliseButton,
            self.exportButton,
            self.technologyFileButton,
            self.marketsButton,
            self.exportBrightwayButton,
            self.testButton,
            self.saveLoaderButton
        ]

        self.testButton.hide()

        self.connect_buttons()
        self.deactivate_recipe_actions()
        self.connect_signals()

    def deactivate_recipe_actions(self):
        for button in self.recipe_buttons:
            button.setEnabled(False)

    def activate_recipe_actions(self):
        for button in self.recipe_buttons:
            button.setEnabled(True)

    def connect_buttons(self):
        self.baseDatabaseButton.pressed.connect(signals.add_base_database.emit)
        self.regionaliseButton.pressed.connect(signals.regionalisation_wizard.emit)
        self.exportButton.pressed.connect(signals.export_recipe.emit)
        self.technologyFileButton.pressed.connect(signals.add_technology_file.emit)
        self.marketsButton.pressed.connect(signals.markets_wizard.emit)

        self.newButton.pressed.connect(signals.new_recipe.emit)
        self.loadButton.pressed.connect(signals.load_recipe.emit)
        self.loaderButton.pressed.connect(signals.load_loader.emit)
        self.saveLoaderButton.pressed.connect(signals.save_loader.emit)

        self.exportBrightwayButton.pressed.connect(signals.export_to_brightway.emit)
        self.testButton.pressed.connect(self.test)

    def connect_signals(self):
        signals.show_recipe_actions.connect(self.activate_recipe_actions)

    def test(self):
        signals.change_status_message.emit('TESTING!!!')


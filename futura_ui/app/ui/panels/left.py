from .frame import FuturaFrame
from ..widgets.load_actions import LoadWidget
from ..widgets.recipe_actions import RecipeWidget
from ..widgets import ActionWidget
from ...signals import signals


class LeftPanel(FuturaFrame):
    side = "left"

    def __init__(self, *args):
        super(LeftPanel, self).__init__(*args)
        self.connect_signals()
        self.label.setText('Actions')

        self.widget_layout.addWidget(ActionWidget())

    def connect_signals(self):
        pass
        #signals.show_load_actions.connect(self.show_load_actions)
        #signals.show_recipe_actions.connect(self.show_recipe_actions)

    def show_load_actions(self):
        self.clear()
        self.widget_layout.addWidget(LoadWidget())

    def show_recipe_actions(self):
        self.clear()
        self.widget_layout.addWidget(RecipeWidget())



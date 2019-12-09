from .frame import FuturaFrame
from ...signals import signals
from ...models import RecipeModel
from PySide2.QtWidgets import QTreeView
from ...utils import findMainWindow


class RightPanel(FuturaFrame):
    side = "right"

    def __init__(self, *args):
        super(RightPanel, self).__init__(*args)
        self.connect_signals()

        self.label.setText('Recipe')
        self.tree_view = QTreeView()
        self.model = RecipeModel()
        self.tree_view.setModel(self.model)
        self.tree_view.setWordWrap(True)
        self.tree_view.setColumnWidth(0, 50)

        self.widget_layout.addWidget(self.tree_view)

        signals.update_recipe.emit()

    def connect_signals(self):
        signals.update_recipe.connect(self.update_recipe)

    def update_recipe(self):

        self.model.parse_recipe(findMainWindow().loader.recipe)

        if self.model.rowCount() == 0:
            self.tree_view.header().hide()
        else:
            self.tree_view.header().show()

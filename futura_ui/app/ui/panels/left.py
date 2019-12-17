from .frame import FuturaFrame
from ..widgets import ActionWidget


class LeftPanel(FuturaFrame):
    side = "left"

    def __init__(self, *args):
        super(LeftPanel, self).__init__(*args)
        self.connect_signals()
        self.label.setText('Actions')

        self.widget_layout.addWidget(ActionWidget())

    def connect_signals(self):
        pass





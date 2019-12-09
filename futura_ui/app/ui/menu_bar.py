from ..signals import signals
from PySide2 import QtWidgets
from .icons import qicons


class MenuBar(object):
    def __init__(self, window):

        self.window = window

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.addMenu(self.setup_file_menu())

        window.setMenuBar(self.menubar)

    def setup_file_menu(self):
        menu = QtWidgets.QMenu('&File', self.window)

        menu.addAction(
            qicons.futura,
            '&New Recipe...',
            signals.new_recipe.emit
        )

        menu.addSeparator()

        menu.addAction(
            qicons.futura,
            '&Save...',
            signals.save_loader.emit
        )
        menu.addAction(
            qicons.futura,
            '&Load...',
            signals.load_loader.emit
        )

        menu.addSeparator()

        menu.addAction(
            qicons.futura,
            '&Load Recipe...',
            signals.load_recipe.emit
        )

        return menu


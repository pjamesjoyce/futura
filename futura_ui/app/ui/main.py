# -*- coding: utf-8 -*-
import sys

from PySide2 import QtCore, QtGui, QtWidgets
#from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

from .utils import load_ui_file

# from .style import header
from .icons import qicons
# from .menu_bar import MenuBar
# from .panels import LeftPanel, RightPanel
# from .statusbar import Statusbar
# from .utils import StdRedirector
from ..signals import signals
import os

APP_NAME = "Futura"
APP_VERSION = "0.0.1"


class MainWindow(QtWidgets.QMainWindow):
    # DEFAULT_NO_METHOD = 'No method selected yet'

    def __init__(self):
        super(MainWindow, self).__init__(None)

        ui_path = os.path.join('main', 'main.ui')
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)
        #self.ui.setupUi(self)

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        # Window title
        self.setWindowTitle("{} {}".format(APP_NAME, APP_VERSION))

        # Background Color
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), QtGui.QColor(148, 143, 143, 127))
        # self.setPalette(p)

        # Small icon in main window titlebar
        self.icon = qicons.futura
        self.setWindowIcon(self.icon)
        t = QtCore.QTimer()
        t.singleShot(0, self.show_rundialog)

    def show_rundialog(self):
        signals.run_dialog.emit(self)


        # self.connect_signals()

    # def connect_signals(self):
    #     # Keyboard shortcuts
    #     self.shortcut_debug = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"), self)
    #     self.shortcut_debug.activated.connect(self.toggle_debug_window)
    #
    # def toggle_debug_window(self):
    #     """Toggle between any window and the debug window."""
    #     if self.stacked.currentWidget() != self.debug_widget:
    #         self.last_widget = self.stacked.currentWidget()
    #         self.stacked.setCurrentWidget(self.debug_widget)
    #         # print("Switching to debug window")
    #     else:
    #         # print("Switching back to last widget")
    #         if self.last_widget:
    #             try:
    #                 self.stacked.setCurrentWidget(self.last_widget)
    #             except:
    #                 print("Previous Widget has been deleted in the meantime. Switching to main window.")
    #                 self.stacked.setCurrentWidget(self.main_widget)
    #         else:  # switch to main window
    #             self.stacked.setCurrentWidget(self.main_widget)
    #
    # def add_tab_to_panel(self, obj, label, side):
    #     panel = self.left_panel if side == 'left' else self.right_panel
    #     panel.addTab(obj, label)
    #
    # def select_tab(self, obj, side):
    #     panel = self.left_panel if side == 'left' else self.right_panel
    #     panel.setCurrentIndex(panel.indexOf(obj))
    #
    # def dialog(self, title, label):
    #     value, ok = QtWidgets.QInputDialog.getText(self, title, label)
    #     if ok:
    #         return value
    #
    # def info(self, label):
    #     QtWidgets.QMessageBox.information(
    #         self,
    #         "Information",
    #         label,
    #         QtWidgets.QMessageBox.Ok,
    #     )
    #
    # def warning(self, title, text):
    #     QtWidgets.QMessageBox.warning(self, title, text)
    #
    # def confirm(self, label):
    #     response = QtWidgets.QMessageBox.question(
    #         self,
    #         "Confirm Action",
    #         label,
    #         QtWidgets.QMessageBox.Yes,
    #         QtWidgets.QMessageBox.No
    #     )
    #     return response == QtWidgets.QMessageBox.Yes

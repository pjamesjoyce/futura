# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtWidgets

from .utils import load_ui_file
from .icons import qicons
from .panels import LeftPanel, RightPanel
from . menu_bar import MenuBar
from ..signals import signals

import time
import os
from futura.recipe_parser import FuturaLoader

from .dialogs.progress import UndefinedProgress
from ..wrappers import FuturaGuiLoader

APP_NAME = "Futura"
APP_VERSION = "0.0.1"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)

        self.loader = FuturaGuiLoader()

        ui_path = os.path.join('main', 'new_main_empty.ui')
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        # Window title
        self.setWindowTitle("{} {}".format(APP_NAME, APP_VERSION))

        self.main_horizontal_box = QtWidgets.QHBoxLayout()

        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        signals.show_load_actions.emit()

        self.menu_bar = MenuBar(self)

        #Add a progress bar to the status bar
        self.statusBar().showMessage('Ready')
        self.progress_bar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setGeometry(30, 40, 50, 25)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        # Small icon in main window titlebar
        self.icon = qicons.futura
        self.setWindowIcon(self.icon)

        self.connect_signals()

        #self.progress = UndefinedProgress('Loading', None, 0, 0, self.centralWidget())

    def start_status_progress(self, maximum):
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def hide_status_progress(self):
        time.sleep(1)
        self.progress_bar.hide()

    def change_status_message(self, message):
        self.statusBar().showMessage(message)

    def reset_status_message(self):
        self.statusBar().showMessage('Ready')

    def connect_signals(self):
        signals.start_status_progress.connect(self.start_status_progress)
        signals.update_status_progress.connect(self.progress_bar.setValue)
        signals.hide_status_progress.connect(self.hide_status_progress)
        signals.change_status_message.connect(self.change_status_message)
        signals.reset_status_message.connect(self.reset_status_message)

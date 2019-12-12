# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtWidgets, QtGui

from futura_ui.app.ui.utils import load_ui_file
from futura_ui.app.ui.icons import qicons
from futura_ui.app.ui.panels import LeftPanel, RightPanel
from futura_ui.app.ui.menu_bar import MenuBar
from futura_ui.app.signals import signals

import time
import os
from futura.loader import FuturaLoader

from futura_ui.app.ui.dialogs.progress import UndefinedProgress
from futura_ui.app.wrappers import FuturaGuiLoader

APP_NAME = "Futura"
APP_VERSION = "0.0.1"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)

        ui_path = os.path.join('main_window', 'main.ui')
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)

        load_ui_file(ui_path, self)

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        self.loader = FuturaGuiLoader()
        self.identifier = 'MainWindow'

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
        print('Signal received - starting the progress bar')
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def hide_status_progress(self):
        time.sleep(1)
        self.progress_bar.hide()

    def change_status_message(self, message):
        print('Signal received - changing the status bar message to {}'.format(message))
        self.statusBar().showMessage(message)

    def reset_status_message(self):
        if len(self.loader.database.db):
            added_message = "Databases: {}    Activities: {}".format(", ".join(self.loader.database.database_names),
                                                                     len(self.loader.database.db))
        else:
            added_message = ''
        self.statusBar().showMessage('Ready    {}'.format(added_message))

    def connect_signals(self):
        signals.start_status_progress.connect(self.start_status_progress)
        signals.update_status_progress.connect(self.progress_bar.setValue)
        signals.hide_status_progress.connect(self.hide_status_progress)
        signals.change_status_message.connect(self.change_status_message)
        signals.reset_status_message.connect(self.reset_status_message)

        self.load_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"), self)
        #self.load_shortcut.activated.connect(signals.load_loader.emit)  # TODO: Reinstate this
        self.load_shortcut.activated.connect(signals.load_base.emit)  # TODO: Delete this



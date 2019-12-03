from PySide2 import QtWidgets, QtCore
from ...signals import signals


class UndefinedProgress(QtWidgets.QProgressDialog):

    def __init__(self, *args, **kwargs):
        super(UndefinedProgress, self).__init__(*args, **kwargs)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setMinimum(0)
        self.setMaximum(0)
        self.connect_signals()

    def connect_signals(self):

        signals.show_undefined_progress.connect(self.show)
        signals.close_undefined_progress.connect(self.close)


class DefinedProgress(QtWidgets.QProgressDialog):

    def __init__(self, *args, **kwargs):
        super(DefinedProgress, self).__init__(*args, **kwargs)
        #self.setWindowModality(QtCore.Qt.WindowModal)
        self.connect_signals()

    def connect_signals(self):

        signals.show_defined_progress.connect(self.show)
        signals.close_defined_progress.connect(self.close)
        signals.set_defined_progress_value.connect(self.setValue)

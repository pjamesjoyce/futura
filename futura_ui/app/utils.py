import typing
from PySide2.QtWidgets import QMainWindow, QApplication


def findMainWindow() -> typing.Union[QMainWindow, None]:
    # Global function to find the (open) QMainWindow in application
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            if getattr(widget, 'identifier', None) == "MainWindow":
                return widget

    return None

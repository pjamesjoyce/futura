# -*- coding: utf-8 -*-
import uuid
from io import StringIO

from PySide2 import QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QMetaObject


class UiLoader(QUiLoader):
    def __init__(self, base_instance):
        QUiLoader.__init__(self, base_instance)
        self.base_instance = base_instance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.base_instance:
            return self.base_instance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.base_instance:
                setattr(self.base_instance, name, widget)
            return widget


def load_ui_file(ui_file, base_instance=None):
    loader = UiLoader(base_instance)
    widget = loader.load(ui_file)
    QMetaObject.connectSlotsByName(widget)
    return widget


class StdRedirector(StringIO):
    # From http://stackoverflow.com/questions/17132994/pyside-and-python-logging/17145093#17145093
    def __init__(self, widget, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit_widget = widget
        self.out = out
        self.color = color

    def write(self, text):
        # TODO: Doesn't seem to have any effect
        if self.color:
            original = self.edit_widget.textColor()
            self.edit_widget.setTextColor(QtGui.QColor(self.color))

        self.edit_widget.moveCursor(QtGui.QTextCursor.End)
        self.edit_widget.insertPlainText(text)

        if self.color:
            self.edit_widget.setTextColor(original)

        if self.out:
            self.out.write(text)

    def flush(self, *args, **kwargs):
        pass


def new_id():
    return uuid.uuid4().hex


abt1 = '16z7c78fbfdzb9fbe893c2'

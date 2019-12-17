# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\panel.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\panel.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PanelWidget(object):
    def setupUi(self, PanelWidget):
        PanelWidget.setObjectName("PanelWidget")
        PanelWidget.resize(762, 690)
        PanelWidget.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(PanelWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(PanelWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.panel_widget = QtWidgets.QWidget(PanelWidget)
        self.panel_widget.setStyleSheet("")
        self.panel_widget.setObjectName("panel_widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.panel_widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget_layout = QtWidgets.QGridLayout()
        self.widget_layout.setObjectName("widget_layout")
        self.gridLayout_3.addLayout(self.widget_layout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.panel_widget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(PanelWidget)
        QtCore.QMetaObject.connectSlotsByName(PanelWidget)

    def retranslateUi(self, PanelWidget):
        PanelWidget.setWindowTitle(QtWidgets.QApplication.translate("PanelWidget", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("PanelWidget", "Text goes here", None, -1))


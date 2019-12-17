# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_widget.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_widget.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FilterWidget(object):
    def setupUi(self, FilterWidget):
        FilterWidget.setObjectName("FilterWidget")
        FilterWidget.resize(542, 57)
        self.gridLayout = QtWidgets.QGridLayout(FilterWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.item_box = QtWidgets.QComboBox(FilterWidget)
        self.item_box.setObjectName("item_box")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.horizontalLayout.addWidget(self.item_box)
        self.filter_box = QtWidgets.QComboBox(FilterWidget)
        self.filter_box.setObjectName("filter_box")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.horizontalLayout.addWidget(self.filter_box)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.subFilterLayout = QtWidgets.QVBoxLayout()
        self.subFilterLayout.setObjectName("subFilterLayout")
        self.gridLayout.addLayout(self.subFilterLayout, 1, 0, 1, 1)

        self.retranslateUi(FilterWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterWidget)

    def retranslateUi(self, FilterWidget):
        FilterWidget.setWindowTitle(QtWidgets.QApplication.translate("FilterWidget", "Form", None, -1))
        self.item_box.setItemText(0, QtWidgets.QApplication.translate("FilterWidget", "Name", None, -1))
        self.item_box.setItemText(1, QtWidgets.QApplication.translate("FilterWidget", "Location", None, -1))
        self.item_box.setItemText(2, QtWidgets.QApplication.translate("FilterWidget", "Unit", None, -1))
        self.item_box.setItemText(3, QtWidgets.QApplication.translate("FilterWidget", "Reference product", None, -1))
        self.item_box.setItemText(4, QtWidgets.QApplication.translate("FilterWidget", "Database", None, -1))
        self.item_box.setItemText(5, QtWidgets.QApplication.translate("FilterWidget", "Code", None, -1))
        self.filter_box.setItemText(0, QtWidgets.QApplication.translate("FilterWidget", "Equals", None, -1))
        self.filter_box.setItemText(1, QtWidgets.QApplication.translate("FilterWidget", "Contains", None, -1))
        self.filter_box.setItemText(2, QtWidgets.QApplication.translate("FilterWidget", "Starts with", None, -1))
        self.filter_box.setItemText(3, QtWidgets.QApplication.translate("FilterWidget", "Doesn\'t contain any", None, -1))
        self.filter_box.setItemText(4, QtWidgets.QApplication.translate("FilterWidget", "Either", None, -1))


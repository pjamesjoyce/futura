# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\sub_filter_widget.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\sub_filter_widget.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SubFilterWidget(object):
    def setupUi(self, SubFilterWidget):
        SubFilterWidget.setObjectName("SubFilterWidget")
        SubFilterWidget.resize(542, 52)
        self.gridLayout = QtWidgets.QGridLayout(SubFilterWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(SubFilterWidget)
        self.line.setMinimumSize(QtCore.QSize(30, 0))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.subaddButton = QtWidgets.QPushButton(SubFilterWidget)
        self.subaddButton.setMaximumSize(QtCore.QSize(24, 16777215))
        self.subaddButton.setText("")
        self.subaddButton.setObjectName("subaddButton")
        self.horizontalLayout.addWidget(self.subaddButton)
        self.subremoveButton = QtWidgets.QPushButton(SubFilterWidget)
        self.subremoveButton.setMaximumSize(QtCore.QSize(24, 16777215))
        self.subremoveButton.setText("")
        self.subremoveButton.setObjectName("subremoveButton")
        self.horizontalLayout.addWidget(self.subremoveButton)
        self.item_box = QtWidgets.QComboBox(SubFilterWidget)
        self.item_box.setObjectName("item_box")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.item_box.addItem("")
        self.horizontalLayout.addWidget(self.item_box)
        self.filter_box = QtWidgets.QComboBox(SubFilterWidget)
        self.filter_box.setObjectName("filter_box")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.horizontalLayout.addWidget(self.filter_box)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(SubFilterWidget)
        QtCore.QMetaObject.connectSlotsByName(SubFilterWidget)

    def retranslateUi(self, SubFilterWidget):
        SubFilterWidget.setWindowTitle(QtWidgets.QApplication.translate("SubFilterWidget", "Form", None, -1))
        self.item_box.setItemText(0, QtWidgets.QApplication.translate("SubFilterWidget", "Name", None, -1))
        self.item_box.setItemText(1, QtWidgets.QApplication.translate("SubFilterWidget", "Location", None, -1))
        self.item_box.setItemText(2, QtWidgets.QApplication.translate("SubFilterWidget", "Unit", None, -1))
        self.item_box.setItemText(3, QtWidgets.QApplication.translate("SubFilterWidget", "Reference product", None, -1))
        self.item_box.setItemText(4, QtWidgets.QApplication.translate("SubFilterWidget", "Database", None, -1))
        self.item_box.setItemText(5, QtWidgets.QApplication.translate("SubFilterWidget", "Code", None, -1))
        self.filter_box.setItemText(0, QtWidgets.QApplication.translate("SubFilterWidget", "Equals", None, -1))
        self.filter_box.setItemText(1, QtWidgets.QApplication.translate("SubFilterWidget", "Contains", None, -1))
        self.filter_box.setItemText(2, QtWidgets.QApplication.translate("SubFilterWidget", "Starts with", None, -1))
        self.filter_box.setItemText(3, QtWidgets.QApplication.translate("SubFilterWidget", "Doesn\'t contain any", None, -1))


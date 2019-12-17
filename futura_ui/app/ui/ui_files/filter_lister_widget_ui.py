# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_lister_widget.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_lister_widget.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FilterListerWidget(object):
    def setupUi(self, FilterListerWidget):
        FilterListerWidget.setObjectName("FilterListerWidget")
        FilterListerWidget.resize(550, 180)
        self.gridLayout_2 = QtWidgets.QGridLayout(FilterListerWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.filterLayout = QtWidgets.QVBoxLayout()
        self.filterLayout.setObjectName("filterLayout")
        self.gridLayout_2.addLayout(self.filterLayout, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(FilterListerWidget)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addButton = QtWidgets.QPushButton(self.frame)
        self.addButton.setMaximumSize(QtCore.QSize(30, 30))
        self.addButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../icons/main/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.addButton.setIcon(icon)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.removeButton = QtWidgets.QPushButton(self.frame)
        self.removeButton.setMaximumSize(QtCore.QSize(30, 30))
        self.removeButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../icons/main/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.removeButton.setIcon(icon1)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_2.addWidget(self.removeButton)
        spacerItem = QtWidgets.QSpacerItem(418, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(FilterListerWidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.testButton = QtWidgets.QPushButton(self.frame_2)
        self.testButton.setObjectName("testButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.testButton)
        self.test_result = QtWidgets.QLabel(self.frame_2)
        self.test_result.setText("")
        self.test_result.setWordWrap(True)
        self.test_result.setObjectName("test_result")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.test_result)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 2, 0, 1, 1)

        self.retranslateUi(FilterListerWidget)
        QtCore.QMetaObject.connectSlotsByName(FilterListerWidget)

    def retranslateUi(self, FilterListerWidget):
        FilterListerWidget.setWindowTitle(QtWidgets.QApplication.translate("FilterListerWidget", "Form", None, -1))
        self.testButton.setText(QtWidgets.QApplication.translate("FilterListerWidget", "Test", None, -1))


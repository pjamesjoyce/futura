# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_lister.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\filter_lister.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FilterListerDialog(object):
    def setupUi(self, FilterListerDialog):
        FilterListerDialog.setObjectName("FilterListerDialog")
        FilterListerDialog.resize(550, 230)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FilterListerDialog.sizePolicy().hasHeightForWidth())
        FilterListerDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(FilterListerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filterLayout = QtWidgets.QVBoxLayout()
        self.filterLayout.setObjectName("filterLayout")
        self.verticalLayout.addLayout(self.filterLayout)
        self.frame = QtWidgets.QFrame(FilterListerDialog)
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
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(FilterListerDialog)
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
        self.test_result.setObjectName("test_result")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.test_result)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(FilterListerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FilterListerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), FilterListerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), FilterListerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FilterListerDialog)

    def retranslateUi(self, FilterListerDialog):
        FilterListerDialog.setWindowTitle(QtWidgets.QApplication.translate("FilterListerDialog", "Dialog", None, -1))
        self.testButton.setText(QtWidgets.QApplication.translate("FilterListerDialog", "Test", None, -1))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\brightway_dialog.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\brightway_dialog.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_BrightwayDialog(object):
    def setupUi(self, BrightwayDialog):
        BrightwayDialog.setObjectName("BrightwayDialog")
        BrightwayDialog.resize(374, 169)
        self.gridLayout = QtWidgets.QGridLayout(BrightwayDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(BrightwayDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.existingRadioButton = QtWidgets.QRadioButton(BrightwayDialog)
        self.existingRadioButton.setObjectName("existingRadioButton")
        self.horizontalLayout.addWidget(self.existingRadioButton)
        self.newRadioButton = QtWidgets.QRadioButton(BrightwayDialog)
        self.newRadioButton.setChecked(True)
        self.newRadioButton.setObjectName("newRadioButton")
        self.horizontalLayout.addWidget(self.newRadioButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(BrightwayDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(BrightwayDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.databaseLineEdit = QtWidgets.QLineEdit(BrightwayDialog)
        self.databaseLineEdit.setObjectName("databaseLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.databaseLineEdit)
        self.projectChoiceLayout = QtWidgets.QHBoxLayout()
        self.projectChoiceLayout.setObjectName("projectChoiceLayout")
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.projectChoiceLayout)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(BrightwayDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(BrightwayDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), BrightwayDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), BrightwayDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BrightwayDialog)

    def retranslateUi(self, BrightwayDialog):
        BrightwayDialog.setWindowTitle(QtWidgets.QApplication.translate("BrightwayDialog", "Export to Brightway", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("BrightwayDialog", "Choose a project and database to export to", None, -1))
        self.existingRadioButton.setText(QtWidgets.QApplication.translate("BrightwayDialog", "Existing project", None, -1))
        self.newRadioButton.setText(QtWidgets.QApplication.translate("BrightwayDialog", "New project", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("BrightwayDialog", "Project:  ", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("BrightwayDialog", "Database name:  ", None, -1))


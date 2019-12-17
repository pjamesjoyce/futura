# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\add_base_database.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\add_base_database.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddBaseDatabaseDialog(object):
    def setupUi(self, AddBaseDatabaseDialog):
        AddBaseDatabaseDialog.setObjectName("AddBaseDatabaseDialog")
        AddBaseDatabaseDialog.resize(528, 153)
        self.gridLayout = QtWidgets.QGridLayout(AddBaseDatabaseDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(AddBaseDatabaseDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(AddBaseDatabaseDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ecoinvent_version = QtWidgets.QComboBox(AddBaseDatabaseDialog)
        self.ecoinvent_version.setObjectName("ecoinvent_version")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ecoinvent_version)
        self.label_3 = QtWidgets.QLabel(AddBaseDatabaseDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.ecoinvent_system_model = QtWidgets.QComboBox(AddBaseDatabaseDialog)
        self.ecoinvent_system_model.setObjectName("ecoinvent_system_model")
        self.ecoinvent_system_model.addItem("")
        self.ecoinvent_system_model.addItem("")
        self.ecoinvent_system_model.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ecoinvent_system_model)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(AddBaseDatabaseDialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(AddBaseDatabaseDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddBaseDatabaseDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddBaseDatabaseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddBaseDatabaseDialog)

    def retranslateUi(self, AddBaseDatabaseDialog):
        AddBaseDatabaseDialog.setWindowTitle(QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Add base database", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Ecoinvent version", None, -1))
        self.ecoinvent_version.setItemText(0, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.6", None, -1))
        self.ecoinvent_version.setItemText(1, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.5", None, -1))
        self.ecoinvent_version.setItemText(2, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.4", None, -1))
        self.ecoinvent_version.setItemText(3, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.3", None, -1))
        self.ecoinvent_version.setItemText(4, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.2", None, -1))
        self.ecoinvent_version.setItemText(5, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.1", None, -1))
        self.ecoinvent_version.setItemText(6, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "3.01", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Ecoinvent system model", None, -1))
        self.ecoinvent_system_model.setItemText(0, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Cut-off", None, -1))
        self.ecoinvent_system_model.setItemText(1, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Allocation at the point of substitution (APOS)", None, -1))
        self.ecoinvent_system_model.setItemText(2, QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Consequential", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AddBaseDatabaseDialog", "Choose a version of the ecoinvent database to use as the base database", None, -1))


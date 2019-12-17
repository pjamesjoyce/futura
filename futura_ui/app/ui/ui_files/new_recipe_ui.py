# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\new_recipe.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\new_recipe.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NewRecipeDialog(object):
    def setupUi(self, NewRecipeDialog):
        NewRecipeDialog.setObjectName("NewRecipeDialog")
        NewRecipeDialog.resize(528, 284)
        self.gridLayout = QtWidgets.QGridLayout(NewRecipeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(NewRecipeDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.name = QtWidgets.QLineEdit(NewRecipeDialog)
        self.name.setObjectName("name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name)
        self.label_2 = QtWidgets.QLabel(NewRecipeDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(NewRecipeDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(NewRecipeDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.ecoinvent_version = QtWidgets.QComboBox(NewRecipeDialog)
        self.ecoinvent_version.setObjectName("ecoinvent_version")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.ecoinvent_version.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ecoinvent_version)
        self.ecoinvent_system_model = QtWidgets.QComboBox(NewRecipeDialog)
        self.ecoinvent_system_model.setObjectName("ecoinvent_system_model")
        self.ecoinvent_system_model.addItem("")
        self.ecoinvent_system_model.addItem("")
        self.ecoinvent_system_model.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ecoinvent_system_model)
        self.description = QtWidgets.QTextEdit(NewRecipeDialog)
        self.description.setObjectName("description")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.description)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewRecipeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NewRecipeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewRecipeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewRecipeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewRecipeDialog)

    def retranslateUi(self, NewRecipeDialog):
        NewRecipeDialog.setWindowTitle(QtWidgets.QApplication.translate("NewRecipeDialog", "Create New Recipe...", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("NewRecipeDialog", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("NewRecipeDialog", "Ecoinvent version", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("NewRecipeDialog", "Ecoinvent system model", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("NewRecipeDialog", "Description", None, -1))
        self.ecoinvent_version.setItemText(0, QtWidgets.QApplication.translate("NewRecipeDialog", "3.6", None, -1))
        self.ecoinvent_version.setItemText(1, QtWidgets.QApplication.translate("NewRecipeDialog", "3.5", None, -1))
        self.ecoinvent_version.setItemText(2, QtWidgets.QApplication.translate("NewRecipeDialog", "3.4", None, -1))
        self.ecoinvent_version.setItemText(3, QtWidgets.QApplication.translate("NewRecipeDialog", "3.3", None, -1))
        self.ecoinvent_version.setItemText(4, QtWidgets.QApplication.translate("NewRecipeDialog", "3.2", None, -1))
        self.ecoinvent_version.setItemText(5, QtWidgets.QApplication.translate("NewRecipeDialog", "3.1", None, -1))
        self.ecoinvent_version.setItemText(6, QtWidgets.QApplication.translate("NewRecipeDialog", "3.01", None, -1))
        self.ecoinvent_system_model.setItemText(0, QtWidgets.QApplication.translate("NewRecipeDialog", "Cut-off", None, -1))
        self.ecoinvent_system_model.setItemText(1, QtWidgets.QApplication.translate("NewRecipeDialog", "Allocation at the point of subsitution (APOS)", None, -1))
        self.ecoinvent_system_model.setItemText(2, QtWidgets.QApplication.translate("NewRecipeDialog", "Consequential", None, -1))


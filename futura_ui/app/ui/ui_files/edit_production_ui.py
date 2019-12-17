# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\edit_production.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\edit_production.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_EditProductionDialog(object):
    def setupUi(self, EditProductionDialog):
        EditProductionDialog.setObjectName("EditProductionDialog")
        EditProductionDialog.resize(376, 199)
        self.gridLayout = QtWidgets.QGridLayout(EditProductionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(EditProductionDialog)
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setMaximumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.nameLabel = QtWidgets.QLabel(EditProductionDialog)
        self.nameLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.nameLabel.setObjectName("nameLabel")
        self.verticalLayout.addWidget(self.nameLabel)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(EditProductionDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(EditProductionDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.currentValueLabel = QtWidgets.QLabel(EditProductionDialog)
        self.currentValueLabel.setObjectName("currentValueLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.currentValueLabel)
        self.newValueLineEdit = QtWidgets.QLineEdit(EditProductionDialog)
        self.newValueLineEdit.setObjectName("newValueLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.newValueLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditProductionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EditProductionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), EditProductionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), EditProductionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditProductionDialog)

    def retranslateUi(self, EditProductionDialog):
        EditProductionDialog.setWindowTitle(QtWidgets.QApplication.translate("EditProductionDialog", "Edit production volume", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("EditProductionDialog", "Edit Production Volume", None, -1))
        self.nameLabel.setText(QtWidgets.QApplication.translate("EditProductionDialog", "Not specified", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("EditProductionDialog", "Current value:  ", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("EditProductionDialog", "New value:  ", None, -1))
        self.currentValueLabel.setText(QtWidgets.QApplication.translate("EditProductionDialog", "0", None, -1))


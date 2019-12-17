# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\ecoinvent_dialog.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\ecoinvent_dialog.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_EcoinventDialog(object):
    def setupUi(self, EcoinventDialog):
        EcoinventDialog.setObjectName("EcoinventDialog")
        EcoinventDialog.resize(311, 177)
        self.gridLayout = QtWidgets.QGridLayout(EcoinventDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(EcoinventDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(EcoinventDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(EcoinventDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.usernameLineEdit = QtWidgets.QLineEdit(EcoinventDialog)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.usernameLineEdit)
        self.passwordLineEdit = QtWidgets.QLineEdit(EcoinventDialog)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordLineEdit)
        self.saveCheckBox = QtWidgets.QCheckBox(EcoinventDialog)
        self.saveCheckBox.setObjectName("saveCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.saveCheckBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EcoinventDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(EcoinventDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), EcoinventDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), EcoinventDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EcoinventDialog)

    def retranslateUi(self, EcoinventDialog):
        EcoinventDialog.setWindowTitle(QtWidgets.QApplication.translate("EcoinventDialog", "Dialog", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("EcoinventDialog", "Enter your ecoinvent.org login details", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("EcoinventDialog", "Username  ", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("EcoinventDialog", "Password  ", None, -1))
        self.saveCheckBox.setText(QtWidgets.QApplication.translate("EcoinventDialog", "Save my details", None, -1))


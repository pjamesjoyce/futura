# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\blank_dialog.ui',
# licensing of 'C:\Users\pjjoyce\Dropbox\00_My_Software\futura\futura_ui\app\ui\ui_files\blank_dialog.ui' applies.
#
# Created: Fri Dec 13 12:59:03 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_BlankDialog(object):
    def setupUi(self, BlankDialog):
        BlankDialog.setObjectName("BlankDialog")
        BlankDialog.resize(550, 230)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BlankDialog.sizePolicy().hasHeightForWidth())
        BlankDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(BlankDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.baseLayout = QtWidgets.QVBoxLayout()
        self.baseLayout.setObjectName("baseLayout")
        self.verticalLayout.addLayout(self.baseLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(BlankDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BlankDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), BlankDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), BlankDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BlankDialog)

    def retranslateUi(self, BlankDialog):
        BlankDialog.setWindowTitle(QtWidgets.QApplication.translate("BlankDialog", "Dialog", None, -1))


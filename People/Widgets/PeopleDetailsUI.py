# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PeopleDetailsUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PeopleDetailsUI(object):
    def setupUi(self, PeopleDetailsUI):
        PeopleDetailsUI.setObjectName("PeopleDetailsUI")
        PeopleDetailsUI.resize(295, 573)
        self.ThumbButton = QtWidgets.QToolButton(PeopleDetailsUI)
        self.ThumbButton.setGeometry(QtCore.QRect(20, 20, 160, 160))
        self.ThumbButton.setText("")
        self.ThumbButton.setIconSize(QtCore.QSize(128, 128))
        self.ThumbButton.setObjectName("ThumbButton")
        self.PeopleUuid = QtWidgets.QLineEdit(PeopleDetailsUI)
        self.PeopleUuid.setGeometry(QtCore.QRect(20, 180, 160, 28))
        self.PeopleUuid.setObjectName("PeopleUuid")
        self.Functions = QtWidgets.QComboBox(PeopleDetailsUI)
        self.Functions.setGeometry(QtCore.QRect(20, 208, 160, 28))
        self.Functions.setObjectName("Functions")
        self.Stacked = QtWidgets.QStackedWidget(PeopleDetailsUI)
        self.Stacked.setGeometry(QtCore.QRect(20, 240, 251, 311))
        self.Stacked.setObjectName("Stacked")

        self.retranslateUi(PeopleDetailsUI)
        self.PeopleUuid.editingFinished.connect(PeopleDetailsUI.PeopleUuidChanged)
        QtCore.QMetaObject.connectSlotsByName(PeopleDetailsUI)

    def retranslateUi(self, PeopleDetailsUI):
        _translate = QtCore.QCoreApplication.translate
        PeopleDetailsUI.setWindowTitle(_translate("PeopleDetailsUI", "人物詳細資訊"))

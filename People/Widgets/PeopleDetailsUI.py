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
        self.Stacked.setGeometry(QtCore.QRect(20, 236, 251, 311))
        self.Stacked.setObjectName("Stacked")
        self.Tables = QtWidgets.QToolButton(PeopleDetailsUI)
        self.Tables.setGeometry(QtCore.QRect(180, 20, 32, 32))
        self.Tables.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/tableproperties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Tables.setIcon(icon)
        self.Tables.setIconSize(QtCore.QSize(32, 32))
        self.Tables.setObjectName("Tables")
        self.FaceButton = QtWidgets.QToolButton(PeopleDetailsUI)
        self.FaceButton.setGeometry(QtCore.QRect(180, 52, 32, 32))
        self.FaceButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/android.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FaceButton.setIcon(icon1)
        self.FaceButton.setIconSize(QtCore.QSize(32, 32))
        self.FaceButton.setObjectName("FaceButton")

        self.retranslateUi(PeopleDetailsUI)
        self.PeopleUuid.editingFinished.connect(PeopleDetailsUI.PeopleUuidChanged)
        self.Tables.clicked.connect(PeopleDetailsUI.TablesEditing)
        self.FaceButton.clicked.connect(PeopleDetailsUI.FaceModel)
        QtCore.QMetaObject.connectSlotsByName(PeopleDetailsUI)

    def retranslateUi(self, PeopleDetailsUI):
        _translate = QtCore.QCoreApplication.translate
        PeopleDetailsUI.setWindowTitle(_translate("PeopleDetailsUI", "人物詳細資訊"))

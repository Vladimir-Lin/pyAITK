# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VtkModelPadUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VtkModelPadUi(object):
    def setupUi(self, VtkModelPadUi):
        VtkModelPadUi.setObjectName("VtkModelPadUi")
        VtkModelPadUi.resize(400, 300)
        self.label = QtWidgets.QLabel(VtkModelPadUi)
        self.label.setGeometry(QtCore.QRect(10, 10, 380, 16))
        self.label.setObjectName("label")

        self.retranslateUi(VtkModelPadUi)
        QtCore.QMetaObject.connectSlotsByName(VtkModelPadUi)

    def retranslateUi(self, VtkModelPadUi):
        _translate = QtCore.QCoreApplication.translate
        VtkModelPadUi.setWindowTitle(_translate("VtkModelPadUi", "三維模型控制板"))
        self.label.setText(_translate("VtkModelPadUi", "三維模型控制板"))
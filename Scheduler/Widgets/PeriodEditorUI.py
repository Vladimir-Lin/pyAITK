# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PeriodEditorUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PeriodEditorUI(object):
    def setupUi(self, PeriodEditorUI):
        PeriodEditorUI.setObjectName("PeriodEditorUI")
        PeriodEditorUI.resize(640, 560)
        PeriodEditorUI.setMinimumSize(QtCore.QSize(640, 560))
        PeriodEditorUI.setMaximumSize(QtCore.QSize(640, 560))
        self.NameLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.NameLabel.setGeometry(QtCore.QRect(20, 20, 100, 28))
        self.NameLabel.setObjectName("NameLabel")
        self.NameEditor = QtWidgets.QLineEdit(PeriodEditorUI)
        self.NameEditor.setGeometry(QtCore.QRect(120, 20, 500, 28))
        self.NameEditor.setAutoFillBackground(False)
        self.NameEditor.setFrame(True)
        self.NameEditor.setPlaceholderText("")
        self.NameEditor.setObjectName("NameEditor")
        self.TypeLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.TypeLabel.setGeometry(QtCore.QRect(20, 60, 100, 28))
        self.TypeLabel.setObjectName("TypeLabel")
        self.TypeBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.TypeBox.setGeometry(QtCore.QRect(120, 60, 120, 28))
        self.TypeBox.setEditable(False)
        self.TypeBox.setObjectName("TypeBox")
        self.UsageLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.UsageLabel.setGeometry(QtCore.QRect(250, 60, 80, 28))
        self.UsageLabel.setObjectName("UsageLabel")
        self.UsageBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.UsageBox.setGeometry(QtCore.QRect(330, 60, 100, 28))
        self.UsageBox.setObjectName("UsageBox")
        self.TimeZoneLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.TimeZoneLabel.setGeometry(QtCore.QRect(440, 60, 60, 28))
        self.TimeZoneLabel.setObjectName("TimeZoneLabel")
        self.TimeZoneBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.TimeZoneBox.setGeometry(QtCore.QRect(500, 60, 120, 28))
        self.TimeZoneBox.setEditable(True)
        self.TimeZoneBox.setObjectName("TimeZoneBox")
        self.StartLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.StartLabel.setGeometry(QtCore.QRect(20, 140, 100, 28))
        self.StartLabel.setObjectName("StartLabel")
        self.StartTime = QtWidgets.QDateTimeEdit(PeriodEditorUI)
        self.StartTime.setGeometry(QtCore.QRect(120, 140, 320, 28))
        self.StartTime.setCalendarPopup(True)
        self.StartTime.setObjectName("StartTime")
        self.FinishLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.FinishLabel.setGeometry(QtCore.QRect(20, 180, 100, 28))
        self.FinishLabel.setObjectName("FinishLabel")
        self.FinishTime = QtWidgets.QDateTimeEdit(PeriodEditorUI)
        self.FinishTime.setGeometry(QtCore.QRect(120, 180, 320, 28))
        self.FinishTime.setCalendarPopup(True)
        self.FinishTime.setObjectName("FinishTime")
        self.ItemLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.ItemLabel.setGeometry(QtCore.QRect(20, 100, 80, 28))
        self.ItemLabel.setObjectName("ItemLabel")
        self.ItemSpin = QtWidgets.QSpinBox(PeriodEditorUI)
        self.ItemSpin.setGeometry(QtCore.QRect(120, 100, 120, 28))
        self.ItemSpin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ItemSpin.setMaximum(999999999)
        self.ItemSpin.setProperty("value", 196833)
        self.ItemSpin.setObjectName("ItemSpin")
        self.StatesLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.StatesLabel.setGeometry(QtCore.QRect(250, 100, 80, 28))
        self.StatesLabel.setObjectName("StatesLabel")
        self.StatesBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.StatesBox.setGeometry(QtCore.QRect(330, 100, 100, 28))
        self.StatesBox.setObjectName("StatesBox")
        self.NoteLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.NoteLabel.setGeometry(QtCore.QRect(20, 220, 100, 28))
        self.NoteLabel.setObjectName("NoteLabel")
        self.NoteEdit = QtWidgets.QTextEdit(PeriodEditorUI)
        self.NoteEdit.setGeometry(QtCore.QRect(120, 220, 500, 160))
        self.NoteEdit.setObjectName("NoteEdit")
        self.FirstLine = QtWidgets.QFrame(PeriodEditorUI)
        self.FirstLine.setGeometry(QtCore.QRect(20, 390, 600, 3))
        self.FirstLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.FirstLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.FirstLine.setObjectName("FirstLine")
        self.Append = QtWidgets.QPushButton(PeriodEditorUI)
        self.Append.setGeometry(QtCore.QRect(20, 350, 80, 28))
        self.Append.setObjectName("Append")
        self.AppleLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.AppleLabel.setGeometry(QtCore.QRect(20, 400, 100, 28))
        self.AppleLabel.setObjectName("AppleLabel")
        self.AppleCalendarBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.AppleCalendarBox.setGeometry(QtCore.QRect(120, 400, 500, 28))
        self.AppleCalendarBox.setMaxVisibleItems(30)
        self.AppleCalendarBox.setObjectName("AppleCalendarBox")
        self.EventLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.EventLabel.setGeometry(QtCore.QRect(20, 440, 100, 28))
        self.EventLabel.setObjectName("EventLabel")
        self.AppleEventEdit = QtWidgets.QLineEdit(PeriodEditorUI)
        self.AppleEventEdit.setGeometry(QtCore.QRect(120, 440, 500, 28))
        self.AppleEventEdit.setReadOnly(False)
        self.AppleEventEdit.setObjectName("AppleEventEdit")
        self.SyncApple = QtWidgets.QPushButton(PeriodEditorUI)
        self.SyncApple.setGeometry(QtCore.QRect(120, 520, 160, 28))
        self.SyncApple.setObjectName("SyncApple")
        self.SyncFromApple = QtWidgets.QPushButton(PeriodEditorUI)
        self.SyncFromApple.setGeometry(QtCore.QRect(290, 520, 160, 28))
        self.SyncFromApple.setObjectName("SyncFromApple")
        self.AppleEventLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.AppleEventLabel.setGeometry(QtCore.QRect(20, 480, 100, 28))
        self.AppleEventLabel.setObjectName("AppleEventLabel")
        self.AppleEventBox = QtWidgets.QComboBox(PeriodEditorUI)
        self.AppleEventBox.setGeometry(QtCore.QRect(120, 480, 500, 28))
        self.AppleEventBox.setObjectName("AppleEventBox")
        self.PullAppleEvents = QtWidgets.QPushButton(PeriodEditorUI)
        self.PullAppleEvents.setGeometry(QtCore.QRect(460, 520, 160, 28))
        self.PullAppleEvents.setObjectName("PullAppleEvents")
        self.SaveNote = QtWidgets.QPushButton(PeriodEditorUI)
        self.SaveNote.setGeometry(QtCore.QRect(20, 260, 80, 28))
        self.SaveNote.setObjectName("SaveNote")
        self.ReportAll = QtWidgets.QPushButton(PeriodEditorUI)
        self.ReportAll.setGeometry(QtCore.QRect(20, 300, 80, 28))
        self.ReportAll.setObjectName("ReportAll")
        self.SetStartNow = QtWidgets.QPushButton(PeriodEditorUI)
        self.SetStartNow.setGeometry(QtCore.QRect(460, 140, 160, 28))
        self.SetStartNow.setObjectName("SetStartNow")
        self.SetFinishNow = QtWidgets.QPushButton(PeriodEditorUI)
        self.SetFinishNow.setGeometry(QtCore.QRect(460, 180, 160, 28))
        self.SetFinishNow.setObjectName("SetFinishNow")
        self.AlarmLabel = QtWidgets.QLabel(PeriodEditorUI)
        self.AlarmLabel.setGeometry(QtCore.QRect(440, 100, 60, 28))
        self.AlarmLabel.setObjectName("AlarmLabel")
        self.AlarmBox = QtWidgets.QSpinBox(PeriodEditorUI)
        self.AlarmBox.setGeometry(QtCore.QRect(500, 100, 120, 28))
        self.AlarmBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AlarmBox.setMaximum(999999999)
        self.AlarmBox.setProperty("value", 3)
        self.AlarmBox.setObjectName("AlarmBox")

        self.retranslateUi(PeriodEditorUI)
        self.NameEditor.editingFinished.connect(PeriodEditorUI.NameChanged)
        self.TypeBox.currentIndexChanged['int'].connect(PeriodEditorUI.TypeChanged)
        self.UsageBox.currentIndexChanged['int'].connect(PeriodEditorUI.UsageChanged)
        self.TimeZoneBox.currentIndexChanged['int'].connect(PeriodEditorUI.TimeZoneChanged)
        self.StartTime.editingFinished.connect(PeriodEditorUI.StartTimeChanged)
        self.FinishTime.editingFinished.connect(PeriodEditorUI.FinishTimeChanged)
        self.ItemSpin.editingFinished.connect(PeriodEditorUI.ItemChanged)
        self.StatesBox.currentIndexChanged['int'].connect(PeriodEditorUI.StatesChanged)
        self.Append.clicked.connect(PeriodEditorUI.AppendPeriod)
        self.AppleCalendarBox.currentIndexChanged['int'].connect(PeriodEditorUI.AppleCalendarChanged)
        self.AppleEventEdit.editingFinished.connect(PeriodEditorUI.AppleEventCidChanged)
        self.SyncApple.clicked.connect(PeriodEditorUI.SyncToApple)
        self.SyncFromApple.clicked.connect(PeriodEditorUI.SyncFromApple)
        self.AppleEventBox.currentIndexChanged['int'].connect(PeriodEditorUI.AssignAppleEvent)
        self.PullAppleEvents.clicked.connect(PeriodEditorUI.PullAppleEvents)
        self.SaveNote.clicked.connect(PeriodEditorUI.NoteChanged)
        self.ReportAll.clicked.connect(PeriodEditorUI.ReportAll)
        self.SetStartNow.clicked.connect(PeriodEditorUI.AssignStartTimeNow)
        self.SetFinishNow.clicked.connect(PeriodEditorUI.AssignFinishTimeNow)
        self.NoteEdit.textChanged.connect(PeriodEditorUI.NoteModified)
        QtCore.QMetaObject.connectSlotsByName(PeriodEditorUI)

    def retranslateUi(self, PeriodEditorUI):
        _translate = QtCore.QCoreApplication.translate
        PeriodEditorUI.setWindowTitle(_translate("PeriodEditorUI", "工作時段編輯器"))
        PeriodEditorUI.setToolTip(_translate("PeriodEditorUI", "工作時段編輯器"))
        PeriodEditorUI.setStatusTip(_translate("PeriodEditorUI", "工作時段編輯器"))
        PeriodEditorUI.setWhatsThis(_translate("PeriodEditorUI", "工作時段編輯器"))
        self.NameLabel.setText(_translate("PeriodEditorUI", "工時內容簡述："))
        self.NameEditor.setToolTip(_translate("PeriodEditorUI", "工作時段內容簡述"))
        self.NameEditor.setStatusTip(_translate("PeriodEditorUI", "工作時段內容簡述"))
        self.NameEditor.setWhatsThis(_translate("PeriodEditorUI", "工作時段內容簡述"))
        self.TypeLabel.setText(_translate("PeriodEditorUI", "時段類型："))
        self.UsageLabel.setText(_translate("PeriodEditorUI", "啟用狀態："))
        self.TimeZoneLabel.setText(_translate("PeriodEditorUI", "時區："))
        self.StartLabel.setText(_translate("PeriodEditorUI", "開始時間："))
        self.StartTime.setDisplayFormat(_translate("PeriodEditorUI", "yyyy/MM/dd HH:mm:ss"))
        self.FinishLabel.setText(_translate("PeriodEditorUI", "結束時間："))
        self.FinishTime.setDisplayFormat(_translate("PeriodEditorUI", "yyyy/MM/dd HH:mm:ss"))
        self.ItemLabel.setText(_translate("PeriodEditorUI", "使用種類："))
        self.StatesLabel.setText(_translate("PeriodEditorUI", "時段狀態："))
        self.NoteLabel.setText(_translate("PeriodEditorUI", "詳細內容："))
        self.NoteEdit.setToolTip(_translate("PeriodEditorUI", "詳細內容"))
        self.NoteEdit.setStatusTip(_translate("PeriodEditorUI", "詳細內容"))
        self.NoteEdit.setWhatsThis(_translate("PeriodEditorUI", "詳細內容"))
        self.Append.setText(_translate("PeriodEditorUI", "新增時段"))
        self.AppleLabel.setText(_translate("PeriodEditorUI", "蘋果行事曆："))
        self.EventLabel.setText(_translate("PeriodEditorUI", "事件編號："))
        self.SyncApple.setText(_translate("PeriodEditorUI", "同步到蘋果行事曆"))
        self.SyncFromApple.setText(_translate("PeriodEditorUI", "從蘋果行事曆同步"))
        self.AppleEventLabel.setText(_translate("PeriodEditorUI", "蘋果事件列表："))
        self.PullAppleEvents.setText(_translate("PeriodEditorUI", "由蘋果拉取事件"))
        self.SaveNote.setText(_translate("PeriodEditorUI", "儲存附記"))
        self.ReportAll.setText(_translate("PeriodEditorUI", "報告"))
        self.SetStartNow.setToolTip(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetStartNow.setStatusTip(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetStartNow.setWhatsThis(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetStartNow.setText(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetFinishNow.setToolTip(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetFinishNow.setStatusTip(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetFinishNow.setWhatsThis(_translate("PeriodEditorUI", "設定現在時間"))
        self.SetFinishNow.setText(_translate("PeriodEditorUI", "設定現在時間"))
        self.AlarmLabel.setText(_translate("PeriodEditorUI", "提醒："))
        self.AlarmBox.setToolTip(_translate("PeriodEditorUI", "提醒時間"))
        self.AlarmBox.setStatusTip(_translate("PeriodEditorUI", "提醒時間"))
        self.AlarmBox.setWhatsThis(_translate("PeriodEditorUI", "提醒時間"))
        self.AlarmBox.setSuffix(_translate("PeriodEditorUI", " 分鐘前"))
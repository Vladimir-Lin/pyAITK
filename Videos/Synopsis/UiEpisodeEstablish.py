# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EpisodeEstablish.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_EpisodeEstablish(object):
    def setupUi(self, EpisodeEstablish):
        if not EpisodeEstablish.objectName():
            EpisodeEstablish.setObjectName(u"EpisodeEstablish")
        EpisodeEstablish.resize(400, 120)
        EpisodeEstablish.setMinimumSize(QSize(400, 120))
        self.label = QLabel(EpisodeEstablish)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(12, 12, 380, 28))
        self.label.setAlignment(Qt.AlignCenter)
        self.Start = QPushButton(EpisodeEstablish)
        self.Start.setObjectName(u"Start")
        self.Start.setGeometry(QRect(40, 60, 140, 32))
        self.Close = QPushButton(EpisodeEstablish)
        self.Close.setObjectName(u"Close")
        self.Close.setGeometry(QRect(220, 60, 140, 32))

        self.retranslateUi(EpisodeEstablish)

        QMetaObject.connectSlotsByName(EpisodeEstablish)
    # setupUi

    def retranslateUi(self, EpisodeEstablish):
        EpisodeEstablish.setWindowTitle(QCoreApplication.translate("EpisodeEstablish", u"\u5efa\u7acb\u5f71\u96c6\u57fa\u672c\u8cc7\u8a0a", None))
#if QT_CONFIG(tooltip)
        EpisodeEstablish.setToolTip(QCoreApplication.translate("EpisodeEstablish", u"\u5efa\u7acb\u5f71\u96c6\u57fa\u672c\u8cc7\u8a0a", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        EpisodeEstablish.setStatusTip(QCoreApplication.translate("EpisodeEstablish", u"\u5efa\u7acb\u5f71\u96c6\u57fa\u672c\u8cc7\u8a0a", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        EpisodeEstablish.setWhatsThis(QCoreApplication.translate("EpisodeEstablish", u"\u5efa\u7acb\u5f71\u96c6\u57fa\u672c\u8cc7\u8a0a", None))
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("EpisodeEstablish", u"\u5f71\u96c6\u57fa\u672c\u8cc7\u8a0a\u5c1a\u672a\u5efa\u7acb\uff0c\u662f\u5426\u958b\u59cb\u9032\u884c\u76ee\u9304\u6383\u63cf\uff1f", None))
#if QT_CONFIG(tooltip)
        self.Start.setToolTip(QCoreApplication.translate("EpisodeEstablish", u"\u958b\u59cb\u5efa\u7acb\u5f71\u96c6\u8cc7\u8a0a", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.Start.setStatusTip(QCoreApplication.translate("EpisodeEstablish", u"\u958b\u59cb\u5efa\u7acb\u5f71\u96c6\u8cc7\u8a0a", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.Start.setWhatsThis(QCoreApplication.translate("EpisodeEstablish", u"\u958b\u59cb\u5efa\u7acb\u5f71\u96c6\u8cc7\u8a0a", None))
#endif // QT_CONFIG(whatsthis)
        self.Start.setText(QCoreApplication.translate("EpisodeEstablish", u"\u958b\u59cb\u5efa\u7acb", None))
#if QT_CONFIG(tooltip)
        self.Close.setToolTip(QCoreApplication.translate("EpisodeEstablish", u"\u95dc\u9589\u5f71\u96c6\u8cc7\u8a0a\u7de8\u8f2f\u8996\u7a97", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.Close.setStatusTip(QCoreApplication.translate("EpisodeEstablish", u"\u95dc\u9589\u5f71\u96c6\u8cc7\u8a0a\u7de8\u8f2f\u8996\u7a97", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.Close.setWhatsThis(QCoreApplication.translate("EpisodeEstablish", u"\u95dc\u9589\u5f71\u96c6\u8cc7\u8a0a\u7de8\u8f2f\u8996\u7a97", None))
#endif // QT_CONFIG(whatsthis)
        self.Close.setText(QCoreApplication.translate("EpisodeEstablish", u"\u95dc\u9589\u8996\u7a97", None))
    # retranslateUi


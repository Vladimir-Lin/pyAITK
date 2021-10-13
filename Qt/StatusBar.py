# -*- coding: utf-8 -*-
##############################################################################
## StatusBar
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QRect
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QStatusBar
##############################################################################
statusStyleSheet = \
"""QStatusBar { background-color: qlineargradient
(spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:0.0,
 stop:0 rgba(224,224,224,255),
 stop:1 rgba(240,240,240,255)) ; }"""
##############################################################################
class StatusBar                 ( QStatusBar                               ) :
  ############################################################################
  def __init__                  ( self , parent = None                     ) :
    ##########################################################################
    global statusStyleSheet
    ##########################################################################
    super ( ) . __init__        ( parent                                     )
    self      . setStyleSheet   ( statusStyleSheet                           )
    self      .  setAttribute   ( Qt . WA_InputMethodEnabled                 )
    ##########################################################################
    return
  ############################################################################
##############################################################################
"""

N::DragDropStatusBar:: DragDropStatusBar (QWidget * parent)
                     : QStatusBar        (          parent)
{
  nConnect ( this , SIGNAL ( pendMessage (QString,int) )   ,
             this , SLOT   ( showMessage (QString,int) ) ) ;
  setAcceptDrops ( true                      )             ;
  setStyleSheet  ( statusStyleSheet          )             ;
  setAttribute   ( Qt::WA_InputMethodEnabled )             ;
}

void N::DragDropStatusBar::dragEnterEvent(QDragEnterEvent *event)
{
  event->acceptProposedAction() ;
  Report ( event->mimeData()  ) ;
}

void N::DragDropStatusBar::dropEvent(QDropEvent *event)
{
  event->acceptProposedAction() ;
  Report ( event->mimeData()  ) ;
}

void N::DragDropStatusBar::Report(const QMimeData * mime)
{
  if (IsNull(mime)) return ;
  QStringList fm = mime->formats() ;
  bool done = false ;
  if (mime->hasImage()) {
     QString m ;
     QString u ;
     QString s ;
     QImage image = qvariant_cast<QImage>(mime->imageData());
     if (!image.isNull()) {
       m = QString("%1 x %2").arg(image.width()).arg(image.height()) ;
     };
     if (mime->hasUrls()) {
       QList<QUrl> urls = mime->urls() ;
       if (urls.count()>0) u = urls[0].toString() ;
     }
     if (u.length()>0) s = u ;
     if (m.length()>0) {
       if (s.length()>0) s = "[" + m + "] " + s ; else s = m ;
     };
     showMessage (s) ;
     done = true     ;
  } else
  if (mime->hasUrls()) {
    QList<QUrl> urls = mime->urls() ;
    if (urls.count()>0) {
      QString m = urls[0].toString() ;
      showMessage(m) ;
      done = true ;
    };
  }
  if (!done) showMessage(fm.join(";"));
}

void N::DragDropStatusBar::postMessage(const QString & message,int timeout)
{
  emit pendMessage ( message , timeout ) ;
}
"""

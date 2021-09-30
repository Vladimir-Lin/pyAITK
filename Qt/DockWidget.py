# -*- coding: utf-8 -*-
##############################################################################
## DockWidget
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
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QDockWidget
##############################################################################
from         . AbstractGui            import AbstractGui as AbstractGui
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
dockStyleSheet = \
"""QDockWidget::title
 { background-color:qlineargradient
 (spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:0.0,
 stop:0 rgba(216,216,216,255),
 stop:1 rgba(240,240,240,255)) ;
 text-align: center center }"""
##############################################################################
class DockWidget                ( QDockWidget , VirtualGui                 ) :
  ############################################################################
  def __init__                  ( self , parent = None                     ) :
    ##########################################################################
    global dockStyleSheet
    ##########################################################################
    super ( QDockWidget , self ) . __init__        ( parent                  )
    super ( VirtualGui  , self ) . __init__        (                         )
    super ( VirtualGui  , self ) . Initialize      ( self                    )
    super ( AbstractGui , self ) . setPlanFunction ( plan                    )
    ##########################################################################
    self . Regular      = True
    self . DockGeometry = QRect (                                            )
    ##########################################################################
    self . setStyleSheet        ( dockStyleSheet                             )
    self . setAttribute         ( Qt.WA_InputMethodEnabled                   )
    ##########################################################################
    return
  ############################################################################
  def event                              ( self , event                    ) :
    super ( QDockWidget , self ) . event (        event                      )
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    if                           ( not self . Regular                      ) :
      return DockGeometry . size (                                           )
    return super ( QDockWidget , self ) . sizeHint (                         )
##############################################################################

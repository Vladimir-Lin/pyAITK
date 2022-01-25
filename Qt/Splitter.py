# -*- coding: utf-8 -*-
##############################################################################
## Splitter
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
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QSplitter
##############################################################################
from         . VirtualGui             import VirtualGui     as VirtualGui
from         . SplitterHandle         import SplitterHandle as SplitterHandle
##############################################################################
class Splitter                             ( QSplitter , VirtualGui        ) :
  ############################################################################
  def __init__                             ( self                          , \
                                             orientation                   , \
                                             parent = None                 , \
                                             plan   = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( orientation , parent            )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . setAttribute                    ( Qt . WA_InputMethodEnabled      )
    self . Menus =                         {                                 }
    ##########################################################################
    return
  ############################################################################
  def createHandle                    ( self                               ) :
    ##########################################################################
    nsh = SplitterHandle              ( self . orientation ( )             , \
                                        self                               , \
                                        self . GetPlan     ( )               )
    nsh . Menus = self . Menus
    nsh . assignOrientation . connect ( self . assignOrientation             )
    ##########################################################################
    return nsh
  ############################################################################
  @pyqtSlot               ( int                                              )
  def assignOrientation   ( self , orientation                             ) :
    self . setOrientation ( orientation                                      )
    return
##############################################################################

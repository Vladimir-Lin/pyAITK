# -*- coding: utf-8 -*-
##############################################################################
## SpinBox
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QCheckBox
##############################################################################
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class CheckBox              ( QCheckBox , VirtualGui                       ) :
  ############################################################################
  UuidChanged = pyqtSignal  ( str , int                                      )
  ############################################################################
  def __init__              ( self , parent = None , plan = None           ) :
    ##########################################################################
    super ( QCheckBox   , self ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    ##########################################################################
    self . setAttribute     ( Qt . WA_InputMethodEnabled                     )
    ##########################################################################
    self . Uuid = 0
    ##########################################################################
    return
  ############################################################################
  def ConnectUuid                 ( self                                   ) :
    ##########################################################################
    self . stateChanged . connect ( self . alterUuidChanged                  )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (        int                                   )
  def alterUuidChanged        ( self , State                               ) :
    ##########################################################################
    self . UuidChanged . emit ( str ( self . Uuid ) , State                  )
    ##########################################################################
    return
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## VoiceTracker
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
from   opencc                          import OpenCC
from   googletrans                     import Translator
##############################################################################
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import pyqtSlot
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
from   PyQt5 . QtCore                  import QSize
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAbstractItemView
from   PyQt5 . QtWidgets               import QTreeWidget
from   PyQt5 . QtWidgets               import QTreeWidgetItem
from   PyQt5 . QtWidgets               import QLineEdit
from   PyQt5 . QtWidgets               import QComboBox
from   PyQt5 . QtWidgets               import QSpinBox
##############################################################################
from   AITK  . Qt . VirtualGui         import VirtualGui    as VirtualGui
from   AITK  . Qt . MenuManager        import MenuManager   as MenuManager
from   AITK  . Qt . AttachDock         import AttachDock    as AttachDock
from   AITK  . Qt . PlainTextEdit      import PlainTextEdit as PlainTextEdit
##############################################################################
class VoiceTracker        ( PlainTextEdit , AttachDock                     ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  attachNone = pyqtSignal ( QWidget                                          )
  attachDock = pyqtSignal ( QWidget , str , int , int                        )
  attachMdi  = pyqtSignal ( QWidget , int                                    )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
    ##########################################################################
    super ( ) . __init__  ( parent , plan                                    )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setFunction    ( self . FunctionDocking , True                    )
    self . setFunction    ( self . HavingMenu      , True                    )
    ##########################################################################
    return
  ############################################################################
  def sizeHint            ( self                                           ) :
    return QSize          ( 240 , 640                                        )
##############################################################################

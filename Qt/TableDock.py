# -*- coding: utf-8 -*-
##############################################################################
## TableDock
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
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTableWidget
from   PyQt5 . QtWidgets              import QTableWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . MenuManager            import MenuManager as MenuManager
from         . TableWidget            import TableWidget as TableWidget
from         . AttachDock             import AttachDock  as AttachDock
from         . LineEdit               import LineEdit    as LineEdit
from         . ComboBox               import ComboBox    as ComboBox
from         . SpinBox                import SpinBox     as SpinBox
##############################################################################
class TableDock               ( TableWidget , AttachDock                   ) :
  ############################################################################
  attachNone  = pyqtSignal    ( QWidget                                      )
  attachDock  = pyqtSignal    ( QWidget , str , int , int                    )
  attachMdi   = pyqtSignal    ( QWidget , int                                )
  emitRestart = pyqtSignal    (                                              )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    ## WidgetClass                                                       ;
    ##########################################################################
    self . ClassTag           = ""
    self . LoopRunning        = True
    self . FetchTableKey      = "Tables"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = None
    self . dockingPlaces      = None
    ## dockingPlace       ( Qt::RightDockWidgetArea     )
    ## dockingPlaces      ( Qt::TopDockWidgetArea       |
    ##                      Qt::BottomDockWidgetArea    |
    ##                      Qt::LeftDockWidgetArea      |
    ##                      Qt::RightDockWidgetArea     )
    ##########################################################################
    self . emitRestart . connect   ( self . restart                          )
    ##########################################################################
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  @pyqtSlot        (                                                         )
  def restart      ( self                                                  ) :
    ##########################################################################
    self . clear   (                                                         )
    self . startup (                                                         )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def AppendRefreshAction    ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Refresh"                                 ]
    icon = QIcon             ( ":/images/reload.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendInsertAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Insert"                                  ]
    icon = QIcon             ( ":/images/plus.png"                           )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendDeleteAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Delete"                                  ]
    icon = QIcon             ( ":/images/delete.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## GUI抽象介面
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
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Pair        import Pair
from   AITK . Database  . Columns     import Columns
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
##############################################################################
class AbstractGui        (                                                 ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    NOW                 = StarDate (                                         )
    NOW  . Now           (                                                   )
    ##########################################################################
    self . Locality        = 1002
    self . Prepared        = False
    self . DB              = { }
    self . Settings        = { }
    self . Translations    = { }
    self . Tables          = { }
    self . Gui             = None
    self . focusState      = False
    self . CreatedDateTime = NOW . Stardate
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def isPrepared         ( self                                            ) :
    return self . Prepared
  ############################################################################
  def setPrepared        ( self , prepared                                 ) :
    self . Prepared = prepared
    return self . Prepared
  ############################################################################
  def getLocality        ( self                                            ) :
    return self . Locality
  ############################################################################
  def setLocality        ( self , locality                                 ) :
    ##########################################################################
    self . Locality = locality
    ##########################################################################
    return self . Locality
  ############################################################################
  def Initialize         ( self , widget = None                            ) :
    ##########################################################################
    self . Gui          = widget
    ##########################################################################
    return
  ############################################################################
  def focusIn            ( self , event                                    ) :
    ##########################################################################
    if                   ( event . gotFocus ( )                            ) :
      if                 ( self  . FocusIn  ( )                            ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = True
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def focusOut           ( self , event                                    ) :
    ##########################################################################
    if                   ( event . lostFocus ( )                           ) :
      if                 ( self  . FocusOut  ( )                           ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = False
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def FocusIn                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def FocusOut                ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def ConnectDB          ( self                                            ) :
    ##########################################################################
    DB = Connection      (                                                   )
    if                   ( not DB . ConnectTo ( self . DB )                ) :
      return None
    DB . Prepare         (                                                   )
    ##########################################################################
    return DB
##############################################################################

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
class AbstractGui ( ) :
  ############################################################################
  def __init__ ( self ) :
    self . Locality    = 1002
    return
  ############################################################################
  def __del__ ( self ) :
    return
  ############################################################################
  def Initialize ( self , widget = None ) :
    self . Gui        = widget
    self . focusState = False
    return
  ############################################################################
  def focusIn ( self , event ) :
    if   ( event . gotFocus ( ) ) :
      if ( self  . FocusIn  ( ) ) :
        event    . accept   ( )
        self     . focusState = True
        return True
    return False
  ############################################################################
  def focusOut ( self , event ) :
    if   ( event . lostFocus ( ) ) :
      if ( self  . FocusOut  ( ) ) :
        event    . accept    ( )
        self     . focusState = False
        return True
    return False
  ############################################################################
  def FocusIn ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def FocusOut ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def setLocality ( self , locality ) :
    self . Locality = locality
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## ListWidget
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class ListWidget ( QListWidget , VirtualGui ) :
  ############################################################################
  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QListWidget , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    return
  ############################################################################
  def Configure ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QListWidget , self ) . focusInEvent ( event )
    return
  ############################################################################
  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QListWidget , self ) . focusOutEvent ( event )
    return
  ############################################################################
  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
      return
    super ( QListWidget , self ) . contextMenuEvent ( event )
    return
  ############################################################################
  def startup ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def FocusIn ( self ) :
    return True
  ############################################################################
  def FocusOut ( self ) :
    return True
  ############################################################################
  def removeParked ( self ) :
    return True
  ############################################################################
  def singleClicked ( self , item , column ) :
    raise NotImplementedError ( )
  ############################################################################
  def doubleClicked ( self , item , column ) :
    raise NotImplementedError ( )
  ############################################################################
  def Insert ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def Delete ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def Menu ( self , pos ) :
    raise NotImplementedError ( )
##############################################################################

# -*- coding: utf-8 -*-

##############################################################################
# QTreeWidget
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
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox

##############################################################################

from         . VirtualGui             import VirtualGui as VirtualGui

##############################################################################

class TreeWidget ( QTreeWidget , VirtualGui ) :

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QTreeWidget , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################

  ############################################################################

  def Configure ( self ) :
    raise NotImplementedError ( )

  ############################################################################

  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusInEvent ( event )
    return

  ############################################################################

  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusOutEvent ( event )
    return

  ############################################################################

  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
      return
    super ( QTreeWidget , self ) . contextMenuEvent ( event )
    return

  ############################################################################

  def setCentralLabels ( self , labels ) :
    it = QTreeWidgetItem ( labels )
    i  = 0
    for x in labels :
      it . setTextAlignment ( i , Qt . AlignCenter )
      i = i + 1
    self . setHeaderItem ( it )
    return it

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
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self . CurrentItem [ "Item"   ]
    column = self . CurrentItem [ "Column" ]
    self   . removeItemWidget ( item , column )
    self   . CurrentItem = { }
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

  ############################################################################

##############################################################################

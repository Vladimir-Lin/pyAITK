# -*- coding: utf-8 -*-

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

import Actions
from   Actions                        import *

##############################################################################

from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets

##############################################################################

from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF

##############################################################################

from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QKeySequence

##############################################################################

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
from   PyQt5 . QtWidgets              import QMdiArea
from   PyQt5 . QtWidgets              import QStackedWidget
from   PyQt5 . QtWidgets              import QMainWindow

##############################################################################

from         . VirtualGui             import VirtualGui

##############################################################################

class MainWindow ( QMainWindow , VirtualGui ) :

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QMainWindow , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    return

  ############################################################################

  def Configure ( self ) :
    self . stacked = QStackedWidget ( self                                   )
    self . mdi     = QMdiArea       ( self . stacked                         )
    self . stacked . addWidget      ( self . mdi                             )
    self . setCentralWidget         ( self . stacked                         )
    ##########################################################################
    return

  ############################################################################

  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QMainWindow , self ) . focusInEvent ( event )
    return

  ############################################################################

  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QMainWindow , self ) . focusOutEvent ( event )
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

  def addMdi                         ( self , widget , showOptions = 1 ) :
    subw = self . mdi . addSubWindow ( widget                            )
    subw . setAttribute              ( Qt . WA_DeleteOnClose             )
    return subw

  ############################################################################

##############################################################################

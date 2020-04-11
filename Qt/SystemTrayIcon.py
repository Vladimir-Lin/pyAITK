# -*- coding: utf-8 -*-

##############################################################################
# System Tray Icon GUI
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
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
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
from   PyQt5 . QtWidgets              import QSystemTrayIcon

##############################################################################

from         . VirtualGui             import VirtualGui
from         . MenuManager            import MenuManager

##############################################################################

class SystemTrayIcon ( QSystemTrayIcon , VirtualGui ) :

  ############################################################################

  def __init__ ( self , icon , parent = None ) :
    ##########################################################################
    QSystemTrayIcon . __init__ ( self , icon , parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    self . Configure ( parent )
    ##########################################################################

  ############################################################################

  def Configure ( self , parent ) :
    raise NotImplementedError ( )

  ############################################################################

##############################################################################

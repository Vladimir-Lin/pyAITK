# -*- coding: utf-8 -*-

##############################################################################
# GUI共同功能介面
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

##############################################################################

from         . AbstractGui            import AbstractGui as AbstractGui

##############################################################################

class VirtualGui               ( AbstractGui                               ) :
  ############################################################################

  ############################################################################
  def __init__                 ( self                                      ) :
    return
  ############################################################################
  def __del__                  ( self                                      ) :
    return
  ############################################################################
  def Initialize               ( self , widget = None                      ) :
    super ( AbstractGui , self ) . Initialize ( widget )
    return
  ############################################################################
  def setAllFont                    ( self , widget , font                 ) :
    ##########################################################################
    widget  . setFont               ( font                                   )
    ##########################################################################
    widgets = widget . findChildren ( QtWidgets . QWidget                    )
    for w in widgets                                                         :
      self . setAllFont             ( w , font                               )
    ##########################################################################
    return
  ############################################################################

  ############################################################################

  ############################################################################

  ############################################################################

##############################################################################

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
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class SpinBox               ( QSpinBox , VirtualGui                         ) :
  ############################################################################
  def __init__              ( self , parent = None , plan = None            ) :
    ##########################################################################
    super ( QSpinBox   , self ) . __init__   ( parent                        )
    super ( VirtualGui , self ) . __init__   (                               )
    super ( VirtualGui , self ) . Initialize ( self                          )
    ##########################################################################
    self . setAttribute     ( Qt . WA_InputMethodEnabled                     )
    ##########################################################################
    self . External = None
    ##########################################################################
    self . valueChanged . connect ( self . assignValue                       )
    ## self . timeout      . connect ( self . DropCommands                      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def DropCommands          ( self                                         ) :
    return
  ############################################################################
  @pyqtSlot(int)
  def assignValue           ( self , value                                 ) :
    ##########################################################################
    if                      ( self . External == None                      ) :
      return
    ##########################################################################
    self . External         ( value                                          )
    ##########################################################################
    return
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## Dialog
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
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QDialog
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class Dialog            ( QDialog , VirtualGui                             ) :
  ############################################################################
  def __init__          ( self , parent = None , plan = None               ) :
    ##########################################################################
    super ( QDialog    , self ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    ##########################################################################
    ## WidgetClass
    self . setAttribute ( Qt . WA_InputMethodEnabled                         )
    self . VoiceJSON = { }
    ##########################################################################
    if                  ( plan != None                                     ) :
      ## Data . Controller = & ( plan->canContinue ) ;
      pass
    ##########################################################################
    return
##############################################################################

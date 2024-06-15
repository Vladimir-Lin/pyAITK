# -*- coding: utf-8 -*-
##############################################################################
## DockWidget
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
import PySide6
from   PySide6              import QtCore
from   PySide6              import QtGui
from   PySide6              import QtWidgets
##############################################################################
from   PySide6 . QtCore     import *
from   PySide6 . QtGui      import *
from   PySide6 . QtWidgets  import *
##############################################################################
from           . VirtualGui import VirtualGui as VirtualGui
##############################################################################
dockStyleSheet = \
"""QDockWidget::title
 { background-color:qlineargradient
 (spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:0.0,
 stop:0 rgba(216,216,216,255),
 stop:1 rgba(240,240,240,255)) ;
 text-align: center center }"""
##############################################################################
class DockWidget                ( QDockWidget , VirtualGui                 ) :
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    global dockStyleSheet
    ##########################################################################
    super ( ) . __init__        ( parent                                     )
    ## super ( QDockWidget , self ) . __init__ ( parent                         )
    ## super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize           ( self                                       )
    self . setPlanFunction      ( plan                                       )
    ##########################################################################
    self . Regular      = True
    self . DockGeometry = QRect (                                            )
    ##########################################################################
    self . setStyleSheet        ( dockStyleSheet                             )
    self . setAttribute         ( Qt . WA_InputMethodEnabled                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    if                           ( not self . Regular                      ) :
      return DockGeometry . size (                                           )
    return super ( ) . sizeHint  (                                           )
##############################################################################

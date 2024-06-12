# -*- coding: utf-8 -*-
##############################################################################
## Splitter
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
from   PySide6                  import QtCore
from   PySide6                  import QtGui
from   PySide6                  import QtWidgets
##############################################################################
from   PySide6 . QtCore         import *
from   PySide6 . QtGui          import *
from   PySide6 . QtWidgets      import *
##############################################################################
from           . VirtualGui     import VirtualGui     as VirtualGui
from           . SplitterHandle import SplitterHandle as SplitterHandle
##############################################################################
class Splitter                             ( QSplitter , VirtualGui        ) :
  ############################################################################
  def __init__                             ( self                          , \
                                             orientation                   , \
                                             parent = None                 , \
                                             plan   = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( orientation , parent            )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . setAttribute                    ( Qt . WA_InputMethodEnabled      )
    self . Menus =                         {                                 }
    ##########################################################################
    return
  ############################################################################
  def createHandle                    ( self                               ) :
    ##########################################################################
    nsh = SplitterHandle              ( self . orientation ( )             , \
                                        self                               , \
                                        self . GetPlan     ( )               )
    nsh . Menus = self . Menus
    nsh . assignOrientation . connect ( self . assignOrientation             )
    ##########################################################################
    return nsh
  ############################################################################
  def assignOrientation   ( self , orientation                             ) :
    self . setOrientation ( orientation                                      )
    return
##############################################################################

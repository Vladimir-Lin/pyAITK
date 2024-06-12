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

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
class SpinBox           ( QSpinBox , VirtualGui                            ) :
  ############################################################################
  def __init__          ( self , parent = None , plan = None               ) :
    ##########################################################################
    super ( QSpinBox    , self ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    ##########################################################################
    self . setAttribute ( Qt . WA_InputMethodEnabled                         )
    ##########################################################################
    self . External = None
    ##########################################################################
    self . valueChanged . connect ( self . assignValue                       )
    ## self . timeout      . connect ( self . DropCommands                      )
    ##########################################################################
    return
  ############################################################################
  def DropCommands          ( self                                         ) :
    return
  ############################################################################
  def assignValue           ( self , value                                 ) :
    ##########################################################################
    if                      ( self . External == None                      ) :
      return
    ##########################################################################
    self . External         ( value                                          )
    ##########################################################################
    return
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## InputTreeWidget
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
from           . Widget     import Widget     as Widget
from           . TreeWidget import TreeWidget as TreeWidget
##############################################################################
class InputTreeWidget ( Widget                                             ) :
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super ( Widget     , self ) . __init__   ( parent , plan                 )
    ##########################################################################
    return
  ############################################################################
  def Prepare                   ( self                                     ) :
    ##########################################################################
    self . EditorHeight = 28
    self . combo = QComboBox    ( self                                       )
    self . line  = QLineEdit    ( self                                       )
    self . tree  = TreeWidget   ( self                                       )
    ##########################################################################
    self . combo . setLineEdit  ( self . line                                )
    ##########################################################################
    self . combo . move         ( 0 , 0                                      )
    self . tree  . move         ( 0 , self . EditorHeight                    )
    ##########################################################################
    self . Prepared    = True
    ##########################################################################
    return
  ############################################################################
  def Configure                 ( self                                     ) :
    raise NotImplementedError   (                                            )
  ############################################################################
  def resizeEvent               ( self , event                             ) :
    ##########################################################################
    QWidget . resizeEvent       ( self , event                               )
    ##########################################################################
    if                          ( not self . Prepared                      ) :
      return
    ##########################################################################
    w       = self  . width     (                                            )
    h       = self  . height    (                                            )
    ##########################################################################
    self    . combo . resize    ( w ,     self . EditorHeight                )
    self    . tree  . resize    ( w , h - self . EditorHeight                )
    ##########################################################################
    return
##############################################################################

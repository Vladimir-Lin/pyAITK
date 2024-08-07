# -*- coding: utf-8 -*-
##############################################################################
## VcfPoints
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
from   PySide6                                  import QtCore
from   PySide6                                  import QtGui
from   PySide6                                  import QtWidgets
##############################################################################
from   PySide6 . QtCore                         import *
from   PySide6 . QtGui                          import *
from   PySide6 . QtWidgets                      import *
##############################################################################
from   AITK    . Math . Geometry . ControlPoint import ControlPoint as ControlPoint
##############################################################################
from           . VcfPath                        import VcfPath      as VcfPath
##############################################################################
class VcfPoints                 ( VcfPath                                  ) :
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent , item , plan                       )
    self . setVcfPointsDefaults (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPointsDefaults ( self                                          ) :
    ##########################################################################
    self . points =        {                                                 }
    ##########################################################################
    self . setBrushColor   ( 1 , QColor ( 224 , 224 , 224 )                  )
    self . setBrushColor   ( 2 , QColor ( 255 , 144 , 144 )                  )
    ##########################################################################
    return
  ############################################################################
  def Painting          ( self , p , region , clip , color                 ) :
    ##########################################################################
    self . pushPainters ( p                                                  )
    ##########################################################################
    ##########################################################################
    self . popPainters  ( p                                                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare            ( self                                            ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################

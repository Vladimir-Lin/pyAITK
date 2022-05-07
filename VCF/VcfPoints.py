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
from   PyQt5                             import QtCore
from   PyQt5                             import QtGui
from   PyQt5                             import QtWidgets
##############################################################################
from   PyQt5 . QtCore                    import QObject
from   PyQt5 . QtCore                    import pyqtSignal
from   PyQt5 . QtCore                    import Qt
from   PyQt5 . QtCore                    import QPoint
from   PyQt5 . QtCore                    import QPointF
##############################################################################
from   PyQt5 . QtGui                     import QIcon
from   PyQt5 . QtGui                     import QCursor
from   PyQt5 . QtGui                     import QFont
from   PyQt5 . QtGui                     import QFontMetricsF
from   PyQt5 . QtGui                     import QColor
from   PyQt5 . QtGui                     import QPen
from   PyQt5 . QtGui                     import QBrush
from   PyQt5 . QtGui                     import QKeySequence
from   PyQt5 . QtGui                     import QPolygonF
##############################################################################
from   PyQt5 . QtWidgets                 import QApplication
from   PyQt5 . QtWidgets                 import qApp
from   PyQt5 . QtWidgets                 import QWidget
from   PyQt5 . QtWidgets                 import QGraphicsView
##############################################################################
from   AITK  . Math . Geometry . ControlPoint import ControlPoint as ControlPoint
##############################################################################
from         . VcfPath                   import VcfPath      as VcfPath
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

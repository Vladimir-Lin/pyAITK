# -*- coding: utf-8 -*-
##############################################################################
## VcfLines
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
from   AITK  . Math . Geometry . Contour import Contour      as Contour
##############################################################################
from         . VcfPath                   import VcfPath      as VcfPath
##############################################################################
class VcfLines                 ( VcfPath                                   ) :
  ############################################################################
  def __init__                 ( self                                      , \
                                 parent = None                             , \
                                 item   = None                             , \
                                 plan   = None                             ) :
    ##########################################################################
    super ( ) . __init__       ( parent , item , plan                        )
    self . setVcfLinesDefaults (                                             )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfLinesDefaults      ( self                                      ) :
    ##########################################################################
    self . contour = Contour   (                                             )
    self . lines   = QPolygonF (                                             )
    ##########################################################################
    self . setBrushColor       ( 1 , QColor ( 224 , 224 , 224 )              )
    self . setBrushColor       ( 2 , QColor ( 255 , 144 , 144 )              )
    ##########################################################################
    return
  ############################################################################
  def Painting          ( self , p , region , clip , color                 ) :
    ##########################################################################
    self . pushPainters ( p                                                  )
    ##########################################################################
    self . PaintPath    ( p , 1                                              )
    self . PaintLines   ( p , 3 , self . lines                               )
    self . PaintPath    ( p , 2                                              )
    ##########################################################################
    self . popPainters  ( p                                                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare            ( self , line = False , dot = False               ) :
    ##########################################################################
    self   . setLines    ( 1 , contour                                       )
    self   . EnablePath  ( 1 , True                                          )
    self   . ShowLines   ( line                                              )
    ##########################################################################
    if                   ( dot                                             ) :
      ########################################################################
      ## self . setPoints   ( 2 , contour                                       )
      self . EnablePath  ( 2 , True                                          )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . EnablePath  ( 2 , False                                         )
    ##########################################################################
    self   . MergePathes ( 0                                                 )
    ##########################################################################
    return
  ############################################################################
  def ShowLines                      ( self , line = False                 ) :
    ##########################################################################
    self   . lines . clear           (                                       )
    if                               ( line                                ) :
      pass
      ## self . lines = self . Polyline ( contour , contour . closed            )
    self   . update                  (                                       )
    ##########################################################################
    return
##############################################################################

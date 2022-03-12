# -*- coding: utf-8 -*-
##############################################################################
## VcfCursor
## 文字游標
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
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
from   PyQt5 . QtCore                 import QTimer
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
from         . VcfRectangle           import VcfRectangle as VcfRectangle
##############################################################################
class VcfCursor                 ( VcfRectangle                             ) :
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent , item , plan                       )
    self . setVcfCursorDefaults (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__           ( self                                             ) :
    ##########################################################################
    self . Timer . stop (                                                    )
    ##########################################################################
    return
  ############################################################################
  def setVcfCursorDefaults    ( self                                       ) :
    ##########################################################################
    self . Timer     = QTimer ( self . Gui                                   )
    self . Showing   = False
    self . Printable = False
    ##########################################################################
    self . Painter . addMap   ( "Default" , 0                                )
    self . Painter . addPen   ( 0 , QColor (   0 ,   0 , 255 )               )
    self . Painter . addBrush ( 0 , QColor ( 224 , 224 , 224 )               )
    ##########################################################################
    self . setFlag            ( QGraphicsItem . ItemIsSelectable , False     )
    self . setFlag            ( QGraphicsItem . ItemIsFocusable  , False     )
    ##########################################################################
    self . Timer . timeout . connect ( self . Twinkling                      )
    self . Timer . setInterval       ( 1000                                  )
    ##########################################################################
    return
  ############################################################################
  def setInterval              ( self , milliseconds                       ) :
    ##########################################################################
    self . Timer . setInterval (        milliseconds                         )
    ##########################################################################
    return
  ############################################################################
  def Start              ( self                                            ) :
    ##########################################################################
    self . Timer . start (                                                   )
    ##########################################################################
    return
  ############################################################################
  def Twinkling   ( self                                                   ) :
    ##########################################################################
    self . update (                                                          )
    ##########################################################################
    return
  ############################################################################
  def Painting                    ( self , p , region , clip , color       ) :
    ##########################################################################
    self . pushPainters           ( p                                        )
    ##########################################################################
    if                            ( self . Showing                         ) :
      ########################################################################
      self . Painter . setPainter ( p , "Default"                            )
      p    . drawRect             ( self . ScreenRect                        )
      ########################################################################
      self . Showing = False
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Showing = True
    ##########################################################################
    self . popPainters            ( p                                        )
    ##########################################################################
    return
##############################################################################

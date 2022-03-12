# -*- coding: utf-8 -*-
##############################################################################
## VcfPaperConf
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
##############################################################################
class VcfPaperConf    (                                                    ) :
  ############################################################################
  vpLeft   = 1
  vpTop    = 2
  vpRight  = 3
  vpBottom = 4
  ############################################################################
  def __init__         ( self                                              ) :
    ##########################################################################
    self . paper     = "A4"
    self . dpi       = 300.0
    self . paperX    = 1
    self . paperY    = 1
    self . direction = Qt . Vertical
    ## self . arrange   = Texts::TopLeftToTopRight
    self . arrange   = 0
    self . borders   = { 1 : 1.0 , 2 : 1.0 , 3 : 1.0 , 4 : 1.0               }
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def assign ( self , conf                                                 ) :
    ##########################################################################
    self . paper     = conf . paper
    self . borders   = conf . borders
    self . paperX    = conf . paperX
    self . paperY    = conf . paperY
    self . dpi       = conf . dpi
    self . direction = conf . direction
    self . arrange   = conf . arrange
    ##########################################################################
    return self
  ############################################################################
  def X ( self , page ) :
    ##########################################################################
    """
    switch (arrange)                   {
      case Texts::TopLeftToTopRight    :
      return   page % paperX           ;
      case Texts::TopLeftToBottomRight :
      return   page / paperY           ;
      case Texts::TopRightToTopLeft    :
      return -(page % paperX)          ;
      case Texts::TopRightToBottomLeft :
      return -(page / paperY)          ;
    }                                  ;
    """
    ##########################################################################
    return 0
  ############################################################################
  def Y ( self , page ) :
    ##########################################################################
    """
    switch (arrange)                   {
      case Texts::TopLeftToTopRight    :
      return   page / paperX           ;
      case Texts::TopLeftToBottomRight :
      return   page % paperY           ;
      case Texts::TopRightToTopLeft    :
      return -(page / paperX)          ;
      case Texts::TopRightToBottomLeft :
      return -(page % paperY)          ;
    }                                  ;
    """
    ##########################################################################
    return 0
  ############################################################################
  def PaperAt                ( self , page , PaperSize                     ) :
    ##########################################################################
    At = QRectF              (                                               )
    x  = self . X            ( page                                          )
    y  = self . Y            ( page                                          )
    ##########################################################################
    w  = PaperSize . width   (                                               )
    h  = PaperSize . height  (                                               )
    p  = PaperSize . topLeft (                                               )
    d  = QPointF             ( w * x , h * y                                 )
    p  = p + d
    ##########################################################################
    At . setTopLeft          ( p                                             )
    At . setWidth            ( w                                             )
    At . setHeight           ( h                                             )
    ##########################################################################
    return At
##############################################################################

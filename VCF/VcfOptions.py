# -*- coding: utf-8 -*-
##############################################################################
## VcfOptions
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
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
##############################################################################
from   PyQt5 . QtWidgets              import qApp
##############################################################################
class VcfOptions      (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    self . Initialize (                                                      )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Initialize               ( self                                      ) :
    ##########################################################################
    self . Private    = False
    self . ColorMode  = True
    self . Insert     = True
    self . LineSpace  = 0.025
    self . PictureDPI = 96.0
    self . PaperDPI   = 300.0
    self . ScaleRatio = QSizeF ( 1.0 , 1.0                                   )
    self . DPIX       = 96.0
    self . DPIY       = 96.0
    self . Fonts      = {                                                    }
    ##########################################################################
    screens           = qApp . screens (                                     )
    if                         ( len ( screens ) <= 0                      ) :
      return
    ##########################################################################
    s                 = screens                  [ 0                         ]
    self . DPIX       = s . physicalDotsPerInchX (                           )
    self . DPIY       = s . physicalDotsPerInchY (                           )
    ##########################################################################
    return
  ############################################################################
  def setOptions ( self , options                                          ) :
    ##########################################################################
    self . Private    = options . Private
    self . ColorMode  = options . ColorMode
    self . Insert     = options . Insert
    self . LineSpace  = options . LineSpace
    self . PictureDPI = options . PictureDPI
    self . PaperDPI   = options . PaperDPI
    self . ScaleRatio = options . ScaleRatio
    self . DPIX       = options . DPIX
    self . DPIY       = options . DPIY
    self . Fonts      = options . Fonts
    ##########################################################################
    return
  ############################################################################
  def cmToPixel   ( self , cm , DPI                                        ) :
    ##########################################################################
    x =     float ( cm                                                       )
    x = x * float ( DPI                                                      )
    x = x * 100.0
    x = x / 254.0
    ##########################################################################
    return x
  ############################################################################
  def pixelToCm   ( self , pixel , DPI                                     ) :
    ##########################################################################
    x =     float ( pixel                                                    )
    x = x * 254.0
    x = x / 100.0
    x = x / float ( DPI                                                      )
    ##########################################################################
    return x
  ############################################################################
  def imageToCm   ( self , pixel                                           ) :
    ##########################################################################
    x =     float ( pixel                                                    )
    x = x * 254.0
    x = x / 100.0
    x = x / float ( self . PictureDPI                                        )
    ##########################################################################
    return x
  ############################################################################
  ## Centimeter to Paper resolution
  ## cm * DPI * 100 / 254
  ############################################################################
  def Position                         ( self , cm                         ) :
    ##########################################################################
    x = self . cmToPixel               ( cm . x ( ) , self . DPIX            )
    x = x / self . ScaleRatio . width  (                                     )
    y = self . cmToPixel               ( cm . y ( ) , self . DPIY            )
    y = y / self . ScaleRatio . height (                                     )
    ##########################################################################
    return QPointF                     ( x , y                               )
  ############################################################################
  def Region            ( self , cm                                        ) :
    ##########################################################################
    S = QPointF         ( cm . left  ( ) , cm . top    ( )                   )
    W = QPointF         ( cm . width ( ) , cm . height ( )                   )
    S = self . Position ( S                                                  )
    W = self . Position ( W                                                  )
    ##########################################################################
    return QRectF       ( S . x ( ) , S . y ( ) , W . x ( ) , W . y ( )      )
  ############################################################################
  def toCM                             ( self , pixel                      ) :
    ##########################################################################
    x = self . pixelToCm               ( pixel . x ( ) , self . DPIX         )
    x = x * self . ScaleRatio . width  (                                     )
    y = self . pixelToCm               ( pixel . y ( ) , self . DPIY         )
    y = y * self . ScaleRatio . height (                                     )
    ##########################################################################
    return QPointF                     ( x , y                               )
  ############################################################################
  def toCmRegion    ( self , pixel                                         ) :
    ##########################################################################
    S = QPointF     ( pixel . left  ( ) , pixel . top    ( )                 )
    W = QPointF     ( pixel . width ( ) , pixel . height ( )                 )
    S = self . toCM ( S                                                      )
    W = self . toCM ( W                                                      )
    ##########################################################################
    return QRectF   ( S . x ( ) , S . y ( ) , W . x ( ) , W . y ( )          )
  ############################################################################
  def PictureToCm        ( self , size                                     ) :
    ##########################################################################
    x = self . imageToCm ( size . width  ( )                                 )
    y = self . imageToCm ( size . height ( )                                 )
    ##########################################################################
    return QPointF       ( x , y                                             )
  ############################################################################
  def PictureOnPaper        ( self , size                                  ) :
    ##########################################################################
    CM = self . PictureToCm ( size                                           )
    SS = self . Position    ( CM                                             )
    ##########################################################################
    return QSizeF           ( SS . x ( ) , SS . y ( )                        )
##############################################################################

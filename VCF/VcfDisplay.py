# -*- coding: utf-8 -*-
##############################################################################
## VcfDisplay
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
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QMargins
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsScene
from   PyQt5 . QtWidgets              import QDoubleSpinBox
##############################################################################
from         . VcfOptions             import VcfOptions
##############################################################################
class VcfDisplay             (                                             ) :
  ############################################################################
  def __init__               ( self                                        ) :
    return
  ############################################################################
  def __del__                ( self                                        ) :
    return
  ############################################################################
  def InitializeDisplay      ( self                                        ) :
    ##########################################################################
    self . Scene         = QGraphicsScene (                                  )
    self . Zooms         =                [                                  ]
    self . Options       = VcfOptions     (                                  )
    self . Margins       = QMargins       ( 0 , 0 , 3 , 3                    )
    self . Transform     = QTransform     (                                  )
    self . Inversion     = QTransform     (                                  )
    self . Transform     . reset          (                                  )
    self . Inversion     . reset          (                                  )
    self . Origin        = QPointF        ( 0 , 0                            )
    self . View          = QRectF         (                                  )
    self . MonitorFactor = 1.0
    self . ZoomFactor    = 1.0
    self . DPI           = 300.0
    self . DPIX          = self . Options . DPIX
    self . DPIY          = self . Options . DPIY
    ##########################################################################
    return
  ############################################################################
  def setOptions ( self , options                                          ) :
    ##########################################################################
    self . Options = options
    self . DPIX    = self . Options . DPIX
    self . DPIY    = self . Options . DPIY
    ##########################################################################
    return
  ############################################################################
  def Enlarge ( self                                                       ) :
    ##########################################################################
    self . ZoomFactor = self . FactorLevel ( self . ZoomFactor , True        )
    ##########################################################################
    return JSON
  ############################################################################
  def Shrink  ( self                                                       ) :
    ##########################################################################
    self . ZoomFactor = self . FactorLevel ( self . ZoomFactor , False       )
    ##########################################################################
    return
  ############################################################################
  def ZoomSpin                  ( self , parent , func                     ) :
    ##########################################################################
    ds = QDoubleSpinBox         (        parent                              )
    ds . setMinimum             (       0.01                                 )
    ds . setMaximum             ( 1000000.0                                  )
    ds . setValue               ( self . ZoomFactor * 100.0                  )
    ds . setSingleStep          ( 1.0                                        )
    ds . setSuffix              ( "%"                                        )
    ds . setAlignment           ( Qt . AlignRight | Qt . AlignVCenter        )
    ds . valueChanged . connect ( func                                       )
    ##########################################################################
    return ds
  ############################################################################
  def ZoomSpinChanged         ( self , value                               ) :
    ##########################################################################
    self . ZoomFactor = float ( value / 100                                  )
    ##########################################################################
    return
  ############################################################################
  def available   ( self , size                                            ) :
    ##########################################################################
    SW = self . Margins . left ( ) + self . Margins . right  ( )
    SH = self . Margins . top  ( ) + self . Margins . bottom ( )
    ##########################################################################
    return QSizeF ( size . width  ( ) - SW , size . height ( ) - SH          )
  ############################################################################
  def centimeter                   ( self , size                           ) :
    ##########################################################################
    w = self . Options . pixelToCm ( size . width  ( ) , self . DPIX         )
    h = self . Options . pixelToCm ( size . height ( ) , self . DPIY         )
    ##########################################################################
    return QSizeF                  ( w , h                                   )
  ############################################################################
  def toPaper                      ( self , cm                             ) :
    ##########################################################################
    x = self . Options . cmToPixel ( cm . width  ( ) , self . DPI            )
    y = self . Options . cmToPixel ( cm . height ( ) , self . DPI            )
    return QSizeF                  ( x , y                                   )
  ############################################################################
  def toRegion         ( self , cm                                         ) :
    ##########################################################################
    S = QSizeF         ( cm . left  ( ) , cm . top    ( )                    )
    W = QSizeF         ( cm . width ( ) , cm . height ( )                    )
    S = self . toPaper ( S                                                   )
    W = self . toPaper ( W                                                   )
    ##########################################################################
    return QRectF      ( S.width() , S.height() , W.width() , W.height()     )
  ############################################################################
  def pointToPaper        ( self , cm                                      ) :
    return self . toPaper (        cm                                        )
  ############################################################################
  def rectToPaper          ( self , region                                 ) :
    return self . toRegion (        region                                   )
  ############################################################################
  def polygonToPaper     ( self , polygon                                  ) :
    ##########################################################################
    R   = QPolygonF      (                                                   )
    ##########################################################################
    for v in polygon                                                         :
      ########################################################################
      z = self . toPaper ( v                                                 )
      R . append         ( z                                                 )
    ##########################################################################
    return R
  ############################################################################
  def asPaper                            ( self , size                     ) :
    ##########################################################################
    S      = size
    C      = self . centimeter           ( size                              )
    P      = self . toPaper              ( C                                 )
    self   . Transform . reset           (                                   )
    sx     = S . width  ( ) / P . width  (                                   )
    sy     = S . height ( ) / P . height (                                   )
    sx     = sx * self . ZoomFactor
    sy     = sy * self . ZoomFactor
    self   . Transform . scale           ( sx , sy                           )
    I , OK = self . Transform . inverted (                                   )
    self   . Inversion = I
    Z      = QPointF                     ( S . width ( ) , S . height ( )    )
    Z      = I . map                     ( Z                                 )
    ##########################################################################
    return QRectF                        ( 0 , 0 , Z . x ( ) , Z . y ( )     )
  ############################################################################
  def Percentage              ( self                                       ) :
    return "{:4.2f}" . format ( self . ZoomFactor * 100.0                    )
  ############################################################################
  def FactorLevel            ( self , Factor , Enlarge                     ) :
    ##########################################################################
    F         = int          ( Factor * 100.0                                )
    B         = False
    TOTAL     = len          ( self . Zooms                                  )
    AT        = 1
    ##########################################################################
    while                    ( AT < TOTAL                                  ) :
      ########################################################################
      if                     ( self . Zooms [ AT - 1 ] == F                ) :
        ######################################################################
        B     = True
        ######################################################################
        if                   ( Enlarge                                     ) :
          F   = self . Zooms [ AT                                            ]
        else                                                                 :
          ####################################################################
          if                 ( AT    > 1                                   ) :
            F = self . Zooms [ AT    - 2                                     ]
          else                                                               :
            F = self . Zooms [ 0                                             ]
        ######################################################################
      elif                   ( self . Zooms [ AT     ] == F                ) :
        ######################################################################
        B     = True
        ######################################################################
        if                   ( Enlarge                                     ) :
          if                 ( ( AT + 1 ) < TOTAL                          ) :
            F = self . Zooms [ AT    + 1                                     ]
          else                                                               :
            F = self . Zooms [ TOTAL - 1                                     ]
        else                                                                 :
          ####################################################################
          if                 ( AT    > 0                                   ) :
            F = self . Zooms [ AT    - 1                                     ]
          else                                                               :
            F = self . Zooms [ 0                                             ]
        ######################################################################
      elif ( self . Zooms [ AT - 1 ] < F ) and ( F < self . Zooms [ AT ] )   :
        ######################################################################
        B     = True
        ######################################################################
        if                   ( Enlarge                                     ) :
          F   = self . Zooms [ AT    + 1                                     ]
        else                                                                 :
          ####################################################################
          if                 ( AT    > 0                                   ) :
            F = self . Zooms [ AT    - 1                                     ]
          else                                                               :
            F = self . Zooms [ 0                                             ]
      ########################################################################
      AT = AT + 1
    ##########################################################################
    return float ( float ( F ) / 100.0 )
  ############################################################################
  def setDefaultZoom ( self                                                ) :
    ##########################################################################
    self . Zooms =   [    1 ,    2 ,    3 ,    4 ,    5 ,                    \
                          6 ,    7 ,    8 ,    9 ,   10 ,                    \
                         15 ,   20 ,   25 ,   30 ,   35 ,                    \
                         40 ,   45 ,   50 ,   55 ,   60 ,                    \
                         65 ,   70 ,   75 ,   80 ,   85 ,                    \
                         90 ,   95 ,  100 ,  110 ,  120 ,                    \
                        130 ,  140 ,  150 ,  160 ,  170 ,                    \
                        180 ,  190 ,  200 ,  300 ,  400 ,                    \
                        500 ,  600 ,  700 ,  800 ,  900 ,                    \
                       1000 , 1100 , 1200 , 1300 , 1400 ,                    \
                       1500 , 1600 , 1700 , 1800 , 1900 ,                    \
                       2000 , 2100 , 2200 , 2300 , 2400 ,                    \
                       2500 , 2600 , 2700 , 2800 , 2900 ,                    \
                       3000 , 3100 , 3200 , 3300 , 3400 ,                    \
                       3500 , 3600 , 3700 , 3800 , 3900 ,                    \
                       4000 , 4100 , 4200 , 4300 , 4400 ,                    \
                       4500 , 4600 , 4700 , 4800 , 4900 ,                    \
                       5000                                                  ]
    ##########################################################################
    return
##############################################################################

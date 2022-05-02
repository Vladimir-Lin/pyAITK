# -*- coding: utf-8 -*-
##############################################################################
## VcfTimeSelector
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
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPainterPath
from   PyQt5 . QtGui                  import QGradient
from   PyQt5 . QtGui                  import QLinearGradient
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsItem
##############################################################################
from   AITK  . Calendars  . StarDate  import StarDate  as StarDate
from   AITK  . Calendars  . Periode   import Periode   as Periode
##############################################################################
from   AITK  . VCF        . VcfCanvas import VcfCanvas as VcfCanvas
##############################################################################
class VcfTimeSelector         ( VcfCanvas                                  ) :
  ############################################################################
  def __init__                ( self                                       , \
                                parent = None                              , \
                                item   = None                              , \
                                plan   = None                              ) :
    ##########################################################################
    super ( ) . __init__      ( parent , item , plan                         )
    self . setVcfTssDefaults  (                                              )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfTssDefaults       ( self                                       ) :
    ##########################################################################
    self . Painter . addMap   ( "Default"  , 0                               )
    self . Painter . addMap   ( "Outdated" , 1                               )
    self . Painter . addMap   ( "Tracking" , 2                               )
    self . Painter . addPen   ( 0 , QColor (   0 , 255 ,   0 ,   0 )         )
    self . Painter . addBrush ( 0 , QColor ( 255 , 255 , 255 ,   0 )         )
    self . Painter . addPen   ( 1 , QColor (  32 , 128 , 255 , 192 )         )
    self . Painter . addBrush ( 1 , QColor ( 255 , 192 , 192 ,  32 )         )
    self . Painter . addPen   ( 2 , QColor ( 153 , 50  , 204 , 224 )         )
    self . Painter . addPen   ( 3 , QColor (   0 ,   0 ,   0 , 255 )         )
    self . Painter . addBrush ( 3 , QColor (   0 ,   0 ,   0 , 255 )         )
    ##########################################################################
    ## FNT  = self . Gui . font  (                                              )
    FNT  = QFont              (                                              )
    FNT  . setPixelSize       ( 48.0                                         )
    self . Painter . fonts [ 3 ] = FNT
    ##########################################################################
    self . setZValue          ( 10000000.0                                   )
    self . setOpacity         ( 1.0                                          )
    self . setPos             ( QPointF ( 0.0 , 0.0 )                        )
    ##########################################################################
    self . setFlag            ( QGraphicsItem . ItemIsMovable    , False     )
    self . setFlag            ( QGraphicsItem . ItemIsSelectable , False     )
    self . setFlag            ( QGraphicsItem . ItemIsFocusable  , False     )
    ##########################################################################
    self . Duration = Periode (                                              )
    self . Current  = 0
    self . TrackingPos = QPointF ( 0.0 , 0.0                                 )
    ##########################################################################
    self . MouseTracking = True
    self . CursorTime    = ""
    self . TimeZone      = "Asia/Taipei"
    ##########################################################################
    return
  ############################################################################
  def Painting                        ( self , p , region , clip , color   ) :
    ##########################################################################
    self . pushPainters               ( p                                    )
    ##########################################################################
    self . Painter . drawRect         ( p , "Default" , self . ScreenRect    )
    self . Painter . drawBorder       ( p , "Default" , self . ScreenRect    )
    self . DrawOutdated               (        p , region , clip , color     )
    self . DrawTracking               (        p , region , clip , color     )
    ##########################################################################
    self . popPainters                ( p                                    )
    ##########################################################################
    return
  ############################################################################
  def DrawOutdated                    ( self , p , region , clip , color   ) :
    ##########################################################################
    if ( self . Current <  self . Duration . Start )                         :
      return
    ##########################################################################
    if ( self . Current >= self . Duration . End                           ) :
      ########################################################################
      self . Painter . drawRect   ( p , "Outdated" , self . ScreenRect       )
      self . Painter . drawBorder ( p , "Outdated" , self . ScreenRect       )
      ########################################################################
      return
    ##########################################################################
    X      = self . ScreenRect . x      (                                    )
    Y      = self . ScreenRect . y      (                                    )
    W      = self . ScreenRect . width  (                                    )
    H      = self . ScreenRect . height (                                    )
    DS     = float                ( self . Current - self . Duration . Start )
    TT     = float                ( self . Duration . toDuration ( )         )
    W      = float                ( W * DS / TT                              )
    RT     = QRectF               ( X , Y , W , H                            )
    ##########################################################################
    self   . Painter . drawRect   ( p , "Outdated" , RT                      )
    self   . Painter . drawBorder ( p , "Outdated" , RT                      )
    ##########################################################################
    return
  ############################################################################
  def DrawTracking                      ( self , p , region , clip , color ) :
    ##########################################################################
    if                                  ( not self . MouseTracking         ) :
      return
    ##########################################################################
    X    = self . TrackingPos . x       (                                    )
    T    = self . ScreenRect  . top     (                                    )
    B    = self . ScreenRect  . bottom  (                                    )
    RP   = self . ScreenRect  . right   (                                    )
    RP   = float                        ( RP - 6.0                           )
    BP   = float                        ( B  - 6.0                           )
    ##########################################################################
    P1   = QPointF                      ( X  , T                             )
    P2   = QPointF                      ( X  , B                             )
    self . Painter . assignPainterPenId ( p  , 2                             )
    p    . drawLine                     ( P1 , P2                            )
    ##########################################################################
    RF   = self . Painter . boundingRect ( 3  , self . CursorTime            )
    FX   = self . TrackingPos . x       (                                    )
    FY   = self . TrackingPos . y       (                                    )
    FX   = float                        ( FX + 48.0                          )
    FY   = float                        ( FY + 60.0                          )
    FW   = RF . width                   (                                    )
    FH   = RF . height                  (                                    )
    FW   = float                        ( FW * 2                             )
    FH   = float                        ( FH * 2                             )
    FR   = float                        ( FX + FW                            )
    FB   = float                        ( FY + FH                            )
    if                                  ( FR > RP                          ) :
      FX = float                        ( FX - 52.0 - FW                     )
    if                                  ( FB > BP                          ) :
      FY = float                        ( FY - 64.0 - FH                     )
    PT   = QRectF                       ( FX , FY , FW , FH                  )
    ##########################################################################
    p    . setFont                      ( self . Painter . fonts [ 3 ]       )
    self . Painter . assignPainterId    ( p  , 3                             )
    p    . drawText                     ( PT , self . CursorTime             )
    ##########################################################################
    return
  ############################################################################
  def ViewChanged                            ( self , View , Update = True ) :
    ##########################################################################
    self   . ScreenRect = View
    self   . PaperRect  = self . rectToPaper ( View                          )
    ##########################################################################
    if                                       ( Update                      ) :
      self . prepareGeometryChange           (                               )
    ##########################################################################
    return
  ############################################################################
  def Hovering              ( self , pos                                   ) :
    ##########################################################################
    if                      ( not self . MouseTracking                     ) :
      return
    ##########################################################################
    self . UpdateCursorTime ( pos                                            )
    self . update           (                                                )
    ##########################################################################
    return
  ############################################################################
  def UpdateCursorTime                ( self , pos                         ) :
    ##########################################################################
    self . TrackingPos = pos
    ##########################################################################
    P    = pos . x                    (                                      )
    ##########################################################################
    X    = self . ScreenRect  . x     (                                      )
    W    = self . ScreenRect  . width (                                      )
    D    = float                      ( P - X                                )
    ##########################################################################
    if                                ( D > W                              ) :
      D  = W
    ##########################################################################
    TT   = float                      ( self . Duration . toDuration ( )     )
    DT   = int                        ( TT * D / W                           )
    DT   = int                        ( DT + self . Duration . Start         )
    ##########################################################################
    NOW  = StarDate                   (                                      )
    NOW  . Stardate   = DT
    CDT  = NOW . toDateTimeString     ( self . TimeZone                    , \
                                        " "                                , \
                                        "%Y/%m/%d"                         , \
                                        "%H:%M:%S"                           )
    self . CursorTime = CDT
    ##########################################################################
    return
  ############################################################################
  def setCurrent    ( self                                                 ) :
    ##########################################################################
    NOW  = StarDate (                                                        )
    NOW  . Now      (                                                        )
    self . Current = NOW . Stardate
    ##########################################################################
    return
  ############################################################################
  def setPeriod                ( self , START , FINAL                      ) :
    ##########################################################################
    self . Duration . Start = START
    self . Duration . End   = FINAL
    ##########################################################################
    return
##############################################################################

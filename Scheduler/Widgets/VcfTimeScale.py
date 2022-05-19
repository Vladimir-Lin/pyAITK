# -*- coding: utf-8 -*-
##############################################################################
## VcfTimeScale
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
from   AITK  . Calendars . StarDate   import StarDate  as StarDate
from   AITK  . Calendars . Periode    import Periode   as Periode
##############################################################################
from   AITK  . VCF       . VcfCanvas  import VcfCanvas as VcfCanvas
##############################################################################
class VcfTimeScale            ( VcfCanvas                                  ) :
  ############################################################################
  def __init__                ( self                                       , \
                                parent = None                              , \
                                item   = None                              , \
                                plan   = None                              ) :
    ##########################################################################
    super ( ) . __init__      ( parent , item , plan                         )
    self . setVcfTsDefaults   (                                              )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfTsDefaults           ( self                                    ) :
    ##########################################################################
    self . Scaling     = False
    ##########################################################################
    self . Gap         = QSizeF  ( 1.0  , 1.0                                )
    self . Dot         = QSizeF  ( 0.02 , 0.02                               )
    self . LineWidth   = QSizeF  ( 0.1  , 0.1                                )
    self . BackColor   = QColor  ( 240 , 240 , 240 , 255                     )
    self . ForeColor   = QColor  ( 128 , 255 ,   0 ,  64                     )
    self . CenterRatio = 0.85
    ##########################################################################
    self . setFlag               ( QGraphicsItem . ItemIsMovable , False     )
    self . setDirection          ( Qt . TopEdge                              )
    ##########################################################################
    self . setZValue             ( 10000.0                                   )
    self . setOpacity            ( 0.95                                      )
    ##########################################################################
    self . CurrentRect = QRectF  ( 0.0 , 0.0 , 0.0 , 0.0                     )
    self . Duration    = Periode (                                           )
    self . Current     = 0
    self . Base        = 0
    self . Gap         = 1
    self . TimeZone    = "Asia/Taipei"
    ##########################################################################
    return
  ############################################################################
  def GetGradient                      ( self , Color                      ) :
    ##########################################################################
    DARK = self . Painter . RatioColor ( Color , self . CenterRatio          )
    LG   = QLinearGradient             (                                     )
    LG   . setColorAt                  ( 0.0 , Color                         )
    LG   . setColorAt                  ( 0.5 , DARK                          )
    LG   . setColorAt                  ( 1.0 , Color                         )
    ##########################################################################
    return LG
  ############################################################################
  def setDirection              ( self , Mode                              ) :
    ##########################################################################
    self . Mode = Mode
    ##########################################################################
    self . Painter . addMap     ( "Default" , 0                              )
    self . Painter . addMap     ( "Current" , 1                              )
    self . Painter . addMap     ( "Grid"    , 2                              )
    ##########################################################################
    BC   = self . GetGradient   ( self . BackColor                           )
    FC   = self . GetGradient   ( self . ForeColor                           )
    self . Painter .addGradient ( 0 , BC                                     )
    self . Painter .addGradient ( 1 , FC                                     )
    ##########################################################################
    self . Painter . addPen     ( 0 , QColor ( 128 , 128 , 128 , 255 )       )
    self . Painter . addPen     ( 1 , QColor ( 255 , 192 ,   0 ,  64 )       )
    self . Painter . addPen     ( 2 , QColor (   0 ,  64 , 255 , 255 )       )
    self . Painter . addBrush   ( 0 , QColor ( 224 , 224 , 224 , 255 )       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItems                ( self                                   ) :
    ##########################################################################
    TL     = self . ScreenRect . topLeft     (                               )
    TR     = self . ScreenRect . topRight    (                               )
    BL     = self . ScreenRect . bottomLeft  (                               )
    BR     = self . ScreenRect . bottomRight (                               )
    ##########################################################################
    if                            ( self . Mode == Qt . TopEdge            ) :
      ########################################################################
      self . Painter . gradients [ 0 ] . setStart     ( TL                   )
      self . Painter . gradients [ 0 ] . setFinalStop ( BL                   )
      ########################################################################
    elif                          ( self . Mode == Qt . BottomEdge         ) :
      ########################################################################
      self . Painter . gradients [ 0 ] . setStart     ( TL                   )
      self . Painter . gradients [ 0 ] . setFinalStop ( BL                   )
      ########################################################################
    elif                          ( self . Mode == Qt . LeftEdge           ) :
      ########################################################################
      self . Painter . gradients [ 0 ] . setStart     ( TL                   )
      self . Painter . gradients [ 0 ] . setFinalStop ( TR                   )
      ########################################################################
    elif                          ( self . Mode == Qt . RightEdge          ) :
      ########################################################################
      self . Painter . gradients [ 0 ] . setStart     ( TL                   )
      self . Painter . gradients [ 0 ] . setFinalStop ( TR                   )
    ##########################################################################
    return
  ############################################################################
  def Painting                        ( self , p , region , clip , color   ) :
    ##########################################################################
    self . pushPainters               ( p                                    )
    ##########################################################################
    self . Painter . drawRectGradient ( p , "Default" , self . ScreenRect    )
    self . Painter . drawPainterPath  ( p , "Grid"                           )
    self . CurrentTimeBlock           (        p , region , clip , color     )
    ##########################################################################
    self . popPainters                ( p                                    )
    ##########################################################################
    return
  ############################################################################
  def CurrentTimeBlock                ( self , p , region , clip , color   ) :
    ##########################################################################
    if ( self . Current <  self . Duration . Start )                         :
      return
    ##########################################################################
    if ( self . Current >= self . Duration . End   )                         :
      ########################################################################
      CTB   = self . ScreenRect
      ########################################################################
    else                                                                     :
      ########################################################################
      START = self . Duration . Start
      END   = self . Duration . End
      TOTAL = float         ( END            - START                         )
      PASS  = float         ( self . Current - START                         )
      ########################################################################
      T     = self . ScreenRect . top    (                                   )
      H     = self . ScreenRect . height (                                   )
      L     = self . ScreenRect . left   (                                   )
      W     = self . ScreenRect . width  (                                   )
      W     = W * PASS / TOTAL
      ########################################################################
      CTB   = QRectF                     ( T , L , W , H                     )
    ##########################################################################
    self . Painter . drawRectGradient ( p , "Current" , CTB                  )
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
    self . Gap              = 1
    ##########################################################################
    NOW  = StarDate            (                                             )
    NOW  . Stardate = START
    SOD  = NOW  . SecondsOfDay ( self . TimeZone                             )
    self . Base = int          ( START - SOD                                 )
    ##########################################################################
    self . PrepareGrid         (                                             )
    ##########################################################################
    return
  ############################################################################
  def PrepareTopGrid60                    ( self , GRID                    ) :
    ##########################################################################
    START    = self . Duration . Start
    END      = self . Duration . End
    BASE     = self . Base
    GAP      = self . Gap
    AT       = START
    TOTAL    = float                      ( END - START                      )
    ##########################################################################
    B        = self . ScreenRect . bottom (                                  )
    H        = self . ScreenRect . height (                                  )
    H6       = float                      ( H / 6.0                          )
    U1       = float                      ( B - ( H6 * 1.4 )                 )
    U2       = float                      ( B - ( H6 * 2.0 )                 )
    U3       = float                      ( B - ( H6 * 2.6 )                 )
    U4       = float                      ( B - ( H6 * 3.2 )                 )
    U5       = float                      ( B - ( H6 * 4.0 )                 )
    L        = self . ScreenRect . left   (                                  )
    W        = self . ScreenRect . width  (                                  )
    ##########################################################################
    while                                 ( AT <= END                      ) :
      ########################################################################
      X      = float                      ( AT - START                       )
      X      = X * W / TOTAL
      ########################################################################
      E      = int                        ( AT - BASE                        )
      E      = int                        ( E  / GAP                         )
      ########################################################################
      if                                  ( ( E % 60 ) == 0                ) :
        GRID . moveTo                     ( X , U5                           )
      elif                                ( ( E % 30 ) == 0                ) :
        GRID . moveTo                     ( X , U4                           )
      elif                                ( ( E % 15 ) == 0                ) :
        GRID . moveTo                     ( X , U3                           )
      elif                                ( ( E %  5 ) == 0                ) :
        GRID . moveTo                     ( X , U2                           )
      else                                                                   :
        GRID . moveTo                     ( X , U1                           )
      ########################################################################
      GRID   . lineTo                     ( X , B                            )
      ########################################################################
      AT     = AT + GAP
    ##########################################################################
    return GRID
  ############################################################################
  def PrepareTopGrid               ( self , GRID                           ) :
    ##########################################################################
    GRID = self . PrepareTopGrid60 (        GRID                             )
    ##########################################################################
    return GRID
  ############################################################################
  def PrepareBottomGrid   ( self , GRID                                    ) :
    ##########################################################################
    ##########################################################################
    return GRID
  ############################################################################
  def PrepareLeftGrid     ( self , GRID                                    ) :
    ##########################################################################
    ##########################################################################
    return GRID
  ############################################################################
  def PrepareRightGrid    ( self , GRID                                    ) :
    ##########################################################################
    ##########################################################################
    return GRID
  ############################################################################
  def PrepareGrid                     ( self                               ) :
    ##########################################################################
    GRID   = QPainterPath             (                                      )
    ##########################################################################
    if                                ( self . Mode == Qt . TopEdge        ) :
      ########################################################################
      GRID = self . PrepareTopGrid    ( GRID                                 )
      ########################################################################
    elif                              ( self . Mode == Qt . BottomEdge     ) :
      ########################################################################
      GRID = self . PrepareBottomGrid ( GRID                                 )
      ########################################################################
    elif                              ( self . Mode == Qt . LeftEdge       ) :
      ########################################################################
      GRID = self . PrepareLeftGrid   ( GRID                                 )
      ########################################################################
    elif                              ( self . Mode == Qt . RightEdge      ) :
      ########################################################################
      GRID = self . PrepareRightGrid  ( GRID                                 )
    ##########################################################################
    self   . Painter . pathes [ 2 ] = GRID
    ##########################################################################
    return
##############################################################################

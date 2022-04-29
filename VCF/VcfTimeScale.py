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
from   AITK  . Calendars  . StarDate  import StarDate  as StarDate
from   AITK  . Calendars  . Periode   import Periode   as Periode
##############################################################################
from         . VcfCanvas              import VcfCanvas as VcfCanvas
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
    self . CurrentRect = QRectF  ( 0.0 , 0.0 , 0.0 , 0.0                     )
    self . Duration    = Periode (                                           )
    self . Current     = 0
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
    ## LG = QGradient ( QGradient . Blessing                         )
    ## LG = QGradient ( QGradient . FreshMilk                        )
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
    self . popPainters                ( p                                  )
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
  def setPeriod        ( self , START , FINAL , GAP                        ) :
    ##########################################################################
    self . Duration . Start = START
    self . Duration . End   = FINAL
    self . Gap              = GAP
    ##########################################################################
    self . PrepareGrid (                                                     )
    ##########################################################################
    return
  ############################################################################
  def PrepareGrid         ( self                                           ) :
    ##########################################################################
    PP    = QPainterPath  (                                                  )
    ##########################################################################
    START = self . Duration . Start
    END   = self . Duration . End
    GAP   = self . Gap
    AT    = START
    TOTAL = float         ( END - START                                      )
    ##########################################################################
    B     = self . ScreenRect . bottom (                                     )
    H     = self . ScreenRect . height (                                     )
    H4    = H / 4.0
    U     = B - H4
    L     = self . ScreenRect . left   (                                     )
    W     = self . ScreenRect . width  (                                     )
    ##########################################################################
    while                 ( AT <= END                                      ) :
      ########################################################################
      X   = float         ( AT - START                                       )
      X   = X * W / TOTAL
      ########################################################################
      PP  . moveTo        ( X , U                                            )
      PP  . lineTo        ( X , B                                            )
      ########################################################################
      AT = AT + GAP
    """
    QPointF G ( Gap . width () , Gap . height () ) ;
    QPointF D ( Dot . width () , Dot . height () ) ;
    QPointF GS = toPaper ( G )                     ;
    QPointF DT = toPaper ( D )                     ;
    QSizeF  DS (DT.x(),DT.y())                     ;
    QPointF DH = DT / 2                            ;
    QPointF BP(ScreenRect.left(),ScreenRect.top()) ;
    QPointF GP                                     ;
    do                                             {
      GP = BP - DH                                 ;
      p -> addEllipse ( QRectF ( GP , DS ) )       ;
      BP . setX ( BP . x ( ) + GS . x ( )  )       ;
      if ( BP . x () > ScreenRect . right () )     {
        BP . setX ( ScreenRect . left () )         ;
        BP . setY ( BP . y () + GS . y() )         ;
      }                                            ;
    } while (BP.x()<=ScreenRect.right ()          &&
             BP.y()<=ScreenRect.bottom()         ) ;
    """
    ##########################################################################
    self . Painter . pathes [ 2 ] = PP
    ##########################################################################
    return
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## VcfGanttPicker
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
from   PyQt5 . QtCore                    import QSize
from   PyQt5 . QtCore                    import QSizeF
from   PyQt5 . QtCore                    import QRect
from   PyQt5 . QtCore                    import QRectF
##############################################################################
from   PyQt5 . QtGui                     import QIcon
from   PyQt5 . QtGui                     import QCursor
from   PyQt5 . QtGui                     import QFont
from   PyQt5 . QtGui                     import QFontMetricsF
from   PyQt5 . QtGui                     import QColor
from   PyQt5 . QtGui                     import QPen
from   PyQt5 . QtGui                     import QBrush
from   PyQt5 . QtGui                     import QKeySequence
from   PyQt5 . QtGui                     import QPainterPath
from   PyQt5 . QtGui                     import QGradient
from   PyQt5 . QtGui                     import QLinearGradient
##############################################################################
from   PyQt5 . QtWidgets                 import QApplication
from   PyQt5 . QtWidgets                 import qApp
from   PyQt5 . QtWidgets                 import QWidget
from   PyQt5 . QtWidgets                 import QGraphicsView
from   PyQt5 . QtWidgets                 import QGraphicsItem
##############################################################################
from   AITK  . Calendars  . StarDate     import StarDate     as StarDate
from   AITK  . Calendars  . Periode      import Periode      as Periode
##############################################################################
from   AITK  . VCF        . VcfRectangle import VcfRectangle as VcfRectangle
from   AITK  . VCF        . VcfCanvas    import VcfCanvas    as VcfCanvas
from   AITK  . VCF        . VcfLabel     import VcfLabel     as VcfLabel
##############################################################################
from                      . VcfTimeScale import VcfTimeScale as VcfTimeScale
##############################################################################
class VcfGanttPicker              ( VcfCanvas                              ) :
  ############################################################################
  def __init__                    ( self                                   , \
                                    parent = None                          , \
                                    item   = None                          , \
                                    plan   = None                          ) :
    ##########################################################################
    super ( ) . __init__          ( parent , item , plan                     )
    self . setGanttPickerDefaults (                                          )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setGanttPickerDefaults    ( self                                     ) :
    ##########################################################################
    self . Painter . addMap     ( "Default"  , 0                             )
    self . Painter . addMap     ( "Outdated" , 1                             )
    self . Painter . addMap     ( "Tracking" , 2                             )
    self . Painter . addPen     ( 0 , QColor (   0 , 255 ,   0 ,   0 )       )
    self . Painter . addBrush   ( 0 , QColor ( 255 , 255 , 255 ,   0 )       )
    self . Painter . addPen     ( 1 , QColor (  32 , 128 , 255 , 192 )       )
    self . Painter . addBrush   ( 1 , QColor ( 255 , 192 , 192 ,  32 )       )
    self . Painter . addPen     ( 2 , QColor ( 153 , 50  , 204 , 224 )       )
    self . Painter . addPen     ( 3 , QColor (   0 ,   0 ,   0 , 255 )       )
    self . Painter . addBrush   ( 3 , QColor (   0 ,   0 ,   0 , 255 )       )
    ##########################################################################
    ## FNT  = self . Gui . font    (                                            )
    FNT  = QFont                (                                            )
    FNT  . setPixelSize         ( 48.0                                       )
    self . Painter . fonts [ 3 ] = FNT
    ##########################################################################
    self . setTimeTracking = None
    self . TZ              = "Asia/Taipei"
    self . Duration        = None
    self . Current         = 0
    self . ZDefault        = 10000.0
    self . ZAbove          = 0
    self . Picking         = False
    self . Ranges          =    { "First" : 0.0 , "Second" : 0.0             }
    self . Picked          =    { "Start" : 0   , "Finish" : 0               }
    self . setAcceptHoverEvents ( False                                      )
    ##########################################################################
    self . setZValue            ( self . ZDefault                            )
    self . setOpacity           ( 0.75                                       )
    self . setPos               ( QPointF ( 0.0 , 0.0 )                      )
    ##########################################################################
    self . setFlag              ( QGraphicsItem . ItemIsMovable    , False   )
    self . setFlag              ( QGraphicsItem . ItemIsSelectable , False   )
    self . setFlag              ( QGraphicsItem . ItemIsFocusable  , False   )
    ##########################################################################
    return
  ############################################################################
  def PrepareItems             ( self , gview                              ) :
    ##########################################################################
    self . Ranger = None
    self . Labels =            {                                             }
    ##########################################################################
    DTVR  = VcfCanvas          ( gview , None , self . PlanFunc              )
    DTVR  . setOptions         ( gview . Options , False                     )
    DTVR  . setRange           ( QRectF ( 5.0 , 1.25 , 3.0 , 1.2 )           )
    DTVR  . setZValue          ( 100.0                                       )
    DTVR  . setOpacity         ( 1.0                                         )
    DTVR  . setVisible         ( False                                       )
    ##########################################################################
    DTVR  . Mode    = 2
    DTVR  . Scaling = False
    ##########################################################################
    DTVR  . Painter . addPen   ( 0 , QColor ( 128 , 128 , 255 , 255 )        )
    DTVR  . Painter . addBrush ( 0 , QColor ( 224 , 224 , 255 , 255 )        )
    ##########################################################################
    DTVR  . setFlag            ( QGraphicsItem . ItemIsMovable    , False    )
    DTVR  . setFlag            ( QGraphicsItem . ItemIsSelectable , False    )
    DTVR  . setFlag            ( QGraphicsItem . ItemIsFocusable  , False    )
    ##########################################################################
    gview . addItem            ( DTVR , self                                 )
    gview . Scene   . addItem  ( DTVR                                        )
    ##########################################################################
    self . Ranger   = DTVR
    ##########################################################################
    LLBL  = VcfLabel           ( gview , None , self . PlanFunc              )
    LLBL  . setOptions         ( gview . Options , False                     )
    LLBL  . setRange           ( QRectF (  3.0 , 1.5 , 6.0 , 0.6 )           )
    LLBL  . setZValue          ( 200.0                                       )
    LLBL  . setOpacity         ( 1.0                                         )
    LLBL  . setVisible         ( False                                       )
    ##########################################################################
    LLBL  . Painter . addPen   ( 0 , QColor (  16 ,  16 ,  16 , 255 )        )
    LLBL  . Painter . addBrush ( 0 , QColor (  16 ,  16 ,  16 , 255 )        )
    ##########################################################################
    LLBL  . setFlag            ( QGraphicsItem . ItemIsMovable    , False    )
    LLBL  . setFlag            ( QGraphicsItem . ItemIsSelectable , False    )
    LLBL  . setFlag            ( QGraphicsItem . ItemIsFocusable  , False    )
    ##########################################################################
    FNT   = QFont              (                                             )
    FNT   . setPixelSize       ( 48.0                                        )
    LLBL  . Painter . fonts [ 0 ] = FNT
    ##########################################################################
    gview . addItem            ( LLBL , self                                 )
    gview . Scene   . addItem  ( LLBL                                        )
    ##########################################################################
    RLBL  = VcfLabel           ( gview , None , self . PlanFunc              )
    RLBL  . setOptions         ( gview . Options , False                     )
    RLBL  . setRange           ( QRectF ( 12.0 , 1.9 , 6.0 , 0.6 )           )
    RLBL  . setZValue          ( 200.0                                       )
    RLBL  . setOpacity         ( 1.0                                         )
    RLBL  . setVisible         ( False                                       )
    ##########################################################################
    RLBL  . Painter . addPen   ( 0 , QColor (  16 ,  16 ,  16 , 255 )        )
    RLBL  . Painter . addBrush ( 0 , QColor (  16 ,  16 ,  16 , 255 )        )
    ##########################################################################
    RLBL  . setFlag            ( QGraphicsItem . ItemIsMovable    , False    )
    RLBL  . setFlag            ( QGraphicsItem . ItemIsSelectable , False    )
    RLBL  . setFlag            ( QGraphicsItem . ItemIsFocusable  , False    )
    ##########################################################################
    FNT   = QFont              (                                             )
    FNT   . setPixelSize       ( 48.0                                        )
    RLBL  . Painter . fonts [ 0 ] = FNT
    ##########################################################################
    gview . addItem            ( RLBL , self                                 )
    gview . Scene   . addItem  ( RLBL                                        )
    ##########################################################################
    TLBL  = VcfLabel           ( gview , None , self . PlanFunc              )
    TLBL  . setOptions         ( gview . Options , False                     )
    TLBL  . setRange           ( QRectF ( 6.0 , 1.25 , 2.0 , 1.2 )           )
    TLBL  . setZValue          ( 300.0                                       )
    TLBL  . setOpacity         ( 1.0                                         )
    TLBL  . setVisible         ( False                                       )
    ##########################################################################
    TLBL  . Painter . addPen   ( 0 , QColor (   0 ,   0 , 255 , 255 )        )
    TLBL  . Painter . addBrush ( 0 , QColor (   0 ,   0 , 255 , 255 )        )
    ##########################################################################
    TLBL  . setFlag            ( QGraphicsItem . ItemIsMovable    , False    )
    TLBL  . setFlag            ( QGraphicsItem . ItemIsSelectable , False    )
    TLBL  . setFlag            ( QGraphicsItem . ItemIsFocusable  , False    )
    ##########################################################################
    FNT   = QFont              (                                             )
    FNT   . setPixelSize       ( 64.0                                        )
    TLBL  . Painter . fonts [ 0 ] = FNT
    ##########################################################################
    gview . addItem            ( TLBL , self                                 )
    gview . Scene   . addItem  ( TLBL                                        )
    ##########################################################################
    self . Labels [ "Left"  ] = LLBL
    self . Labels [ "Right" ] = RLBL
    self . Labels [ "Time"  ] = TLBL
    ##########################################################################
    return
  ############################################################################
  def Painting                        ( self , p , region , clip , color   ) :
    ##########################################################################
    self . pushPainters               ( p                                    )
    ##########################################################################
    self . Painter . drawRect         ( p , "Outdated" , self . ScreenRect   )
    ##########################################################################
    self . popPainters                ( p                                    )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent                 ( self , event                       ) :
    ##########################################################################
    OKAY      = self . IsMask         ( event.buttons ( ) , Qt.LeftButton    )
    if                                ( OKAY                               ) :
      ########################################################################
      if                              ( self . StartRange ( event )        ) :
        event     . accept            (                                      )
      else                                                                   :
        super ( ) . mousePressEvent   (        event                         )
      ########################################################################
      return
    ##########################################################################
    super     ( ) . mousePressEvent   (        event                         )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent                  ( self , event                       ) :
    ##########################################################################
    OKAY      = self . IsMask         ( event.buttons ( ) , Qt.LeftButton    )
    if                                ( OKAY                               ) :
      ########################################################################
      if                              ( self . MoveRange ( event )         ) :
        event     . accept            (                                      )
      else                                                                   :
        super ( ) . mouseMoveEvent    (        event                         )
      ########################################################################
      return
    ##########################################################################
    super     ( ) . mouseMoveEvent    (        event                         )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent           ( self , event                           ) :
    ##########################################################################
    if                            ( self . FinalRange ( event )            ) :
      event   . accept            (                                          )
      return
    ##########################################################################
    super ( ) . mouseReleaseEvent (        event                             )
    ##########################################################################
    return
  ############################################################################
  def StartRange                ( self , event                             ) :
    ##########################################################################
    self . Picking  = True
    self . Ranges [ "First"  ] = event . pos ( ) . x (                       )
    self . Ranges [ "Second" ] = event . pos ( ) . x (                       )
    self . setZValue            ( self . ZAbove                              )
    self . setAcceptHoverEvents ( True                                       )
    self . setCursor            ( Qt . SplitHCursor                          )
    self . setTimeTracking      ( False                                      )
    self . PrepareDuration      (                                            )
    ##########################################################################
    return True
  ############################################################################
  def MoveRange                 ( self , event                             ) :
    ##########################################################################
    if                          ( not self . Picking                       ) :
      return False
    ##########################################################################
    self . Ranges [ "Second" ] = event . pos ( ) . x (                       )
    self . MoveDuration         (                                            )
    ##########################################################################
    return True
  ############################################################################
  def FinalRange                ( self , event                             ) :
    ##########################################################################
    if                          ( not self . Picking                       ) :
      return False
    ##########################################################################
    self . Picking  = False
    self . Ranges [ "Second" ] = event . pos ( ) . x (                       )
    self . setZValue            ( self . ZDefault                            )
    self . setAcceptHoverEvents ( False                                      )
    self . setCursor            ( Qt . ArrowCursor                           )
    self . setTimeTracking      ( True                                       )
    self . FinalDuration        (                                            )
    ##########################################################################
    return True
  ############################################################################
  def PrepareDuration                      ( self                          ) :
    ##########################################################################
    self . MoveDuration                    (                                 )
    ##########################################################################
    self . Ranger             . setVisible ( True                            )
    self . Labels [ "Left"  ] . setVisible ( True                            )
    self . Labels [ "Right" ] . setVisible ( True                            )
    self . Labels [ "Time"  ] . setVisible ( True                            )
    ##########################################################################
    return
  ############################################################################
  def MoveDuration           ( self                                        ) :
    ##########################################################################
    PP   = self . PaperPos
    PR   = self . PaperRect
    SR   = self . ScreenRect
    TL   = PR   . topLeft    (                                               )
    SL   = SR   . left       (                                               )
    SW   = SR   . width      (                                               )
    PW   = PR   . width      (                                               )
    PH   = PR   . height     (                                               )
    ##########################################################################
    KK   = PP + TL
    HH   = float             ( PH - 0.3                                      )
    ##########################################################################
    P1   = self . Ranges     [ "First"                                       ]
    P2   = self . Ranges     [ "Second"                                      ]
    ##########################################################################
    if                       ( P1 > P2                                     ) :
      ########################################################################
      T  = P1
      P1 = P2
      P2 = T
    ##########################################################################
    D1   = float             ( float ( P1 - SL ) / SW                        )
    D2   = float             ( float ( P2 - SL ) / SW                        )
    YY   = float             ( KK . y ( ) + 0.15                             )
    XX   = float             ( D1 * PW                                       )
    W2   = float             ( D2 * PW                                       )
    WW   = float             ( W2 - XX                                       )
    ##########################################################################
    TBLK = QRectF            ( KK . x ( ) + XX , YY , WW , HH                )
    self . Ranger . setRange ( TBLK                                          )
    self . Ranger . prepareGeometryChange (                                  )
    self . Ranger . update   (                                               )
    ##########################################################################
    ST   = self . Duration . Start
    TD   = self . Duration . toDuration   (                                  )
    ##########################################################################
    T1   = int               ( float ( TD ) * D1                             )
    T2   = int               ( float ( TD ) * D2                             )
    ##########################################################################
    T1   = int               ( T1 + ST                                       )
    T2   = int               ( T2 + ST                                       )
    T1   = self . CalibrateTimeAlign ( T1                                    )
    T2   = self . CalibrateTimeAlign ( T2                                    )
    DT   = int               ( T2 - T1                                       )
    ##########################################################################
    self . Picked [ "Start"  ] = T1
    self . Picked [ "Finish" ] = T2
    ##########################################################################
    NOW  = StarDate          (                                               )
    TZ   = self . TZ
    ##########################################################################
    self . Labels [ "Time"  ] . setRange ( TBLK                              )
    self . Labels [ "Time"  ] . setText  ( self . TickToString ( DT )        )
    ##########################################################################
    NOW  . Stardate = T1
    DTX  = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"       )
    LLBL = self . Labels     [ "Left"                                        ]
    ##########################################################################
    LLBL . setText           ( DTX                                           )
    RR   = LLBL . Painter . boundingRect ( 0 , DTX                           )
    RR   = self . rectToPaper            ( RR                                )
    TW   = RR   . width      (                                               )
    TH   = RR   . height     (                                               )
    TW   = float             ( ( TW * 2 ) + 0.2                              )
    TH   = float             ( TH + 0.1                                      )
    XP   = float             ( XX - TW                                       )
    if                       ( XP < 0.1                                    ) :
      XP = 0.1
    LBLK = QRectF            ( KK . x ( ) + XP , YY , TW , TH                )
    LLBL . setRange          ( LBLK                                          )
    LLBL . prepareGeometryChange (                                           )
    LLBL . update            (                                               )
    ##########################################################################
    NOW  . Stardate = T2
    DTX  = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"       )
    RLBL = self . Labels     [ "Right"                                       ]
    ##########################################################################
    RLBL . setText           ( DTX                                           )
    RR   = RLBL . Painter . boundingRect ( 0 , DTX                           )
    RR   = self . rectToPaper            ( RR                                )
    TW   = RR   . width      (                                               )
    TH   = RR   . height     (                                               )
    TW   = float             ( ( TW * 2 ) + 0.2                              )
    TH   = float             ( TH + 0.1                                      )
    XP   = float             ( XX + WW + 0.2                                 )
    YP   = float             ( YY + 1.2 - TH                                 )
    if                       ( ( XP + TW + 0.1 ) > PW                      ) :
      XP = float             ( PW - TW - 0.1                                 )
    RBLK = QRectF            ( KK . x ( ) + XP , YP , TW , TH                )
    RLBL . setRange          ( RBLK                                          )
    RLBL . prepareGeometryChange (                                           )
    RLBL . update            (                                               )
    ##########################################################################
    return
  ############################################################################
  def FinalDuration                        ( self                          ) :
    ##########################################################################
    self . Ranger             . setVisible ( False                           )
    self . Labels [ "Left"  ] . setVisible ( False                           )
    self . Labels [ "Right" ] . setVisible ( False                           )
    self . Labels [ "Time"  ] . setVisible ( False                           )
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def CalibrateTimeAlign ( self , T                                        ) :
    ##########################################################################
    ##########################################################################
    return T
  ############################################################################
  def TickToString       ( self , DT                                       ) :
    ##########################################################################
    ##########################################################################
    return f"{DT} s"
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

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
from   PyQt5                               import QtCore
from   PyQt5                               import QtGui
from   PyQt5                               import QtWidgets
##############################################################################
from   PyQt5 . QtCore                      import QObject
from   PyQt5 . QtCore                      import pyqtSignal
from   PyQt5 . QtCore                      import Qt
from   PyQt5 . QtCore                      import QPoint
from   PyQt5 . QtCore                      import QPointF
from   PyQt5 . QtCore                      import QSize
from   PyQt5 . QtCore                      import QSizeF
from   PyQt5 . QtCore                      import QRect
from   PyQt5 . QtCore                      import QRectF
##############################################################################
from   PyQt5 . QtGui                       import QIcon
from   PyQt5 . QtGui                       import QCursor
from   PyQt5 . QtGui                       import QFont
from   PyQt5 . QtGui                       import QFontMetricsF
from   PyQt5 . QtGui                       import QColor
from   PyQt5 . QtGui                       import QPen
from   PyQt5 . QtGui                       import QBrush
from   PyQt5 . QtGui                       import QKeySequence
from   PyQt5 . QtGui                       import QPainterPath
from   PyQt5 . QtGui                       import QGradient
from   PyQt5 . QtGui                       import QLinearGradient
##############################################################################
from   PyQt5 . QtWidgets                   import QApplication
from   PyQt5 . QtWidgets                   import qApp
from   PyQt5 . QtWidgets                   import QWidget
from   PyQt5 . QtWidgets                   import QGraphicsView
from   PyQt5 . QtWidgets                   import QGraphicsItem
##############################################################################
from   AITK  . Qt . MenuManager            import MenuManager    as MenuManager
##############################################################################
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
##############################################################################
from   AITK  . VCF        . VcfRectangle   import VcfRectangle   as VcfRectangle
from   AITK  . VCF        . VcfCanvas      import VcfCanvas      as VcfCanvas
##############################################################################
from                      . VcfTimeScale   import VcfTimeScale   as VcfTimeScale
from                      . VcfDurationBar import VcfDurationBar as VcfDurationBar
from                      . VcfPeriodeBar  import VcfPeriodeBar  as VcfPeriodeBar
from                      . VcfGanttPicker import VcfGanttPicker as VcfGanttPicker
from                      . VcfGantt       import VcfGantt       as VcfGantt
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
    self . TimeScale     = None
    self . Picker        = None
    self . Gantt         = None
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
  def TimeScaleViewChanged ( self , View , Update = True                   ) :
    ##########################################################################
    if                     ( self . NotOkay ( self . TimeScale )           ) :
      return
    ##########################################################################
    XX   = self . TimeScale . ScreenRect . x      (                          )
    YY   = self . TimeScale . ScreenRect . y      (                          )
    WW   = View . width                           (                          )
    HH   = self . TimeScale . ScreenRect . height (                          )
    ##########################################################################
    SRV  = QRectF                                 ( XX , YY , WW , HH        )
    PRV  = self . TimeScale . rectToPaper         ( SRV                      )
    ##########################################################################
    self . TimeScale . ScreenRect = SRV
    self . TimeScale . PaperRect  = PRV
    self . TimeScale . PrepareGrid                (                          )
    ##########################################################################
    if                                            ( Update                 ) :
      self . TimeScale . prepareGeometryChange    (                          )
    ##########################################################################
    return
  ############################################################################
  def PickerViewChanged    ( self , View , Update = True                   ) :
    ##########################################################################
    if                     ( self . NotOkay ( self . Picker )              ) :
      return
    ##########################################################################
    XX   = self . Picker . ScreenRect . x      (                             )
    YY   = self . Picker . ScreenRect . y      (                             )
    WW   = View . width                        (                             )
    HH   = self . Picker . ScreenRect . height (                             )
    ##########################################################################
    SRV  = QRectF                              ( XX , YY , WW , HH           )
    PRV  = self . Picker . rectToPaper         ( SRV                         )
    ##########################################################################
    self . Picker . ScreenRect = SRV
    self . Picker . PaperRect  = PRV
    ## self . Picker . PrepareGrid                (                             )
    ##########################################################################
    if                                         ( Update                    ) :
      self . Picker . prepareGeometryChange    (                             )
    ##########################################################################
    return
  ############################################################################
  def GanttViewChanged     ( self , View , Update = True                   ) :
    ##########################################################################
    if                     ( self . NotOkay ( self . Gantt )               ) :
      return
    ##########################################################################
    XX   = self . Gantt . ScreenRect . x      (                              )
    YY   = self . Gantt . ScreenRect . y      (                              )
    WW   = View . width                       (                              )
    HH   = View . height                      (                              )
    PM   = self . paperToPoint                ( self . Gantt . PaperPos      )
    YP   = PM   . y                           (                              )
    ##########################################################################
    HH   = HH - YP - 4
    ##########################################################################
    SRV  = QRectF                             ( XX , YY , WW , HH            )
    PRV  = self . Gantt . rectToPaper         ( SRV                          )
    ##########################################################################
    self . Gantt . ScreenRect = SRV
    self . Gantt . PaperRect  = PRV
    ## self . Gantt . PrepareGrid                (                              )
    ##########################################################################
    if                                        ( Update                     ) :
      self . Gantt . prepareGeometryChange    (                              )
    ##########################################################################
    return
  ############################################################################
  def ViewChanged                            ( self , View , Update = True ) :
    ##########################################################################
    self   . ScreenRect = View
    self   . PaperRect  = self . rectToPaper (        View                   )
    ##########################################################################
    self   . TimeScaleViewChanged            (        View , Update          )
    self   . PickerViewChanged               (        View , Update          )
    self   . GanttViewChanged                (        View , Update          )
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
  def addTimeScale          ( self , gview                                 ) :
    ##########################################################################
    SDT   = self . Duration . Start
    EDT   = self . Duration . End
    ##########################################################################
    VTSI  = VcfTimeScale    ( gview , None , self . PlanFunc                 )
    VTSI  . setOptions      ( gview . Options , False                        )
    VTSI  . setRange        ( QRectF ( 0.0 , 0.0 , 0.1 , 1.0 )               )
    VTSI  . PrepareItems    (                                                )
    VTSI  . setPeriod       ( SDT , EDT                                      )
    VTSI  . setCurrent      (                                                )
    ##########################################################################
    VTSI  . Languages = self . Languages
    VTSI  . Menus     = self . Menus
    ##########################################################################
    gview . addItem         ( VTSI , self                                    )
    gview . Scene . addItem ( VTSI                                           )
    ##########################################################################
    self  . TimeScale = VTSI
    ##########################################################################
    return
  ############################################################################
  def addPicker             ( self , gview                                 ) :
    ##########################################################################
    VTSI  = VcfGanttPicker  ( gview , None , self . PlanFunc                 )
    VTSI  . setOptions      ( gview . Options , False                        )
    VTSI  . setRange        ( QRectF ( 0.0 , 1.1 , 0.1 , 1.5 )               )
    VTSI  . Duration = self . Duration
    VTSI  . ZAbove   = self . zValue ( ) + 10000.0
    VTSI  . setTimeTracking = self . setTimeTracking
    ##########################################################################
    VTSI  . Languages = self . Languages
    VTSI  . Menus     = self . Menus
    ##########################################################################
    gview . addItem         ( VTSI , self                                    )
    gview . Scene . addItem ( VTSI                                           )
    ##########################################################################
    VTSI  . PrepareItems    ( gview                                          )
    ##########################################################################
    self  . Picker = VTSI
    ##########################################################################
    return
  ############################################################################
  def addGantt              ( self , gview                                 ) :
    ##########################################################################
    VTSI  = VcfGantt        ( gview , None , self . PlanFunc                 )
    VTSI  . setOptions      ( gview . Options , False                        )
    VTSI  . setRange        ( QRectF ( 0.0 , 2.7 , 0.1 , 1.0 )               )
    ##########################################################################
    VTSI  . Languages = self . Languages
    VTSI  . Menus     = self . Menus
    ##########################################################################
    gview . addItem         ( VTSI , self                                    )
    gview . Scene . addItem ( VTSI                                           )
    ##########################################################################
    self  . Gantt = VTSI
    ##########################################################################
    return
  ############################################################################
  def addGadgets        ( self , gview                                     ) :
    ##########################################################################
    self . addTimeScale (        gview                                       )
    self . addPicker    (        gview                                       )
    self . addGantt     (        gview                                       )
    ##########################################################################
    return
  ############################################################################
  def setCurrent    ( self                                                 ) :
    ##########################################################################
    NOW  = StarDate (                                                        )
    NOW  . Now      (                                                        )
    self . Current = NOW . Stardate
    ##########################################################################
    if              ( self . IsOkay ( self . TimeScale )                   ) :
      ########################################################################
      self . TimeScale . Current = self . Current
    ##########################################################################
    if              ( self . IsOkay ( self . Picker    )                   ) :
      self . Picker . Current    = self . Current
    ##########################################################################
    return
  ############################################################################
  def setPeriod                ( self , START , FINAL                      ) :
    ##########################################################################
    self . Duration . Start = START
    self . Duration . End   = FINAL
    ##########################################################################
    return
  ############################################################################
  def setTimeTracking ( self , tracking                                    ) :
    ##########################################################################
    self . MouseTracking = tracking
    ##########################################################################
    return
  ############################################################################
  def TimeAlignMenu              ( self , mm                               ) :
    ##########################################################################
    msg     = self . getMenuItem ( "TimeAlignment"                           )
    LOM     = mm   . addMenu     ( msg                                       )
    ##########################################################################
    ENABLED =                    ( self . Picker . TimeAlignment == 0        )
    msg     = self . getMenuItem ( "Seconds"                                 )
    mm      . addActionFromMenu  ( LOM , 98439001 , msg , True , ENABLED     )
    ##########################################################################
    ENABLED =                    ( self . Picker . TimeAlignment == 1        )
    msg     = self . getMenuItem ( "Minutes"                                 )
    mm      . addActionFromMenu  ( LOM , 98439002 , msg , True , ENABLED     )
    ##########################################################################
    ENABLED =                    ( self . Picker . TimeAlignment == 2        )
    msg     = self . getMenuItem ( "Hours"                                   )
    mm      . addActionFromMenu  ( LOM , 98439003 , msg , True , ENABLED     )
    ##########################################################################
    ENABLED =                    ( self . Picker . TimeAlignment == 3        )
    msg     = self . getMenuItem ( "Days"                                    )
    mm      . addActionFromMenu  ( LOM , 98439004 , msg , True , ENABLED     )
    ##########################################################################
    return
  ############################################################################
  def RunTimeAlignMenu ( self , at                                         ) :
    ##########################################################################
    if                 ( ( at >= 98439001 ) and ( at <= 98439004 )         ) :
      ########################################################################
      self . Picker . TimeAlignment = int ( at - 98439001                    )
      ########################################################################
      return True
    ##########################################################################
    return True
  ############################################################################
  def Menu               ( self , gview , pos , spos                       ) :
    ##########################################################################
    mm   = MenuManager   ( gview                                             )
    ##########################################################################
    self . TimeAlignMenu ( mm                                                )
    ##########################################################################
    mm   . setFont       ( gview   . menuFont ( )                            )
    aa   = mm . exec_    ( QCursor . pos      ( )                            )
    at   = mm . at       ( aa                                                )
    ##########################################################################
    if                   ( self . RunTimeAlignMenu ( at )                  ) :
      return True
    ##########################################################################
    return True
##############################################################################

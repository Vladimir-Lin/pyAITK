# -*- coding: utf-8 -*-
##############################################################################
## VcfWidget
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
import vtk
##############################################################################
import PySide6
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
##############################################################################
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
##############################################################################
from   AITK    . Qt6 . VirtualGui      import VirtualGui   as VirtualGui
from   AITK    . Qt6 . AttachDock      import AttachDock   as AttachDock
##############################################################################
from   AITK    . Calendars  . StarDate import StarDate     as StarDate
from   AITK    . Calendars  . Periode  import Periode      as Periode
##############################################################################
from           . VcfFont               import VcfFont      as VcfFont
from           . VcfDisplay            import VcfDisplay   as VcfDisplay
from           . VcfOptions            import VcfOptions   as VcfOptions
from           . VcfManager            import VcfManager   as VcfManager
from           . VcfItem               import VcfItem      as VcfItem
from           . VcfRectangle          import VcfRectangle as VcfRectangle
from           . VcfCanvas             import VcfCanvas    as VcfCanvas
##############################################################################
class VcfWidget           ( QGraphicsView                                  , \
                            VirtualGui                                     , \
                            AttachDock                                     , \
                            VcfDisplay                                     , \
                            VcfManager                                     ) :
  ############################################################################
  attachNone         = Signal ( QWidget                                      )
  attachDock         = Signal ( QWidget , str , int , int                    )
  attachMdi          = Signal ( QWidget , int                                )
  emitMenuCaller     = Signal ( dict                                         )
  emitLog            = Signal ( str                                          )
  emitBustle         = Signal (                                              )
  emitVacancy        = Signal (                                              )
  OnBusy             = Signal (                                              )
  GoRelax            = Signal (                                              )
  emitGeometryChange = Signal ( QGraphicsItem                                )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    super ( AttachDock , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . InitializeDock                  ( plan                            )
    self . InitializeDisplay               (                                 )
    self . InitializeManager               ( self                            )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setAttribute          ( Qt . WA_InputMethodEnabled                )
    self . VoiceJSON =           {                                           }
    self . UiConf    =           {                                           }
    self . setDefaultZoom        (                                           )
    self . setScene              ( self . Scene                              )
    self . setRenderHint         ( QPainter . Antialiasing           , True  )
    self . setRenderHint         ( QPainter . TextAntialiasing       , True  )
    ## self . setRenderHint         ( QPainter . LosslessImageRendering , True  )
    ##########################################################################
    self . emitMenuCaller     . connect ( self . acceptMenuCaller            )
    self . emitBustle         . connect ( self . DoBustle                    )
    self . emitVacancy        . connect ( self . DoVacancy                   )
    self . OnBusy             . connect ( self . AtBusy                      )
    self . GoRelax            . connect ( self . OnRelax                     )
    self . emitGeometryChange . connect ( self . doGeometryChange            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 640 )                       )
  ############################################################################
  def focusInEvent            ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusIn ( event )                   ) :
      return
    ##########################################################################
    super ( ) . focusInEvent  ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusOut ( event )                  ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                 ( self                                       ) :
    return True
  ############################################################################
  def FocusOut                ( self                                       ) :
    return True
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def Relocation                    ( self                                 ) :
    return self . windowSizeChanged ( self . width  ( ) , self . height ( )  )
  ############################################################################
  def defaultCloseEvent      ( self , event                                ) :
    ##########################################################################
    if                       ( self . Shutdown ( )                         ) :
      super ( ) . closeEvent ( event                                         )
    else                                                                     :
      event     . ignore     (                                               )
    ##########################################################################
    return
  ############################################################################
  def Shutdown          ( self                                             ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def DockIn        ( self , shown                                         ) :
    ##########################################################################
    self . ShowDock (        shown                                           )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    ##########################################################################
    self . Visiblity (        visible                                        )
    ##########################################################################
    return
  ############################################################################
  def AtBusy           ( self                                              ) :
    ##########################################################################
    self . doStartBusy (                                                     )
    ##########################################################################
    return
  ############################################################################
  def OnRelax          ( self                                              ) :
    ##########################################################################
    self . doStopBusy  (                                                     )
    ##########################################################################
    return
  ############################################################################
  def DoBustle                ( self                                       ) :
    self . Bustle             (                                              )
    return
  ############################################################################
  def setBustle               ( self                                       ) :
    self . emitBustle  . emit (                                              )
    return
  ############################################################################
  def DoVacancy               ( self                                       ) :
    self . Vacancy            (                                              )
    return
  ############################################################################
  def setVacancy              ( self                                       ) :
    self . emitVacancy . emit (                                              )
    return
  ############################################################################
  def addLog              ( self , msg                                     ) :
    ##########################################################################
    self . emitLog . emit ( msg                                              )
    ##########################################################################
    return
  ############################################################################
  def doGeometryChange           ( self , ITEM                             ) :
    ##########################################################################
    ITEM . prepareGeometryChange (                                           )
    ##########################################################################
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu                    ( self , menu                         ) :
    ##########################################################################
    canDock = self . isFunction      ( self . FunctionDocking                )
    if                               ( not canDock                         ) :
      return
    ##########################################################################
    p       = self . parentWidget    (                                       )
    S       = False
    D       = False
    M       = False
    ##########################################################################
    if                               ( p == None                           ) :
      S     = True
    else                                                                     :
      ########################################################################
      if                             ( self . isDocking ( )                ) :
        D   = True
      else                                                                   :
        M   = True
    ##########################################################################
    menu    . addSeparator           (                                       )
    ##########################################################################
    if                               (     S or D                          ) :
      msg   = self . getLocalMessage ( self . AttachToMdi                    )
      menu  . addAction              ( self . AttachToMdi  , msg             )
    ##########################################################################
    if                               (     S or M                          ) :
      msg   = self . getLocalMessage ( self . AttachToDock                   )
      menu  . addAction              ( self . AttachToDock , msg             )
    ##########################################################################
    if                               ( not S                               ) :
      msg   = self . getLocalMessage ( self . AttachToNone                   )
      menu  . addAction              ( self . AttachToNone , msg             )
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == self . AttachToNone                 ) :
      self . attachNone . emit ( self                                        )
      return True
    ##########################################################################
    if                         ( at == self . AttachToMdi                  ) :
      self . attachMdi  . emit ( self , self . dockingOrientation            )
      return True
    ##########################################################################
    if                         ( at == self . AttachToDock                 ) :
      self . attachDock . emit ( self                                      , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  def AttachRatio                ( self , enabled                          ) :
    ##########################################################################
    msg     = self . getMenuItem ( "ViewRatioTip"                            )
    Ratio   = self . GetRatioBox (                                           )
    Ratio   . setEnabled         ( enabled                                   )
    Ratio   . setToolTip         ( msg                                       )
    ##########################################################################
    ics     = QMetaMethod . fromSignal ( Ratio . currentIndexChanged         )
    ##########################################################################
    if                           ( Ratio . isSignalConnected ( ics )       ) :
      ########################################################################
      Ratio . currentIndexChanged . disconnect (                             )
    ##########################################################################
    if                           ( enabled                                 ) :
      ########################################################################
      self  . UpdateRatioBox     (                                           )
      Ratio . currentIndexChanged . connect   ( self . ViewRatioChanged      )
    ##########################################################################
    return
  ############################################################################
  def UpdateRatioBox             ( self                                    ) :
    ##########################################################################
    AT      = -1
    ZF      = int                ( self . ZoomFactor * 100.0                 )
    Ratio   = self . GetRatioBox (                                           )
    Ratio   . blockSignals       ( True                                      )
    ##########################################################################
    for id in range              ( 0 , Ratio . count ( )                   ) :
      ########################################################################
      V     = Ratio . itemData   ( id                                        )
      V     = int                ( V                                         )
      ########################################################################
      if                         ( V == ZF                                 ) :
        AT  = id
    ##########################################################################
    if                           ( AT >= 0                                 ) :
      ########################################################################
      Ratio . setCurrentIndex    ( AT                                        )
    ##########################################################################
    Ratio   . blockSignals       ( False                                     )
    ##########################################################################
    return
  ############################################################################
  def ViewRatioChanged          ( self , index                             ) :
    ##########################################################################
    if                          ( index < 0                                ) :
      return
    ##########################################################################
    Ratio = self  . GetRatioBox (                                            )
    V     = Ratio . itemData    ( index                                      )
    V     = int                 ( V                                          )
    ZF    = float               ( float ( V ) / 100.0                        )
    self  . ZoomFactor = ZF
    ##########################################################################
    self  . Transform . reset   (                                            )
    self  . Transform = self . Transform . scale ( ZF , ZF                   )
    ##########################################################################
    self  . setTransform        ( self . Transform                           )
    self  . update              (                                            )
    ##########################################################################
    return
  ############################################################################
  def OriginalView           ( self                                        ) :
    ##########################################################################
    self . ZoomFactor = 1.0
    self . Transform . reset (                                               )
    self . setTransform      ( self . Transform                              )
    self . UpdateRatioBox    (                                               )
    self . update            (                                               )
    ##########################################################################
    return
  ############################################################################
  def ZoomIn                 ( self                                        ) :
    ##########################################################################
    self . Enlarge           (                                               )
    ##########################################################################
    self . Transform . reset (                                               )
    ZF   = self . ZoomFactor
    self . Transform = self . Transform . scale ( ZF , ZF                    )
    ##########################################################################
    self . setTransform      ( self . Transform                              )
    self . UpdateRatioBox    (                                               )
    self . update            (                                               )
    ##########################################################################
    return
  ############################################################################
  def ZoomOut                ( self                                        ) :
    ##########################################################################
    self . Shrink            (                                               )
    ##########################################################################
    self . Transform . reset (                                               )
    ZF   = self . ZoomFactor
    self . Transform = self . Transform . scale ( ZF , ZF                    )
    ##########################################################################
    self . setTransform      ( self . Transform                              )
    self . UpdateRatioBox    (                                               )
    self . update            (                                               )
    ##########################################################################
    return
  ############################################################################
  def WindowSizeView             ( self , size                             ) :
    ##########################################################################
    self . View = self . asPaper ( self . available ( size )                 )
    self . Scene . setSceneRect  ( self . View                               )
    self . setTransform          ( self . Transform                          )
    ##########################################################################
    return
  ############################################################################
  def PerfectView         ( self                                           ) :
    self . WindowSizeView ( self . size ( )                                  )
    return
  ############################################################################
  def windowSizeChanged   ( self , width , height                          ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . WindowSizeView ( QSizeF ( width , height )                        )
    ##########################################################################
    return True
  ############################################################################
  def acceptMenuCaller ( self , JSON                                       ) :
    ##########################################################################
    if                 ( "Item"     not in JSON                            ) :
      return
    ##########################################################################
    if                 ( "Position" not in JSON                            ) :
      return
    ##########################################################################
    item   = JSON      [ "Item"                                              ]
    pos    = JSON      [ "Position"                                          ]
    gpos   = item . mapToScene   (  pos                                      )
    spos   = self . mapFromScene ( gpos                                      )
    ##########################################################################
    Caller = getattr   ( item , "Menu" , None                                )
    if                 ( callable ( Caller )                               ) :
      Caller           ( self , pos , spos                                   )
    ##########################################################################
    return
  ############################################################################
  def MenuCallerEmitter          ( self , item , pos                       ) :
    ##########################################################################
    JSON =                       { "Item" : item , "Position" : pos          }
    self . emitMenuCaller . emit ( JSON                                      )
    ##########################################################################
    return
  ############################################################################
  def assignItemProperties   ( self , ITEM                                 ) :
    ##########################################################################
    ITEM . Initialize        ( self                                          )
    ITEM . setMenus          ( self . Menus                                  )
    ITEM . setLanguages      ( self . Languages                              )
    ##########################################################################
    ITEM . DB           = self . DB
    ITEM . Settings     = self . Settings
    ITEM . Translations = self . Translations
    ITEM . Tables       = self . Tables
    ##########################################################################
    return
  ############################################################################
  def startup                ( self                                        ) :
    ##########################################################################
    self . PerfectView       (                                               )
    PUID  = 3800400000000000042
    ## print(PUID)
    ##########################################################################
    VRIT  = VcfCanvas        ( self , None , self . PlanFunc                 )
    VRIT  . setOptions       ( self . Options , False                        )
    ## VRIT  . Mode = 1
    VRIT  . Mode = 2
    VRIT  . setRange         ( QRectF     ( 1.0 , 1.0 , 5.0 , 5.0 )          )
    ## VRIT  . Painter . addPen ( 0 , QColor ( 255 , 192 , 192       )          )
    VRIT  . Painter . addBrush ( 0 , QColor ( 255 , 240 , 240 )              )
    VRIT  . setMenuCaller    ( self . MenuCallerEmitter                      )
    VRIT  . setZValue        ( 10000                                         )
    VRIT  . setOpacity       ( 0.75                                          )
    ##########################################################################
    self  . addItem          ( VRIT                                          )
    self  . Scene . addItem  ( VRIT                                          )
    ##########################################################################
    self  . setPrepared      ( True                                          )
    ##########################################################################
    return
##############################################################################

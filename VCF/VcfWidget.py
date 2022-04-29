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
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QPainter
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
from   AITK  . Qt . VirtualGui        import VirtualGui   as VirtualGui
from   AITK  . Qt . AttachDock        import AttachDock   as AttachDock
##############################################################################
from   AITK  . Calendars  . StarDate  import StarDate     as StarDate
from   AITK  . Calendars  . Periode   import Periode      as Periode
##############################################################################
from         . VcfFont                import VcfFont      as VcfFont
from         . VcfDisplay             import VcfDisplay   as VcfDisplay
from         . VcfOptions             import VcfOptions   as VcfOptions
from         . VcfManager             import VcfManager   as VcfManager
from         . VcfItem                import VcfItem      as VcfItem
from         . VcfRectangle           import VcfRectangle as VcfRectangle
from         . VcfCanvas              import VcfCanvas    as VcfCanvas
from         . VcfTimeScale           import VcfTimeScale as VcfTimeScale
##############################################################################
class VcfWidget           ( QGraphicsView                                  , \
                            VirtualGui                                     , \
                            AttachDock                                     , \
                            VcfDisplay                                     , \
                            VcfManager                                     ) :
  ############################################################################
  attachNone     = pyqtSignal ( QWidget                                      )
  attachDock     = pyqtSignal ( QWidget , str , int , int                    )
  attachMdi      = pyqtSignal ( QWidget , int                                )
  emitMenuCaller = pyqtSignal ( dict                                         )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
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
    self . setDefaultZoom        (                                           )
    self . setScene              ( self . Scene                              )
    self . setRenderHint         ( QPainter . Antialiasing           , True  )
    self . setRenderHint         ( QPainter . TextAntialiasing       , True  )
    ## self . setRenderHint         ( QPainter . LosslessImageRendering , True  )
    ##########################################################################
    self . emitMenuCaller . connect ( self . acceptMenuCaller                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 640 )                       )
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
    NOW   = StarDate         (                                               )
    NOW   . Now              (                                               )
    SDT   = int              ( NOW . Stardate - 60                           )
    EDT   = int              ( SDT + 180                                     )
    ##########################################################################
    VTSI  = VcfTimeScale     ( self , None , self . PlanFunc                 )
    VTSI  . setOptions       ( self . Options , False                        )
    VTSI  . setRange         ( QRectF ( 0.0 , 0.0 , 30.0 , 1.0 )             )
    VTSI  . PrepareItems     (                                               )
    VTSI  . setMenuCaller    ( self . MenuCallerEmitter                      )
    VTSI  . setZValue        ( 1000                                          )
    VTSI  . setOpacity       ( 0.95                                          )
    ##########################################################################
    VTSI  . setPeriod        ( SDT , EDT , 1                                 )
    VTSI  . Duration . Start = SDT
    VTSI  . Duration . End   = EDT
    VTSI  . Current          = NOW . Stardate
    VTSI  . Gap              = 1
    ##########################################################################
    ##########################################################################
    self  . addItem          ( VTSI                                          )
    self  . Scene . addItem  ( VTSI                                          )
    ##########################################################################
    self  . setPrepared      ( True                                          )
    ##########################################################################
    return
##############################################################################

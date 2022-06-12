# -*- coding: utf-8 -*-
##############################################################################
## VcfProject
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
from   PyQt5 . QtCore                      import QTimer
##############################################################################
from   PyQt5 . QtGui                       import QIcon
from   PyQt5 . QtGui                       import QColor
from   PyQt5 . QtGui                       import QCursor
from   PyQt5 . QtGui                       import QKeySequence
from   PyQt5 . QtGui                       import QPen
from   PyQt5 . QtGui                       import QBrush
from   PyQt5 . QtGui                       import QPainter
##############################################################################
from   PyQt5 . QtWidgets                   import QApplication
from   PyQt5 . QtWidgets                   import qApp
from   PyQt5 . QtWidgets                   import QWidget
from   PyQt5 . QtWidgets                   import QGraphicsView
##############################################################################
from   AITK  . Qt        . VirtualGui      import VirtualGui      as VirtualGui
from   AITK  . Qt        . AttachDock      import AttachDock      as AttachDock
##############################################################################
from   AITK  . Calendars . StarDate        import StarDate        as StarDate
from   AITK  . Calendars . Periode         import Periode         as Periode
##############################################################################
from   AITK  . VCF       . VcfFont         import VcfFont         as VcfFont
from   AITK  . VCF       . VcfDisplay      import VcfDisplay      as VcfDisplay
from   AITK  . VCF       . VcfOptions      import VcfOptions      as VcfOptions
from   AITK  . VCF       . VcfManager      import VcfManager      as VcfManager
from   AITK  . VCF       . VcfItem         import VcfItem         as VcfItem
from   AITK  . VCF       . VcfRectangle    import VcfRectangle    as VcfRectangle
from   AITK  . VCF       . VcfCanvas       import VcfCanvas       as VcfCanvas
from   AITK  . VCF       . VcfWidget       import VcfWidget       as VcfWidget
##############################################################################
from                     . VcfDurationBar  import VcfDurationBar  as VcfDurationBar
from                     . VcfPeriodeBar   import VcfPeriodeBar   as VcfPeriodeBar
from                     . VcfGanttPicker  import VcfGanttPicker  as VcfGanttPicker
from                     . VcfGantt        import VcfGantt        as VcfGantt
from                     . VcfTimeScale    import VcfTimeScale    as VcfTimeScale
from                     . VcfTimeSelector import VcfTimeSelector as VcfTimeSelector
##############################################################################
class VcfProject                  ( VcfWidget                              ) :
  ############################################################################
  Adjustment   = pyqtSignal       ( QWidget , QSize                          )
  JsonCallback = pyqtSignal       ( dict                                     )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . setJsonCaller          ( self . JsonCaller                        )
    self . JsonCallback . connect ( self . JsonAccepter                      )
    ##########################################################################
    self . TimeSelector = None
    self . Tracker      = QTimer  ( self                                     )
    self . Tracker . setInterval  ( 1000                                     )
    self . Tracker . timeout . connect ( self . RefreshRegularly             )
    ##########################################################################
    return
  ############################################################################
  def __del__                 ( self                                       ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      if                      ( self . Tracker . isActive ( )              ) :
        self . Tracker . stop (                                              )
      ########################################################################
    except                                                                   :
      pass
    ##########################################################################
    return
  ############################################################################
  def JsonCaller               ( self , JSON                               ) :
    ##########################################################################
    self . JsonCallback . emit (        JSON                                 )
    ##########################################################################
    return
  ############################################################################
  def JsonAccepter                ( self , JSON                            ) :
    ##########################################################################
    CALLER = JSON                 [ "Function"                               ]
    ##########################################################################
    if                            ( CALLER == "DeleteItem"                 ) :
      ########################################################################
      ITEM   = JSON               [ "Item"                                   ]
      self   . takeItem           ( ITEM                                     )
      self   . Scene . removeItem ( ITEM                                     )
      ########################################################################
      return
    ##########################################################################
    if                            ( CALLER == "AppendItem"                 ) :
      ########################################################################
      ITEM   = JSON               [ "Item"                                   ]
      PARENT = JSON               [ "Parent"                                 ]
      self   . addItem            ( ITEM , PARENT                            )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def WindowSizeView             ( self , size                             ) :
    ##########################################################################
    self . View = self . asPaper ( self . available ( size )                 )
    self . Scene . setSceneRect  ( self . View                               )
    self . setTransform          ( self . Transform                          )
    ##########################################################################
    if                           ( self . IsOkay ( self . TimeSelector )   ) :
      self . TimeSelector . ViewChanged ( self . View                        )
    ##########################################################################
    return
  ############################################################################
  def RefreshRegularly      ( self                                         ) :
    ##########################################################################
    if                      ( self . IsOkay ( self . TimeSelector )        ) :
      ########################################################################
      self . TimeSelector . setCurrent            (                          )
      self . TimeSelector . prepareGeometryChange (                          )
    ##########################################################################
    return
  ############################################################################
  def addTimeScale             ( self , Selector                           ) :
    ##########################################################################
    SDT      = Selector . Duration . Start
    EDT      = Selector . Duration . End
    ##########################################################################
    VTSI     = VcfTimeScale    ( self , None , self . PlanFunc               )
    VTSI     . setOptions      ( self . Options , False                      )
    VTSI     . setRange        ( QRectF ( 0.0 , 0.0 , 0.1 , 1.0 )            )
    VTSI     . PrepareItems    (                                             )
    VTSI     . setPeriod       ( SDT , EDT                                   )
    VTSI     . setCurrent      (                                             )
    ## VTSI     . setMenuCaller ( self . MenuCallerEmitter                   )
    ##########################################################################
    self     . addItem         ( VTSI , Selector                             )
    self     . Scene . addItem ( VTSI                                        )
    ##########################################################################
    Selector . TimeScale = VTSI
    ##########################################################################
    return
  ############################################################################
  def addTimeSelector      ( self                                          ) :
    ##########################################################################
    VTS  = VcfTimeSelector ( self , None , self . PlanFunc                   )
    VTS  . setOptions      ( self . Options , False                          )
    VTS  . setRange        ( QRectF     ( 0.0 , 0.0 , 0.1 , 0.1 )            )
    VTS  . setMenuCaller   ( self . MenuCallerEmitter                        )
    ##########################################################################
    VTS  . Languages = self . Languages
    VTS  . Menus     = self . Menus
    ##########################################################################
    self . addItem         ( VTS                                             )
    self . Scene . addItem ( VTS                                             )
    ##########################################################################
    return VTS
  ############################################################################
  def startup                         ( self                               ) :
    ##########################################################################
    self . PerfectView                (                                      )
    ##########################################################################
    NOW  = StarDate                   (                                      )
    NOW  . Now                        (                                      )
    SDT  = int                        ( NOW . Stardate - 60                  )
    EDT  = int                        ( SDT + 600                            )
    ##########################################################################
    TSIW = self . addTimeSelector     (                                      )
    self . TimeSelector = TSIW
    self . TimeSelector . setPeriod   ( SDT , EDT                            )
    self . TimeSelector . setCurrent  (                                      )
    ## self . addTimeScale               ( TSIW                                 )
    self . TimeSelector . addGadgets  ( self                                 )
    ##########################################################################
    self . setPrepared                ( True                                 )
    ##########################################################################
    VW   = self . asPaper             ( self . available ( self . size ( ) ) )
    self . TimeSelector . ViewChanged ( self . View , False                  )
    ##########################################################################
    self . Tracker . start            (                                      )
    ##########################################################################
    return
##############################################################################

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
from   PyQt5                            import QtCore
from   PyQt5                            import QtGui
from   PyQt5                            import QtWidgets
##############################################################################
from   PyQt5 . QtCore                   import QObject
from   PyQt5 . QtCore                   import pyqtSignal
from   PyQt5 . QtCore                   import Qt
from   PyQt5 . QtCore                   import QPoint
from   PyQt5 . QtCore                   import QPointF
from   PyQt5 . QtCore                   import QSize
from   PyQt5 . QtCore                   import QSizeF
from   PyQt5 . QtCore                   import QRect
from   PyQt5 . QtCore                   import QRectF
##############################################################################
from   PyQt5 . QtGui                    import QIcon
from   PyQt5 . QtGui                    import QColor
from   PyQt5 . QtGui                    import QCursor
from   PyQt5 . QtGui                    import QKeySequence
from   PyQt5 . QtGui                    import QPen
from   PyQt5 . QtGui                    import QBrush
from   PyQt5 . QtGui                    import QPainter
##############################################################################
from   PyQt5 . QtWidgets                import QApplication
from   PyQt5 . QtWidgets                import qApp
from   PyQt5 . QtWidgets                import QWidget
from   PyQt5 . QtWidgets                import QGraphicsView
##############################################################################
from   AITK  . Qt        . VirtualGui   import VirtualGui   as VirtualGui
from   AITK  . Qt        . AttachDock   import AttachDock   as AttachDock
##############################################################################
from   AITK  . Calendars . StarDate     import StarDate     as StarDate
from   AITK  . Calendars . Periode      import Periode      as Periode
##############################################################################
from   AITK  . VCF       . VcfFont      import VcfFont      as VcfFont
from   AITK  . VCF       . VcfDisplay   import VcfDisplay   as VcfDisplay
from   AITK  . VCF       . VcfOptions   import VcfOptions   as VcfOptions
from   AITK  . VCF       . VcfManager   import VcfManager   as VcfManager
from   AITK  . VCF       . VcfItem      import VcfItem      as VcfItem
from   AITK  . VCF       . VcfRectangle import VcfRectangle as VcfRectangle
from   AITK  . VCF       . VcfCanvas    import VcfCanvas    as VcfCanvas
from   AITK  . VCF       . VcfWidget    import VcfWidget    as VcfWidget
##############################################################################
from                     . VcfTimeScale import VcfTimeScale as VcfTimeScale
##############################################################################
class VcfProject          ( VcfWidget                                      ) :
  ############################################################################
  attachNone     = pyqtSignal ( QWidget                                      )
  attachDock     = pyqtSignal ( QWidget , str , int , int                    )
  attachMdi      = pyqtSignal ( QWidget , int                                )
  emitMenuCaller = pyqtSignal ( dict                                         )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
    ##########################################################################
    super ( ) . __init__  (        parent        , plan                      )
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
    EDT   = int              ( SDT + 600                                     )
    ##########################################################################
    VTSI  = VcfTimeScale     ( self , None , self . PlanFunc                 )
    VTSI  . setOptions       ( self . Options , False                        )
    VTSI  . setRange         ( QRectF ( 0.0 , 0.0 , 63.0 , 1.0 )             )
    VTSI  . PrepareItems     (                                               )
    VTSI  . setPeriod        ( SDT , EDT                                     )
    VTSI  . setCurrent       (                                               )
    VTSI  . setMenuCaller    ( self . MenuCallerEmitter                      )
    ##########################################################################
    self  . addItem          ( VTSI                                          )
    self  . Scene . addItem  ( VTSI                                          )
    ##########################################################################
    self  . setPrepared      ( True                                          )
    ##########################################################################
    return
##############################################################################

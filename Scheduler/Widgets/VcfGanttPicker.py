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
    self . Duration = None
    self . Current  = 0
    self . ZDefault = 10000.0
    self . ZAbove   = 0
    self . Picking  = False
    self . Ranges   =           { "First" : 0.0 , "Second" : 0.0             }
    self . setAcceptHoverEvents ( False                                      )
    ##########################################################################
    self . setZValue            ( self . ZDefault                            )
    self . setOpacity           ( 0.95                                       )
    self . setPos               ( QPointF ( 0.0 , 0.0 )                      )
    ##########################################################################
    self . setFlag              ( QGraphicsItem . ItemIsMovable    , False   )
    self . setFlag              ( QGraphicsItem . ItemIsSelectable , False   )
    self . setFlag              ( QGraphicsItem . ItemIsFocusable  , False   )
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
    self . FinalDuration        (                                            )
    ##########################################################################
    return True
  ############################################################################
  def PrepareDuration           ( self                                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def MoveDuration              ( self                                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def FinalDuration             ( self                                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

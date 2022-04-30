# -*- coding: utf-8 -*-
##############################################################################
## VcfFaceRegion
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
from   PyQt5 . QtGui                  import QTransform
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsItem
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager  as MenuManager
##############################################################################
from   AITK  . Essentials . Object    import Object       as Object
from   AITK  . VCF . VcfItem          import VcfItem      as VcfItem
from   AITK  . VCF . VcfRectangle     import VcfRectangle as VcfRectangle
from   AITK  . VCF . VcfCanvas        import VcfCanvas    as VcfCanvas
##############################################################################
class VcfFaceRegion                 ( VcfCanvas                            ) :
  ############################################################################
  def __init__                      ( self                                 , \
                                      parent = None                        , \
                                      item   = None                        , \
                                      plan   = None                        ) :
    ##########################################################################
    super ( ) . __init__            ( parent , item , plan                   )
    self . setVcfFaceRegionDefaults (                                        )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfFaceRegionDefaults ( self                                      ) :
    ##########################################################################
    self . JsonCaller  = None
    self . PictureDPI  = 96
    self . PictureItem = None
    self . Region      = None
    self . Mode        = 2
    self . setZValue           ( 50000                                       )
    self . setOpacity          ( 0.4                                         )
    ##########################################################################
    self . Painter . addPen    ( 0 , QColor (  64 ,  64 ,  64 )              )
    self . Painter . addBrush  ( 0 , QColor ( 255 , 255 , 255 )              )
    ##########################################################################
    return
  ############################################################################
  def BasicFacialRecognition  ( self                                       ) :
    ##########################################################################
    RR = self . ScreenRect
    print(RR)
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  def Menu                    ( self , gview , pos , spos                  ) :
    ##########################################################################
    mm     = MenuManager      ( gview                                        )
    ##########################################################################
    MSG    = "基礎人臉辨識"
    mm     . addAction        ( 1001 , MSG                                   )
    ##########################################################################
    mm     . setFont          ( gview   . menuFont ( )                       )
    aa     = mm . exec_       ( QCursor . pos      ( )                       )
    at     = mm . at          ( aa                                           )
    ##########################################################################
    if                        ( at == 1001                                 ) :
      ########################################################################
      self . BasicFacialRecognition (                                        )
      ########################################################################
      return
    ##########################################################################
    return
##############################################################################

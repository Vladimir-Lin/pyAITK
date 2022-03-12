# -*- coding: utf-8 -*-
##############################################################################
## VcfContours
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
from         . VcfPath                import VcfPath      as VcfPath
##############################################################################
class VcfContours                 ( VcfPath                                ) :
  ############################################################################
  def __init__                    ( self                                   , \
                                    parent = None                          , \
                                    item   = None                          , \
                                    plan   = None                          ) :
    ##########################################################################
    super ( ) . __init__          ( parent , item , plan                     )
    self . setVcfContoursDefaults (                                          )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfContoursDefaults   ( self                                      ) :
    ##########################################################################
    ## self . contour = Contour
    self . contour = None
    self . lines   = QPolygonF (                                             )
    ##########################################################################
    """
    setDropFlag(DropText    ,false) ;
    setDropFlag(DropUrls    ,false) ;
    setDropFlag(DropImage   ,false) ;
    setDropFlag(DropHtml    ,false) ;
    setDropFlag(DropColor   ,true ) ;
    setDropFlag(DropTag     ,true ) ;
    setDropFlag(DropPicture ,false) ;
    setDropFlag(DropPeople  ,false) ;
    setDropFlag(DropVideo   ,false) ;
    setDropFlag(DropAlbum   ,false) ;
    setDropFlag(DropGender  ,false) ;
    setDropFlag(DropDivision,false) ;
    setDropFlag(DropURIs    ,false) ;
    setDropFlag(DropBookmark,false) ;
    setDropFlag(DropFont    ,false) ;
    setDropFlag(DropPen     ,true ) ;
    setDropFlag(DropBrush   ,true ) ;
    setDropFlag(DropGradient,false) ;
    """
    ##########################################################################
    return
  ############################################################################
  def Painting        ( self , p , region , clip , color                   ) :
    ##########################################################################
    self . PaintPath  ( p , 1                                                )
    self . PaintLines ( p , 3 , self . lines                                 )
    self . PaintPath  ( p , 2                                                )
    ##########################################################################
    return
  ############################################################################
  def Prepare ( self , line = False , dot = False ) :
    ##########################################################################
    """
    setContour   ( 1 , contour ) ;
    EnablePath   ( 1 , true    ) ;
    ShowLines    ( line        ) ;
    if (dot )                    {
      setPoints  ( 2 , contour ) ;
      EnablePath ( 2 , true    ) ;
    } else                       {
      EnablePath ( 2 , false   ) ;
    }                            ;
    MergePathes  ( 0           ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def ShowLines                      ( self , line = False                 ) :
    ##########################################################################
    self   . lines . clear           (                                       )
    if                               ( line                                ) :
      pass
      ## self . lines = self . Polyline ( contour , contour.closed )
    self   . update                  (                                       )
    ##########################################################################
    return
  ############################################################################
  def dropColor ( self , source , pos , color ) :
    return True
  ############################################################################
  def dropTags ( self , source , pos , Uuids ) :
    return True
  ############################################################################
  def dropPen ( self , source , pos , penUuid ) :
    ##########################################################################
    """
    GraphicsManager GM (plan )                         ;
    EnterSQL ( SC , plan->sql )                        ;
      Painter . pens    [1] = GM . GetPen   (SC,pen  ) ;
    LeaveSQL ( SC , plan->sql )                        ;
    """
    self . update ( )
    ##########################################################################
    return True
  ############################################################################
  def dropBrush ( self , source , pos , brushUuid ) :
    ##########################################################################
    """
    GraphicsManager GM (plan )                         ;
    EnterSQL ( SC , plan->sql )                        ;
      Painter . brushes [1] = GM . GetBrush (SC,brush) ;
    LeaveSQL ( SC , plan->sql )                        ;
    """
    self . update ( )
    ##########################################################################
    return True
##############################################################################

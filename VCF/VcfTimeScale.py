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
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
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
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfTsDefaults        ( self                                       ) :
    ##########################################################################
    self . Gap       = QSizeF ( 1.0  , 1.0                                   )
    self . Dot       = QSizeF ( 0.02 , 0.02                                  )
    self . LineWidth = QSizeF ( 0.1  , 0.1                                   )
    ##########################################################################
    self . Painter . addMap   ( "Default" , 0                                )
    self . Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 )               )
    self . Painter . addBrush ( 0 , QColor ( 224 , 224 , 224 )               )
    ##########################################################################
    self . Mode = 2
    ##########################################################################
    return
  ############################################################################
  def Painting                  ( self , p , region , clip , color         ) :
    ##########################################################################
    self . pushPainters         ( p                                          )
    ##########################################################################
    if                            ( self . Mode == self . EmptyMode        ) :
      pass
    elif                          ( self . Mode == self . BorderMode       ) :
      self . Painter . drawBorder ( p , "Default" , self . ScreenRect        )
    elif                          ( self . Mode == self . BoardMode        ) :
      self . Painter . drawRect   ( p , "Default" , self . ScreenRect        )
    else                                                                     :
      self . CustomPainting       (        p , region , clip , color         )
    """
    self . Painter . setPainter ( p , "Default"                              )
    if                          ( 0 in self . Painter . pathes             ) :
      p  . drawPath             ( self . Painter . pathes [ 0 ]              )
    """
    ##########################################################################
    self . popPainters          ( p                                          )
    ##########################################################################
    return
  ############################################################################
  def CreatePath       ( self                                              ) :
    ##########################################################################
    self . Painter . pathes [ 0 ] = QPainterPath (                           )
    self . CreateShape ( self . Painter . pathes [ 0 ]                       )
    ##########################################################################
    return
  ############################################################################
  def CreateShape ( self , p ) :
    ##########################################################################
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
    return
##############################################################################

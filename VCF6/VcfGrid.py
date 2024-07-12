# -*- coding: utf-8 -*-
##############################################################################
## VcfGrid
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
import PySide6
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
from           . VcfCanvas import VcfCanvas as VcfCanvas
##############################################################################
class VcfGrid                 ( VcfCanvas                                  ) :
  ############################################################################
  def __init__                ( self                                       , \
                                parent = None                              , \
                                item   = None                              , \
                                plan   = None                              ) :
    ##########################################################################
    super ( ) . __init__      ( parent , item , plan                         )
    self . setVcfGridDefaults (                                              )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfGridDefaults      ( self                                       ) :
    ##########################################################################
    self . Gap       = QSizeF ( 1.0  , 1.0                                   )
    self . Dot       = QSizeF ( 0.02 , 0.02                                  )
    self . LineWidth = QSizeF ( 0.1  , 0.1                                   )
    ##########################################################################
    self . Painter . addMap   ( "Default" , 0                                )
    self . Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 )               )
    self . Painter . addBrush ( 0 , QColor ( 224 , 224 , 224 )               )
    ##########################################################################
    return
  ############################################################################
  def Painting                  ( self , p , region , clip , color         ) :
    ##########################################################################
    self . pushPainters         ( p                                          )
    ##########################################################################
    self . Painter . setPainter ( p , "Default"                              )
    if                          ( 0 in self . Painter . pathes             ) :
      p  . drawPath             ( self . Painter . pathes [ 0 ]              )
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

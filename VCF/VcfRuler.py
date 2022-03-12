# -*- coding: utf-8 -*-
##############################################################################
## VcfRuler
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
from   PyQt5 . QtGui                  import QPainterPath
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
from         . VcfRectangle           import VcfRectangle as VcfRectangle
##############################################################################
class VcfRuler                  ( VcfRectangle                             ) :
  ############################################################################
  vrEast  = 0
  vrSouth = 1
  vrWest  = 2
  vrNorth = 3
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent , item , plan                       )
    self . setVcfRulerDefaults  (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfRulerDefaults       ( self                                     ) :
    ##########################################################################
    self . Direction = self . vrNorth
    ##########################################################################
    self . Painter   . addMap   ( "Default" , 0                              )
    self . Painter   . addPen   ( 0 , QColor ( 192 , 192 , 192 )             )
    self . Painter   . addBrush ( 0 , QColor ( 252 , 252 , 252 )             )
    ##########################################################################
    return
  ############################################################################
  def paint         ( self , painter , options , widget                    ) :
    ##########################################################################
    self . Painting (        painter , self . ScreenRect , True , True       )
    ##########################################################################
    return
  ############################################################################
  def Painting                ( self , p , region , clip , color           ) :
    ##########################################################################
    self . pushPainters       ( p                                            )
    ##########################################################################
    self . Painter . drawRect ( p , "Default" , self . ScreenRect            )
    ##########################################################################
    if                        ( self . Painter . pathes . contains ( 0 )   ) :
      p  . drawPath           ( self . Painter . pathes [ 0 ]                )
    ##########################################################################
    self . popPainters        ( p                                            )
    ##########################################################################
    return
  ############################################################################
  def CreatePath        ( self                                             ) :
    ##########################################################################
    self . Painter . pathes [ 0 ] = QPainterPath (                           )
    ##########################################################################
    if                  ( self . Direction == self . vrEast                ) :
      self . PaintEast  ( self . Painter . pathes [ 0 ]                      )
      return
    ##########################################################################
    if                  ( self . Direction == self . vrSouth               ) :
      self . PaintSouth ( self . Painter . pathes [ 0 ]                      )
      return
    ##########################################################################
    if                  ( self . Direction == self . vrWest                ) :
      self . PaintWest  ( self . Painter . pathes [ 0 ]                      )
      return
    ##########################################################################
    if                  ( self . Direction == self . vrNorth               ) :
      self . PaintNorth ( self . Painter . pathes [ 0 ]                      )
      return
    ##########################################################################
    return
  ############################################################################
  def PaintEast  ( self , p ) :
    ##########################################################################
    """
    QRectF  dr = ScreenRect  ;
    qreal   ep = dr.height() ;
    qreal   dw = dr.width () ;
    qreal   mw = dw / 2      ;
    qreal   mm = dw / 4      ;
    qreal   dl = 0           ;
    int     di = 0           ;
    QPointF xy               ;
    do {
      dl  = di ;
      dl /= 10 ;
      xy.setX(dl);
      xy.setY(dl);
      xy  = toPaper(xy);
      dl  = xy.x();
      if (dl<ep) {
        p->moveTo(dr.left(),dr.top()+dl);
        if ((di%10)==0) p->lineTo(dr.right()   ,dr.top()+dl); else
        if ((di% 5)==0) p->lineTo(dr.left ()+mw,dr.top()+dl); else
                        p->lineTo(dr.left ()+mm,dr.top()+dl);
      };
      di ++ ;
    } while (dl<ep);
    """
    ##########################################################################
    return
  ############################################################################
  def PaintSouth ( self , p ) :
    ##########################################################################
    """
    QRectF  dr = ScreenRect  ;
    qreal   ep = dr.width () ;
    qreal   dh = dr.height() ;
    qreal   mh = dh / 2      ;
    qreal   mm = dh / 4      ;
    qreal   dl = 0           ;
    int     di = 0           ;
    QPointF xy               ;
    do {
      dl  = di ;
      dl /= 10 ;
      xy.setX(dl);
      xy.setY(dl);
      xy  = toPaper(xy);
      dl  = xy.x();
      if (dl<ep) {
        p->moveTo(dr.left()+dl,dr.top());
        if ((di%10)==0) p->lineTo(dr.left()+dl,dr.bottom()   ); else
        if ((di% 5)==0) p->lineTo(dr.left()+dl,dr.top   ()+mh); else
                        p->lineTo(dr.left()+dl,dr.top   ()+mm);
      };
      di ++ ;
    } while (dl<ep);
    """
    ##########################################################################
    return
  ############################################################################
  def PaintWest  ( self , p ) :
    ##########################################################################
    """
    QRectF  dr = ScreenRect  ;
    qreal   ep = dr.height() ;
    qreal   dw = dr.width () ;
    qreal   mw = dw / 2      ;
    qreal   mm = dw / 4      ;
    qreal   dl = 0           ;
    int     di = 0           ;
    QPointF xy               ;
    do {
      dl  = di ;
      dl /= 10 ;
      xy.setX(dl);
      xy.setY(dl);
      xy  = toPaper(xy);
      dl  = xy.x();
      if (dl<ep) {
        p->moveTo(dr.right(),dr.top()+dl);
        if ((di%10)==0) p->lineTo(dr.left ()   ,dr.top()+dl); else
        if ((di% 5)==0) p->lineTo(dr.right()-mw,dr.top()+dl); else
                        p->lineTo(dr.right()-mm,dr.top()+dl);
      };
      di ++ ;
    } while (dl<ep);
    """
    ##########################################################################
    return
  ############################################################################
  def PaintNorth ( self , p ) :
    ##########################################################################
    """
    QRectF  dr = ScreenRect ;
    qreal   ep = dr.width ();
    qreal   dh = dr.height();
    qreal   mh = dh / 2     ;
    qreal   mm = dh / 4     ;
    qreal   dl = 0          ;
    int     di = 0          ;
    QPointF xy              ;
    do {
      dl  = di ;
      dl /= 10 ;
      xy.setX(dl);
      xy.setY(dl);
      xy  = toPaper(xy);
      dl  = xy.x();
      if (dl<ep) {
        p->moveTo(dr.left()+dl,dr.bottom());
        if ((di%10)==0) p->lineTo(dr.left()+dl,dr.top   ()   ); else
        if ((di% 5)==0) p->lineTo(dr.left()+dl,dr.bottom()-mh); else
                        p->lineTo(dr.left()+dl,dr.bottom()-mm);
      };
      di ++    ;
    } while (dl<ep);
    """
    ##########################################################################
    return
##############################################################################

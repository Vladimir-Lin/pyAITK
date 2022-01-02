# -*- coding: utf-8 -*-
##############################################################################
## VcfOptions
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
from   PyQt5 . QtWidgets              import QGraphicsScene
##############################################################################
from         . VcfFont                import VcfFont
##############################################################################
class VcfOptions      (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    self . Initialize (                                                      )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Initialize      ( self                                               ) :
    ##########################################################################
    self . Private = False
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
  ############################################################################
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfOptions
{
  public:

    explicit VcfOptions     (void) ;
    virtual ~VcfOptions     (void) ;

    bool                Private    ;
    bool                ColorMode  ;
    int                 DPI        ;
    double              PictureDPI ;
    bool                Insert     ;
    double              LineSpace  ;
    QSizeF              ScaleRatio ;
    QMap<int,VcfFont *> fonts      ;

    QPointF position        (QPointF cm           ) ;
    QRectF  Region          (QRectF  cm           ) ;
    QPointF Standard        (QPointF paper        ) ;
    QRectF  Standard        (QRectF  paper        ) ;
    QSizeF  PictureOnPaper  (QSize   size         ) ;
    QSizeF  PictureOnPaper  (QSize   size ,int DPI) ;

    VcfOptions & operator = (VcfOptions & options ) ;

  protected:

  private:

};

N::VcfOptions:: VcfOptions ( void        )
              : Private    ( false       )
              , ColorMode  ( true        )
              , DPI        ( 300         )
              , Insert     ( true        )
              , LineSpace  ( 0.025       )
              , PictureDPI ( 96.00       )
              , ScaleRatio ( 1.00 , 1.00 )
{
}

N::VcfOptions::~VcfOptions (void)
{
}

// Centimeter to Paper resolution
// cm * DPI * 100 / 254
QPointF N::VcfOptions::position(QPointF cm)
{
  qreal x = cm.x() ; x *= DPI ; x *= 100 ; x /= 254 ; x /= ScaleRatio.width () ;
  qreal y = cm.y() ; y *= DPI ; y *= 100 ; y /= 254 ; y /= ScaleRatio.height() ;
  return QPointF(x,y)                                                          ;
}

QRectF N::VcfOptions::Region(QRectF cm)
{
  QPointF S(cm.left(),cm.top())          ;
  QPointF W(cm.width(),cm.height())      ;
  S = position(S)                        ;
  W = position(W)                        ;
  return QRectF(S.x(),S.y(),W.x(),W.y()) ;
}

QPointF N::VcfOptions::Standard(QPointF paper)
{
  qreal x = paper.x() ; x *= 254 ; x /= 100 ; x /= DPI ; x *= ScaleRatio.width () ;
  qreal y = paper.y() ; y *= 254 ; y /= 100 ; y /= DPI ; y *= ScaleRatio.height() ;
  return QPointF(x,y)                                                             ;
}

QRectF N::VcfOptions::Standard(QRectF paper)
{
  QPointF S(paper.left(),paper.top())     ;
  QPointF W(paper.width(),paper.height()) ;
  S = Standard(S)                         ;
  W = Standard(W)                         ;
  return QRectF(S.x(),S.y(),W.x(),W.y())  ;
}

QSizeF N::VcfOptions::PictureOnPaper(QSize size)
{
  return PictureOnPaper(size,PictureDPI) ;
}

QSizeF N::VcfOptions::PictureOnPaper(QSize size,int DPI)
{
  // Convert to CM first
  QPointF C(size.width(),size.height())                          ;
  C.setX(C.x() * 254) ; C.setX(C.x() / 100); C.setX(C.x() / DPI) ;
  C.setY(C.y() * 254) ; C.setY(C.y() / 100); C.setX(C.y() / DPI) ;
  // Convert to Paper
  QPointF S = position(C)                                        ;
  return QSizeF(S.x(),S.y())                                     ;
}

N::VcfOptions & N::VcfOptions::operator = (VcfOptions & options)
{
  Private    = options.Private    ;
  ColorMode  = options.ColorMode  ;
  DPI        = options.DPI        ;
  PictureDPI = options.PictureDPI ;
  Insert     = options.Insert     ;
  LineSpace  = options.LineSpace  ;
  ScaleRatio = options.ScaleRatio ;
  fonts      = options.fonts      ;
  return (*this)                  ;
}
"""

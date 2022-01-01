# -*- coding: utf-8 -*-
##############################################################################
## VcfPainter
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
class VcfPainter      (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfPainter
{
  public:

    UMAPs     Names     ;
    Pens      pens      ;
    Brushes   brushes   ;
    Gradients gradients ;
    FONTs     fonts     ;
    Pathes    pathes    ;
    BMAPs     switches  ;

    explicit VcfPainter        (void) ;
    virtual ~VcfPainter        (void) ;

    int           addPen       (int Id,QColor color) ;
    int           addBrush     (int Id,QColor color) ;
    void          addMap       (QString name,int Id) ;
    void          setPainter   (QPainter * painter,QString name) ;
    void          drawRect     (QPainter * painter,QString name,QRectF rect) ;
    void          drawBorder   (QPainter * painter,QString name,QRectF rect) ;
    QFontMetricsF FontMetrics  (int Id) ;
    QRectF        boundingRect (int Id,QString text);

  protected:

  private:

};

N::VcfPainter:: VcfPainter (void)
{
}

N::VcfPainter::~VcfPainter (void)
{
}

int N::VcfPainter::addPen(int Id,QColor color)
{
  pens [ Id ] = Pen   ( color ) ;
  return pens . count (       ) ;
}

int N::VcfPainter::addBrush(int Id,QColor color)
{
  brushes [ Id ] = Brush ( color ) ;
  return brushes . count (       ) ;
}

void N::VcfPainter::addMap(QString name,int Id)
{
  Names[name] = Id ;
}

void N::VcfPainter::setPainter(QPainter * p,QString name)
{
  if (!Names.contains(name)) return                     ;
  int Id = Names[name]                                  ;
  if (pens   .contains(Id)) p -> setPen   (pens   [Id]) ;
  if (brushes.contains(Id)) p -> setBrush (brushes[Id]) ;
}

void N::VcfPainter::drawRect(QPainter * p,QString name,QRectF Rect)
{
  if (!Names.contains(name)) return                     ;
  int Id = Names[name]                                  ;
  if (pens   .contains(Id)) p -> setPen   (pens   [Id]) ;
  if (brushes.contains(Id)) p -> setBrush (brushes[Id]) ;
  p -> drawRect ( Rect )                                ;
}

void N::VcfPainter::drawBorder(QPainter * p,QString name,QRectF Rect)
{
  if (!Names.contains(name)) return ;
  int Id = Names[name]              ;
  if (pens   .contains(Id))         {
    p -> setPen ( pens [ Id ] )     ;
  }                                 ;
  QPolygonF P                       ;
  P << Rect . topLeft     (   )     ;
  P << Rect . topRight    (   )     ;
  P << Rect . bottomRight (   )     ;
  P << Rect . bottomLeft  (   )     ;
  P << Rect . topLeft     (   )     ;
  p -> drawPolyline       ( P )     ;
}

QFontMetricsF N::VcfPainter::FontMetrics (int Id)
{
  return QFontMetricsF(fonts[Id]) ;
}

QRectF N::VcfPainter::boundingRect(int Id,QString text)
{
  return FontMetrics(Id).boundingRect(text) ;
}
"""

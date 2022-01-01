# -*- coding: utf-8 -*-
##############################################################################
## VcfPaperConf
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
class VcfPaperConf    (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfPaperConf
{
  public:

    QString paper     ;
    DMAPs   borders   ;
    int     paperX    ;
    int     paperY    ;
    int     dpi       ;
    int     direction ; // Qt::Vertical , Qt::Horizontal
    int     arrange   ; // Neutrino::Texts::...

    explicit VcfPaperConf     (void) ;
             VcfPaperConf     (const VcfPaperConf & conf) ;
    virtual ~VcfPaperConf     (void) ;

    VcfPaperConf & operator = (const VcfPaperConf & conf) ;

    int X                     (int page) ;
    int Y                     (int page) ;

    QRectF PaperAt            (int page,QRectF PaperSize) ;

  protected:

  private:

};

N::VcfPaperConf:: VcfPaperConf (void)
{
  direction = Qt::Vertical              ;
  arrange   = Texts::TopLeftToTopRight  ;
  paperX    = 1                         ;
  paperY    = 1                         ;
  dpi       = 300                       ;
  paper     = "A4"                      ;
  borders [ VcfPaper :: Left   ] = 1.00 ;
  borders [ VcfPaper :: Top    ] = 1.00 ;
  borders [ VcfPaper :: Right  ] = 1.00 ;
  borders [ VcfPaper :: Bottom ] = 1.00 ;
}

N::VcfPaperConf:: VcfPaperConf (const VcfPaperConf & conf)
{
  ME = conf ;
}

N::VcfPaperConf::~VcfPaperConf(void)
{
}

N::VcfPaperConf & N::VcfPaperConf::operator = (const VcfPaperConf & conf)
{
  nMemberCopy ( conf , paper     ) ;
  nMemberCopy ( conf , borders   ) ;
  nMemberCopy ( conf , paperX    ) ;
  nMemberCopy ( conf , paperY    ) ;
  nMemberCopy ( conf , dpi       ) ;
  nMemberCopy ( conf , direction ) ;
  nMemberCopy ( conf , arrange   ) ;
  return ME                        ;
}

int N::VcfPaperConf::X(int page)
{
  switch (arrange)                   {
    case Texts::TopLeftToTopRight    :
    return   page % paperX           ;
    case Texts::TopLeftToBottomRight :
    return   page / paperY           ;
    case Texts::TopRightToTopLeft    :
    return -(page % paperX)          ;
    case Texts::TopRightToBottomLeft :
    return -(page / paperY)          ;
  }                                  ;
  return 0                           ;
}

int N::VcfPaperConf::Y(int page)
{
  switch (arrange)                   {
    case Texts::TopLeftToTopRight    :
    return   page / paperX           ;
    case Texts::TopLeftToBottomRight :
    return   page % paperY           ;
    case Texts::TopRightToTopLeft    :
    return -(page / paperX)          ;
    case Texts::TopRightToBottomLeft :
    return -(page % paperY)          ;
  }                                  ;
  return 0                           ;
}

QRectF N::VcfPaperConf::PaperAt(int page,QRectF PaperSize)
{
  QRectF  At                      ;
  int     x = X(page)             ;
  int     y = Y(page)             ;
  qreal   w = PaperSize.width  () ;
  qreal   h = PaperSize.height () ;
  QPointF p = PaperSize.topLeft() ;
  QPointF d ( w * x , h * y )     ;
  p += d                          ;
  At . setTopLeft ( p )           ;
  At . setWidth   ( w )           ;
  At . setHeight  ( h )           ;
  return At                       ;
}
"""

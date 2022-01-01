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
class VcfGrid         (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfGrid : public VcfCanvas
{
  Q_OBJECT
  public:

    QSizeF Gap ;
    QSizeF Dot ;

    enum { Type = UserType + VCF::Grid };
    virtual int type(void) const { return Type; }

    explicit VcfGrid  (QObject * parent,QGraphicsItem * item,Plan * plan = NULL);
    virtual ~VcfGrid  (void);

  protected:

  private:

  public slots:

    void CreatePath    (void) ;
    void CreateShape   (QPainterPath * p);
    void Paint         (QPainter * painter,QRectF Region,bool clip,bool color);

  protected slots:

  private slots:

  signals:

};

N::VcfGrid:: VcfGrid   (QObject * parent,QGraphicsItem * item,Plan * p)
           : VcfCanvas (          parent,                item,       p)
           , Gap       ( QSizeF ( 1.00 , 1.00 )                       )
           , Dot       ( QSizeF ( 0.02 , 0.02 )                       )
{
  Painter . addMap   ( "Default" , 0                  ) ;
  Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 ) ) ;
  Painter . addBrush ( 0 , QColor ( 224 , 224 , 224 ) ) ;
}

N::VcfGrid::~VcfGrid(void)
{
}

void N::VcfGrid::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  pushPainters ( p )                     ;
  Painter . setPainter ( p , "Default" ) ;
  if (Painter.pathes.contains(0))        {
    p->drawPath(Painter.pathes[0])       ;
  }                                      ;
  popPainters  ( p )                     ;
}

void N::VcfGrid::CreatePath(void)
{
  Painter.pathes[0] = QPainterPath() ;
  CreateShape ( &Painter.pathes[0] ) ;
}

void N::VcfGrid::CreateShape(QPainterPath * p)
{
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
}
"""

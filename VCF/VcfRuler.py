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
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
class VcfRuler        (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfRuler : public VcfRectangle
{
  Q_OBJECT
  public:

    Direction direction ;

    enum { Type = UserType + VCF::Ruler };
    virtual int type(void) const { return Type; }

    explicit VcfRuler  (QObject * parent,QGraphicsItem * item,Plan * plan = NULL) ;
    virtual ~VcfRuler  (void);

    virtual void paint (QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget = 0);

  protected:

  private:

  public slots:

    void CreatePath    (void) ;
    void Paint         (QPainter * painter,QRectF Region,bool clip,bool color);
    void PaintNorth    (QPainterPath * painter);
    void PaintSouth    (QPainterPath * painter);
    void PaintEast     (QPainterPath * painter);
    void PaintWest     (QPainterPath * painter);

  protected slots:

  private slots:

  signals:

};

N::VcfRuler:: VcfRuler     (QObject * parent,QGraphicsItem * item,Plan * p)
            : VcfRectangle (          parent,                item,       p)
            , direction    (North                                         )
{
  Painter . addMap   ( "Default" , 0                  ) ;
  Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 ) ) ;
  Painter . addBrush ( 0 , QColor ( 252 , 252 , 252 ) ) ;
}

N::VcfRuler::~VcfRuler(void)
{
}

void N::VcfRuler::paint(QPainter * p,const QStyleOptionGraphicsItem *,QWidget *)
{
  Paint(p,ScreenRect,true,true);
}

void N::VcfRuler::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  pushPainters ( p )         ;
  Painter . drawRect ( p , "Default" , ScreenRect ) ;
  if (Painter.pathes.contains(0)) p->drawPath(Painter.pathes[0]);
  popPainters  ( p )         ;
}

void N::VcfRuler::CreatePath(void)
{
  Painter.pathes[0] = QPainterPath() ;
  switch (direction)                 {
    case North                       :
      PaintNorth(&Painter.pathes[0]) ;
    break                            ;
    case South                       :
      PaintSouth(&Painter.pathes[0]) ;
    break                            ;
    case East                        :
      PaintEast (&Painter.pathes[0]) ;
    break                            ;
    case West                        :
      PaintWest (&Painter.pathes[0]) ;
    break                            ;
  }                                  ;
}

void N::VcfRuler::PaintNorth(QPainterPath * p)
{
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
}

void N::VcfRuler::PaintSouth(QPainterPath * p)
{
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
}

void N::VcfRuler::PaintEast(QPainterPath * p)
{
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
}

void N::VcfRuler::PaintWest(QPainterPath * p)
{
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
}
"""

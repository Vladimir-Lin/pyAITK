# -*- coding: utf-8 -*-
##############################################################################
## VcfPaper
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
class VcfPaper        (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfPaper : public VcfRectangle
{
  Q_OBJECT
  public:

    enum BorderNames {
      Left   = 1 ,
      Top    = 2 ,
      Right  = 3 ,
      Bottom = 4
    };

    enum DrawingStyle {
      Editing   = 0 ,
      FrameOnly = 1
    };

    QString   Paper     ;
    int       DPI       ;
    int       Direction ;
    int       Alignment ;
    SUID      Page      ;
    QString   Name      ;
    DMAPs     Borders   ;
    bool      Movable   ;
    int       Style     ;
    VcfFont * Font      ;

    enum { Type = UserType + VCF::Paper } ;
    virtual int type(void) const { return Type; }

    explicit VcfPaper             (QObject       * parent       ,
                                   QGraphicsItem * item         ,
                                   Plan          * plan = NULL) ;
    virtual ~VcfPaper             (void);

    virtual void         paint    (QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget);
    virtual QPainterPath shape    (void) const ;
    virtual QRectF PaperEditing   (void) const ;

  protected:

    QMenu * menu ;

    virtual void contextMenuEvent (QGraphicsSceneContextMenuEvent * event);
    virtual void hoverMoveEvent   (QGraphicsSceneHoverEvent       * event);

  private:

  public slots:

    virtual void   Paint          (QPainter * painter,QRectF Region,bool clip,bool color) ;

    virtual void   PaintEditing   (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void   PaintFrame     (QPainter * painter,QRectF Region,bool clip,bool color) ;

    void Print                    (QPainter * painter,QRectF rect);
    void PaintRegion              (QPainter * painter);
    void PaintBorder              (QPainter * painter);
    void PaintName                (QPainter * painter,QRectF rect,bool clip);

    void setMargins               (qreal left,qreal top,qreal right,qreal bottom);
    void setMovable               (bool enable);
    void setMenu                  (QMenu * menu) ;

  protected slots:

    virtual bool Menu             (QPointF pos) ;

  private slots:

  signals:

    void Menu                     (VcfPaper * paper,QPointF pos) ;
    void Moving                   (QString name,QPointF pos,QPointF paper,QPointF scene);

};

N::VcfPaper:: VcfPaper     (QObject * parent,QGraphicsItem * item,Plan * p)
            : VcfRectangle (          parent,                item,       p)
            , Paper        ("A4"                                          )
            , DPI          (300                                           )
            , Direction    (Qt::Vertical                                  )
            , Alignment    (Qt::AlignRight | Qt::AlignVCenter             )
            , Page         (0                                             )
            , Name         (""                                            )
            , Movable      (false                                         )
            , Style        (Editing                                       )
            , menu         (NULL                                          )
            , Font         (NULL                                          )
{
  Borders[Left  ] = 1.00                            ;
  Borders[Top   ] = 1.00                            ;
  Borders[Right ] = 1.00                            ;
  Borders[Bottom] = 1.00                            ;
  Painter . addMap   ( "Default" , 0 )              ;
  Painter . addMap   ( "Black"   , 1 )              ;
  Painter . addMap   ( "Dash"    , 2 )              ;
  Painter . addPen   ( 0 , QColor(192,192,192)    ) ;
  Painter . addPen   ( 1 , QColor(  0,  0,  0)    ) ;
  Painter . addPen   ( 2 , QColor(128,128,128)    ) ;
  Painter . addBrush ( 0 , QColor(255,255,255)    ) ;
  Painter . pens [2] . setStyle ( Qt::DashDotLine ) ;
}

N::VcfPaper::~VcfPaper (void)
{
}

void N::VcfPaper::contextMenuEvent(QGraphicsSceneContextMenuEvent * event)
{
  if (Menu(event->pos())) event->accept()     ;
  else QGraphicsItem::contextMenuEvent(event) ;
}

void N::VcfPaper::hoverMoveEvent(QGraphicsSceneHoverEvent * event)
{
  VcfRectangle::hoverMoveEvent(event)         ;
  if (IsNull(plan)) return                    ;
  QPointF pf = event -> pos          (      ) ;
  QPointF ps = mapToScene            (pf    ) ;
  QPointF px = plan  -> toCentimeter (pf,DPI) ;
  emit Moving ( Name , px , ps , pf )         ;
}

QPainterPath N::VcfPaper::shape(void) const
{
  QPainterPath path          ;
  path . addRect(ScreenRect) ;
  return path                ;
}

QRectF N::VcfPaper::PaperEditing(void) const
{
  QRectF Range = PaperRange()                                    ;
  QRectF R(Range . left   () + Borders[Left]                     ,
           Range . top    () + Borders[Top ]                     ,
           Range . width  () - Borders[Left] - Borders[Right ]   ,
           Range . height () - Borders[Top ] - Borders[Bottom] ) ;
  return R                                                       ;
}

void N::VcfPaper::paint(QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget)
{
  Paint (painter,ScreenRect,true,true) ;
}

void N::VcfPaper::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  switch (Style)                         {
    case Editing                         :
      PaintEditing (p,Region,clip,color) ;
    break                                ;
    case FrameOnly                       :
      PaintFrame   (p,Region,clip,color) ;
    break                                ;
  }                                      ;
}

void N::VcfPaper::PaintEditing(QPainter * p,QRectF Region,bool clip,bool color)
{
  PaintRegion (p                 ) ;
  PaintBorder (p                 ) ;
  PaintName   (p,ScreenRect,false) ;
}

void N::VcfPaper::PaintFrame(QPainter * p,QRectF Region,bool clip,bool color)
{
  PaintRegion (p) ;
}

void N::VcfPaper::PaintRegion(QPainter * p)
{
  Painter . drawRect ( p , "Default" , ScreenRect ) ;
}

void N::VcfPaper::Print(QPainter * p,QRectF rt)
{
  PaintName(p,rt,true) ;
}

void N::VcfPaper::PaintBorder(QPainter * p)
{
  qreal   x    = Borders[Left ]                   ;
  qreal   y    = Borders[Top  ]                   ;
  qreal   w    = Borders[Left ] + Borders[Right ] ;
  qreal   h    = Borders[Top  ] + Borders[Bottom] ;
  QPointF S    = plan->toPaper(QPointF(x,y),DPI)  ;
  QPointF R    = plan->toPaper(QPointF(w,h),DPI)  ;
  QRectF  SR   = ScreenRect                       ;
  QRectF  T (SR.left()+S.x(),SR.top()+S.y(),SR.width()-R.x(),SR.height()-R.y());
  int     ID   = Painter . Names   [ "Default"  ] ;
  int     DL   = Painter . Names   [ "Dash"     ] ;
  QPen    P    = Painter . pens    [ID          ] ;
  QBrush  B    = Painter . brushes [ID          ] ;
  if (isSelected()) P = Painter . pens [ DL     ] ;
  p -> setPen   (P)                               ;
  p -> setBrush (B)                               ;
  p -> drawRect (T)                               ;
}

void N::VcfPaper::PaintName(QPainter * p,QRectF rt,bool clip)
{
  if (Name.length()<=0) return                   ;
  if (IsNull(Font)) return                       ;
  qreal   x    = Borders[Left ]                  ;
  qreal   y    = Borders[Top  ] / 4              ;
  qreal   w    = Borders[Left] + Borders[Right]  ;
  qreal   h    = Borders[Top  ] / 2              ;
  int     ID   = Painter . Names   [ "Default" ] ;
  int     BD   = Painter . Names   [ "Black"   ] ;
  QPen    P    = Painter . pens    [ID         ] ;
  QBrush  B    = Painter . brushes [ID         ] ;
  QPen    W    = Painter . pens    [BD         ] ;
  QPointF S    = plan->toPaper(QPointF(x,y),DPI) ;
  QPointF R    = plan->toPaper(QPointF(w,h),DPI) ;
  QRectF  SR   = ScreenRect                      ;
  QRectF  T(SR.left()+S.x(),SR.top()+S.y(),SR.width()-R.x(),R.y());
  qreal   px   = R.y(); px *= 2; px /= 3         ;
  if (clip)                                      {
    QRectF TR                                    ;
    TR . setLeft   (T.left  ()-rt.left())        ;
    TR . setTop    (T.top   ()-rt.top ())        ;
    TR . setWidth  (T.width ()          )        ;
    TR . setHeight (T.height()          )        ;
    T = TR                                       ;
    Font-> setFont  (p,DPI)                      ;
    p   -> setPen   (W)                          ;
    p   -> setBrush (B)                          ;
    p   -> drawText (T,Alignment,Name)           ;
  } else                                         {
    Font-> setFont  (p,DPI           )           ;
    p   -> setPen   (Font->pen       )           ;
    p   -> setBrush (Font->brush     )           ;
    p   -> drawText (T,Alignment,Name)           ;
  }                                              ;
}

void N::VcfPaper::setMargins(qreal left,qreal top,qreal right,qreal bottom)
{
  Borders[Left  ] = left   ;
  Borders[Top   ] = top    ;
  Borders[Right ] = right  ;
  Borders[Bottom] = bottom ;
}

void N::VcfPaper::setMovable(bool enable)
{
  Movable = enable;
  setFlag(ItemIsMovable,enable);
}

void N::VcfPaper::setMenu(QMenu * m)
{
  menu = m ;
}

bool N::VcfPaper::Menu(QPointF pos)
{
  if (IsNull(menu))          {
    emit Menu ( this , pos ) ;
    return false             ;
  }                          ;
  QPoint g = toGlobal(pos)   ;
  menu->exec(g)              ;
  return true                ;
}
"""

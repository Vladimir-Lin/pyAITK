# -*- coding: utf-8 -*-
##############################################################################
## VcfSlider
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
class VcfSlider       (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfSlider : public VcfItem
{
  Q_OBJECT
  public:

    QString ToolTip ;

    enum { Type = UserType + VCF::Slider } ;
    virtual int type(void) const { return Type; }

    explicit VcfSlider                 (QObject       * parent       ,
                                        QGraphicsItem * item         ,
                                        Plan          * plan = NULL) ;
    virtual ~VcfSlider                 (void);

    virtual QRectF       boundingRect  (void) const ;
    virtual QPainterPath shape         (void) const ;
    virtual void         paint         (QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget = 0);

    double Minimum                     (void) ;
    double Maximum                     (void) ;
    double Value                       (QPointF pos) ;

  protected:

    DMAPs             Values ;
    QMap<int,QPointF> Points ;

    virtual void Configure             (void) ;

    virtual void hoverEnterEvent       (QGraphicsSceneHoverEvent * event);
    virtual void hoverLeaveEvent       (QGraphicsSceneHoverEvent * event);
    virtual void hoverMoveEvent        (QGraphicsSceneHoverEvent * event);
    virtual void Hovering              (QPointF pos);

    virtual void mouseDoubleClickEvent (QGraphicsSceneMouseEvent * event) ;
    virtual void mouseMoveEvent        (QGraphicsSceneMouseEvent * event);
    virtual void mousePressEvent       (QGraphicsSceneMouseEvent * event);
    virtual void mouseReleaseEvent     (QGraphicsSceneMouseEvent * event);

  private:

  public slots:

    virtual void Paint                 (QPainter * painter,QRectF Region,bool clip,bool color) ;

    virtual void setLine               (double width,double inside,QPointF P1,QPointF P2) ;
    virtual void setLine               (double width,double inside,QLineF L) ;

    virtual void setRange              (double minimum,double maximum) ;
    virtual void setVisible            (double start  ,double final  ) ;

    virtual void startPosition         (QPointF pos) ;
    virtual void setPosition           (QPointF pos) ;
    virtual void endPosition           (void) ;
    virtual void updatePosition        (void) ;

  protected slots:

  private slots:

  signals:

    void Visible                       (double start,double final,int step) ;

};

N::VcfSlider:: VcfSlider (QObject * parent,QGraphicsItem * item,Plan * p)
             : VcfItem   (          parent,                item,       p)
{
  Configure ( ) ;
}

N::VcfSlider::~VcfSlider (void)
{
  if (IsNull(Options)  ) return ;
  if (!Options->Private) return ;
  delete Options                ;
  Options = NULL                ;
}

void N::VcfSlider::Configure(void)
{
  setFlag(ItemIsMovable           ,false)                       ;
  setFlag(ItemIsSelectable        ,true )                       ;
  setFlag(ItemIsFocusable         ,true )                       ;
  setFlag(ItemClipsToShape        ,false)                       ;
  setFlag(ItemClipsChildrenToShape,false)                       ;
  ///////////////////////////////////////////////////////////////
  Painter . addMap   ( "Default" , 0                  )         ;
  Painter . addMap   ( "Holder"  , 1                  )         ;
  Painter . addPen   ( 0 , QColor ( 224 , 224 , 224 ) )         ;
  Painter . addPen   ( 1 , QColor ( 192 , 192 , 192 ) )         ;
  ///////////////////////////////////////////////////////////////
  QLinearGradient * linear                                      ;
  ///////////////////////////////////////////////////////////////
  Painter . gradients[0] = Gradient(QGradient::LinearGradient)  ;
  linear = Painter . gradients[0] .linear()                     ;
  linear->setColorAt(0.0,QColor(224,224,224))                   ;
  linear->setColorAt(0.5,QColor(252,252,252))                   ;
  linear->setColorAt(1.0,QColor(224,224,224))                   ;
  ///////////////////////////////////////////////////////////////
  Painter . gradients[1] = Gradient(QGradient::LinearGradient)  ;
  linear = Painter . gradients[1] .linear()                     ;
  linear->setColorAt(0.0,QColor(192,192,192))                   ;
  linear->setColorAt(0.5,QColor(240,240,240))                   ;
  linear->setColorAt(1.0,QColor(192,192,192))                   ;
  ///////////////////////////////////////////////////////////////
  ToolTip = tr("[%1,%2] range [%3,%4]")                         ;
}

QRectF N::VcfSlider::boundingRect(void) const
{
  if (Painter.pathes.contains(0))           {
    return Painter.pathes[0].boundingRect() ;
  }                                         ;
  return QRectF ( 0 , 0 , 1 , 1 )           ;
}

QPainterPath N::VcfSlider::shape(void) const
{
  QPainterPath path               ;
  if (Painter.pathes.contains(0)) {
    path = Painter . pathes [ 0 ] ;
  }                               ;
  return path                     ;
}

void N::VcfSlider::paint(QPainter * p,const QStyleOptionGraphicsItem *,QWidget *)
{
  QRectF Z(0,0,0,0)              ;
  Paint ( p , Z , false , true ) ;
}

void N::VcfSlider::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  QLinearGradient * linear                                              ;
  if (Points.contains(31))                                              {
      linear = Painter . gradients[0] .linear()                         ;
      linear->setStart     ( Points[31] )                               ;
      linear->setFinalStop ( Points[32] )                               ;
      Painter . brushes  [0] = Brush(*(Painter.gradients[0].gradient))  ;
  }                                                                     ;
  if (Points.contains(41))                                              {
      linear = Painter . gradients[1] .linear()                         ;
      linear->setStart     ( Points[41] )                               ;
      linear->setFinalStop ( Points[42] )                               ;
      Painter . brushes  [1] = Brush(*(Painter.gradients[1].gradient))  ;
  }                                                                     ;
  ///////////////////////////////////////////////////////////////////////
  PaintPathes ( p )                                                     ;
}

void N::VcfSlider::hoverEnterEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverEnterEvent(event) ;
}

void N::VcfSlider::hoverLeaveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverLeaveEvent(event) ;
}

void N::VcfSlider::hoverMoveEvent(QGraphicsSceneHoverEvent * event)
{
  Hovering ( event->pos() )            ;
  QGraphicsItem::hoverMoveEvent(event) ;
}

void N::VcfSlider::Hovering(QPointF pos)
{
  if (!Painter.pathes.contains(1)) return       ;
  bool inside = Painter.pathes[1].contains(pos) ;
  if (!inside) return                           ;
  if (!Values.contains(11)) return              ;
  if (!Values.contains(12)) return              ;
  if (!Values.contains(14)) return              ;
  if (!Values.contains(15)) return              ;
  QString M = QString(ToolTip                   )
              .arg(Values[14]                   )
              .arg(Values[15]                   )
              .arg(Values[11]                   )
              .arg(Values[12]                 ) ;
  QToolTip :: showText ( QCursor::pos() , M   ) ;
}

void N::VcfSlider::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
{
  QGraphicsItem::mouseDoubleClickEvent(event) ;
}

void N::VcfSlider::mouseMoveEvent(QGraphicsSceneMouseEvent * event)
{
  if (IsMask(event->buttons(),Qt::LeftButton)) {
    setPosition     ( event->pos() )           ;
    event -> accept (              )           ;
  } else QGraphicsItem::mouseMoveEvent(event)  ;
}

void N::VcfSlider::mousePressEvent(QGraphicsSceneMouseEvent * event)
{
  if (IsMask(event->buttons(),Qt::LeftButton)) {
    startPosition   ( event->pos() )           ;
    event -> accept (              )           ;
  } else QGraphicsItem::mousePressEvent(event) ;
}

void N::VcfSlider::mouseReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  endPosition                      (       ) ;
  QGraphicsItem::mouseReleaseEvent ( event ) ;
}

void N::VcfSlider::setLine(double width,double inside,QLineF L)
{
  setLine ( width , inside , L.p1() , L.p2() ) ;
}

void N::VcfSlider::setLine(double width,double inside,QPointF P1,QPointF P2)
{
  QPainterPath         path                                ;
  VcfShape             shape                               ;
  QPointF              wl (width,inside)                   ;
  QPointF              p1   = Options->position(P1)        ;
  QPointF              p2   = Options->position(P2)        ;
  wl                        = Options->position(wl)        ;
  Values             [ 0 ]  = width                        ;
  Values             [ 1 ]  = wl.x()                       ;
  Values             [ 2 ]  = inside                       ;
  Values             [ 3 ]  = wl.y()                       ;
  Points             [ 0 ]  = P1                           ;
  Points             [ 1 ]  = P2                           ;
  Points             [ 4 ]  = p1                           ;
  Points             [ 5 ]  = p2                           ;
  QPolygonF            P    = shape.WideLine(wl.x(),p1,p2) ;
  Points             [ 31]  = P [ 0 ]                      ;
  Points             [ 32]  = P [ 3 ]                      ;
  P <<              P[ 0 ]                                 ;
  path                      . addPolygon ( P )             ;
  Painter . pathes   [ 0 ]  = path                         ;
  Painter . switches [ 0 ]  = true                         ;
}

double N::VcfSlider::Minimum(void)
{
  if (Values.contains(11)) return 0 ;
  return Values [ 11 ]              ;
}

double N::VcfSlider::Maximum(void)
{
  if (Values.contains(12)) return 0 ;
  return Values [ 12 ]              ;
}

void N::VcfSlider::setRange(double minimum,double maximum)
{
  Values[11] = minimum           ;
  Values[12] = maximum           ;
  Values[13] = maximum - minimum ;
  updatePosition (   )           ;
}

void N::VcfSlider::setVisible(double start,double final)
{
  Values[14] = start         ;
  Values[15] = final         ;
  Values[16] = final - start ;
  updatePosition ( )         ;
}

void N::VcfSlider::startPosition(QPointF pos)
{
  if (!Painter.pathes   .contains(1  )) return ;
  if (!Painter.pathes[1].contains(pos)) return ;
  Points[ 2]   = pos                           ;
  Values[24]   = Values[14]                    ;
  Values[25]   = Values[15]                    ;
  Values[26]   = Values[16]                    ;
  Values[34]   = Value(pos)                    ;
  emit Visible ( Values[14] , Values[15] ,0 )  ;
}

void N::VcfSlider::setPosition(QPointF pos)
{
  if (!Points.contains(2)) return ;
  Points [ 3]    = pos            ;
  Values [35]    = Value(pos)     ;
  double minimum = Values[11]     ;
  double maximum = Values[12]     ;
  double start   = Values[24]     ;
  double final   = Values[25]     ;
  double range   = Values[26]     ;
  double drag    = Values[34]     ;
  double fetch   = Values[35]     ;
  fetch         -= drag           ;
  start         += fetch          ;
  final         += fetch          ;
  if (start<minimum)              {
    start = minimum               ;
    final = start + range         ;
  }                               ;
  if (final>maximum)              {
    final = maximum               ;
    start = final - range         ;
  }                               ;
  Values [14]    = start          ;
  Values [15]    = final          ;
  updatePosition ( )              ;
  emit Visible ( start,final,1 )  ;
}

void N::VcfSlider::endPosition(void)
{
  updatePosition  (   )                          ;
  Points . remove ( 2 )                          ;
  Points . remove ( 3 )                          ;
  if (!Values.contains(14)) return               ;
  if (!Values.contains(15)) return               ;
  emit Visible ( Values [14] , Values [15] , 2 ) ;
}

double N::VcfSlider::Value(QPointF pos)
{
  QPointF dp = Points[5] - Points[4] ;
  double  oa = dp.x() * dp.x()       ;
  double  ob                         ;
  oa        += dp.y() * dp.y()       ;
  ob         = sqrt(oa)              ;
  if (ob<0.000001) return Values[11] ;
  dp        /= ob                    ;
  QPointF ds = pos       - Points[4] ;
  double  dr = ds . x () * dp . x () ;
  dr        += ds . y () * dp . y () ;
  dr        /= ob                    ;
  double  range = Values[13]         ;
  dr *= range                        ;
  return Values[11] + dr             ;
}

void N::VcfSlider::updatePosition(void)
{
  if (!Values.contains(11)) return             ;
  if (!Values.contains(12)) return             ;
  if (!Values.contains(13)) return             ;
  if (!Values.contains(14)) return             ;
  if (!Values.contains(15)) return             ;
  //////////////////////////////////////////////
  QPainterPath path                            ;
  VcfShape     shape                           ;
  QPointF p0 = Points[ 4]                      ;
  QPointF dp = Points[ 5] - p0                 ;
  double  wi = Values[ 3]                      ;
  double  wr = Values[13]                      ;
  double  ws = Values[14] - Values[11]         ;
  double  wf = Values[15] - Values[11]         ;
  ws /= wr                                     ;
  wf /= wr                                     ;
  QPointF p1 = dp                              ;
  QPointF p2 = dp                              ;
  p1 *= ws                                     ;
  p2 *= wf                                     ;
  p1 += p0                                     ;
  p2 += p0                                     ;
  Points [ 6 ] = p1                            ;
  Points [ 7 ] = p2                            ;
  //////////////////////////////////////////////
  QPolygonF P = shape.WideLine(wi,p1,p2)       ;
  Points [ 41]  = P [ 0 ]                      ;
  Points [ 42]  = P [ 3 ]                      ;
  P <<  P[ 0 ]                                 ;
  path                      . addPolygon ( P ) ;
  Painter . pathes   [ 1 ]  = path             ;
  Painter . switches [ 1 ]  = true             ;
  update ( )                                   ;
  //////////////////////////////////////////////
  QString M = QString(ToolTip                  )
              .arg(Values[14]                  )
              .arg(Values[15]                  )
              .arg(Values[11]                  )
              .arg(Values[12]                ) ;
  QToolTip :: showText ( QCursor::pos() , M  ) ;
}
"""

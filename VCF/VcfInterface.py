# -*- coding: utf-8 -*-
##############################################################################
## VcfInterface
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
from         . VcfCanvas              import VcfCanvas as VcfCanvas
##############################################################################
class VcfInterface    ( VcfCanvas                                          ) :
  ############################################################################
  def __init__        ( self                                               , \
                        parent = None                                      , \
                        item   = None                                      , \
                        plan   = None                                      ) :
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
class Q_COMPONENTS_EXPORT VcfInterface : public VcfCanvas
{
  Q_OBJECT
  public:

    bool    showHeader       ;
    QRectF  HeaderRect       ;
    QString Title            ;

    enum { Type = UserType + VCF::Interface } ;
    virtual int type(void) const { return Type; }

    explicit VcfInterface              (QObject       * parent       ,
                                        QGraphicsItem * item         ,
                                        Plan          * plan = NULL) ;
    virtual ~VcfInterface              (void) ;

    virtual QPainterPath shape         (void) const ;

    QRect mapToPixel                   (QRectF rect) ;

  protected:

    QMap<int,double> Margins ;

    virtual void Configure             (void) ;

    virtual QVariant itemChange        (GraphicsItemChange change,const QVariant & value);

    virtual void hoverEnterEvent       (QGraphicsSceneHoverEvent * event);
    virtual void hoverLeaveEvent       (QGraphicsSceneHoverEvent * event);
    virtual void hoverMoveEvent        (QGraphicsSceneHoverEvent * event);
    virtual void Hovering              (QPointF pos);

    virtual void contextMenuEvent      (QGraphicsSceneContextMenuEvent * event) ;
    virtual void mouseDoubleClickEvent (QGraphicsSceneMouseEvent * event) ;
    virtual void mouseMoveEvent        (QGraphicsSceneMouseEvent * event);
    virtual void mousePressEvent       (QGraphicsSceneMouseEvent * event);
    virtual void mouseReleaseEvent     (QGraphicsSceneMouseEvent * event);

    virtual bool CursorMoving          (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeStart           (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeMoving          (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeFinish          (QGraphicsSceneMouseEvent * event) ;

    virtual bool ResizeWidget          (void) ;

  private:

  public slots:

    virtual void Paint                 (QPainter * painter,QRectF  Region,bool clip,bool color) ;
    virtual void setWidget             (QWidget  * widget ,QPointF CM,QRect Frame,QRect Child) ;
    virtual void setChild              (QWidget  * widget ,QPointF CM,QRect Frame,QRect Child) ;

    virtual void AdjustHeader          (void) ;
    virtual void Finish                (void) ;

  protected slots:

    virtual bool InterfaceMenu         (QPointF pos) ;

  private slots:

  signals:

    void Resized                       (VcfItem * item) ;
    void Finish                        (VcfItem * item) ;

};


N::VcfInterface:: VcfInterface (QObject * parent,QGraphicsItem * item,Plan * p)
                : VcfCanvas    (          parent,                item,       p)
                , showHeader   (false                                         )
                , Title        (""                                            )
{
  Configure ( ) ;
}

N::VcfInterface::~VcfInterface(void)
{
}

QPainterPath N::VcfInterface::shape(void) const
{
  if ( Painter . pathes . contains ( 0 ) ) {
    return Painter . pathes [ 0 ]          ;
  }                                        ;
  //////////////////////////////////////////
  QPainterPath path                        ;
  path . addRect ( ScreenRect )            ;
  return path                              ;
}

void N::VcfInterface::Configure(void)
{
  Printable = true                                      ;
  Scaling   = true                                      ;
  Editable  = true                                      ;
  ///////////////////////////////////////////////////////
  setFlag ( ItemIsMovable                 , true  )     ;
  setFlag ( ItemIsSelectable              , true  )     ;
  setFlag ( ItemIsFocusable               , true  )     ;
  setFlag ( ItemClipsToShape              , false )     ;
  setFlag ( ItemClipsChildrenToShape      , false )     ;
  setFlag ( ItemIgnoresParentOpacity      , true  )     ;
  setFlag ( ItemSendsGeometryChanges      , true  )     ;
  setFlag ( ItemSendsScenePositionChanges , true  )     ;
  setFlag ( ItemAcceptsInputMethod        , false )     ;
  ///////////////////////////////////////////////////////
  setOpacity (1.0)                                      ;
  Painter . addMap   ( "Default" , 0                  ) ;
  Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 ) ) ;
  Painter . addPen   ( 1 , QColor (   0 ,   0 ,   0 ) ) ;
  Painter . addBrush ( 0 , QColor ( 255 , 255 , 255 ) ) ;
  Painter . addBrush ( 1 , QColor (   0 ,   0 ,   0 ) ) ;
}

QVariant N::VcfInterface::itemChange(GraphicsItemChange change,const QVariant & value)
{
  switch (change)                                {
    case ItemPositionChange                      :
    case ItemPositionHasChanged                  :
      if (NotNull(Options))                      {
        QPointF p = QGraphicsItem::pos()         ;
        PaperPos = Options->Standard(p)          ;
        ResizeWidget ( )                         ;
      }                                          ;
    break                                        ;
    case ItemSelectedHasChanged                  :
    break                                        ;
  }                                              ;
  return QGraphicsItem::itemChange(change,value) ;
}

void N::VcfInterface::hoverEnterEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverEnterEvent(event);
  if (!Scaling) return;
}

void N::VcfInterface::hoverLeaveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverLeaveEvent(event);
  if (!Scaling) return;
  setCursor(Qt::ArrowCursor);
}

void N::VcfInterface::hoverMoveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverMoveEvent(event) ;
  Hovering (event->pos())              ;
  if (!Scaling) return                 ;
  int Corner = atCorner(event->pos())  ;
  switch (Corner)                      {
    case TopLeft                       :
    case TopRight                      :
    case BottomLeft                    :
    case BottomRight                   :
    case LeftSide                      :
    case RightSide                     :
    case TopSide                       :
    case BottomSide                    :
      setCornerCursor(Corner)          ;
    break                              ;
    default                            :
      setCursor ( Qt::OpenHandCursor ) ;
    return                             ;
  }                                    ;
}

void N::VcfInterface::Hovering(QPointF pos)
{
}

void N::VcfInterface::contextMenuEvent(QGraphicsSceneContextMenuEvent * e)
{
  if (   isFunction ( 32001 ) )               {
    QGraphicsItem::contextMenuEvent ( e )     ;
  } else                                      {
    if ( isFunction ( 32002 ) )               {
      if ( InterfaceMenu ( e -> pos ( ) ) )   {
        e -> accept ( )                       ;
      } else                                  {
        QGraphicsItem::contextMenuEvent ( e ) ;
      }                                       ;
    }                                         ;
    e -> accept ( )                           ;
  }                                           ;
}

void N::VcfInterface::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
{
  QGraphicsItem::mouseDoubleClickEvent(event) ;
}

void N::VcfInterface::mousePressEvent(QGraphicsSceneMouseEvent * event)
{
  if (Scaling && IsMask(event->buttons(),Qt::LeftButton)) {
    if (ResizeStart ( event ) ) event -> accept () ; else {
      QGraphicsItem::mousePressEvent(event)               ;
    }                                                     ;
  } else                                                  {
    QGraphicsItem::mousePressEvent(event)                 ;
  }                                                       ;
}

void N::VcfInterface::mouseMoveEvent(QGraphicsSceneMouseEvent * event)
{
  if (Scaling && IsMask(event->buttons(),Qt::LeftButton))  {
    if (ResizeMoving ( event ) ) event -> accept () ; else {
      QGraphicsItem::mouseMoveEvent(event)                 ;
    }                                                      ;
  } else if (Scaling)                                      {
    if (CursorMoving ( event ) ) event->accept () ; else   {
      QGraphicsItem::mouseMoveEvent(event)                 ;
    }                                                      ;
  } else QGraphicsItem::mouseMoveEvent(event)              ;
}

void N::VcfInterface::mouseReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  if (Markers[0]==1) ResizeFinish(event) ;
  QGraphicsItem::mouseReleaseEvent(event);
}

bool N::VcfInterface::CursorMoving(QGraphicsSceneMouseEvent * event)
{
  int Corner = atCorner(event->pos())         ;
  switch (Corner)                             {
    case NoSide                               :
      setCursor(Qt::ArrowCursor    )          ;
    break                                     ;
    case TopLeft                              :
      if ( ! isFunction(33005) ) return false ;
      setCursor(Qt::SizeFDiagCursor)          ;
    return true                               ;
    case TopRight                             :
      if ( ! isFunction(33006) ) return false ;
      setCursor(Qt::SizeBDiagCursor)          ;
    return true                               ;
    case BottomLeft                           :
      if ( ! isFunction(33007) ) return false ;
      setCursor(Qt::SizeBDiagCursor)          ;
    return true                               ;
    case BottomRight                          :
      if ( ! isFunction(33008) ) return false ;
      setCursor(Qt::SizeFDiagCursor)          ;
    return true                               ;
    case LeftSide                             :
      if ( ! isFunction(33001) ) return false ;
      setCursor(Qt::SizeHorCursor  )          ;
    return true                               ;
    case RightSide                            :
      if ( ! isFunction(33002) ) return false ;
      setCursor(Qt::SizeHorCursor  )          ;
    return true                               ;
    case TopSide                              :
      if ( ! isFunction(33003) ) return false ;
      setCursor(Qt::SizeVerCursor  )          ;
    return true                               ;
    case BottomSide                           :
      if ( ! isFunction(33004) ) return false ;
      setCursor(Qt::SizeVerCursor  )          ;
    return true                               ;
    default                                   :
      setCursor(Qt::OpenHandCursor )          ;
    break                                     ;
  }                                           ;
  return false                                ;
}

bool N::VcfInterface::ResizeStart(QGraphicsSceneMouseEvent * event)
{
  int Corner = atCorner(event->pos())                ;
  switch (Corner)                                    {
    case NoSide                                      :
      setCursor(Qt::ArrowCursor    )                 ;
      Markers    [0] = 0                             ;
      Markers    [1] = NoSide                        ;
      Rectangles [0] = ScreenRect                    ;
      Rectangles [9] = HeaderRect                    ;
    return false                                     ;
    case TopLeft                                     :
      if ( isFunction ( 33005 ) )                    {
        setCursor(Qt::SizeFDiagCursor)               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . topLeft     () ;
        Points     [3] = ScreenRect . bottomRight () ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case TopRight                                    :
      if ( isFunction ( 33006 ) )                    {
        setCursor(Qt::SizeBDiagCursor)               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . topRight   ()  ;
        Points     [3] = ScreenRect . bottomLeft ()  ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case BottomLeft                                  :
      if ( isFunction ( 33007 ) )                    {
        setCursor(Qt::SizeBDiagCursor)               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . bottomLeft ()  ;
        Points     [3] = ScreenRect . topRight   ()  ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case BottomRight                                 :
      if ( isFunction ( 33008 ) )                    {
        setCursor(Qt::SizeFDiagCursor)               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . bottomRight () ;
        Points     [3] = ScreenRect . topLeft     () ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case LeftSide                                    :
      if ( isFunction ( 33001 ) )                    {
        setCursor(Qt::SizeHorCursor  )               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . topLeft  ()    ;
        Points     [3] = ScreenRect . topRight ()    ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case RightSide                                   :
      if ( isFunction ( 33002 ) )                    {
        setCursor(Qt::SizeHorCursor  )               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . topRight ()    ;
        Points     [3] = ScreenRect . topLeft  ()    ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case TopSide                                     :
      if ( isFunction ( 33003 ) )                    {
        setCursor(Qt::SizeVerCursor  )               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . topLeft    ()  ;
        Points     [3] = ScreenRect . bottomLeft ()  ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case BottomSide                                  :
      if ( isFunction ( 33004 ) )                    {
        setCursor(Qt::SizeVerCursor  )               ;
        Markers    [0] = 1                           ;
        Markers    [1] = Corner                      ;
        Points     [0] = event->pos()                ;
        Points     [2] = ScreenRect . bottomLeft ()  ;
        Points     [3] = ScreenRect . topLeft    ()  ;
        Rectangles [0] = ScreenRect                  ;
        Rectangles [9] = HeaderRect                  ;
        return true                                  ;
      }                                              ;
    return false                                     ;
    case Inside                                      :
      Markers    [0] = 0                             ;
      Markers    [1] = Inside                        ;
      Rectangles [0] = ScreenRect                    ;
      Rectangles [9] = HeaderRect                    ;
      setCursor(Qt::OpenHandCursor )                 ;
    return false                                     ;
  }                                                  ;
  return false                                       ;
}

bool N::VcfInterface::ResizeMoving(QGraphicsSceneMouseEvent * event)
{
  int     Corner = Markers [1]                       ;
  QPointF P1                                         ;
  QPointF P2                                         ;
  switch (Corner)                                    {
    case TopLeft                                     :
    case TopRight                                    :
    case BottomLeft                                  :
    case BottomRight                                 :
      Points [1] = event -> pos ()                   ;
      P1         = Points[2] + Points[1] - Points[0] ;
      P2         = Points[3]                         ;
      ResizeRect   ( P1 , P2 )                       ;
      ResizeWidget (         )                       ;
    return true                                      ;
    case LeftSide                                    :
    case RightSide                                   :
      Points [1] = event -> pos ()                   ;
      P1         = Points[2] + Points[1] - Points[0] ;
      P2         = Points[3]                         ;
      ResizeWidth  ( P1 , P2 )                       ;
      ResizeWidget (         )                       ;
    return true                                      ;
    case TopSide                                     :
    case BottomSide                                  :
      Points [1] = event -> pos ()                   ;
      P1         = Points[2] + Points[1] - Points[0] ;
      P2         = Points[3]                         ;
      ResizeHeight ( P1 , P2 )                       ;
      ResizeWidget (         )                       ;
    return true                                      ;
    case Inside                                      :
    return false                                     ;
    case NoSide                                      :
    break                                            ;
  }                                                  ;
  return false                                       ;
}

bool N::VcfInterface::ResizeFinish(QGraphicsSceneMouseEvent * event)
{
  if (Markers[0]==0) return false            ;
  PaperRect  = Options->Standard(ScreenRect) ;
  Markers[0] = 0                             ;
  setCursor             ( Qt::ArrowCursor )  ;
  prepareGeometryChange (                 )  ;
  update                (                 )  ;
  return true                                ;
}

void N::VcfInterface::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  pushPainters       ( p                                               ) ;
  Painter . drawRect ( p , "Default" , ScreenRect                      ) ;
  if ( showHeader && ( Title . length ( ) > 0 )                        ) {
    QRectF HR                                                            ;
    HR . setLeft     ( ScreenRect . left   ( ) + HeaderRect . left ( ) ) ;
    HR . setTop      ( ScreenRect . top    ( ) + HeaderRect . top  ( ) ) ;
    HR . setWidth    ( HeaderRect . width  ( )                         ) ;
    HR . setHeight   ( HeaderRect . height ( )                         ) ;
    p -> setPen      ( Painter.pens   [1]                              ) ;
    p -> setBrush    ( Painter.brushes[1]                              ) ;
    p -> drawText    ( HR , Qt::AlignCenter , Title                    ) ;
  }                                                                      ;
  popPainters        ( p                                               ) ;
}

bool N::VcfInterface::ResizeWidget(void)
{
  QRectF  WR                                                    ;
  WR . setLeft   ( ScreenRect . left   () + Margins [0] )       ;
  WR . setTop    ( ScreenRect . top    () + Margins [1] )       ;
  WR . setRight  ( ScreenRect . right  () - Margins [2] )       ;
  WR . setBottom ( ScreenRect . bottom () - Margins [3] )       ;
  if ( Proxys . contains ( 0 ) )                                {
    Proxys [ 0 ] -> setGeometry ( WR )                          ;
  } else
  if (Widgets.contains(0))                                      {
    QRectF sc = mapToScene(WR).boundingRect()                   ;
    QRect  sr = GraphicsView()->mapFromScene(sc).boundingRect() ;
    Widgets [ 0 ] -> setGeometry ( sr )                         ;
    emit Resized ( this )                                       ;
  }                                                             ;
  HeaderRect . setWidth  ( WR . width  ( ) )                    ;
  update ( )                                                    ;
  if ( Proxys . contains ( 0 ) ) Proxys [ 0 ] -> update ( )     ;
  return true                                                   ;
}

void N::VcfInterface::setWidget(QWidget * widget,QPointF CM,QRect Frame,QRect Child)
{
  if (IsNull(Options)) return                                    ;
  QGraphicsItem::setPos(Options->position(CM))                   ;
  ////////////////////////////////////////////////////////////////
  QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget (this) ;
  proxy -> setFlag   ( ItemAcceptsInputMethod , true )           ;
  proxy -> setWidget ( widget                        )           ;
  Proxys  [ 0 ] = proxy                                          ;
  Widgets [ 0 ] = widget                                         ;
  ////////////////////////////////////////////////////////////////
  Margins [ 0 ] = Child . left   () - Frame . left   ()          ;
  Margins [ 1 ] = Child . top    () - Frame . top    ()          ;
  Margins [ 2 ] = Frame . right  () - Child . right  ()          ;
  Margins [ 3 ] = Frame . bottom () - Child . bottom ()          ;
  ////////////////////////////////////////////////////////////////
  QRectF FF = Frame                                              ;
  QRectF SR                                                      ;
  QTransform T                                                   ;
  T . reset()                                                    ;
  SR = GraphicsView() -> mapToScene ( Frame ) . boundingRect ( ) ;
  SR = mapFromScene ( SR ) . boundingRect ( )                    ;
  double sx = SR . width  ( )                                    ;
  double sy = SR . height ( )                                    ;
  sx /= FF . width  ( )                                          ;
  sy /= FF . height ( )                                          ;
  T . scale ( sx , sy )                                          ;
  setTransform ( T )                                             ;
  Options -> ScaleRatio = QSizeF ( sx , sy )                     ;
  ////////////////////////////////////////////////////////////////
  ScreenRect = FF                                                ;
  proxy     -> setGeometry ( Child )                             ;
  proxy     -> setOpacity  ( 1.00  )                             ;
  proxy     -> setZValue   ( 1.00  )                             ;
  ////////////////////////////////////////////////////////////////
  prepareGeometryChange (  )                                     ;
}

void N::VcfInterface::setChild(QWidget * widget,QPointF CM,QRect Frame,QRect Child)
{
  if (IsNull(Options)) return                                    ;
  QGraphicsItem::setPos(Options->position(CM))                   ;
  ////////////////////////////////////////////////////////////////
  Widgets [ 0 ] = widget                                         ;
  ////////////////////////////////////////////////////////////////
  Margins [ 0 ] = Child . left   () - Frame . left   ()          ;
  Margins [ 1 ] = Child . top    () - Frame . top    ()          ;
  Margins [ 2 ] = Frame . right  () - Child . right  ()          ;
  Margins [ 3 ] = Frame . bottom () - Child . bottom ()          ;
  ////////////////////////////////////////////////////////////////
  QRectF FF = Frame                                              ;
  QRectF SR                                                      ;
  QTransform T                                                   ;
  T . reset()                                                    ;
  SR = GraphicsView() -> mapToScene ( Frame ) . boundingRect ( ) ;
  SR = mapFromScene ( SR ) . boundingRect ( )                    ;
  double sx = SR . width  ( )                                    ;
  double sy = SR . height ( )                                    ;
  sx /= FF . width  ( )                                          ;
  sy /= FF . height ( )                                          ;
  T . scale ( sx , sy )                                          ;
  setTransform ( T )                                             ;
  Options -> ScaleRatio = QSizeF ( sx , sy )                     ;
  ////////////////////////////////////////////////////////////////
  ScreenRect = FF                                                ;
  QRectF sc = mapToScene(Child).boundingRect()                   ;
  QRect  sr = GraphicsView()->mapFromScene(sc).boundingRect()    ;
  Widgets [ 0 ] -> setGeometry ( sr )                            ;
  ////////////////////////////////////////////////////////////////
  prepareGeometryChange (  )                                     ;
}

void N::VcfInterface::AdjustHeader(void)
{
  ResizeWidget ( ) ;
}

void N::VcfInterface::Finish(void)
{
  DeleteGadgets (      ) ;
  emit Finish   ( this ) ;
}

QRect N::VcfInterface::mapToPixel(QRectF rect)
{
  QRect    RR                                  ;
  QPolygon PR                                  ;
  PR = GraphicsView() -> mapFromScene ( rect ) ;
  RR = PR . boundingRect ( )                   ;
  return RR                                    ;
}

bool N::VcfInterface::InterfaceMenu(QPointF)
{
  nScopedMenu  (mm,GraphicsView()) ;
  QAction    * aa                  ;
  mm . add     ( 101,tr("Close") ) ;
  mm . setFont ( plan            ) ;
  aa = mm.exec ( QCursor::pos () ) ;
  if (IsNull(aa)) return true      ;
  switch (mm[aa])                  {
    case 101                       :
      Finish ( )                   ;
    break                          ;
  }                                ;
  return true                      ;
}
"""

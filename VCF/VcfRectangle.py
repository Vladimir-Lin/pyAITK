# -*- coding: utf-8 -*-
##############################################################################
## VcfRectangle
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
class VcfRectangle    (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfRectangle : public VcfItem
{
  Q_OBJECT
  public:

    QPointF    PaperPos   ;
    QRectF     PaperRect  ;
    QRectF     ScreenRect ;
    bool       Scaling    ;
    bool       Editing    ;
    double     Angle      ;
    QTransform Transform  ;

    enum { Type = UserType + VCF::Rectangle } ;
    virtual int type(void) const { return Type ; }

    explicit VcfRectangle          (QObject       * parent        ,
                                    QGraphicsItem * item          ,
                                    Plan          * plan = NULL ) ;
    virtual ~VcfRectangle          (void);

    virtual QRectF  boundingRect   (void) const;
    virtual QSizeF  PaperSize      (void) const;
    virtual QPointF PaperMiddle    (void) const;
    virtual QRectF  PaperRange     (void) const;

    QLineEdit     * NewLineEdit    (int Id) ;
    QComboBox     * NewComboBox    (int Id) ;

  protected:

    enum CornerPosition {
      NoSide      = 0   ,
      TopLeft     = 1   ,
      TopRight    = 2   ,
      BottomLeft  = 3   ,
      BottomRight = 4   ,
      LeftSide    = 5   ,
      RightSide   = 6   ,
      TopSide     = 7   ,
      BottomSide  = 8   ,
      Inside      = 9 } ;

    VcfProxys     Proxys     ;
    VcfWidgets    Widgets    ;
    VcfPoints     Points     ;
    VcfRectangles Rectangles ;
    IMAPs         Markers    ;

    virtual QVariant itemChange    (GraphicsItemChange change  ,
                                    const QVariant   & value ) ;

    virtual int  atCorner          (QPointF pos);

    virtual void hoverEnterEvent   (QGraphicsSceneHoverEvent * event);
    virtual void hoverLeaveEvent   (QGraphicsSceneHoverEvent * event);
    virtual void hoverMoveEvent    (QGraphicsSceneHoverEvent * event);

    virtual void Hovering          (QPointF pos);
    virtual void setCornerCursor   (int corner);

    virtual bool CursorMoving      (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeStart       (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeMoving      (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeFinish      (QGraphicsSceneMouseEvent * event) ;

    virtual void ResizeRect        (QPointF P1,QPointF P2) ;
    virtual void ResizeWidth       (QPointF P1,QPointF P2) ;
    virtual void ResizeHeight      (QPointF P1,QPointF P2) ;

    virtual void scalePressEvent   (QGraphicsSceneMouseEvent * event) ;
    virtual void scaleMoveEvent    (QGraphicsSceneMouseEvent * event) ;
    virtual void scaleReleaseEvent (QGraphicsSceneMouseEvent * event) ;

    void DeleteGadgets             (void);
    void AttachZLevel              (void);
    void AttachOpacity             (void);
    void AttachRotation            (void);

    virtual void MountZLevel       (QGraphicsProxyWidget * proxy,QSlider * slider);
    virtual void MountOpacity      (QGraphicsProxyWidget * proxy,QSlider * slider);
    virtual void MountRotation     (QGraphicsProxyWidget * proxy,QDial   * dial  );
    virtual void RotationUpdated   (void);

  private:

  public slots:

    virtual void setPos            (QPointF CM);
    virtual void setRect           (QRectF  Region);
    virtual void setRange          (QRectF  paper);

  protected slots:

    void modifyZLevel              (int Z);
    void modifyOpacity             (int Opacity);
    void modifyRotation            (int Rotation);

  private slots:

  signals:

    void GeometryChanged           (VcfItem * item) ;

};

#pragma message("VcfRectangle is needed to fix the top/bottom resize problem")

N::VcfRectangle:: VcfRectangle (QObject * parent,QGraphicsItem * item,Plan * p)
                : VcfItem      (          parent,                item,       p)
                , Scaling      (false                                         )
                , Editing      (false                                         )
                , Angle        (0.0                                           )
{
  Markers [ 0 ] = 0             ;
  ///////////////////////////////
  setFunction ( 32001 , false ) ;
  setFunction ( 32002 , true  ) ;
  ///////////////////////////////
  setFunction ( 33001 , true  ) ;
  setFunction ( 33002 , true  ) ;
  setFunction ( 33003 , true  ) ;
  setFunction ( 33004 , true  ) ;
  setFunction ( 33005 , true  ) ;
  setFunction ( 33006 , true  ) ;
  setFunction ( 33007 , true  ) ;
  setFunction ( 33008 , true  ) ;
}

N::VcfRectangle::~VcfRectangle (void)
{
}

QRectF N::VcfRectangle::boundingRect (void) const
{
  return ScreenRect ;
}

QSizeF N::VcfRectangle::PaperSize(void) const
{
  return QSizeF ( PaperRect . width ( ) , PaperRect . height ( ) ) ;
}

QPointF N::VcfRectangle::PaperMiddle(void) const
{
  return QPointF ( PaperRect . width ( ) / 2 , PaperRect . height ( ) / 2 ) ;
}

QRectF N::VcfRectangle::PaperRange(void) const
{
  return QRectF ( PaperPos , PaperSize ( ) ) ;
}

void N::VcfRectangle::setPos(QPointF CM)
{
  PaperPos = CM                                        ;
  if ( IsNull ( Options ) ) return                     ;
  QGraphicsItem::setPos ( Options -> position ( CM ) ) ;
}

void N::VcfRectangle::setRect(QRectF Region)
{
  PaperRect = Region                        ;
  if (IsNull(Options)) return               ;
  QPointF tl = PaperRect.topLeft     (    ) ;
  QPointF br = PaperRect.bottomRight (    ) ;
  tl = Options->position             ( tl ) ;
  br = Options->position             ( br ) ;
  ScreenRect . setTopLeft            ( tl ) ;
  ScreenRect . setBottomRight        ( br ) ;
  prepareGeometryChange              (    ) ;
}

void N::VcfRectangle::setRange(QRectF paper)
{
  setPos  ( paper.topLeft()                             ) ;
  setRect ( QRectF ( 0,0,paper.width(),paper.height() ) ) ;
}

int N::VcfRectangle::atCorner(QPointF pos)
{
  QRectF Inner(ScreenRect . left  ( ) + 4 , ScreenRect . top    ( ) + 4     ,
               ScreenRect . width ( ) - 8 , ScreenRect . height ( ) - 8 )   ;
  if ( Inner . contains ( pos ) ) return Inside                             ;
  QRectF SS = ScreenRect                                                    ;
  QRectF LT ( SS.left ()   , SS.top   ()   ,            4 ,             4 ) ;
  QRectF RT ( SS.right()-4 , SS.top   ()   ,            4 ,             4 ) ;
  QRectF LB ( SS.left ()   , SS.bottom()-4 ,            4 ,             4 ) ;
  QRectF RB ( SS.right()-4 , SS.bottom()-4 ,            4 ,             4 ) ;
  QRectF LC ( SS.left ()   , SS.top   ()+4 ,            4 , SS.height()-8 ) ;
  QRectF RC ( SS.right()-4 , SS.top   ()+4 ,            4 , SS.height()-8 ) ;
  QRectF TC ( SS.left ()+4 , SS.top   ()   , SS.width()-8 ,             4 ) ;
  QRectF BC ( SS.left ()+4 , SS.bottom()-4 , SS.width()-8 ,             4 ) ;
  if ( LT . contains ( pos ) ) return TopLeft                          ; else
  if ( RT . contains ( pos ) ) return TopRight                         ; else
  if ( LB . contains ( pos ) ) return BottomLeft                       ; else
  if ( RB . contains ( pos ) ) return BottomRight                      ; else
  if ( LC . contains ( pos ) ) return LeftSide                         ; else
  if ( RC . contains ( pos ) ) return RightSide                        ; else
  if ( TC . contains ( pos ) ) return TopSide                          ; else
  if ( BC . contains ( pos ) ) return BottomSide                            ;
  return NoSide                                                             ;
}

void N::VcfRectangle::hoverEnterEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverEnterEvent ( event ) ;
  if ( ! Scaling ) return                  ;
}

void N::VcfRectangle::hoverLeaveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverLeaveEvent ( event ) ;
  if ( ! Scaling ) return                  ;
  setCursor ( Qt::ArrowCursor )            ;
}

void N::VcfRectangle::hoverMoveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverMoveEvent ( event ) ;
  Hovering ( event->pos() )               ;
  if ( ! Scaling ) return                 ;
  int Corner = atCorner  ( event->pos() ) ;
  setCornerCursor        ( Corner       ) ;
}

void N::VcfRectangle::Hovering(QPointF pos)
{
}

void N::VcfRectangle::setCornerCursor(int Corner)
{
  switch (Corner)                       {
    case NoSide                         :
      setCursor(Qt::ArrowCursor    )    ;
    break                               ;
    case TopLeft                        :
      if ( ! isFunction(33005) ) return ;
      setCursor(Qt::SizeFDiagCursor)    ;
    break                               ;
    case TopRight                       :
      if ( ! isFunction(33006) ) return ;
      setCursor(Qt::SizeBDiagCursor)    ;
    break                               ;
    case BottomLeft                     :
      if ( ! isFunction(33007) ) return ;
      setCursor(Qt::SizeBDiagCursor)    ;
    break                               ;
    case BottomRight                    :
      if ( ! isFunction(33008) ) return ;
      setCursor(Qt::SizeFDiagCursor)    ;
    break                               ;
    case LeftSide                       :
      if ( ! isFunction(33001) ) return ;
      setCursor(Qt::SizeHorCursor  )    ;
    break                               ;
    case RightSide                      :
      if ( ! isFunction(33002) ) return ;
      setCursor(Qt::SizeHorCursor  )    ;
    break                               ;
    case TopSide                        :
      if ( ! isFunction(33003) ) return ;
      setCursor(Qt::SizeVerCursor  )    ;
    break                               ;
    case BottomSide                     :
      if ( ! isFunction(33004) ) return ;
      setCursor(Qt::SizeVerCursor  )    ;
    break                               ;
    case Inside                         :
      setCursor(Qt::ArrowCursor    )    ;
    break                               ;
  }                                     ;
}

void N::VcfRectangle::ResizeRect(QPointF P1,QPointF P2)
{
  double x1 = P1 . x     (      )              ;
  double x2 = P2 . x     (      )              ;
  double y1 = P1 . y     (      )              ;
  double y2 = P2 . y     (      )              ;
  double t  = 0                                ;
  if ( x1 > x2 ) { t = x1 ; x1 = x2 ; x2 = t ; }
  if ( y1 > y2 ) { t = y1 ; y1 = y2 ; y2 = t ; }
  ScreenRect . setLeft   ( x1   )              ;
  ScreenRect . setTop    ( y1   )              ;
  ScreenRect . setRight  ( x2   )              ;
  ScreenRect . setBottom ( y2   )              ;
  prepareGeometryChange  (      )              ;
  update                 (      )              ;
  emit GeometryChanged   ( this )              ;
}

void N::VcfRectangle::ResizeWidth(QPointF P1,QPointF P2)
{
  double x1 = P1 . x     (      )              ;
  double x2 = P2 . x     (      )              ;
  double t  = 0                                ;
  if ( x1 > x2 ) { t = x1 ; x1 = x2 ; x2 = t ; }
  ScreenRect . setLeft   ( x1   )              ;
  ScreenRect . setRight  ( x2   )              ;
  prepareGeometryChange  (      )              ;
  update                 (      )              ;
  emit GeometryChanged   ( this )              ;
}

void N::VcfRectangle::ResizeHeight(QPointF P1,QPointF P2)
{
  double y1 = P1 . y     (      )              ;
  double y2 = P2 . y     (      )              ;
  double t  = 0                                ;
  if ( y1 > y2 ) { t = y1 ; y1 = y2 ; y2 = t ; }
  ScreenRect . setTop    ( y1   )              ;
  ScreenRect . setBottom ( y2   )              ;
  prepareGeometryChange  (      )              ;
  update                 (      )              ;
  emit GeometryChanged   ( this )              ;
}

bool N::VcfRectangle::CursorMoving(QGraphicsSceneMouseEvent * event)
{
  int Corner = atCorner ( event->pos() ) ;
  setCornerCursor ( Corner )             ;
  return false                           ;
}

bool N::VcfRectangle::ResizeStart(QGraphicsSceneMouseEvent * event)
{
  int Corner = atCorner(event->pos())                 ;
  switch (Corner)                                     {
    case NoSide                                       :
      setCursor(Qt::ArrowCursor    )                  ;
      Markers [0] = 0                                 ;
      Markers [1] = NoSide                            ;
    return false                                      ;
    case TopLeft                                      :
      if ( isFunction ( 33005 ) )                     {
        setCursor(Qt::SizeFDiagCursor)                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . topLeft     ( ) ;
        Points     [3] = ScreenRect . bottomRight ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case TopRight                                     :
      if ( isFunction ( 33006 ) )                     {
        setCursor(Qt::SizeBDiagCursor)                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . topRight    ( ) ;
        Points     [3] = ScreenRect . bottomLeft  ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case BottomLeft                                   :
      if ( isFunction ( 33007 ) )                     {
        setCursor(Qt::SizeBDiagCursor)                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . bottomLeft  ( ) ;
        Points     [3] = ScreenRect . topRight    ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case BottomRight                                  :
      if ( isFunction ( 33008 ) )                     {
        setCursor(Qt::SizeFDiagCursor)                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . bottomRight ( ) ;
        Points     [3] = ScreenRect . topLeft     ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case LeftSide                                     :
      if ( isFunction ( 33001 ) )                     {
        setCursor(Qt::SizeHorCursor  )                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . topLeft     ( ) ;
        Points     [3] = ScreenRect . topRight    ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case RightSide                                    :
      if ( isFunction ( 33002 ) )                     {
        setCursor(Qt::SizeHorCursor  )                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . topRight    ( ) ;
        Points     [3] = ScreenRect . topLeft     ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case TopSide                                      :
      if ( isFunction ( 33003 ) )                     {
        setCursor(Qt::SizeVerCursor  )                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . topLeft     ( ) ;
        Points     [3] = ScreenRect . bottomLeft  ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case BottomSide                                   :
      if ( isFunction ( 33004 ) )                     {
        setCursor(Qt::SizeVerCursor  )                ;
        Markers    [0] = 1                            ;
        Markers    [1] = Corner                       ;
        Points     [0] = event->pos()                 ;
        Points     [2] = ScreenRect . bottomLeft  ( ) ;
        Points     [3] = ScreenRect . topLeft     ( ) ;
        Rectangles [0] = ScreenRect                   ;
        return true                                   ;
      }                                               ;
    return false                                      ;
    case Inside                                       :
      setCursor(Qt::ArrowCursor    )                  ;
      Markers [0] = 0                                 ;
      Markers [1] = NoSide                            ;
    return false                                      ;
  }                                                   ;
  return false                                        ;
}

bool N::VcfRectangle::ResizeMoving(QGraphicsSceneMouseEvent * event)
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
    return true                                      ;
    case LeftSide                                    :
    case RightSide                                   :
      Points [1] = event -> pos ()                   ;
      P1         = Points[2] + Points[1] - Points[0] ;
      P2         = Points[3]                         ;
      ResizeWidth  ( P1 , P2 )                       ;
    return true                                      ;
    case TopSide                                     :
    case BottomSide                                  :
      Points [1] = event -> pos ()                   ;
      P1         = Points[2] + Points[1] - Points[0] ;
      P2         = Points[3]                         ;
      ResizeHeight ( P1 , P2 )                       ;
    return true                                      ;
    case NoSide                                      :
    break                                            ;
    case Inside                                      :
    break                                            ;
  }                                                  ;
  return false                                       ;
}

bool N::VcfRectangle::ResizeFinish(QGraphicsSceneMouseEvent * event)
{
  if (Markers[0]==0) return false            ;
  PaperRect  = Options->Standard(ScreenRect) ;
  Markers[0] = 0                             ;
  setCursor             ( Qt::ArrowCursor )  ;
  prepareGeometryChange (                 )  ;
  update                (                 )  ;
  emit GeometryChanged  ( this            )  ;
  return true                                ;
}

void N::VcfRectangle::scalePressEvent(QGraphicsSceneMouseEvent * event)
{
  if (Scaling && IsMask(event->buttons(),Qt::LeftButton)) {
    if (ResizeStart ( event ) ) event -> accept () ; else {
      QGraphicsItem::mousePressEvent(event)               ;
    }                                                     ;
  } else                                                  {
    QGraphicsItem::mousePressEvent(event)                 ;
    DeleteGadgets()                                       ;
  }                                                       ;
}

void N::VcfRectangle::scaleMoveEvent(QGraphicsSceneMouseEvent * event)
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

void N::VcfRectangle::scaleReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  if ( 1 == Markers [ 0 ]) ResizeFinish ( event ) ;
  QGraphicsItem::mouseReleaseEvent      ( event ) ;
}

void N::VcfRectangle::DeleteGadgets(void)
{
  CUIDs K = Proxys . keys ( )                ;
  int k                                      ;
  foreach ( k , K )                          {
    scene ( ) -> removeItem ( Proxys [ k ] ) ;
    Proxys [ k ] -> deleteLater ( )          ;
  }                                          ;
  Widgets . clear ( )                        ;
  Proxys  . clear ( )                        ;
  update          ( )                        ;
}

QVariant N::VcfRectangle::itemChange(GraphicsItemChange change,const QVariant &value)
{
  switch ( change )                                   {
    case ItemPositionChange                           :
      emit GeometryChanged ( this )                   ;
    break                                             ;
  }                                                   ;
  return QGraphicsItem::itemChange ( change , value ) ;
}

QLineEdit * N::VcfRectangle::NewLineEdit(int Id)
{
  QLineEdit            * line  = new QLineEdit            (      ) ;
  QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget ( this ) ;
  proxy -> setFlag   ( ItemAcceptsInputMethod , true )             ;
  proxy -> setWidget ( line )                                      ;
  Proxys  [ Id ] = proxy                                           ;
  Widgets [ Id ] = line                                            ;
  return line                                                      ;
}

QComboBox * N::VcfRectangle::NewComboBox(int Id)
{
  QComboBox            * combo = new QComboBox            (      ) ;
  QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget ( this ) ;
  proxy -> setFlag   ( ItemAcceptsInputMethod , true )             ;
  proxy -> setWidget ( combo )                                     ;
  Proxys  [ Id ] = proxy                                           ;
  Widgets [ Id ] = combo                                           ;
  return combo                                                     ;
}

void N::VcfRectangle::AttachZLevel(void)
{
  QSlider              * slider = new QSlider              ( Qt::Horizontal ) ;
  QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( this           ) ;
  proxy  -> setFlag   ( ItemAcceptsInputMethod , true )                       ;
  proxy  -> setWidget ( slider            )                                   ;
  MountZLevel         ( proxy    , slider )                                   ;
  slider -> setRange  ( 0        , 1000   )                                   ;
  slider -> setValue  ( zValue() * 1000   )                                   ;
  nConnect ( slider,SIGNAL(valueChanged(int)),this,SLOT(modifyZLevel(int)) )  ;
}

void N::VcfRectangle::MountZLevel(QGraphicsProxyWidget * proxy,QSlider * slider)
{
}

void N::VcfRectangle::modifyZLevel(int Z)
{
  double z = Z                                              ;
  z /= 1000                                                 ;
  setZValue ( z )                                           ;
  update    (   )                                           ;
  QToolTip::showText ( QCursor::pos(),tr("Z : %1").arg(z) ) ;
}

void N::VcfRectangle::AttachOpacity(void)
{
  QSlider              * slider = new QSlider              ( Qt::Horizontal ) ;
  QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( this           ) ;
  proxy  -> setFlag   ( ItemAcceptsInputMethod , true   )                     ;
  proxy  -> setWidget ( slider                          )                     ;
  MountOpacity        ( proxy , slider                  )                     ;
  slider -> setRange  ( 0 , 1000                        )                     ;
  slider -> setValue  ( QGraphicsItem::opacity() * 1000 )                     ;
  nConnect (slider,SIGNAL(valueChanged(int)),this,SLOT(modifyOpacity(int))  ) ;
}

void N::VcfRectangle::MountOpacity(QGraphicsProxyWidget * proxy,QSlider * slider)
{
}

void N::VcfRectangle::modifyOpacity(int Opacity)
{
  double O = Opacity                                              ;
  O /= 1000                                                       ;
  setOpacity ( O )                                                ;
  update     (   )                                                ;
  QToolTip::showText ( QCursor::pos(),tr("Opacity : %1").arg(O) ) ;
}

void N::VcfRectangle::AttachRotation(void)
{
  QDial                * dial   = new QDial                (      )          ;
  QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( NULL )          ;
  proxy -> setFlag     ( ItemAcceptsInputMethod , true )                     ;
  proxy -> setWidget   ( dial         )                                      ;
  MountRotation        ( proxy , dial )                                      ;
  dial  -> setWrapping ( true         )                                      ;
  dial  -> setRange    ( 0 , 360000   )                                      ;
  dial  -> setValue    ( Angle * 1000 )                                      ;
  nConnect ( dial,SIGNAL(valueChanged(int)),this,SLOT(modifyRotation(int)) ) ;
  scene ( ) -> addItem ( proxy        )                                      ;
}

void N::VcfRectangle::MountRotation(QGraphicsProxyWidget * proxy,QDial * dial)
{
}

void N::VcfRectangle::modifyRotation(int Rotation)
{
  Angle = Rotation                                               ;
  Angle/= 1000                                                   ;
  RotationUpdated ( )                                            ;
  update          ( )                                            ;
  QToolTip::showText(QCursor::pos(),tr("Angle : %1").arg(Angle)) ;
}

void N::VcfRectangle::RotationUpdated(void)
{
}
"""

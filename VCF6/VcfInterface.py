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
import PySide6
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
from           . VcfCanvas import VcfCanvas as VcfCanvas
##############################################################################
class VcfInterface                 ( VcfCanvas                             ) :
  ############################################################################
  def __init__                     ( self                                  , \
                                     parent = None                         , \
                                     item   = None                         , \
                                     plan   = None                         ) :
    ##########################################################################
    super ( ) . __init__           ( parent , item , plan                    )
    self . setVcfInterfaceDefaults (                                         )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfInterfaceDefaults  ( self                                      ) :
    ##########################################################################
    self . showHeader = False
    self . Margins    =        {                                             }
    self . HeaderRect = QRectF (                                             )
    self . Title      = ""
    self . Printable  = True
    self . Scaling    = True
    self . Editable   = True
    ##########################################################################
    self . setFlag ( QGraphicsItem . ItemIsMovable                 , True    )
    self . setFlag ( QGraphicsItem . ItemIsSelectable              , True    )
    self . setFlag ( QGraphicsItem . ItemIsFocusable               , True    )
    self . setFlag ( QGraphicsItem . ItemClipsToShape              , False   )
    self . setFlag ( QGraphicsItem . ItemClipsChildrenToShape      , False   )
    self . setFlag ( QGraphicsItem . ItemIgnoresParentOpacity      , True    )
    self . setFlag ( QGraphicsItem . ItemSendsGeometryChanges      , True    )
    self . setFlag ( QGraphicsItem . ItemSendsScenePositionChanges , True    )
    self . setFlag ( QGraphicsItem . ItemAcceptsInputMethod        , False   )
    ##########################################################################
    self . setOpacity         ( 1.0                                          )
    ##########################################################################
    self . Painter . addMap   ( "Default" , 0                                )
    self . Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 , 255 )         )
    self . Painter . addBrush ( 0 , QColor ( 255 , 255 , 255 , 255 )         )
    ##########################################################################
    self . Painter . addMap   ( "Title" , 1                                  )
    self . Painter . addPen   ( 1 , QColor (   0 ,   0 ,   0 , 255 )         )
    self . Painter . addBrush ( 1 , QColor (   0 ,   0 ,   0 , 255 )         )
    ##########################################################################
    return
  ############################################################################
  def shape                          ( self                                ) :
    ##########################################################################
    if                               ( 0 in self . Painter . pathes        ) :
      return self . Painter . pathes [ 0                                     ]
    ##########################################################################
    path = QPainterPath              (                                       )
    path . addRect                   ( self . ScreenRect                     )
    ##########################################################################
    return path
    ##########################################################################
    return
  ############################################################################
  def mapToPixel                                ( self , rect              ) :
    ##########################################################################
    PR = self . GraphicsView ( ) . mapFromScene (        rect                )
    ##########################################################################
    return PR . boundingRect                    (                            )
  ############################################################################
  def Painting                ( self , p , region , clip , color           ) :
    ##########################################################################
    self . pushPainters       (        p                                     )
    ##########################################################################
    self . Painter . drawRect (        p , "Default" , self . ScreenRect     )
    self . PaintingTitle      (        p , region , clip , color             )
    ##########################################################################
    self . popPainters        (        p                                     )
    ##########################################################################
    return
  ############################################################################
  def PaintingTitle                  ( self , p , region , clip , color    ) :
    ##########################################################################
    if                               ( not self . showHeader               ) :
      return
    ##########################################################################
    if                               ( len ( self . Title ) <= 0           ) :
      return
    ##########################################################################
    HR   = QRectF                    (                                       )
    ##########################################################################
    XX   = self . ScreenRect . left ( ) + self . HeaderRect . left (         )
    YY   = self . ScreenRect . top  ( ) + self . HeaderRect . top  (         )
    ##########################################################################
    HR   . setLeft                   ( XX                                    )
    HR   . setTop                    ( YY                                    )
    HR   . setWidth                  ( self . HeaderRect . width  ( )        )
    HR   . setHeight                 ( self . HeaderRect . height ( )        )
    ##########################################################################
    self . Painter . assignPainterId ( p , 1                                 )
    p    . drawText                  ( HR , Qt . AlignCenter , self . Title  )
    ##########################################################################
    return
  ############################################################################
  """
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
  """
  ############################################################################
  def hoverMoveEvent            ( self , event                             ) :
    ##########################################################################
    super ( ) . hoverMoveEvent  (        event                               )
    ##########################################################################
    self      . Hovering        ( event . pos ( )                            )
    ##########################################################################
    if                          ( not self . Scaling                       ) :
      return
    ##########################################################################
    Corner    = self . atCorner ( event . pos ( )                            )
    ##########################################################################
    DEFs      = [ self . vrTopLeft                                         , \
                  self . vrTopRight                                        , \
                  self . vrBottomLeft                                      , \
                  self . vrBottomRight                                     , \
                  self . vrLeftSide                                        , \
                  self . vrRightSide                                       , \
                  self . vrTopSide                                         , \
                  self . vrBottomSide                                        ]
    ##########################################################################
    if                          ( Corner in DEFs                           ) :
      self    . setCornerCursor ( Corner                                     )
    else                                                                     :
      self    . setCursor       ( Qt . OpenHandCursor                        )
    ##########################################################################
    return
  ############################################################################
  """
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
  """
  ############################################################################
  """
  void N::VcfInterface::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
  {
    QGraphicsItem::mouseDoubleClickEvent(event) ;
  }
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
  void N::VcfInterface::mouseReleaseEvent(QGraphicsSceneMouseEvent * event)
  {
    if (Markers[0]==1) ResizeFinish(event) ;
    QGraphicsItem::mouseReleaseEvent(event);
  }
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
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
  """
  ############################################################################
  """
  void N::VcfInterface::AdjustHeader(void)
  {
    ResizeWidget ( ) ;
  }
  """
  ############################################################################
  """
  void N::VcfInterface::Finish(void)
  {
    DeleteGadgets (      ) ;
    emit Finish   ( this ) ;
  }
  """
  ############################################################################
  """
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
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
"""

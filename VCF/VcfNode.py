# -*- coding: utf-8 -*-
##############################################################################
## VcfNode
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
from   AITK  . Math . Essentials      import Object  as Object
from   AITK  . Math . Node            import Node    as Node
##############################################################################
from                . VcfItem         import VcfItem as VcfItem
##############################################################################
class VcfNode         (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfNode : public VcfItem
                                  , public Object
                                  , public Node
{
  Q_OBJECT
  public:

    enum BorderNames {
      Left   = 1     ,
      Top    = 2     ,
      Right  = 3     ,
      Bottom = 4   } ;

    QPointF    PaperPos      ;
    QRectF     PaperRect     ;
    QRectF     ScreenRect    ;
    QRectF     ParagraphRect ;
    QPolygonF  Lines         ;
    Contour    contour       ;
    double     Angle         ;
    QTransform Transform     ;
    DMAPs      Borders       ;
    int        Mode          ;
    int        Drawing       ;
    int        Alignment     ;
    bool       Scaling       ;
    bool       Bounding      ;
    bool       Editing       ;
    bool       Updated       ;

    enum { Type = UserType + VCF::Node } ;
    virtual int type(void) const { return Type; }

    explicit VcfNode                        (QObject       * parent       ,
                                             QGraphicsItem * item         ,
                                             Plan          * plan = NULL) ;
    virtual ~VcfNode                        (void);

    virtual QRectF       boundingRect       (void) const ;
    virtual QPainterPath shape              (void) const ;
    virtual void         paint              (QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget = 0);

    virtual void setUuid                    (SUID uuid,int type) ;
    virtual bool AttemptMelt                (VcfLinker * Linker,QPointF base) ;
    virtual bool AllowMelts                 (int side) ;

    virtual void settings                   (int item) ;

    QLineEdit *  NewLineEdit                (int Id) ;
    QPointF      PaperPosition              (VcfItem * item,QPointF position) ;

  protected:

    enum CornerPosition  {
      NoSide      =  0   ,
      TopLeft     =  1   ,
      TopRight    =  2   ,
      BottomLeft  =  3   ,
      BottomRight =  4   ,
      LeftSide    =  5   ,
      RightSide   =  6   ,
      TopSide     =  7   ,
      BottomSide  =  8   ,
      Inside      =  9   ,
      Holder      = 10   ,
      Dragger     = 11 } ;

    enum EditWays          {
      EditNothing    = 0   ,
      DragEditing    = 1   ,
      ScaleEditing   = 2   ,
      ContentEditing = 3   ,
      ShapeEditing   = 4   ,
      ConnectEditing = 5 } ;

    VcfProxys     Proxys       ;
    VcfWidgets    Widgets      ;
    VcfPoints     Points       ;
    VcfRectangles Rectangles   ;
    IMAPs         Markers      ;
    BMAPs         AllowCorners ;

    virtual enum EditWays       CastEditing (void) ;
    virtual enum CornerPosition atCorner    (QPointF pos) ;
    virtual void setCornerCursor            (enum CornerPosition corner) ;

    virtual void Configure                  (void) ;

    virtual void hoverEnterEvent            (QGraphicsSceneHoverEvent * event);
    virtual void hoverLeaveEvent            (QGraphicsSceneHoverEvent * event);
    virtual void hoverMoveEvent             (QGraphicsSceneHoverEvent * event);
    virtual void Hovering                   (QPointF pos);

    virtual void contextMenuEvent           (QGraphicsSceneContextMenuEvent * event);
    virtual void mouseDoubleClickEvent      (QGraphicsSceneMouseEvent * event);

    virtual void mousePressEvent            (QGraphicsSceneMouseEvent * event);
    virtual void mouseMoveEvent             (QGraphicsSceneMouseEvent * event);
    virtual void mouseReleaseEvent          (QGraphicsSceneMouseEvent * event);

    virtual void draggingPressEvent         (QGraphicsSceneMouseEvent * event);
    virtual void draggingMoveEvent          (QGraphicsSceneMouseEvent * event);
    virtual void draggingReleaseEvent       (QGraphicsSceneMouseEvent * event);

    virtual void scalePressEvent            (QGraphicsSceneMouseEvent * event);
    virtual void scaleMoveEvent             (QGraphicsSceneMouseEvent * event);
    virtual void scaleReleaseEvent          (QGraphicsSceneMouseEvent * event);

    virtual bool CursorMoving               (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeStart                (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeMoving               (QGraphicsSceneMouseEvent * event) ;
    virtual bool ResizeFinish               (QGraphicsSceneMouseEvent * event) ;

    virtual void ResizeRect                 (QPointF P1,QPointF P2) ;
    virtual void ResizeWidth                (QPointF P1,QPointF P2) ;
    virtual void ResizeHeight               (QPointF P1,QPointF P2) ;
    virtual void NewSize                    (QRectF rect) ;
    virtual void FinalSize                  (void) ;

    virtual void contentPressEvent          (QGraphicsSceneMouseEvent * event);
    virtual void contentMoveEvent           (QGraphicsSceneMouseEvent * event);
    virtual void contentReleaseEvent        (QGraphicsSceneMouseEvent * event);

    virtual void shapePressEvent            (QGraphicsSceneMouseEvent * event);
    virtual void shapeMoveEvent             (QGraphicsSceneMouseEvent * event);
    virtual void shapeReleaseEvent          (QGraphicsSceneMouseEvent * event);

    virtual void connectPressEvent          (QGraphicsSceneMouseEvent * event);
    virtual void connectMoveEvent           (QGraphicsSceneMouseEvent * event);
    virtual void connectReleaseEvent        (QGraphicsSceneMouseEvent * event);

    virtual QVariant itemChange             (GraphicsItemChange change,const QVariant & value);

    virtual bool dropFont                   (QWidget * source,QPointF pos,const SUID font ) ;
    virtual bool dropPen                    (QWidget * source,QPointF pos,const SUID pen  ) ;
    virtual bool dropBrush                  (QWidget * source,QPointF pos,const SUID brush) ;

    virtual void setContour                 (int Id,Contour & contour) ;

  private:

  public slots:

    virtual void Paint                      (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void RenderAppearance           (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void RenderObjects              (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void RenderParagraph            (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void RenderDocument             (QPainter * painter,QRectF Region,bool clip,bool color) ;

    virtual bool FocusIn                    (void) ;
    virtual bool FocusOut                   (void) ;

    virtual void EditMenu                   (MenuManager & menu,QPointF pos) ;
    virtual void RelationMenu               (MenuManager & menu,QPointF pos) ;
    virtual void AdjustmentMenu             (MenuManager & menu,QPointF pos) ;
    virtual void NodeMenu                   (VcfNode * node,QPointF pos) ;
    virtual bool Menu                       (QPointF pos) ;
    virtual bool MenuProcess                (QAction * action,MenuManager & menu) ;

    void         DeleteGadgets              (void) ;

    virtual void setPos                     (QPointF pos) ;
    virtual void setRect                    (QRectF rect) ;
    virtual void setRoundedRect             (QRectF rect,double xRadius,double yRadius) ;
    virtual void setPolygon                 (QPolygonF polygon) ;
    virtual void setContour                 (Contour & contour) ;

    virtual void DisplayBounding            (bool enabled) ;

    virtual bool doubleClicked              (QPointF pos) ;

  protected slots:

    virtual void connectNode                (VcfNode   * node) ;
    virtual void connectLinker              (VcfLinker * linker) ;
    virtual void AcceptAppend               (VcfItem   * item,VcfItem * parent) ;
    virtual void AcceptRemove               (VcfItem   * item) ;
    virtual void AcceptDissolve             (VcfItem   * item) ;
    virtual void AcceptMoving               (VcfItem   * item) ;
    virtual void SignalReceiver             (int command) ;

  private slots:

  signals:

    void Append                             (VcfItem * item,VcfItem * parent) ;
    void Remove                             (VcfItem * item) ;
    void Moving                             (VcfItem * item) ;
    void Menu                               (VcfNode * node,QPointF pos) ;

};

N::VcfNode:: VcfNode       (QObject * parent,QGraphicsItem * item,Plan * p)
           : VcfItem       (          parent,                item,       p)
           , Node          (                                              )
           , Object        (0 , Types::None                               )
           , PaperPos      (QPointF ( 0 , 0         )                     )
           , PaperRect     (QRectF  ( 0 , 0 , 0 , 0 )                     )
           , ScreenRect    (QRectF  ( 0 , 0 , 0 , 0 )                     )
           , ParagraphRect (QRectF  ( 0 , 0 , 0 , 0 )                     )
           , Mode          (0                                             )
           , Drawing       (1                                             )
           , Alignment     (Qt::AlignCenter                               )
           , Scaling       (false                                         )
           , Bounding      (false                                         )
           , Editing       (true                                          )
           , Updated       (false                                         )
           , Angle         (0                                             )
{
  Configure ( ) ;
}

N::VcfNode::~VcfNode (void)
{
}

QRectF N::VcfNode::boundingRect(void) const
{
  if (Painter.pathes.contains(0))           {
    return Painter.pathes[0].boundingRect() ;
  }                                         ;
  return QRectF ( 0 , 0 , 1 , 1 )           ;
}

QPainterPath N::VcfNode::shape(void) const
{
  QPainterPath path               ;
  if (Painter.pathes.contains(0)) {
    path = Painter . pathes [ 0 ] ;
  }                               ;
  return path                     ;
}

void N::VcfNode::paint(QPainter * p,const QStyleOptionGraphicsItem * option,QWidget * widget)
{
  QRectF Z = clipRect (                      ) ;
  Paint               ( p , Z , false , true ) ;
}

void N::VcfNode::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  RenderAppearance ( p , Region , clip , color ) ;
  RenderObjects    ( p , Region , clip , color ) ;
  RenderParagraph  ( p , Region , clip , color ) ;
  RenderDocument   ( p , Region , clip , color ) ;
}

void N::VcfNode::RenderAppearance(QPainter * p,QRectF,bool,bool)
{
  PaintPathes ( p ) ;
}

void N::VcfNode::RenderObjects(QPainter * p,QRectF Region,bool clip,bool color)
{
}

void N::VcfNode::RenderParagraph(QPainter * p,QRectF Region,bool clip,bool color)
{
  if ( name          . length () <=0 ) return               ;
  if ( ParagraphRect . width  () <=0 ) return               ;
  if ( ParagraphRect . height () <=0 ) return               ;
  ///////////////////////////////////////////////////////////
  pushPainters         ( p                                ) ;
  Painter . setPainter ( p , "Text"                       ) ;
  if (Painter.fonts.contains(4))                            {
    Painter.fonts[4].setDPI( Options -> DPI      )          ;
    p -> setFont           ( Painter  . fonts[4] )          ;
  }                                                         ;
  p      -> drawText   ( ParagraphRect , Alignment , name ) ;
  popPainters          ( p                                ) ;
}

void N::VcfNode::RenderDocument(QPainter * p,QRectF Region,bool clip,bool color)
{
}

enum N::VcfNode::EditWays N::VcfNode::CastEditing(void)
{
  if (!Editable             ) return EditNothing ;
  if (!Markers.contains(999)) return EditNothing ;
  return (enum EditWays)Markers[999]             ;
}

enum N::VcfNode::CornerPosition N::VcfNode::atCorner(QPointF pos)
{
  double lp = 4                                                        ;
  double rp = 4                                                        ;
  double tp = 4                                                        ;
  double bp = 4                                                        ;
  //////////////////////////////////////////////////////////////////////
  QPointF W (Borders[Left ],Borders[Top   ])                           ;
  QPointF E (Borders[Right],Borders[Bottom])                           ;
  if (NotNull(Options))                                                {
    W = Options->position(W)                                           ;
    E = Options->position(E)                                           ;
    lp = W . x ( )                                                     ;
    tp = W . y ( )                                                     ;
    rp = E . x ( )                                                     ;
    bp = E . y ( )                                                     ;
  }                                                                    ;
  //////////////////////////////////////////////////////////////////////
  double ha = tp + bp                                                  ;
  double wa = lp + rp                                                  ;
  QRectF Inner(ScreenRect.left ()+lp,ScreenRect.top   ()+tp            ,
               ScreenRect.width()-wa,ScreenRect.height()-ha          ) ;
  if (Inner.contains(pos)) return Inside                               ;
  //////////////////////////////////////////////////////////////////////
  QRectF SS = ScreenRect                                               ;
  QRectF LT(SS.left ()   ,SS.top   ()   ,           lp,            tp) ;
  QRectF RT(SS.right()-rp,SS.top   ()   ,           rp,            tp) ;
  QRectF LB(SS.left ()   ,SS.bottom()-bp,           lp,            bp) ;
  QRectF RB(SS.right()-rp,SS.bottom()-bp,           rp,            bp) ;
  QRectF LC(SS.left ()   ,SS.top   ()+tp,           lp,SS.height()-ha) ;
  QRectF RC(SS.right()-rp,SS.top   ()+tp,           rp,SS.height()-ha) ;
  QRectF TC(SS.left ()+lp,SS.top   ()   ,SS.width()-wa,            tp) ;
  QRectF BC(SS.left ()+lp,SS.bottom()-bp,SS.width()-wa,            bp) ;
  //////////////////////////////////////////////////////////////////////
  if (LT.contains(pos)) return TopLeft                                 ;
  if (RT.contains(pos)) return TopRight                                ;
  if (LB.contains(pos)) return BottomLeft                              ;
  if (RB.contains(pos)) return BottomRight                             ;
  if (LC.contains(pos)) return LeftSide                                ;
  if (RC.contains(pos)) return RightSide                               ;
  if (TC.contains(pos)) return TopSide                                 ;
  if (BC.contains(pos)) return BottomSide                              ;
  return NoSide                                                        ;
}

void N::VcfNode::setCornerCursor(enum CornerPosition Corner)
{
  if (!AllowCorners[Corner]) return    ;
  switch (Corner)                      {
    case NoSide                        :
      setCursor(Qt::ArrowCursor      ) ;
    break                              ;
    case TopLeft                       :
      setCursor(Qt::SizeFDiagCursor  ) ;
    break                              ;
    case TopRight                      :
      setCursor(Qt::SizeBDiagCursor  ) ;
    break                              ;
    case BottomLeft                    :
      setCursor(Qt::SizeBDiagCursor  ) ;
    break                              ;
    case BottomRight                   :
      setCursor(Qt::SizeFDiagCursor  ) ;
    break                              ;
    case LeftSide                      :
      setCursor(Qt::SizeHorCursor    ) ;
    break                              ;
    case RightSide                     :
      setCursor(Qt::SizeHorCursor    ) ;
    break                              ;
    case TopSide                       :
      setCursor(Qt::SizeVerCursor    ) ;
    break                              ;
    case BottomSide                    :
      setCursor(Qt::SizeVerCursor    ) ;
    break                              ;
    case Inside                        :
      setCursor(Qt::ArrowCursor      ) ;
    break                              ;
    case Holder                        :
      setCursor(Qt::OpenHandCursor   ) ;
    break                              ;
    case Dragger                       :
      setCursor(Qt::ClosedHandCursor ) ;
    break                              ;
  }                                    ;
}

void N::VcfNode::Configure(void)
{
  Transform . reset (                                  ) ;
  ////////////////////////////////////////////////////////
  Editable           = true                              ;
  Borders [ Left   ] = 0.05                              ;
  Borders [ Top    ] = 0.05                              ;
  Borders [ Right  ] = 0.05                              ;
  Borders [ Bottom ] = 0.05                              ;
  ////////////////////////////////////////////////////////
  setFlag      ( ItemIsMovable                 , true  ) ;
  setFlag      ( ItemIsSelectable              , true  ) ;
  setFlag      ( ItemIsFocusable               , true  ) ;
  setFlag      ( ItemClipsToShape              , false ) ;
  setFlag      ( ItemClipsChildrenToShape      , false ) ;
  setFlag      ( ItemSendsGeometryChanges      , true  ) ;
  setFlag      ( ItemSendsScenePositionChanges , true  ) ;
  ////////////////////////////////////////////////////////
  Painter . addMap  ( "Default" , 1                    ) ;
  Painter . addMap  ( "Dots"    , 2                    ) ;
  Painter . addMap  ( "Lines"   , 3                    ) ;
  Painter . addMap  ( "Text"    , 4                    ) ;
  ////////////////////////////////////////////////////////
  setPenColor       ( 1 , QColor ( 192 , 192 , 192 )   ) ;
  setPenColor       ( 2 , QColor ( 255 ,  64 , 255 )   ) ;
  setPenColor       ( 3 , QColor ( 192 , 192 , 255 )   ) ;
  setPenStyle       ( 3 , Qt::DashDotDotLine           ) ;
  setPenColor       ( 4 , QColor (   0 ,   0 ,   0 )   ) ;
  setBrushColor     ( 4 , QColor (   0 ,   0 ,   0 )   ) ;
  ////////////////////////////////////////////////////////
  setDropFlag       ( DropPen   , true                 ) ;
  setDropFlag       ( DropBrush , true                 ) ;
  setDropFlag       ( DropFont  , true                 ) ;
  ////////////////////////////////////////////////////////
  AllowCorners [ NoSide      ] = true                    ;
  AllowCorners [ TopLeft     ] = true                    ;
  AllowCorners [ TopRight    ] = true                    ;
  AllowCorners [ BottomLeft  ] = true                    ;
  AllowCorners [ BottomRight ] = true                    ;
  AllowCorners [ LeftSide    ] = true                    ;
  AllowCorners [ RightSide   ] = true                    ;
  AllowCorners [ TopSide     ] = true                    ;
  AllowCorners [ BottomSide  ] = true                    ;
  AllowCorners [ Inside      ] = true                    ;
  AllowCorners [ Holder      ] = true                    ;
  AllowCorners [ Dragger     ] = true                    ;
}

void N::VcfNode::hoverEnterEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverEnterEvent(event);
}

void N::VcfNode::hoverLeaveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverLeaveEvent(event);
  if (!Scaling && !Editable) return;
  setCursor(Qt::ArrowCursor);
}

void N::VcfNode::hoverMoveEvent(QGraphicsSceneHoverEvent * event)
{
  QGraphicsItem::hoverMoveEvent(event) ;
  Hovering (event->pos())              ;
}

void N::VcfNode::Hovering(QPointF pos)
{
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::contextMenuEvent(QGraphicsSceneContextMenuEvent * event)
{
  if (Menu(event->pos())) event->accept (       ) ;
  else QGraphicsItem::contextMenuEvent  ( event ) ;
}

void N::VcfNode::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
{
  if (doubleClicked(event->pos())) event->accept() ;
  else QGraphicsItem::mouseDoubleClickEvent(event) ;
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::mousePressEvent(QGraphicsSceneMouseEvent * event)
{
  switch (CastEditing())                       {
    case EditNothing                           :
      QGraphicsItem::mousePressEvent ( event ) ;
    break                                      ;
    case DragEditing                           :
      draggingPressEvent             ( event ) ;
    break                                      ;
    case ScaleEditing                          :
      scalePressEvent                ( event ) ;
    break                                      ;
    case ContentEditing                        :
      contentPressEvent              ( event ) ;
    break                                      ;
    case ShapeEditing                          :
      shapePressEvent                ( event ) ;
    break                                      ;
    case ConnectEditing                        :
      connectPressEvent              ( event ) ;
    break                                      ;
  }                                            ;
  DeleteGadgets ( )                            ;
}

void N::VcfNode::mouseMoveEvent(QGraphicsSceneMouseEvent * event)
{
  switch (CastEditing())                      {
    case EditNothing                          :
      QGraphicsItem::mouseMoveEvent ( event ) ;
    break                                     ;
    case DragEditing                          :
      draggingMoveEvent             ( event ) ;
    break                                     ;
    case ScaleEditing                         :
      scaleMoveEvent                ( event ) ;
    break                                     ;
    case ContentEditing                       :
      contentMoveEvent              ( event ) ;
    break                                     ;
    case ShapeEditing                         :
      shapeMoveEvent                ( event ) ;
    break                                     ;
    case ConnectEditing                       :
      connectMoveEvent              ( event ) ;
    break                                     ;
  }                                           ;
}

void N::VcfNode::mouseReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  switch (CastEditing())                         {
    case EditNothing                             :
      QGraphicsItem::mouseReleaseEvent ( event ) ;
    break                                        ;
    case DragEditing                             :
      draggingReleaseEvent             ( event ) ;
    break                                        ;
    case ScaleEditing                            :
      scaleReleaseEvent                ( event ) ;
    break                                        ;
    case ContentEditing                          :
      contentReleaseEvent              ( event ) ;
    break                                        ;
    case ShapeEditing                            :
      shapeReleaseEvent                ( event ) ;
    break                                        ;
    case ConnectEditing                          :
      connectReleaseEvent              ( event ) ;
    break                                        ;
  }                                              ;
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::scalePressEvent(QGraphicsSceneMouseEvent * event)
{
  if (Scaling && IsMask(event->buttons(),Qt::LeftButton)) {
    if (ResizeStart ( event ) ) event -> accept () ; else {
      QGraphicsItem::mousePressEvent(event)               ;
    }                                                     ;
  } else                                                  {
    QGraphicsItem::mousePressEvent(event)                 ;
  }                                                       ;
}

void N::VcfNode::scaleMoveEvent(QGraphicsSceneMouseEvent * event)
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

void N::VcfNode::scaleReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  if (Markers[0]==1) ResizeFinish(event) ;
  QGraphicsItem::mouseReleaseEvent(event);
}

bool N::VcfNode::CursorMoving(QGraphicsSceneMouseEvent * event)
{
  enum CornerPosition cp = atCorner ( event->pos() ) ;
  setCornerCursor ( cp )                             ;
  switch (cp)                                        {
    case TopLeft                                     :
    case TopRight                                    :
    case BottomLeft                                  :
    case BottomRight                                 :
    case LeftSide                                    :
    case RightSide                                   :
    case TopSide                                     :
    case BottomSide                                  :
    return true                                      ;
    case NoSide                                      :
    case Inside                                      :
    break                                            ;
  }                                                  ;
  return false                                       ;
}

bool N::VcfNode::ResizeStart(QGraphicsSceneMouseEvent * event)
{
  int Corner = atCorner(event->pos())              ;
  switch (Corner)                                  {
    case NoSide                                    :
      setCursor(Qt::ArrowCursor    )               ;
      Markers [0] = 0                              ;
      Markers [1] = NoSide                         ;
    return false                                   ;
    case TopLeft                                   :
      setCursor(Qt::SizeFDiagCursor)               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . topLeft     () ;
      Points     [3] = ScreenRect . bottomRight () ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case TopRight                                  :
      setCursor(Qt::SizeBDiagCursor)               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . topRight   ()  ;
      Points     [3] = ScreenRect . bottomLeft ()  ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case BottomLeft                                :
      setCursor(Qt::SizeBDiagCursor)               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . bottomLeft ()  ;
      Points     [3] = ScreenRect . topRight   ()  ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case BottomRight                               :
      setCursor(Qt::SizeFDiagCursor)               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . bottomRight () ;
      Points     [3] = ScreenRect . topLeft     () ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case LeftSide                                  :
      setCursor(Qt::SizeHorCursor  )               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . topLeft  ()    ;
      Points     [3] = ScreenRect . topRight ()    ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case RightSide                                 :
      setCursor(Qt::SizeHorCursor  )               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . topRight ()    ;
      Points     [3] = ScreenRect . topLeft  ()    ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case TopSide                                   :
      setCursor(Qt::SizeVerCursor  )               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . topLeft    ()  ;
      Points     [3] = ScreenRect . bottomLeft ()  ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case BottomSide                                :
      setCursor(Qt::SizeVerCursor  )               ;
      Markers    [0] = 1                           ;
      Markers    [1] = Corner                      ;
      Points     [0] = event->pos()                ;
      Points     [2] = ScreenRect . bottomLeft ()  ;
      Points     [3] = ScreenRect . topLeft    ()  ;
      Rectangles [0] = ScreenRect                  ;
    return true                                    ;
    case Inside                                    :
      setCursor(Qt::ArrowCursor    )               ;
      Markers [0] = 0                              ;
      Markers [1] = NoSide                         ;
    return false                                   ;
  }                                                ;
  return false                                     ;
}

bool N::VcfNode::ResizeMoving(QGraphicsSceneMouseEvent * event)
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

bool N::VcfNode::ResizeFinish(QGraphicsSceneMouseEvent * event)
{
  if (Markers[0]==0) return false            ;
  PaperRect  = Options->Standard(ScreenRect) ;
  Markers[0] = 0                             ;
  setCursor ( Qt::ArrowCursor )              ;
  FinalSize (                 )              ;
  update    (                 )              ;
  return true                                ;
}

void N::VcfNode::ResizeRect(QPointF P1,QPointF P2)
{
  double x1 = P1 . x ( )                   ;
  double x2 = P2 . x ( )                   ;
  double y1 = P1 . y ( )                   ;
  double y2 = P2 . y ( )                   ;
  double t  = 0                            ;
  if (x1>x2) { t = x1 ; x1 = x2 ; x2 = t ; }
  if (y1>y2) { t = y1 ; y1 = y2 ; y2 = t ; }
  ScreenRect . setLeft   ( x1 )            ;
  ScreenRect . setTop    ( y1 )            ;
  ScreenRect . setRight  ( x2 )            ;
  ScreenRect . setBottom ( y2 )            ;
  NewSize ( ScreenRect )                   ;
  update()                                 ;
}

void N::VcfNode::ResizeWidth(QPointF P1,QPointF P2)
{
  double x1 = P1.x()                       ;
  double x2 = P2.x()                       ;
  double t  = 0                            ;
  if (x1>x2) { t = x1 ; x1 = x2 ; x2 = t ; }
  ScreenRect . setLeft   ( x1 )            ;
  ScreenRect . setRight  ( x2 )            ;
  NewSize ( ScreenRect )                   ;
  update()                                 ;
}

void N::VcfNode::ResizeHeight(QPointF P1,QPointF P2)
{
  double y1 = P1.y()                       ;
  double y2 = P2.y()                       ;
  double t  = 0                            ;
  if (y1>y2) { t = y1 ; y1 = y2 ; y2 = t ; }
  ScreenRect . setTop    ( y1 )            ;
  ScreenRect . setBottom ( y2 )            ;
  NewSize ( ScreenRect )                   ;
  update()                                 ;
}

void N::VcfNode::NewSize(QRectF rect)
{
}

void N::VcfNode::FinalSize(void)
{
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::draggingPressEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::draggingMoveEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::draggingReleaseEvent(QGraphicsSceneMouseEvent * event)
{
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::contentPressEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::contentMoveEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::contentReleaseEvent(QGraphicsSceneMouseEvent * event)
{
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::shapePressEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::shapeMoveEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::shapeReleaseEvent(QGraphicsSceneMouseEvent * event)
{
}

//////////////////////////////////////////////////////////////////////////////

void N::VcfNode::connectPressEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::connectMoveEvent(QGraphicsSceneMouseEvent * event)
{
}

void N::VcfNode::connectReleaseEvent(QGraphicsSceneMouseEvent * event)
{
}

//////////////////////////////////////////////////////////////////////////////

QVariant N::VcfNode::itemChange(GraphicsItemChange change,const QVariant & value)
{
  switch (change)                                {
    case ItemPositionChange                      :
      if (NotNull(Options))                      {
        QPointF p = QGraphicsItem::pos()         ;
        PaperPos = Options->Standard(p)          ;
        emit Moving ( this )                     ;
      }                                          ;
    break                                        ;
    case ItemPositionHasChanged                  :
      if (NotNull(Options))                      {
        QPointF p = QGraphicsItem::pos()         ;
        PaperPos = Options->Standard(p)          ;
        emit Moving ( this )                     ;
      }                                          ;
    break                                        ;
    case ItemSelectedHasChanged                  :
      DeleteGadgets()                            ;
    break                                        ;
  }                                              ;
  return QGraphicsItem::itemChange(change,value) ;
}

bool N::VcfNode::dropFont(QWidget * source,QPointF pos,const SUID font)
{ Q_UNUSED ( source )                             ;
  Q_UNUSED ( pos    )                             ;
  GraphicsManager GM ( plan )                     ;
  EnterSQL ( SC , plan->sql )                     ;
    Painter . fonts [4] = GM . GetFont (SC,font ) ;
  LeaveSQL ( SC , plan->sql )                     ;
  update   (                )                     ;
  return true                                     ;
}

bool N::VcfNode::dropPen(QWidget * source,QPointF pos,const SUID pen)
{ Q_UNUSED ( source )                               ;
  Q_UNUSED ( pos    )                               ;
  GraphicsManager GM ( plan )                       ;
  EnterSQL ( SC , plan->sql )                       ;
    Painter . pens    [ 1] = GM . GetPen (SC,pen  ) ;
    Painter . pens    [21] = Painter . pens    [ 1] ;
  LeaveSQL ( SC , plan->sql )                       ;
  update   (                )                       ;
  return true                                       ;
}

bool N::VcfNode::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{ Q_UNUSED ( source )                                 ;
  Q_UNUSED ( pos    )                                 ;
  GraphicsManager GM ( plan )                         ;
  EnterSQL ( SC , plan->sql )                         ;
    Painter . brushes [ 1] = GM . GetBrush (SC,brush) ;
    Painter . brushes [21] = Painter . brushes [ 1]   ;
  LeaveSQL ( SC , plan->sql )                         ;
  update   (                )                         ;
  return true                                         ;
}

bool N::VcfNode::FocusIn(void)
{
  return false ;
}

bool N::VcfNode::FocusOut(void)
{
  return false ;
}

void N::VcfNode::DeleteGadgets(void)
{
  QList<int> Keys = Proxys.keys()  ;
  for (int i=0;i<Keys.count();i++) {
    Proxys[Keys[i]]->deleteLater() ;
  }                                ;
  Widgets . clear ( )              ;
  Proxys  . clear ( )              ;
  update          ( )              ;
}

void N::VcfNode::setPos(QPointF pos)
{
  if (IsNull(Options)) return                   ;
  QGraphicsItem::setPos(Options->position(pos)) ;
  PaperPos = pos                                ;
}

void N::VcfNode::setRect(QRectF rect)
{
  if (IsNull(Options)) return ;
  QPainterPath path           ;
  QRectF R                    ;
  PaperRect = rect            ;
  R = Options->Region(rect)   ;
  path.addRect  ( R        )  ;
  Painter.pathes [1] = path   ;
  EnablePath    ( 1 , true )  ;
  MergePathes   ( 0        )  ;
  ScreenRect = boundingRect() ;
  update        (          )  ;
}

void N::VcfNode::setRoundedRect(QRectF rect,double xRadius,double yRadius)
{
  if (IsNull(Options)) return                 ;
  QPainterPath path                           ;
  QRectF       R                              ;
  QPointF      C        ( xRadius , yRadius ) ;
  PaperRect = rect                            ;
  R = Options->Region   ( rect              ) ;
  C = Options->position ( C                 ) ;
  path.addRoundedRect   ( R,C.x() , C.y()   ) ;
  Painter.pathes [1] = path                   ;
  EnablePath    ( 1 , true )                  ;
  MergePathes   ( 0        )                  ;
  ScreenRect = boundingRect()                 ;
  update        (          )                  ;
}

void N::VcfNode::setPolygon(QPolygonF polygon)
{
  if (IsNull(Options)  ) return ;
  if (polygon.count()<3) return ;
  QPainterPath path             ;
  QPolygonF    S                ;
  QPolygonF    P = polygon      ;
  P << P[0]                     ;
  S = toPaper ( P )             ;
  path . addPolygon(S)          ;
  Lines = polygon               ;
  Painter.pathes [1] = path     ;
  EnablePath    ( 1 , true )    ;
  MergePathes   ( 0        )    ;
  ScreenRect = boundingRect()   ;
  update      (             )   ;
}

void N::VcfNode::setContour(Contour & c)
{
  if (IsNull(Options)  ) return ;
  contour = c                   ;
  EnablePath  ( 1 , true    )   ;
  setContour  ( 1 , c       )   ;
  MergePathes ( 0           )   ;
  ScreenRect = boundingRect()   ;
  update      (             )   ;
}

void N::VcfNode::setContour(int Id,Contour & c)
{
  if (c.count()<3) return                             ;
  QPolygonF    P                                      ;
  QPolygonF    M                                      ;
  QPolygonF    R                                      ;
  QPointF      P0                                     ;
  QPointF      P1                                     ;
  QPointF      P2                                     ;
  QPointF      P3                                     ;
  QPainterPath path                                   ;
  int          Sum = c.count()                        ;
  int          DPI = Options->DPI                     ;
  for (int a=0;a<Sum;a++)                             {
    int i = c . index [ a ]                           ;
    P << c.points[i].Point(DPI)                       ;
  }                                                   ;
  for (int a=0;a<Sum;a++)                             {
    int b = a + 1 ; b %= Sum                          ;
    int c = a + 2 ; c %= Sum                          ;
    P1 = P[a]                                         ;
    P2 = P[b]                                         ;
    P3 = P[c]                                         ;
    P0 = P1 + P2 ; P0 /= 2                            ;
    M << P0                                           ;
    P0 = Quadratic(0.5,P1,P2,P3)                      ;
    R << P0                                           ;
  }                                                   ;
  int i = 0                                           ;
  int j                                               ;
  int k                                               ;
  int A                                               ;
  int B                                               ;
  int C                                               ;
  int T1                                              ;
  int T2                                              ;
  int T3                                              ;
  j  = i - 1 + Sum ; j %= Sum                         ;
  A  = c . index  [ i ]                               ;
  B  = c . index  [ j ]                               ;
  T1 = c . points [ A ] . Control()                   ;
  switch (T1)                                         {
    case Graphics::Start                              :
    case Graphics::End                                :
    case Graphics::Flat                               :
      path . moveTo ( P [ i ] )                       ;
      i++                                             ;
    break                                             ;
    case Graphics::Quadratic                          :
      path . moveTo ( R [ j ] )                       ;
      i++                                             ;
    break                                             ;
  }                                                   ;
  while (i<Sum)                                       {
    A  = c . index  [ i ]                             ;
    T1 = c . points [ A ] . Control()                 ;
    switch (T1)                                       {
      case Graphics::Start                            :
        path . moveTo ( P [ i ] )                     ;
        i++                                           ;
      break                                           ;
      case Graphics::End                              :
      case Graphics::Flat                             :
        j  = i - 1 + Sum ; j %= Sum                   ;
        B  = c . index  [ j ]                         ;
        T2 = c . points [ B ] . Control()             ;
        if (T2==Graphics::Quadratic)                  {
          path . quadTo ( M [ j ] , P [ i ] )         ;
        } else                                        {
          path . lineTo ( P [ i ] )                   ;
        }                                             ;
        i++                                           ;
      break                                           ;
      case Graphics::Quadratic                        :
        j  = i - 1 + Sum ; j %= Sum                   ;
        k  = i + 1       ; k %= Sum                   ;
        B  = c . index  [ j ]                         ;
        C  = c . index  [ k ]                         ;
        T2 = c . points [ B ] . Control()             ;
        T3 = c . points [ C ] . Control()             ;
        if (T2!=Graphics::Quadratic                  &&
            T3!=Graphics::Quadratic )                 {
          path . quadTo ( P[ i ] , P[ k ] )           ;
          i += 2                                      ;
        } else if (T2==Graphics::Quadratic           &&
                   T3!=Graphics::Quadratic)           {
          path . quadTo ( M [ j ] , P [ i ] )         ;
          i++                                         ;
        } else                                        {
          path . quadTo ( M [ j ] , R [ j ] )         ;
          i++                                         ;
        }                                             ;
      break                                           ;
    }                                                 ;
  }                                                   ;
  i  = 0                                              ;
  j  = Sum - 1                                        ;
  k  = 1                                              ;
  A  = c . index  [ i ]                               ;
  T1 = c . points [ A ] . Control()                   ;
  switch (T1)                                         {
    case Graphics::Start                              :
    case Graphics::End                                :
    case Graphics::Flat                               :
      B  = c . index  [ j ]                           ;
      T2 = c . points [ B ] . Control()               ;
      if (T2==Graphics::Quadratic)                    {
        path . quadTo ( M [ j ] , P [ i ] )           ;
      } else                                          {
        path . lineTo ( P [ i ] )                     ;
      }                                               ;
    break                                             ;
    case Graphics::Quadratic                          :
      B  = c . index  [ j ]                           ;
      C  = c . index  [ k ]                           ;
      T2 = c . points [ B ] . Control()               ;
      T3 = c . points [ C ] . Control()               ;
      if (T2!=Graphics::Quadratic                    &&
          T3!=Graphics::Quadratic )                   {
        path . quadTo ( P[ i ] , P[ k ] )             ;
        i += 2                                        ;
      } else if (T2==Graphics::Quadratic             &&
                 T3!=Graphics::Quadratic)             {
        path . quadTo ( M [ j ] , P [ i ] )           ;
        i++                                           ;
      } else                                          {
        path . quadTo ( M [ j ] , R [ j ] )           ;
        i++                                           ;
      }                                               ;
    break                                             ;
  }                                                   ;
  Painter . pathes [Id] = path                        ;
  update ( )                                          ;
}

void N::VcfNode::DisplayBounding(bool enabled)
{
  if (IsNull(Options)) return         ;
  if (enabled)                        {
    QPainterPath Path                 ;
    QPainterPath Shape                ;
    Path.addRect  ( ScreenRect )      ;
    Painter.pathes [3] = Path         ;
    EnablePath    ( 3 , true   )      ;
    Shape.addRect  ( ScreenRect )     ;
    Painter.pathes [0] = Shape        ;
  } else                              {
    Painter . switches . remove ( 3 ) ;
    Painter . pathes   . remove ( 3 ) ;
    MergePathes ( 0 )                 ;
  }                                   ;
  update      (   )                   ;
}

void N::VcfNode::setUuid(SUID u,int t)
{
  uuid     = u ;
  node     = u ;
  nodeType = t ;
}

bool N::VcfNode::AttemptMelt(VcfLinker * Linker,QPointF base)
{
  return false ;
}

bool N::VcfNode::AllowMelts(int side)
{
  return false ;
}

void N::VcfNode::settings(int item)
{
}

void N::VcfNode::EditMenu(MenuManager & menu,QPointF pos)
{
  QMenu * ma = NULL                       ;
  /////////////////////////////////////////
  ma = menu.addMenu(tr("Edit"))           ;
  /////////////////////////////////////////
  menu . add ( ma , 801 , tr("Delete" ) ) ;
}

void N::VcfNode::RelationMenu(MenuManager & menu,QPointF pos)
{
  QMenu * ma = NULL                         ;
  ///////////////////////////////////////////
  ma = menu.addMenu(tr("Relations"))        ;
  ///////////////////////////////////////////
  menu . add ( ma , 701 , tr("Dissolve" ) ) ;
}

void N::VcfNode::AdjustmentMenu(MenuManager & menu,QPointF pos)
{
  QMenu           * ma       = NULL                          ;
  QAction         * aa       = NULL                          ;
  GraphicsItemFlags ff       = QGraphicsItem::flags (      ) ;
  bool              movable  = IsMask ( ff , ItemIsMovable ) ;
  ////////////////////////////////////////////////////////////
  ma = menu.addMenu(tr("Adjustments"))                       ;
  ////////////////////////////////////////////////////////////
  aa = menu . add    ( ma , 901 , tr("Editable" ) )          ;
  aa -> setCheckable ( true                       )          ;
  aa -> setChecked   ( Editable                   )          ;
  aa = menu . add    ( ma , 902 , tr("Movable"  ) )          ;
  aa -> setCheckable ( true                       )          ;
  aa -> setChecked   ( movable                    )          ;
  aa = menu . add    ( ma , 903 , tr("Resizable") )          ;
  aa -> setCheckable ( true                       )          ;
  aa -> setChecked   ( Scaling                    )          ;
}

void N::VcfNode::NodeMenu(VcfNode * node,QPointF pos)
{
  nScopedMenu ( mm , GraphicsView() ) ;
  QAction    * aa = NULL          ;
  EditMenu       ( mm , pos )     ;
  RelationMenu   ( mm , pos )     ;
  AdjustmentMenu ( mm , pos )     ;
  mm . setFont   ( plan     )     ;
  aa = mm . exec (          )     ;
  if (IsNull     (aa   )) return  ;
  MenuProcess(aa,mm)              ;
}

bool N::VcfNode::Menu(QPointF pos)
{
  emit Menu ( this , pos ) ;
  return true              ;
}

bool N::VcfNode::MenuProcess(QAction * action,MenuManager & menu)
{
  switch (menu[action])                                       {
    case 901                                                  :
      Editable = action -> isChecked ( )                      ;
    break                                                     ;
    case 902                                                  :
      setFlag         ( ItemIsMovable , action->isChecked() ) ;
    break                                                     ;
    case 903                                                  :
      Scaling = action->isChecked()                           ;
      DisplayBounding ( action->isChecked()                 ) ;
    return true                                               ;
  }                                                           ;
  return false                                                ;
}

bool N::VcfNode::doubleClicked(QPointF pos)
{
  return false ;
}

void N::VcfNode::connectNode(VcfNode * node)
{
  connect(node,SIGNAL(Append        (VcfItem*,VcfItem*))   ,
          this,SLOT  (AcceptAppend  (VcfItem*,VcfItem*)) ) ;
  connect(node,SIGNAL(Remove        (VcfItem*         ))   ,
          this,SLOT  (AcceptRemove  (VcfItem*         )) ) ;
  connect(node,SIGNAL(Moving        (VcfItem*         ))   ,
          this,SLOT  (AcceptMoving  (VcfItem*         )) ) ;
}

void N::VcfNode::connectLinker(VcfLinker * linker)
{
  connect(linker,SIGNAL(Append        (VcfItem*,VcfItem*))   ,
          this  ,SLOT  (AcceptAppend  (VcfItem*,VcfItem*)) ) ;
  connect(linker,SIGNAL(Remove        (VcfItem*         ))   ,
          this  ,SLOT  (AcceptRemove  (VcfItem*         )) ) ;
  connect(linker,SIGNAL(Dissolve      (VcfItem*         ))   ,
          this  ,SLOT  (AcceptDissolve(VcfItem*         )) ) ;
}

void N::VcfNode::AcceptAppend(VcfItem * item,VcfItem * parent)
{
  emit Append ( item , parent ) ;
}

void N::VcfNode::AcceptRemove(VcfItem * item)
{
  emit Remove ( item ) ;
}

void N::VcfNode::AcceptDissolve(VcfItem * item)
{
}

void N::VcfNode::AcceptMoving(VcfItem * item)
{
}

void N::VcfNode::SignalReceiver(int command)
{
  plan -> Play ( command ) ;
}

QPointF N::VcfNode::PaperPosition(VcfItem * item,QPointF position)
{
  QPointF ps = Options->position ( position  ) ;
  ps = mapToItem                 ( item , ps ) ;
  ps = Options -> Standard       ( ps        ) ;
  return ps                                    ;
}

QLineEdit * N::VcfNode::NewLineEdit(int Id)
{
  QLineEdit            * line  = new QLineEdit            (    ) ;
  QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget (this) ;
  proxy -> setWidget ( line )                                    ;
  Proxys  [ Id ] = proxy                                         ;
  Widgets [ Id ] = line                                          ;
  return line                                                    ;
}
"""

# -*- coding: utf-8 -*-
##############################################################################
## VcfItem
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
from   PyQt5 . QtWidgets              import QGraphicsItem
##############################################################################
from   AITK  . Qt . AbstractGui       import AbstractGui as AbstractGui
##############################################################################
class VcfItem                   ( QObject                                  , \
                                  QGraphicsItem                            , \
                                  AbstractGui                              ) :
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent                                     )
    self      . setParentItem   ( item                                       )
    self      . Initialize      ( self                                       )
    self      . setPlanFunction ( plan                                       )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfItem : public QObject
                                  , public QGraphicsItem
                                  , public AbstractGui
{
  Q_OBJECT
  Q_INTERFACES(QGraphicsItem)
  public:

    VcfOptions        * Options   ;
    VcfPainter          Painter   ;
    bool                Printable ;
    bool                Editable  ;
    bool                Modified  ;
    bool                Overlay   ;
    bool                Lockup    ;
    VcfItems            Related   ;
    QMap<VcfItem *,int> Relations ;

    explicit VcfItem                 (QObject       * parent       ,
                                      QGraphicsItem * item         ,
                                      Plan          * plan = NULL) ;
    virtual ~VcfItem                 (void);

    void ItemMarriage                (VcfItem * item,int relationship);
    void ItemDivorce                 (VcfItem * item);
    int  Relationship                (VcfItem * item);

    void setOptions                  (VcfOptions & options,bool privated = false) ;
    void setPenStyle                 (int Id,Qt::PenStyle style) ;
    void setPenColor                 (int Id,QColor color) ;
    void setBrushStyle               (int Id,Qt::BrushStyle style) ;
    void setBrushColor               (int Id,QColor color) ;

    QPointF         toPaper          (QPointF cm) ;
    QRectF          toPaper          (QRectF region) ;
    QPolygonF       toPaper          (QPolygonF & polygon) ;

    QPoint          toView           (QPointF pos) ;
    QPoint          toGlobal         (QPointF pos) ;

    QPointF         FromView         (QPoint pos) ;

    QGraphicsView * GraphicsView     (void) ;

    QPointF Quadratic                (double t,QPointF & P1,QPointF & P2,QPointF & P3) ;
    QPointF Quadratic                (double t,int index,QPolygonF & polygon) ;
    QPointF Cubic                    (double t,int index,QPolygonF & polygon) ;

    QPainterPath UnitedPathes        (void) ;

    bool FetchFont                   (int Id,SUID uuid) ;
    bool FetchPen                    (int Id,SUID uuid) ;
    bool FetchBrush                  (int Id,SUID uuid) ;
    bool FetchGradient               (int Id,SUID uuid) ;

    bool FetchFont                   (int Id,QString name) ;
    bool FetchPen                    (int Id,QString name) ;
    bool FetchBrush                  (int Id,QString name) ;
    bool FetchGradient               (int Id,QString name) ;

    virtual void   settings          (int item) ;

    void           pushTransform     (void) ;
    void           popTransform      (void) ;
    void           adjustTransform   (void) ;
    virtual void   PaperTransform    (int DPI,QRectF Paper) ;

    virtual QRectF clipRect          (void) ;
    virtual QRectF visibleRect       (void) ;

    virtual QPointF mousePosition    (void) ;

  protected:

    QList<QPen      > pens         ;
    QList<QBrush    > brushes      ;
    QList<QFont     > fonts        ;
    QList<QTransform> transforms   ;
    QRectF            WritingPaper ;
    int               PaperDPI     ;

    void           pushPainters      (QPainter * p) ;
    void           popPainters       (QPainter * p) ;

    virtual bool Bustle              (void) ;
    virtual bool Vacancy             (void) ;

    virtual void focusInEvent        (QFocusEvent * event);
    virtual void focusOutEvent       (QFocusEvent * event);

    virtual void dragEnterEvent      (QGraphicsSceneDragDropEvent * event);
    virtual void dragLeaveEvent      (QGraphicsSceneDragDropEvent * event);
    virtual void dragMoveEvent       (QGraphicsSceneDragDropEvent * event);
    virtual void dropEvent           (QGraphicsSceneDragDropEvent * event);

    bool allowDrop                   (void);

    virtual bool        acceptDrop   (nDeclWidget,const QMimeData * mime);
    virtual bool        dropNew      (nDeclWidget,const QMimeData * mime,QPointF pos);
    virtual bool        dropMoving   (nDeclWidget,const QMimeData * mime,QPointF pos);
    virtual bool        dropAppend   (nDeclWidget,const QMimeData * mime,QPointF pos);
    virtual bool        removeDrop   (void);

    virtual bool        dragEnter    (QGraphicsSceneDragDropEvent * event) ;
    virtual bool        dragMove     (QGraphicsSceneDragDropEvent * event) ;
    virtual bool        drop         (QGraphicsSceneDragDropEvent * event) ;

  private:

  public slots:

    virtual void Paint               (QPainter * painter,QRectF Region,bool clip,bool color) = 0 ;

    virtual void PaintPath           (QPainter * painter,int Id) ;
    virtual void PaintPathes         (QPainter * painter) ;
    virtual void PaintLines          (QPainter * painter,int Id,QPolygonF & Lines);

    virtual void setPoints           (int Id,QSizeF radius,QPolygonF & dots) ;
    virtual void setWideLine         (int Id,double width,QLineF & Line) ;
    virtual void setFoldLines        (int Id,double width,QPolygonF & Lines) ;
    virtual void setQuadratic        (int Id,QPolygonF & polygon);

    virtual bool FocusIn             (void) ;
    virtual bool FocusOut            (void) ;

    virtual void ClearPathes         (void) ;
    virtual void MergePathes         (int TargetId) ;
    virtual void EnablePath          (int Id,bool enable) ;

  protected slots:

  private slots:

  signals:

    void FocusIn                     (VcfItem * item);
    void FocusOut                    (VcfItem * item);
    void contentModified             (VcfItem * item);
    void Canvas                      (VcfItem * item,QRectF Screen);
    void Selection                   (VcfItem * item,QRectF Screen);

};

N::VcfItem:: VcfItem       ( QObject * parent,QGraphicsItem * item,Plan * p )
           : QObject       (           parent                               )
           , QGraphicsItem (                                  item          )
           , AbstractGui   ( (QGraphicsItem *) this               ,       p )
           , Options       ( NULL                                           )
           , Printable     ( true                                           )
           , Editable      ( true                                           )
           , Overlay       ( false                                          )
           , Lockup        ( false                                          )
{
  setAcceptHoverEvents ( true                          ) ;
  setAcceptDrops       ( true                          ) ;
  setFlag              ( ItemAcceptsInputMethod , true ) ;
}

N::VcfItem::~VcfItem (void)
{
  nDropOut    ( IsNull(Options)   ) ;
  nDropOut    ( !Options->Private ) ;
  nEnsureNull ( Options           ) ;
}

void N::VcfItem::focusInEvent(QFocusEvent * event)
{
  QGraphicsItem::focusInEvent  ( event ) ;
  FocusIn                      (       ) ;
}

void N::VcfItem::focusOutEvent(QFocusEvent * event)
{
  QGraphicsItem::focusOutEvent ( event ) ;
  FocusOut                     (       ) ;
}

void N::VcfItem::dragEnterEvent(QGraphicsSceneDragDropEvent * event)
{
  if (allowDrop() && dragEnter(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QGraphicsItem::dragEnterEvent(event);
    else event->ignore() ;
  };
}

void N::VcfItem::dragLeaveEvent(QGraphicsSceneDragDropEvent * event)
{
  if (removeDrop()) event->accept() ; else {
    if (PassDragDrop) QGraphicsItem::dragLeaveEvent(event);
    else event->ignore() ;
  };
}

void N::VcfItem::dragMoveEvent(QGraphicsSceneDragDropEvent * event)
{
  if (allowDrop() && dragMove(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QGraphicsItem::dragMoveEvent(event);
    else event->ignore() ;
  };
}

void N::VcfItem::dropEvent(QGraphicsSceneDragDropEvent * event)
{
  if (allowDrop() && drop(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QGraphicsItem::dropEvent(event);
    else event->ignore() ;
  };
}

bool N::VcfItem::allowDrop(void)
{
  return acceptDrops () ;
}

bool N::VcfItem::acceptDrop(QWidget * source,const QMimeData * mime)
{
  return dropHandler(mime) ;
}

bool N::VcfItem::dropNew(QWidget * source,const QMimeData * mime,QPointF pos)
{
  return true ;
}

bool N::VcfItem::dropMoving(QWidget * source,const QMimeData * mime,QPointF pos)
{
  return true ;
}

bool N::VcfItem::dropAppend(QWidget * source,const QMimeData * mime,QPointF pos)
{
  return dropItems(source,mime,pos) ;
}

bool N::VcfItem::removeDrop(void)
{
  return false ;
}

bool N::VcfItem::dragEnter(QGraphicsSceneDragDropEvent * event)
{
  nKickOut(!acceptDrop(event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropNew   (event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                 ;
}

bool N::VcfItem::dragMove(QGraphicsSceneDragDropEvent  * event)
{
  nKickOut(!acceptDrop(event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropMoving(event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                 ;
}

bool N::VcfItem::drop(QGraphicsSceneDragDropEvent * event)
{
  nKickOut(!acceptDrop(event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropAppend(event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                 ;
}

QGraphicsView * N::VcfItem::GraphicsView(void)
{
  QGraphicsScene * gs = scene ( )         ;
  nKickOut ( IsNull(gs)      , NULL )     ;
  QList<QGraphicsView *> vs = gs->views() ;
  nKickOut ( vs.count() <= 0 , NULL )     ;
  return Casting( QGraphicsView , vs[0] ) ;
}

void N::VcfItem::setPenStyle(int Id,Qt::PenStyle style)
{
  Painter . pens   [ Id ] . setStyle (style) ;
}

void N::VcfItem::setPenColor(int Id,QColor color)
{
  Painter . addPen   (Id,color) ;
}

void N::VcfItem::setBrushStyle(int Id,Qt::BrushStyle style)
{
  Painter . brushes [ Id ] . setStyle (style) ;
}

void N::VcfItem::setBrushColor(int Id,QColor color)
{
  Painter . addBrush (Id,color) ;
}

void N::VcfItem::pushPainters(QPainter * p)
{
  pens    << p->pen   () ;
  brushes << p->brush () ;
  fonts   << p->font  () ;
}

void N::VcfItem::popPainters(QPainter * p)
{
  int index = pens.count() - 1      ;
  nDropOut ( index < 0 )            ;
  p -> setPen      (pens   [index]) ;
  p -> setBrush    (brushes[index]) ;
  p -> setFont     (fonts  [index]) ;
  pens    . takeAt (index         ) ;
  brushes . takeAt (index         ) ;
  fonts   . takeAt (index         ) ;
}

void N::VcfItem::pushTransform(void)
{
  transforms << transform() ;
}

void N::VcfItem::PaperTransform(int DPI,QRectF Paper)
{
  PaperDPI     = DPI   ;
  WritingPaper = Paper ;
}

QRectF N::VcfItem::clipRect(void)
{
  return WritingPaper ;
}

QRectF N::VcfItem::visibleRect(void)
{
  QSize  GS = GraphicsView()->size()                        ;
  QRect  GR(0,0,GS.width(),GS.height())                     ;
  QRectF SR = GraphicsView()->mapToScene(GR).boundingRect() ;
  return mapFromScene(SR).boundingRect()                    ;
}

void N::VcfItem::popTransform(void)
{
  int index = transforms.count() - 1 ;
  nDropOut ( index < 0 )             ;
  setTransform(transforms[index])    ;
  transforms.takeAt(index)           ;
}

void N::VcfItem::PaintPath(QPainter * p,int Id)
{
  pushPainters         ( p              ) ;
  if (Painter.pathes.contains(Id))        {
    if (Painter.pens.contains(Id))        {
      p -> setPen   (Painter.pens   [Id]) ;
    }                                     ;
    if (Painter.brushes.contains(Id))     {
      p -> setBrush (Painter.brushes[Id]) ;
    }                                     ;
    p -> drawPath ( Painter.pathes[Id]  ) ;
  }                                       ;
  popPainters          ( p              ) ;
}

void N::VcfItem::PaintPathes(QPainter * p)
{
  CUIDs Index = Painter.switches.keys() ;
  CUID  i                               ;
  nDropOut ( Index.count() <= 0 )       ;
  qSort(Index.begin(),Index.end())      ;
  foreach (i,Index)                     {
    if (Painter.switches[i])            {
      PaintPath ( p , i )               ;
    }                                   ;
  }                                     ;
}

void N::VcfItem::PaintLines(QPainter * p,int Id,QPolygonF & Lines)
{
  nDropOut ( Lines.count() <= 0  ) ;
  pushPainters ( p               ) ;
  if (Painter.pens.contains(Id))   {
    p -> setPen (Painter.pens[Id]) ;
  }                                ;
  p -> drawPolyline ( Lines )      ;
  popPainters  ( p               ) ;
}

void N::VcfItem::EnablePath(int Id,bool enable)
{
  Painter.switches[Id] = enable ;
}

void N::VcfItem::MergePathes(int TargetId)
{
  Painter . pathes [ TargetId ] = UnitedPathes ( ) ;
}

void N::VcfItem::ClearPathes(void)
{
  Painter . switches . clear ( ) ;
  Painter . pathes   . clear ( ) ;
}

QPainterPath N::VcfItem::UnitedPathes(void)
{
  CUIDs Index = Painter.switches.keys() ;
  QPainterPath path                     ;
  nKickOut ( Index.count()<=0 , path )  ;
  qSort(Index.begin(),Index.end())      ;
  path = Painter.pathes[ Index [ 0 ] ]  ;
  for (int i=1;i<Index.count();i++)     {
    int j = Index[i]                    ;
    if (Painter.switches[j])            {
      path.addPath(Painter.pathes[j])   ;
    }                                   ;
  }                                     ;
  return path.simplified()              ;
}

QPointF N::VcfItem::toPaper(QPointF cm)
{
  nKickOut ( IsNull(Options) , QPointF(0.00f,0.00f) ) ;
  return Options->position(cm)                        ;
}

QRectF N::VcfItem::toPaper(QRectF region)
{
  nKickOut ( IsNull(Options) , QRectF(0.00f,0.00f,0.00f,0.00f) ) ;
  return Options->Region(region)                                 ;
}

QPolygonF N::VcfItem::toPaper(QPolygonF & polygon)
{
  QPolygonF p                            ;
  nKickOut ( IsNull(Options) , polygon ) ;
  for (int i=0;i<polygon.count();i++)    {
    QPointF P = polygon [ i ]            ;
    P = Options -> position ( P )        ;
    p << P                               ;
  }                                      ;
  return    p                            ;
}

QPoint N::VcfItem::toView(QPointF pos)
{
  QGraphicsView * gv = GraphicsView     (   ) ;
  nKickOut ( IsNull(gv) , QPoint (0,0)      ) ;
  QPointF         s  = mapToScene       (pos) ;
  QPoint          w  = gv->mapFromScene (s  ) ;
  return w                                    ;
}

QPoint N::VcfItem::toGlobal(QPointF pos)
{
  QGraphicsView * gv = GraphicsView     (   ) ;
  nKickOut ( IsNull(gv) , QPoint (0,0)      ) ;
  QPointF         s  = mapToScene       (pos) ;
  QPoint          w  = gv->mapFromScene (s  ) ;
  QPoint          g  = gv->mapToGlobal  (w  ) ;
  return g                                    ;
}

QPointF N::VcfItem::FromView(QPoint pos)
{
  QGraphicsView * gv = GraphicsView (   ) ;
  nKickOut ( IsNull(gv) , QPoint (0,0)  ) ;
  QPointF s = gv->mapToScene        (pos) ;
  QPointF w =     mapFromScene      ( s ) ;
  return  w                               ;
}

QPointF N::VcfItem::Quadratic(double t,QPointF & P1,QPointF & P2,QPointF & P3)
{
  double  mt = 1 - t       ;
  double  tt = t           ;
  double  A  = mt * mt     ;
  double  B  = mt * tt * 2 ;
  double  C  = tt * tt     ;
  QPointF P                ;
  P   = P1 * A             ;
  P  += P2 * B             ;
  P  += P3 * C             ;
  return  P                ;
}

QPointF N::VcfItem::Quadratic(double t,int index,QPolygonF & polygon)
{
  double  mt = 1 - t              ;
  double  tt = t                  ;
  double  A  = mt * mt            ;
  double  B  = mt * tt * 2        ;
  double  C  = tt * tt            ;
  QPointF P                       ;
  P   = polygon [ index     ] * A ;
  P  += polygon [ index + 1 ] * B ;
  P  += polygon [ index + 2 ] * C ;
  return  P                       ;
}

QPointF N::VcfItem::Cubic(double t,int index,QPolygonF & polygon)
{
  double  mt = 1 - t              ;
  double  tt = t                  ;
  double  at = mt * tt * 3        ;
  double  A  = mt * mt * mt       ;
  double  B  = at * mt            ;
  double  C  = at * tt            ;
  double  D  = tt * tt * tt       ;
  QPointF P                       ;
  P   = polygon [ index     ] * A ;
  P  += polygon [ index + 1 ] * B ;
  P  += polygon [ index + 2 ] * C ;
  P  += polygon [ index + 3 ] * D ;
  return  P                       ;
}

void N::VcfItem::setPoints(int Id,QSizeF radius,QPolygonF & dots)
{
  QPointF   R(radius.width(),radius.height()) ;
  QPolygonF P = toPaper ( dots )              ;
  QPainterPath path                           ;
  R = toPaper ( R )                           ;
  for (int i=0;i<P.count();i++)               {
    QPointF c = P [ i ]                       ;
    path . addEllipse ( c , R.x() , R.y() )   ;
  }                                           ;
  Painter . pathes [Id] = path                ;
  update ( )                                  ;
}

void N::VcfItem::setWideLine(int Id,double width,QLineF & Line)
{
  VcfShape     vs                               ;
  QPolygonF    G = vs.WideLine ( width , Line ) ;
  QPolygonF    P = toPaper     ( G            ) ;
  QPainterPath path                             ;
  path . addPolygon ( P )                       ;
  Painter . pathes [Id] = path                  ;
  update ( )                                    ;
}

void N::VcfItem::setFoldLines(int Id,double width,QPolygonF & Lines)
{
  VcfShape     vs                                 ;
  QPolygonF    G = vs.FoldLines ( width , Lines ) ;
  QPolygonF    P = toPaper      ( G             ) ;
  QPainterPath path                               ;
  path . addPolygon ( P )                         ;
  Painter . pathes [Id] = path                    ;
  update ( )                                      ;
}

void N::VcfItem::setQuadratic(int Id,QPolygonF & polygon)
{
  nDropOut ( polygon.count() < 3 )      ;
  QPolygonF    P  = toPaper ( polygon ) ;
  QPolygonF    C                        ;
  QPolygonF    R                        ;
  QPointF      P0                       ;
  QPointF      P1                       ;
  QPointF      P2                       ;
  QPointF      P3                       ;
  QPainterPath path                     ;
  int          total = P.count()        ;
  for (int a=0;a<total;a++)             {
    int b = a + 1 ; b %= total          ;
    int c = a + 2 ; c %= total          ;
    P1 = P[a]                           ;
    P2 = P[b]                           ;
    P3 = P[c]                           ;
    P0 = P1 + P2 ; P0 /= 2              ;
    C << P0                             ;
    P0 = Quadratic(0.5,P1,P2,P3)        ;
    R << P0                             ;
  }                                     ;
  path . moveTo ( R[0] )                ;
  for (int i=1;i<total;i++)             {
    path . quadTo ( C[ i ] , R[ i ] )   ;
  }                                     ;
  path . quadTo ( C[ 0 ] , R[ 0 ] )     ;
  Painter . pathes [Id] = path          ;
  update ( )                            ;
}

bool N::VcfItem::FocusIn(void)
{
  return true ;
}

bool N::VcfItem::FocusOut(void)
{
  return true ;
}

bool N::VcfItem::Bustle(void)
{
  LockGui   (                 ) ;
  setCursor ( Qt::WaitCursor  ) ;
  return true                   ;
}

bool N::VcfItem::Vacancy(void)
{
  setCursor ( Qt::ArrowCursor ) ;
  UnlockGui (                 ) ;
  return true                   ;
}

bool N::VcfItem::FetchFont(int Id,SUID uuid)
{
  GraphicsManager GM (plan )                              ;
  EnterSQL ( SC , plan->sql )                             ;
    Painter . fonts     [Id] = GM . GetFont ( SC , uuid ) ;
  LeaveSQL ( SC , plan->sql )                             ;
  return true                                             ;
}

bool N::VcfItem::FetchPen(int Id,SUID uuid)
{
  GraphicsManager GM (plan )                             ;
  EnterSQL ( SC , plan->sql )                            ;
    Painter . pens      [Id] = GM . GetPen ( SC , uuid ) ;
  LeaveSQL ( SC , plan->sql )                            ;
  return true                                            ;
}

bool N::VcfItem::FetchBrush(int Id,SUID uuid)
{
  GraphicsManager GM (plan )                               ;
  EnterSQL ( SC , plan->sql )                              ;
    Painter . brushes   [Id] = GM . GetBrush ( SC , uuid ) ;
  LeaveSQL ( SC , plan->sql )                              ;
  return true ;
}

bool N::VcfItem::FetchGradient(int Id,SUID uuid)
{
  GraphicsManager GM (plan )                                  ;
  EnterSQL ( SC , plan->sql )                                 ;
    Painter . gradients [Id] = GM . GetGradient ( SC , uuid ) ;
  LeaveSQL ( SC , plan->sql )                                 ;
  return true ;
}

bool N::VcfItem::FetchFont(int Id,QString name)
{
  GraphicsManager GM (plan )                              ;
  EnterSQL ( SC , plan->sql )                             ;
    Painter . fonts     [Id] = GM . GetFont ( SC , name ) ;
  LeaveSQL ( SC , plan->sql )                             ;
  return true                                             ;
}

bool N::VcfItem::FetchPen(int Id,QString name)
{
  GraphicsManager GM (plan )                             ;
  EnterSQL ( SC , plan->sql )                            ;
    Painter . pens      [Id] = GM . GetPen ( SC , name ) ;
  LeaveSQL ( SC , plan->sql )                            ;
  return true                                            ;
}

bool N::VcfItem::FetchBrush(int Id,QString name)
{
  GraphicsManager GM (plan )                               ;
  EnterSQL ( SC , plan->sql )                              ;
    Painter . brushes   [Id] = GM . GetBrush ( SC , name ) ;
  LeaveSQL ( SC , plan->sql )                              ;
  return true                                              ;
}

bool N::VcfItem::FetchGradient(int Id,QString name)
{
  GraphicsManager GM (plan )                                  ;
  EnterSQL ( SC , plan->sql )                                 ;
    Painter . gradients [Id] = GM . GetGradient ( SC , name ) ;
  LeaveSQL ( SC , plan->sql )                                 ;
  return true                                                 ;
}

void N::VcfItem::setOptions(VcfOptions & options,bool privated)
{
  if ( ! privated ) Options = &options ; else {
      Options  = new VcfOptions()             ;
    (*Options) = options                      ;
      Options -> Private = true               ;
  }                                           ;
}

void N::VcfItem::adjustTransform(void)
{
  nDropOut ( IsNull ( Options )   ) ;
  nDropOut ( ! Options -> Private ) ;
}

void N::VcfItem::ItemMarriage(VcfItem * item,int relationship)
{
  if ( ! Related . contains ( item ) ) {
    Related << item                    ;
  }                                    ;
  Relations [ item ] = relationship    ;
}

void N::VcfItem::ItemDivorce(VcfItem * item)
{
  nDropOut ( ! Related . contains ( item ) ) ;
  int index =  Related . indexOf  ( item )   ;
  nDropOut ( index < 0                     ) ;
  Relations . remove ( item  )               ;
  Related   . takeAt ( index )               ;
}

int N::VcfItem:: Relationship(VcfItem * item)
{
  nKickOut ( !Related  .contains(item) , 0 ) ;
  nKickOut ( !Relations.contains(item) , 0 ) ;
  return Relations [ item ]                  ;
}

void N::VcfItem::settings(int item)
{
}

QPointF N::VcfItem::mousePosition(void)
{
  QPoint pos  = QCursor::pos ( )                         ;
  pos         = GraphicsView ( ) ->mapFromGlobal ( pos ) ;
  QPointF pfs = GraphicsView ( ) ->mapToScene    ( pos ) ;
  pfs         = mapFromScene                     ( pfs ) ;
  return pfs                                             ;
}
"""

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
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
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
from              . VcfOptions        import VcfOptions as VcfOptions
from              . VcfPainter        import VcfPainter as VcfPainter
##############################################################################
class VcfItem                   ( QGraphicsItem                            , \
                                  AbstractGui                              ) :
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( item                                       )
    self . Initialize           ( self                                       )
    self . setPlanFunction      ( plan                                       )
    self . setVcfItemDefaults   (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfItemDefaults             ( self                                ) :
    ##########################################################################
    self . Options      = VcfOptions (                                       )
    self . Painter      = VcfPainter (                                       )
    self . Printable    = True
    self . Editable     = True
    self . Modified     = False
    self . Overlay      = False
    self . Lockup       = False
    self . Related      = [ ]
    self . Relations    = { }
    self . pens         = [ ]
    self . brushes      = [ ]
    self . fonts        = [ ]
    self . transforms   = [ ]
    self . WritingPaper = QRectF     (                                       )
    self . PaperDPI     = 300
    ##########################################################################
    self . setAcceptHoverEvents      ( True                                  )
    self . setAcceptDrops            ( True                                  )
    ##########################################################################
    self . setFlag ( QGraphicsItem . ItemAcceptsInputMethod , True           )
    ##########################################################################
    return
  ############################################################################
  def GraphicsView    ( self                                               ) :
    ##########################################################################
    gs = self . scene (                                                      )
    if                ( gs in [ False , None ]                             ) :
      return None
    ##########################################################################
    vs = gs . views   (                                                      )
    if                ( len ( vs ) <= 0                                    ) :
      return None
    ##########################################################################
    return vs         [ 0                                                    ]
  ############################################################################
  def focusInEvent            ( self , event                               ) :
    ##########################################################################
    super ( ) . focusInEvent  (        event                                 )
    self      . FocusIn       (                                              )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    super ( ) . focusOutEvent (        event                                 )
    self      . FocusOut      (                                              )
    ##########################################################################
    return
  ############################################################################
  def FocusIn  ( self                                                      ) :
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    return True
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def pushPainters          ( self , p                                     ) :
    ##########################################################################
    self . pens    . append ( p . pen   ( )                                  )
    self . brushes . append ( p . brush ( )                                  )
    self . fonts   . append ( p . font  ( )                                  )
    ##########################################################################
    return
  ############################################################################
  def popPainters      ( self , p                                          ) :
    ##########################################################################
    AT = len           ( self . pens                                         )
    AT = AT - 1
    ##########################################################################
    if                 ( AT < 0                                            ) :
      return
    ##########################################################################
    p  . setPen        ( self . pens    [ AT ]                               )
    p  . setBrush      ( self . brushes [ AT ]                               )
    p  . setFont       ( self . fonts   [ AT ]                               )
    ##########################################################################
    del self . pens    [ AT                                                  ]
    del self . brushes [ AT                                                  ]
    del self . fonts   [ AT                                                  ]
    ##########################################################################
    return
  ############################################################################
  def setPenStyle                           ( self , Id , style            ) :
    self . Painter . pens [ Id ] . setStyle (             style              )
    return
  ############################################################################
  def setPenColor           ( self , Id , color                            ) :
    self . Painter . addPen (        Id , color                              )
    return
  ############################################################################
  def setBrushStyle                            ( self , Id , style         ) :
    self . Painter . brushes [ Id ] . setStyle (             style           )
    return
  ############################################################################
  def setBrushColor           ( self , Id , color                          ) :
    self . Painter . addBrush (        Id , color                            )
    return
  ############################################################################
  def pushTransform            ( self                                      ) :
    self . transforms . append ( self . transform ( )                        )
    return
  ############################################################################
  def PaperTransform ( self , DPI , Paper                                  ) :
    self . PaperDPI     = DPI
    self . WritingPaper = Paper
    return
  ############################################################################
  def clipRect ( self                                                      ) :
    return self . WritingPaper
  ############################################################################
  def visibleRect              ( self                                      ) :
    ##########################################################################
    gv = self . GraphicsView   (                                             )
    if                         ( gv in [ False , None ]                    ) :
      return QRectF            ( 0 , 0 , 1 , 1                               )
    ##########################################################################
    GS = gv . size             (                                             )
    GR = QRect                 ( 0 , 0 , GS . width ( ) , GS . height ( )    )
    SR = gv     . mapToScene   ( GR ) . boundingRect (                       )
    ##########################################################################
    return self . mapFromScene ( SR ) . boundingRect (                       )
  ############################################################################
  def popTransform        ( self                                           ) :
    ##########################################################################
    AT   = len            ( self . transforms                                )
    AT   = AT - 1
    if                    ( AT < 0                                         ) :
      return
    ##########################################################################
    self . setTransform   ( self . transforms [ AT ]                         )
    del self . transforms [ AT                                               ]
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def Bustle         ( self                                                ) :
    ##########################################################################
    self . LockGui   (                                                       )
    self . setCursor ( Qt . WaitCursor                                       )
    ##########################################################################
    return True
  ############################################################################
  def Vacancy        ( self                                                ) :
    ##########################################################################
    self . setCursor ( Qt . ArrowCursor                                      )
    self . UnlockGui (                                                       )
    ##########################################################################
    return True
  ############################################################################
  def setOptions ( self , options , privated ) :
    ##########################################################################
    if ( not privated ) :
      self . Options . setOptions ( options )
      return
    ##########################################################################
    """
      Options  = new VcfOptions()             ;
    (*Options) = options                      ;
      Options -> Private = true               ;
    """
    self . Options . Private = True
    ##########################################################################
    return
  ############################################################################
  def adjustTransform ( self                                               ) :
    ##########################################################################
    """
    nDropOut ( IsNull ( Options )   ) ;
    nDropOut ( ! Options -> Private ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def ItemMarriage            ( self , item , relationship                 ) :
    ##########################################################################
    if                        ( item not in self . Related                 ) :
      self . Related . append ( item                                         )
    ##########################################################################
    self . Relations [ item ] = relationship
    ##########################################################################
    return
  ############################################################################
  def ItemDivorce               ( self , item                              ) :
    ##########################################################################
    if                          ( item not in self . Related               ) :
      return
    ##########################################################################
    AT = self . Related . index ( item                                       )
    if                          ( AT < 0                                   ) :
      return
    ##########################################################################
    del self . Relations        [ item                                       ]
    del self . Related          [ AT                                         ]
    ##########################################################################
    return
  ############################################################################
  def Relationship          ( self , item                                  ) :
    ##########################################################################
    if                      ( item not in self . Related                   ) :
      return 0
    ##########################################################################
    if                      ( item not in self . Relations                 ) :
      return 0
    ##########################################################################
    return self . Relations [ item                                           ]
  ############################################################################
  def settings ( self , item                                               ) :
    return
  ############################################################################
  def mousePosition            ( self                                      ) :
    ##########################################################################
    pos = QCursor . pos        (                                             )
    gv  = self . GraphicsView  (                                             )
    if                         ( gv in [ False , None ]                    ) :
      return pos
    ##########################################################################
    pos = gv . mapFromGlobal   ( pos                                         )
    pfs = gv . mapToScene      ( pos                                         )
    ##########################################################################
    return self . mapFromScene ( pfs                                         )
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
"""

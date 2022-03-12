# -*- coding: utf-8 -*-
##############################################################################
## VcfLinker
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
from   AITK  . Essentials . Object    import Object   as Object
from   AITK  . Math       . Node      import Node     as Node
from   AITK  . Math       . Relation  import Relation as Relation
##############################################################################
from         . VcfLines               import VcfLines as VcfLines
##############################################################################
class VcfLinker       ( VcfLines , Relation                                ) :
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
class Q_COMPONENTS_EXPORT VcfLinker : public VcfLines
                                    , public Relation
{
  Q_OBJECT
  public:

    enum EditModel   {
      Freehand = 0   ,
      Node     = 1   ,
      Tree     = 2 } ;

    enum EditStatus   {
      Display  = 0    ,
      Line     = 1    ,
      Connect  = 2  } ;

    enum MovementMethod {
      Ignore     = 0    ,
      Direct     = 1    ,
      Horizontal = 2    ,
      Vertical   = 3    ,
      Optimize   = 4  } ;

    IMAPs                    Arrows     ;
    DMAPs                    Paraments  ;
    QMap<int,QPainterPath *> Intersects ;
    QMap<int,QPointF       > Melts      ;
    QMap<int,VcfNode      *> Linking    ;
    enum EditModel           Model      ;
    enum EditStatus          Status     ;
    enum MovementMethod      Movement   ;

    enum { Type = UserType + VCF::Linker } ;
    virtual int type(void) const { return Type; }

    explicit VcfLinker             (QObject       * parent       ,
                                    QGraphicsItem * item         ,
                                    Plan          * plan = NULL) ;
    virtual ~VcfLinker             (void) ;

    virtual void     setType       (int Type,SUID relation = 0) ;
    virtual Contour  Render        (void) ;

    virtual void settings          (int item) ;

    virtual bool hasFirst          (void) ;
    virtual bool hasSecond         (void) ;

  protected:

    VcfProxys     Proxys     ;
    VcfWidgets    Widgets    ;
    VcfPoints     Points     ;
    VcfRectangles Rectangles ;
    IMAPs         Markers    ;

    virtual void Configure        (void) ;

    virtual void contextMenuEvent (QGraphicsSceneContextMenuEvent * event) ;
    virtual QVariant itemChange   (GraphicsItemChange change,const QVariant & value) ;

  private:

  public slots:

    virtual void Paint            (QPainter * p,QRectF Region,bool,bool) ;

    virtual bool FocusIn          (void) ;
    virtual bool FocusOut         (void) ;

    virtual bool Menu             (QPointF pos) ;

    virtual void Prepare          (bool line = false,bool dot = false) ;

    virtual void setArrowLine     (int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments) ;
    virtual void setArrowSegments (int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments) ;
    virtual void setArrowLines    (int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments) ;

    virtual void setFirst         (VcfNode * first ) ;
    virtual void setSecond        (VcfNode * second) ;
    virtual void detach           (void) ;

    virtual void setFirst         (QPointF pos) ;
    virtual void setEnd           (QPointF pos) ;

    virtual void ClipPath         (QPainterPath & Path) ;

    virtual void EnableArrow      (int id,bool enable = true) ;

  protected slots:

  private slots:

  signals:

    void Append                   (VcfItem * item,VcfItem * parent) ;
    void Remove                   (VcfItem * item) ;
    void Dissolve                 (VcfItem * item) ;

};

N::VcfLinker:: VcfLinker (QObject * parent,QGraphicsItem * item,Plan * p)
             : VcfLines  (          parent,                item,       p)
             , Relation  (                                              )
{
  Configure ( ) ;
}

N::VcfLinker::~VcfLinker (void)
{
}

void N::VcfLinker::setType (int T,SUID relate)
{
  linkType = T      ;
  relation = relate ;
}

void N::VcfLinker::Configure(void)
{
  setFlag ( ItemIsMovable            , false ) ;
  setFlag ( ItemIsSelectable         , true  ) ;
  setFlag ( ItemIsFocusable          , true  ) ;
  setFlag ( ItemClipsToShape         , false ) ;
  setFlag ( ItemClipsChildrenToShape , false ) ;
  //////////////////////////////////////////////
  Movement = Ignore                            ;
  //////////////////////////////////////////////
  Arrows    [0] = 1                            ; // start arrow
  Arrows    [1] = 1                            ; // end arrow
  Paraments [0] = 0.35                         ; // arrow length
  Paraments [1] = 0.30                         ; // center length
  Paraments [2] = 0.25                         ; // arrow width
}

void N::VcfLinker::Paint(QPainter * p,QRectF Region,bool,bool)
{
  PaintPath  ( p , 1        ) ;
  PaintLines ( p , 3 ,lines ) ;
  PaintPath  ( p , 2        ) ;
}

void N::VcfLinker::contextMenuEvent(QGraphicsSceneContextMenuEvent * event)
{
  if (Menu(event->pos())) event->accept (       ) ;
  else QGraphicsItem::contextMenuEvent  ( event ) ;
}

QVariant N::VcfLinker::itemChange(GraphicsItemChange change,const QVariant & value)
{
  switch (change)                                       {
    case ItemPositionChange                             :
    case ItemPositionHasChanged                         :
    break                                               ;
    case ItemSelectedHasChanged                         :
    break                                               ;
  }                                                     ;
  return QGraphicsItem::itemChange(change,value)        ;
}

bool N::VcfLinker::FocusIn(void)
{
  return false ;
}

bool N::VcfLinker::FocusOut(void)
{
  return false ;
}

void N::VcfLinker::Prepare(bool line,bool dot)
{
  setArrowLines ( 1 , contour , Arrows , Paraments ) ;
  EnablePath    ( 1 , true                         ) ;
  ShowLines     ( line                             ) ;
  if (dot )                                          {
    setPoints   ( 2 , contour                      ) ;
    EnablePath  ( 2 , true                         ) ;
  } else                                             {
    EnablePath  ( 2 , false                        ) ;
  }                                                  ;
  MergePathes   ( 0                                ) ;
}

void N::VcfLinker::setArrowLine(int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments)
{
  VcfShape  vs                                              ;
  bool      startArrow  = ( Arrows[0] == 1 )                ;
  bool      finalArrow  = ( Arrows[1] == 1 )                ;
  double    arrowLength = Paraments [0]                     ;
  double    arrowCenter = Paraments [1]                     ;
  double    arrowWidth  = Paraments [2]                     ;
  double    altotal     = 0                                 ;
  double    lineLength  = 0                                 ;
  int       a  = contour.index[0]                           ;
  int       b  = contour.index[1]                           ;
  QPointF   P1 = contour.points[a].Point()                  ;
  QPointF   P2 = contour.points[b].Point()                  ;
  QPointF   DP = P2 - P1                                    ;
  QPointF   DV = DP                                         ;
  QLineF    LS(P2,P1)                                       ;
  QLineF    LF(P1,P2)                                       ;
  QPolygonF A1                                              ;
  QPolygonF A2                                              ;
  lineLength  = DP.x() * DP.x()                             ;
  lineLength += DP.y() * DP.y()                             ;
  lineLength  = sqrt ( lineLength )                         ;
  DV         /= lineLength                                  ;
  DV         *= arrowCenter                                 ;
  if (startArrow) altotal += arrowLength                    ;
  if (finalArrow) altotal += arrowLength                    ;
  if (lineLength>altotal)                                   {
    if (startArrow)                                         {
      A1  = vs.Triangle(arrowWidth,arrowLength,LS)          ;
      P1 += DV                                              ;
    }                                                       ;
    if (finalArrow)                                         {
      A2  = vs.Triangle(arrowWidth,arrowLength,LF)          ;
      P2 -= DV                                              ;
    }                                                       ;
  } else                                                    {
    startArrow = false                                      ;
    finalArrow = false                                      ;
  }                                                         ;
  ///////////////////////////////////////////////////////////
  QLineF  LE (P1,P2)                                        ;
  ///////////////////////////////////////////////////////////
  QPolygonF    G = vs.WideLine ( contour.thickness.z , LE ) ;
  QPolygonF    F                                            ;
  if (startArrow)                                           {
    F << A1 [ 0 ]                                           ;
    F << A1 [ 1 ]                                           ;
    F << A1 [ 2 ]                                           ;
  }                                                         ;
  F   << G  [ 0 ]                                           ;
  F   << G  [ 1 ]                                           ;
  if (finalArrow)                                           {
    F << A2 [ 0 ]                                           ;
    F << A2 [ 1 ]                                           ;
    F << A2 [ 2 ]                                           ;
  }                                                         ;
  F   << G  [ 2 ]                                           ;
  F   << G  [ 3 ]                                           ;
  ///////////////////////////////////////////////////////////
  QPolygonF    P = toPaper     ( F )                        ;
  QPainterPath path                                         ;
  path . addPolygon ( P )                                   ;
  Painter . pathes [Id] = path                              ;
  update ( )                                                ;
}

void N::VcfLinker::setArrowSegments(int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments)
{
  VcfShape  vs                                              ;
  bool      startArrow  = ( Arrows[0] == 1 )                ;
  bool      finalArrow  = ( Arrows[1] == 1 )                ;
  double    arrowLength = Paraments [0]                     ;
  double    arrowCenter = Paraments [1]                     ;
  double    arrowWidth  = Paraments [2]                     ;
  int       t           = contour.index.count()             ;
  QPolygonF Dots                                            ;
  QPolygonF A1                                              ;
  QPolygonF A2                                              ;
  ///////////////////////////////////////////////////////////
  for (int i=0;i<t;i++)                                     {
    int c = contour.index[i]                                ;
    ControlPoint ncp = contour . points [ c ]               ;
    Dots << QPointF ( ncp.x , ncp.y )                       ;
  }                                                         ;
  ///////////////////////////////////////////////////////////
  if (startArrow)                                           {
    QPointF P1         = Dots[0]                            ;
    QPointF P2         = Dots[1]                            ;
    QPointF DP         = P2 - P1                            ;
    QPointF DV         = DP                                 ;
    QLineF  LS (P2,P1)                                      ;
    double  lineLength = 0                                  ;
    lineLength  = DP.x() * DP.x()                           ;
    lineLength += DP.y() * DP.y()                           ;
    lineLength  = sqrt ( lineLength )                       ;
    DV         /= lineLength                                ;
    DV         *= arrowCenter                               ;
    if (lineLength>arrowLength)                             {
      A1         = vs.Triangle(arrowWidth,arrowLength,LS)   ;
      P1        += DV                                       ;
      Dots [ 0 ] = P1                                       ;
    } else startArrow = false                               ;
  }                                                         ;
  ///////////////////////////////////////////////////////////
  if (finalArrow)                                           {
    QPointF P1         = Dots[t-1]                          ;
    QPointF P2         = Dots[t-2]                          ;
    QPointF DP         = P2 - P1                            ;
    QPointF DV         = DP                                 ;
    QLineF  LS (P2,P1)                                      ;
    double  lineLength = 0                                  ;
    lineLength  = DP.x() * DP.x()                           ;
    lineLength += DP.y() * DP.y()                           ;
    lineLength  = sqrt ( lineLength )                       ;
    DV         /= lineLength                                ;
    DV         *= arrowCenter                               ;
    if (lineLength>arrowLength)                             {
      A2         = vs.Triangle(arrowWidth,arrowLength,LS)   ;
      P1        += DV                                       ;
      Dots [t-1] = P1                                       ;
    } else finalArrow = false                               ;
  }                                                         ;
  ///////////////////////////////////////////////////////////
  QPolygonF G = vs.FoldLines (contour.thickness.z,Dots)     ;
  QPolygonF F                                               ;
  int sid = 0                                               ;
  if (startArrow)                                           {
    F << A1 [ 0 ]                                           ;
    F << A1 [ 1 ]                                           ;
    F << A1 [ 2 ]                                           ;
  }                                                         ;
  for (int i=0;i<t;i++,sid++) F << G [ sid ]                ;
  if (finalArrow)                                           {
    F << A2 [ 0 ]                                           ;
    F << A2 [ 1 ]                                           ;
    F << A2 [ 2 ]                                           ;
  }                                                         ;
  for (int i=0;i<t;i++,sid++) F << G [ sid ]                ;
  ///////////////////////////////////////////////////////////
  QPolygonF    P = toPaper     ( F )                        ;
  QPainterPath path                                         ;
  path . addPolygon ( P )                                   ;
  Painter . pathes [Id] = path                              ;
  update ( )                                                ;
}

void N::VcfLinker::setArrowLines(int Id,Contour & contour,IMAPs & arrows,DMAPs & paraments)
{
  if (contour.count()<2) return                      ;
  if (contour.count()==2)                            {
    Contour C = Render ( )                           ;
    setArrowLine     ( Id , C , arrows , paraments ) ;
  } else                                             {
    Contour C = Render ( )                           ;
    setArrowSegments ( Id , C , arrows , paraments ) ;
  }                                                  ;
}

N::Contour N::VcfLinker::Render(void)
{
  Contour C = contour ;
  return  C           ;
}

bool N::VcfLinker::Menu(QPointF pos)
{
  nScopedMenu ( mm , GraphicsView() )  ;
  bool         editing = false         ;
  QMenu      * mx                      ;
  QAction    * aa                      ;
  if (Painter.switches.contains(2))    {
    editing = Painter.switches[2]      ;
  }                                    ;
  if (!editing) mm.add(101,tr("Edit")) ;
  if ( editing) mm.add(102,tr("Done")) ;
  //////////////////////////////////////
  mm . setFont   ( plan )              ;
  aa = mm . exec (      )              ;
  if (IsNull(aa)) return true          ;
  //////////////////////////////////////
  switch (mm[aa])                      {
    case 101                           :
      Prepare    ( false , true  )     ;
    break                              ;
    case 102                           :
      EnablePath (     2 , false )     ;
      Painter . pathes . remove ( 2 )  ;
      update ( )                       ;
    break                              ;
  }                                    ;
  return true                          ;
}

void N::VcfLinker::settings(int item)
{
}

bool N::VcfLinker::hasFirst(void)
{
  return Linking.contains(0) ;
}

bool N::VcfLinker::hasSecond(void)
{
  return Linking.contains(1) ;
}

void N::VcfLinker::setFirst(VcfNode * first)
{
  if (IsNull(first))    {
    Linking . remove(0) ;
  } else                {
    Linking [0] = first ;
  }                     ;
}

void N::VcfLinker::setSecond(VcfNode * second)
{
  if (IsNull(second))    {
    Linking . remove(1)  ;
  } else                 {
    Linking [1] = second ;
  }                      ;
}

void N::VcfLinker::setFirst(QPointF pos)
{
  int index = contour.index[0] ;
  contour.points[index] = pos  ;
}

void N::VcfLinker::setEnd(QPointF pos)
{
  int index = contour.index.count() - 1 ;
  index     = contour.index[index]      ;
  contour   . points[index] = pos       ;
}

void N::VcfLinker::ClipPath(QPainterPath & Path)
{
  QPainterPath p = Painter.pathes[1] ;
  QPainterPath s = Path              ;
  p = p.subtracted(s)                ;
  Painter.pathes[1] = p              ;
}

void N::VcfLinker::detach(void)
{
  Linking . clear ( ) ;
}

void N::VcfLinker::EnableArrow(int id,bool enable)
{
  Arrows [ id ] = enable ? 1 : 0 ;
}
"""

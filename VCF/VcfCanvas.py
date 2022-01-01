# -*- coding: utf-8 -*-
##############################################################################
## VcfCanvas
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
class VcfCanvas       (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfCanvas : public VcfRectangle
                                    , public Object
{
  Q_OBJECT
  public:

    enum CanvasMode {
      Empty  = 0    ,
      Border = 1    ,
      Board  = 2    ,
      Custom = 3  } ;

    int  Mode       ;

    enum { Type = UserType + VCF::Canvas };
    virtual int type(void) const { return Type; }

    explicit VcfCanvas                 (QObject       * parent       ,
                                        QGraphicsItem * item         ,
                                        Plan          * plan = NULL) ;
    virtual ~VcfCanvas                 (void);

    virtual void paint                 (QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget = 0);

    virtual void settings              (int item) ;

  protected:

    bool GradientEditing ;

    virtual void contextMenuEvent      (QGraphicsSceneContextMenuEvent * event);
    virtual void Hovering              (QPointF pos);
    virtual void setCornerCursor       (int corner);

    virtual void mouseDoubleClickEvent (QGraphicsSceneMouseEvent * event);
    virtual void mouseMoveEvent        (QGraphicsSceneMouseEvent * event);
    virtual void mousePressEvent       (QGraphicsSceneMouseEvent * event);
    virtual void mouseReleaseEvent     (QGraphicsSceneMouseEvent * event);

    virtual void MountZLevel           (QGraphicsProxyWidget * proxy,QSlider * slider);
    virtual void MountOpacity          (QGraphicsProxyWidget * proxy,QSlider * slider);
    virtual void MountRotation         (QGraphicsProxyWidget * proxy,QDial   * dial  );
    virtual void RotationUpdated       (void);
    virtual void NormalTransform       (void);

    virtual bool dropColor             (QWidget * source,QPointF pos,const QColor & color   ) ;
    virtual bool dropTags              (QWidget * source,QPointF pos,const UUIDs  & Uuids   ) ;
    virtual bool dropPen               (QWidget * source,QPointF pos,const SUID     pen     ) ;
    virtual bool dropBrush             (QWidget * source,QPointF pos,const SUID     brush   ) ;
    virtual bool dropGradient          (QWidget * source,QPointF pos,const SUID     gradient) ;

  private:

    QRectF       PanelRect             (void);
    QRectF       CenterRect            (void);

  public slots:

    virtual void Paint                 (QPainter * painter,QRectF Region,bool clip,bool color) ;
    virtual void setCanvas             (QRectF selection) ;

    virtual void addAdjustMenu         (MenuManager & menu) ;
    virtual void addFontMenu           (MenuManager & menu) ;
    virtual void addPenMenu            (MenuManager & menu) ;
    virtual void addBrushMenu          (MenuManager & menu) ;
    virtual void addGradientMenu       (MenuManager & menu) ;

    virtual bool MenuCommands          (int Id,QAction * Action) ;

    virtual void SavePen               (void) ;
    virtual void SaveBrush             (void) ;
    virtual void SaveGradient          (void) ;

    virtual void SaveContours          (void) ;

  protected slots:

    virtual void PenFinished           (void) ;
    virtual void BrushFinished         (void) ;
    virtual void GradientFinished      (void) ;
    virtual void ContourFinished       (void) ;

  private slots:

  signals:

    void Menu                          (VcfCanvas * canvas,QPointF pos);
    void ShapeName                     (VcfCanvas * canvas,QString name);

};


N::VcfCanvas:: VcfCanvas       (QObject * parent,QGraphicsItem * item,Plan * p)
             : VcfRectangle    (          parent,                item,       p)
             , Object          (0,Types::None                                 )
             , Mode            (Empty                                         )
             , GradientEditing (false                                         )
{
  Printable = false                                     ;
  Scaling   = true                                      ;
  setFlag     ( ItemIsMovable            , true  )      ;
  setFlag     ( ItemIsSelectable         , true  )      ;
  setFlag     ( ItemIsFocusable          , true  )      ;
  setFlag     ( ItemClipsToShape         , false )      ;
  setFlag     ( ItemClipsChildrenToShape , false )      ;
  Painter . addMap   ( "Default" , 0                  ) ;
  Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 ) ) ;
  Painter . addBrush ( 0 , QColor ( 240 , 240 , 240 ) ) ;
  Painter . pens [ 0 ] . setWidthF ( 2.8 )              ;
  ///////////////////////////////////////////////////////
  setDropFlag ( DropText     , false )                  ;
  setDropFlag ( DropUrls     , false )                  ;
  setDropFlag ( DropImage    , false )                  ;
  setDropFlag ( DropHtml     , false )                  ;
  setDropFlag ( DropColor    , true  )                  ;
  setDropFlag ( DropTag      , true  )                  ;
  setDropFlag ( DropPicture  , false )                  ;
  setDropFlag ( DropPeople   , false )                  ;
  setDropFlag ( DropVideo    , false )                  ;
  setDropFlag ( DropAlbum    , false )                  ;
  setDropFlag ( DropGender   , false )                  ;
  setDropFlag ( DropDivision , false )                  ;
  setDropFlag ( DropURIs     , false )                  ;
  setDropFlag ( DropBookmark , false )                  ;
  setDropFlag ( DropFont     , false )                  ;
  setDropFlag ( DropPen      , true  )                  ;
  setDropFlag ( DropBrush    , true  )                  ;
  setDropFlag ( DropGradient , true  )                  ;
}

N::VcfCanvas::~VcfCanvas(void)
{
}

void N::VcfCanvas::contextMenuEvent(QGraphicsSceneContextMenuEvent * e)
{
  if (   isFunction ( 32001 ) )           {
    QGraphicsItem::contextMenuEvent ( e ) ;
  } else                                  {
    if ( isFunction ( 32002 ) )           {
      emit Menu   ( this , e -> pos ( ) ) ;
    }                                     ;
    e -> accept (                       ) ;
  }                                       ;
}

void N::VcfCanvas::paint(QPainter * p,const QStyleOptionGraphicsItem *,QWidget *)
{
  Paint ( p , ScreenRect , false , true ) ;
}

void N::VcfCanvas::Hovering(QPointF pos)
{
}

void N::VcfCanvas::setCornerCursor(int Corner)
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

void N::VcfCanvas::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
{
  QGraphicsItem :: mouseDoubleClickEvent ( event ) ;
  DeleteGadgets                          (       ) ;
}

void N::VcfCanvas::mousePressEvent(QGraphicsSceneMouseEvent * event)
{
  if (GradientEditing)      {
    QLinearGradient  * linear  = Painter.gradients[0].linear () ;
    QRadialGradient  * radial  = Painter.gradients[0].radial () ;
    QConicalGradient * conical = Painter.gradients[0].conical() ;
    if (NotNull(linear ))                                       {
      QPointF p = event->pos()                                  ;
      QPointF t = ScreenRect.topLeft()                          ;
      QPointF b = ScreenRect.bottomLeft()                       ;
      QColor  c = Painter.gradients[0].color                    ;
      double  r = ( p.y() - t.y() ) / ( b.y() - t.y() )         ;
      linear->setColorAt(r,c)                                   ;
      Painter . brushes  [0] = Brush(*linear)                   ;
    } else
    if (NotNull(radial ))                                       {
      int     s = Painter.gradients[0].step                     ;
      QPointF p = event->pos()                                  ;
      QColor  c = Painter.gradients[0].color                    ;
      QPointF r                                                 ;
      switch (s)                                                {
        case 1                                                  :
          radial -> setColorAt(0,c)                             ;
          radial -> setCenter(p)                                ;
          s = 2                                                 ;
        break                                                   ;
        case 2                                                  :
          r = radial->center()                                  ;
          r = r - p                                             ;
          radial->setCenterRadius(r.manhattanLength())          ;
          s = 3                                                 ;
        break                                                   ;
        case 3                                                  :
          radial -> setColorAt(1.0,c    )                       ;
          radial -> setFocalPoint (p)                           ;
          s = 4                                                 ;
        break                                                   ;
        case 4                                                  :
          r = radial->focalPoint()                              ;
          r = r - p                                             ;
          radial->setFocalRadius(r.manhattanLength())           ;
          GradientEditing = false                               ;
          s = 0                                                 ;
        break                                                   ;
      }                                                         ;
      Painter . gradients[0] . step = s                         ;
      Painter . brushes  [0]        = Brush(*radial)            ;
    } else
    if (NotNull(conical))                                       {
      int     s = Painter.gradients[0].step                     ;
      QPointF p = event->pos()                                  ;
      QColor  c = Painter.gradients[0].color                    ;
      QLineF  l                                                 ;
      switch (s)                                                {
        case 1                                                  :
          conical -> setCenter (p)                              ;
          conical -> setColorAt(0,c)                            ;
          s = 2                                                 ;
        break                                                   ;
        case 2                                                  :
          GradientEditing = false                               ;
          l . setP1 (conical->center())                         ;
          l . setP2 (p                )                         ;
          conical -> setAngle  (l.angle())                      ;
          conical -> setColorAt(1.0,c    )                      ;
          s = 0                                                 ;
        break                                                   ;
      }                                                         ;
      Painter . gradients[0] . step = s                         ;
      Painter . brushes  [0]        = Brush(*conical)           ;
    }                                                           ;
  }                                                             ;
  scalePressEvent ( event )                                     ;
  DeleteGadgets   (       )                                     ;
}

void N::VcfCanvas::mouseMoveEvent(QGraphicsSceneMouseEvent * event)
{
  scaleMoveEvent ( event ) ;
}

void N::VcfCanvas::mouseReleaseEvent(QGraphicsSceneMouseEvent * event)
{
  scaleReleaseEvent ( event ) ;
}

void N::VcfCanvas::Paint(QPainter * p,QRectF,bool,bool)
{
  pushPainters             ( p                          ) ;
  switch (Mode)                                           {
    case Empty                                            :
    break                                                 ;
    case Border                                           :
      Painter . drawBorder ( p , "Default" , ScreenRect ) ;
    break                                                 ;
    case Board                                            :
      Painter . drawRect   ( p , "Default" , ScreenRect ) ;
    break                                                 ;
  }                                                       ;
  popPainters              ( p                          ) ;
}

void N::VcfCanvas::setCanvas(QRectF selection)
{
  QGraphicsItem::setPos(QPointF(0,0)) ;
  ScreenRect = selection              ;
  prepareGeometryChange          (  ) ;
}

void N::VcfCanvas::addAdjustMenu(MenuManager & menu)
{
  DeleteGadgets()                               ;
  bool movable = IsMask (flags(),ItemIsMovable) ;
  QAction * aa                                  ;
  if (uuid>0)                                   {
    aa  = menu.add(1,QString::number(uuid))     ;
    aa -> setEnabled(false)                     ;
  }                                             ;
  QMenu * ma = menu.addMenu(tr("Adjustments" )) ;
  aa  = menu.add(ma,10001,tr("Movable"       )) ;
  aa -> setCheckable ( true    )                ;
  aa -> setChecked   ( movable )                ;
  aa  = menu.add(ma,10002,tr("Resizable"     )) ;
  aa -> setCheckable ( true    )                ;
  aa -> setChecked   ( Scaling                ) ;
        menu.addSeparator ( ma )                ;
        menu.add(ma,10003,tr("Z level"       )) ;
        menu.add(ma,10004,tr("Opacity"       )) ;
        menu.add(ma,10005,tr("Rotate"        )) ;
}

void N::VcfCanvas::addFontMenu(MenuManager & menu)
{
}

void N::VcfCanvas::addPenMenu(MenuManager & menu)
{
  QMenu   * pm = menu.addMenu(tr("Pen"               )) ;
  QMenu   * ps                                          ;
  QMenu   * cs                                          ;
  QMenu   * js                                          ;
  QAction * aa                                          ;
        menu.add(pm,11001,tr("Save pen configuration")) ;
        menu.addSeparator ( pm                        ) ;
        menu.add(pm,11002,tr("Pen color"             )) ;
        menu.addSeparator ( pm                        ) ;
        menu.add(pm,11003,tr("Line width"            )) ;
        menu.add(pm,11004,tr("Miter limit"           )) ;
  aa  = menu.add(pm,11005,tr("Cosmetic"              )) ;
  aa -> setCheckable ( true                           ) ;
  aa -> setChecked   (Painter.pens[0].isCosmetic()    ) ;
        menu.addSeparator ( pm                        ) ;
  ps  = menu.addMenu(pm,tr("Pen styles"              )) ;
  cs  = menu.addMenu(pm,tr("Pen cap styles"          )) ;
  js  = menu.addMenu(pm,tr("Pen join styles"         )) ;
        menu.add(ps,11101,tr("No pen"                )) ;
        menu.add(ps,11102,tr("Solid pen"             )) ;
        menu.add(ps,11103,tr("Dash line"             )) ;
        menu.add(ps,11104,tr("Dot line"              )) ;
        menu.add(ps,11105,tr("Dash dot line"         )) ;
        menu.add(ps,11106,tr("Dash dot dot line"     )) ;
        menu.add(cs,11201,tr("Flat cap style"        )) ;
        menu.add(cs,11202,tr("Square cap style"      )) ;
        menu.add(cs,11203,tr("Round cap style"       )) ;
        menu.add(js,11301,tr("Miter join"            )) ;
        menu.add(js,11302,tr("Bevel join"            )) ;
        menu.add(js,11303,tr("Round join"            )) ;
        menu.add(js,11304,tr("SVG Miter join"        )) ;
}

void N::VcfCanvas::addBrushMenu(MenuManager & menu)
{
  QMenu * bm = menu.addMenu(tr("Brush"           )) ;
  menu.add(bm,12001,tr("Save brush configuration")) ;
  menu.addSeparator(bm                            ) ;
  menu.add(bm,12002,tr("Brush color"             )) ;
  QMenu * bs = menu.addMenu(bm,tr("Brush styles" )) ;
  menu.add(bs,12011,tr("No brush"                )) ;
  menu.add(bs,12012,tr("Solid pattern"           )) ;
  menu.add(bs,12013,tr("Dense 1"                 )) ;
  menu.add(bs,12014,tr("Dense 2"                 )) ;
  menu.add(bs,12015,tr("Dense 3"                 )) ;
  menu.add(bs,12016,tr("Dense 4"                 )) ;
  menu.add(bs,12017,tr("Dense 5"                 )) ;
  menu.add(bs,12018,tr("Dense 6"                 )) ;
  menu.add(bs,12019,tr("Dense 7"                 )) ;
  menu.add(bs,12020,tr("Horizontal lines"        )) ;
  menu.add(bs,12021,tr("Vertical lines"          )) ;
  menu.add(bs,12022,tr("Crossing lines"          )) ;
  menu.add(bs,12023,tr("Backward diagonal lines" )) ;
  menu.add(bs,12024,tr("Forward diagonal lines"  )) ;
  menu.add(bs,12025,tr("Crossing diagonal lines" )) ;
}

void N::VcfCanvas::addGradientMenu(MenuManager & menu)
{
  QMenu * bm = menu.addMenu(tr("Gradient"             )) ;
  if (Painter.gradients.contains(0))                     {
    menu.add(bm,13001,tr("Save gradient configuration")) ;
    menu.add(bm,13002,tr("Gradient colors"            )) ;
    menu.add(bm,13003,tr("Gradient points"            )) ;
  }                                                      ;
  QMenu * bs = menu.addMenu(bm,tr("Gradient styles"   )) ;
  menu.add(bs,13011,tr("No gradient"                  )) ;
  menu.add(bs,13012,tr("Linear gradient"              )) ;
  menu.add(bs,13013,tr("Conical gradient"             )) ;
  menu.add(bs,13014,tr("Radial gradient"              )) ;
}

bool N::VcfCanvas::MenuCommands(int Id,QAction * Action)
{
  QLinearGradient  * linear                                        ;
  QConicalGradient * conical                                       ;
  QRadialGradient  * radial                                        ;
  DeleteGadgets()                                                  ;
  switch (Id)                                                      {
    case 10003                                                     :
      AttachZLevel   ( )                                           ;
    break                                                          ;
    case 10004                                                     :
      AttachOpacity  ( )                                           ;
    break                                                          ;
    case 10005                                                     :
      AttachRotation ( )                                           ;
    break                                                          ;
    case 11005                                                     :
      Painter.pens[0].setCosmetic(Action->isChecked() )            ;
    return true                                                    ;
    case 11101                                                     :
      Painter.pens[0].setStyle ( Qt::NoPen          )              ;
    return true                                                    ;
    case 11102                                                     :
      Painter.pens[0].setStyle ( Qt::SolidLine      )              ;
    return true                                                    ;
    case 11103                                                     :
      Painter.pens[0].setStyle ( Qt::DashLine       )              ;
    return true                                                    ;
    case 11104                                                     :
      Painter.pens[0].setStyle ( Qt::DotLine        )              ;
    return true                                                    ;
    case 11105                                                     :
      Painter.pens[0].setStyle ( Qt::DashDotLine    )              ;
    return true                                                    ;
    case 11106                                                     :
      Painter.pens[0].setStyle ( Qt::DashDotDotLine )              ;
    return true                                                    ;
    case 11201                                                     :
      Painter.pens[0].setCapStyle ( Qt::FlatCap       )            ;
    return true                                                    ;
    case 11202                                                     :
      Painter.pens[0].setCapStyle ( Qt::SquareCap     )            ;
    return true                                                    ;
    case 11203                                                     :
      Painter.pens[0].setCapStyle ( Qt::RoundCap      )            ;
    return true                                                    ;
    case 11301                                                     :
      Painter.pens[0].setJoinStyle ( Qt::MiterJoin    )            ;
    return true                                                    ;
    case 11302                                                     :
      Painter.pens[0].setJoinStyle ( Qt::BevelJoin    )            ;
    return true                                                    ;
    case 11303                                                     :
      Painter.pens[0].setJoinStyle ( Qt::RoundJoin    )            ;
    return true                                                    ;
    case 11304                                                     :
      Painter.pens[0].setJoinStyle ( Qt::SvgMiterJoin )            ;
    return true                                                    ;
    case 12011                                                     :
      Painter.brushes[0].setStyle(Qt::NoBrush         )            ;
    return true                                                    ;
    case 12012                                                     :
      Painter.brushes[0].setStyle(Qt::SolidPattern    )            ;
    return true                                                    ;
    case 12013                                                     :
      Painter.brushes[0].setStyle(Qt::Dense1Pattern   )            ;
    return true                                                    ;
    case 12014                                                     :
      Painter.brushes[0].setStyle(Qt::Dense2Pattern   )            ;
    return true                                                    ;
    case 12015                                                     :
      Painter.brushes[0].setStyle(Qt::Dense3Pattern   )            ;
    return true                                                    ;
    case 12016                                                     :
      Painter.brushes[0].setStyle(Qt::Dense4Pattern   )            ;
    return true                                                    ;
    case 12017                                                     :
      Painter.brushes[0].setStyle(Qt::Dense5Pattern   )            ;
    return true                                                    ;
    case 12018                                                     :
      Painter.brushes[0].setStyle(Qt::Dense6Pattern   )            ;
    return true                                                    ;
    case 12019                                                     :
      Painter.brushes[0].setStyle(Qt::Dense7Pattern   )            ;
    return true                                                    ;
    case 12020                                                     :
      Painter.brushes[0].setStyle(Qt::HorPattern      )            ;
    return true                                                    ;
    case 12021                                                     :
      Painter.brushes[0].setStyle(Qt::VerPattern      )            ;
    return true                                                    ;
    case 12022                                                     :
      Painter.brushes[0].setStyle(Qt::CrossPattern    )            ;
    return true                                                    ;
    case 12023                                                     :
      Painter.brushes[0].setStyle(Qt::BDiagPattern    )            ;
    return true                                                    ;
    case 12024                                                     :
      Painter.brushes[0].setStyle(Qt::FDiagPattern    )            ;
    return true                                                    ;
    case 12025                                                     :
      Painter.brushes[0].setStyle(Qt::DiagCrossPattern)            ;
    return true                                                    ;
    case 13001                                                     :
    return true                                                    ;
    case 13002                                                     :
    return true                                                    ;
    case 13003                                                     :
      if (GradientEditing)                                         {
        GradientEditing           = false                          ;
      } else                                                       {
        GradientEditing           = true                           ;
        Painter.gradients[0].step = 1                              ;
      }                                                            ;
    return true                                                    ;
    case 13011                                                     :
      Painter.brushes[0] = Painter.brushes[-1]                     ;
      Painter.gradients.remove(0)                                  ;
    return true                                                    ;
    case 13012                                                     :
      Painter.brushes  [-1] = Painter.brushes[0]                   ;
      Painter.gradients[ 0] = Gradient(QGradient::LinearGradient ) ;
      linear = Painter . gradients[0] .linear()                    ;
      linear -> setStart     ( ScreenRect . topLeft    () )        ;
      linear -> setFinalStop ( ScreenRect . bottomLeft () )        ;
      Painter . brushes  [0] = Brush(*linear)                      ;
    return true                                                    ;
    case 13013                                                     :
      Painter.brushes  [-1] = Painter.brushes[0]                   ;
      Painter.gradients[ 0] = Gradient(QGradient::ConicalGradient) ;
      conical = Painter . gradients[0] .conical()                  ;
      Painter . brushes  [0] = Brush(*conical)                     ;
    return true                                                    ;
    case 13014                                                     :
      Painter.brushes  [-1] = Painter.brushes[0]                   ;
      Painter.gradients[ 0] = Gradient(QGradient::RadialGradient ) ;
      radial  = Painter . gradients[0] .radial()                   ;
      Painter . brushes  [0] = Brush(*radial )                     ;
    return true                                                    ;
  }                                                                ;
  update ( )                                                       ;
  return false                                                     ;
}

QRectF N::VcfCanvas::PanelRect(void)
{
  QPointF X ( 3.0 , 0.40 )                                               ;
  QPointF TL = ScreenRect . bottomLeft ( )                               ;
  TL = mapToScene          ( TL )                                        ;
  TL = Options -> Standard ( TL )                                        ;
  QRectF Z ( TL.x() , TL.y() , X.x() , X.y() )                           ;
  Z  = Options -> Region ( Z )                                           ;
  Z  = mapFromScene ( Z ) . boundingRect ( )                             ;
  return QRectF(ScreenRect.left(),Z.top(),ScreenRect.width(),Z.height()) ;
}

QRectF N::VcfCanvas::CenterRect(void)
{
  QPointF X(3.0,3.0)                             ;
  QPointF H = X / 2                              ;
  QPointF C = ScreenRect.center()                ;
  C = mapToScene(C)                              ;
  C = Options->Standard(C)                       ;
  QRectF Z (C.x()-H.x(),C.y()-H.y(),X.x(),X.y()) ;
  Z  = Options->Region(Z)                        ;
  return Z                                       ;
}

void N::VcfCanvas::MountZLevel(QGraphicsProxyWidget * proxy,QSlider * slider)
{
  Proxys  [1] = proxy       ;
  Widgets [1] = slider      ;
  QRectF R = PanelRect()    ;
  proxy->setGeometry(R    ) ;
  proxy->setZValue  (0.90f) ;
  proxy->setOpacity (0.75f) ;
}

void N::VcfCanvas::MountOpacity(QGraphicsProxyWidget * proxy,QSlider * slider)
{
  Proxys  [2] = proxy       ;
  Widgets [2] = slider      ;
  QRectF R = PanelRect()    ;
  proxy->setGeometry(R)     ;
  proxy->setZValue  (0.90f) ;
  proxy->setOpacity (0.75f) ;
}

void N::VcfCanvas::MountRotation(QGraphicsProxyWidget * proxy,QDial * dial)
{
  Proxys  [3] = proxy       ;
  Widgets [3] = dial        ;
  QRectF R = CenterRect()   ;
  qreal  z = zValue()       ;
  z += 0.90f                ;
  if (z>1.0) z = 1.0        ;
  proxy->setGeometry(R)     ;
  proxy->setZValue  (z    ) ;
  proxy->setOpacity (0.75f) ;
}

void N::VcfCanvas::RotationUpdated(void)
{
  QTransform T = Transform ;
  T = T.rotate(Angle)      ;
  setTransform(T)          ;
}

void N::VcfCanvas::NormalTransform(void)
{
  QTransform T            ;
  T.reset()               ;
  Angle = 0.0             ;
//  qreal sx = Options->DPI ;
//  qreal sy = Options->DPI ;
//  sx /= PictureDPI        ;
//  sy /= PictureDPI        ;
//  T = T.scale(sx,sy)      ;
  Transform = T           ;
  setTransform(T)         ;
}

void N::VcfCanvas::SavePen(void)
{
  DeleteGadgets                (     )  ;
  QLineEdit * le = NewLineEdit (4    )  ;
  QRectF      R  = PanelRect   (     )  ;
  Proxys [ 4 ]  -> setGeometry (R    )  ;
  Proxys [ 4 ]  -> setZValue   (0.90f)  ;
  Proxys [ 4 ]  -> setOpacity  (1.00f)  ;
  le->setText(Painter.pens[0].name   )  ;
  connect(le,SIGNAL(editingFinished())  ,
          this,SLOT(PenFinished    ())) ;
  le -> setFocus ( Qt::TabFocusReason ) ;
}

void N::VcfCanvas::PenFinished(void)
{
  QString     name = ""                                    ;
  QLineEdit * le   = qobject_cast<QLineEdit *>(Widgets[4]) ;
  if (NotNull(le)) name = le -> text ( )                   ;
  DeleteGadgets ( )                                        ;
  if (name.length()<=0) return                             ;
  Painter.pens[0].name = name                              ;
  GraphicsManager GM ( plan                    )           ;
  EnterSQL           ( SC , plan->sql          )           ;
  GM . SavePen       ( SC , Painter . pens[0]  )           ;
  LeaveSQL           ( SC , plan->sql          )           ;
  Alert              ( Done                    )           ;
}

void N::VcfCanvas::SaveBrush(void)
{
  DeleteGadgets                (     )  ;
  QLineEdit * le = NewLineEdit (4    )  ;
  QRectF      R  = PanelRect   (     )  ;
  Proxys [ 4 ]  -> setGeometry (R    )  ;
  Proxys [ 4 ]  -> setZValue   (0.90f)  ;
  Proxys [ 4 ]  -> setOpacity  (1.00f)  ;
  le->setText(Painter.brushes[0].name)  ;
  connect(le,SIGNAL(editingFinished())  ,
          this,SLOT(BrushFinished  ())) ;
  le -> setFocus ( Qt::TabFocusReason ) ;
}

void N::VcfCanvas::BrushFinished(void)
{
  QString     name = ""                                    ;
  QLineEdit * le   = qobject_cast<QLineEdit *>(Widgets[4]) ;
  if (NotNull(le)) name = le -> text ( )                   ;
  DeleteGadgets ( )                                        ;
  if (name.length()<=0) return                             ;
  Painter.brushes[0].name = name                           ;
  GraphicsManager GM ( plan                    )           ;
  EnterSQL           ( SC , plan->sql          )           ;
  GM . SaveBrush     ( SC , Painter.brushes[0] )           ;
  LeaveSQL           ( SC , plan->sql          )           ;
  Alert              ( Done                    )           ;
}

void N::VcfCanvas::SaveGradient(void)
{
  DeleteGadgets                (     )   ;
  QLineEdit * le = NewLineEdit (4    )   ;
  QRectF      R  = PanelRect   (     )   ;
  Proxys [ 4 ]  -> setGeometry (R    )   ;
  Proxys [ 4 ]  -> setZValue   (0.90f)   ;
  Proxys [ 4 ]  -> setOpacity  (1.00f)   ;
  le->setText(Painter.brushes[0].name)   ;
  connect(le,SIGNAL(editingFinished ())  ,
          this,SLOT(GradientFinished())) ;
  le -> setFocus ( Qt::TabFocusReason  ) ;
}

void N::VcfCanvas::GradientFinished(void)
{
  QString     name = ""                                    ;
  QLineEdit * le   = qobject_cast<QLineEdit *>(Widgets[4]) ;
  if (NotNull(le)) name = le -> text ( )                   ;
  DeleteGadgets ( )                                        ;
  if (name.length()<=0) return                             ;
  Painter.gradients[0].name = name                         ;
  GraphicsManager GM ( plan                      )         ;
  EnterSQL           ( SC , plan->sql            )         ;
  GM . SaveGradient  ( SC , Painter.gradients[0] )         ;
  LeaveSQL           ( SC , plan->sql            )         ;
  GradientEditing  = false                                 ;
  Alert ( Done )                                           ;
}

void N::VcfCanvas::settings(int item)
{
}

void N::VcfCanvas::SaveContours(void)
{
  DeleteGadgets                (     )  ;
  QLineEdit * le = NewLineEdit (4    )  ;
  QRectF      R  = PanelRect   (     )  ;
  Proxys [ 4 ]  -> setGeometry (R    )  ;
  Proxys [ 4 ]  -> setZValue   (0.90f)  ;
  Proxys [ 4 ]  -> setOpacity  (1.00f)  ;
  le->setText(Painter.brushes[0].name)  ;
  connect(le,SIGNAL(editingFinished())  ,
          this,SLOT(ContourFinished())) ;
  le -> setFocus ( Qt::TabFocusReason ) ;
}

void N::VcfCanvas::ContourFinished(void)
{
  QString     name = ""                            ;
  QLineEdit * le   = Casting(QLineEdit,Widgets[4]) ;
  if (NotNull(le)) name = le -> text ( )           ;
  DeleteGadgets ( )                                ;
  if (name.length()<=0) return                     ;
  emit ShapeName ( this , name )                   ;
}

bool N::VcfCanvas::dropColor(QWidget * source,QPointF pos,const QColor & color)
{
  return true ;
}

bool N::VcfCanvas::dropTags(QWidget * source,QPointF pos,const UUIDs & Uuids)
{
  return true ;
}

bool N::VcfCanvas::dropPen(QWidget * source,QPointF pos,const SUID pen)
{
  FetchPen ( 0 , pen ) ;
  update   (         ) ;
  return true          ;
}

bool N::VcfCanvas::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{
  FetchBrush ( 0 , brush ) ;
  update     (           ) ;
  return true              ;
}

bool N::VcfCanvas::dropGradient(QWidget * source,QPointF pos,const SUID gradient)
{ Q_UNUSED ( source )                                          ;
  Q_UNUSED ( pos    )                                          ;
  FetchGradient ( 0 , gradient )                               ;
  QLinearGradient * linear = Painter.gradients[0].linear()     ;
  if (NotNull(linear))                                         {
    linear->setStart(ScreenRect.topLeft())                     ;
    linear->setFinalStop(ScreenRect.bottomLeft())              ;
  }                                                            ;
  Painter.brushes[0] = Brush(*(Painter.gradients[0].gradient)) ;
  update        (              )                               ;
  return true                                                  ;
}
"""

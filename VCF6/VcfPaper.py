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
from         . VcfRectangle           import VcfRectangle as VcfRectangle
##############################################################################
class VcfPaper                 ( VcfRectangle                              ) :
  ############################################################################
  def __init__                 ( self                                      , \
                                 parent = None                             , \
                                 item   = None                             , \
                                 plan   = None                             ) :
    ##########################################################################
    super ( ) . __init__       ( parent , item , plan                        )
    self . setVcfPaperDefaults (                                             )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPaperDefaults ( self                                           ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def shape             ( self                                             ) :
    ##########################################################################
    path = QPainterPath (                                                    )
    path . addRect      ( self . ScreenRect                                  )
    ##########################################################################
    return path
  ############################################################################
  def hoverMoveEvent ( self , event ) :
    ##########################################################################
    """
    VcfRectangle::hoverMoveEvent(event)         ;
    if (IsNull(plan)) return                    ;
    QPointF pf = event -> pos          (      ) ;
    QPointF ps = mapToScene            (pf    ) ;
    QPointF px = plan  -> toCentimeter (pf,DPI) ;
    emit Moving ( Name , px , ps , pf )         ;
    """
    ##########################################################################
    return
  ############################################################################
  def PaperEditing ( self ) :
    ##########################################################################
    """
    QRectF Range = PaperRange()                                    ;
    QRectF R(Range . left   () + Borders[Left]                     ,
             Range . top    () + Borders[Top ]                     ,
             Range . width  () - Borders[Left] - Borders[Right ]   ,
             Range . height () - Borders[Top ] - Borders[Bottom] ) ;
    return R                                                       ;
  """
    ##########################################################################
    return
  ############################################################################
  def paint         ( self , painter , options , widget                    ) :
    ##########################################################################
    self . Painting (        painter , self . ScreenRect , True , True       )
    ##########################################################################
    return
  ############################################################################
  def Painting                    ( self , p , region , clip , color       ) :
    ##########################################################################
    self . pushPainters           ( p                                        )
    ##########################################################################
    """
    switch (Style)                         {
      case Editing                         :
        PaintEditing (p,Region,clip,color) ;
      break                                ;
      case FrameOnly                       :
        PaintFrame   (p,Region,clip,color) ;
      break                                ;
    }                                      ;
    """
    ##########################################################################
    self . popPainters            ( p                                        )
    ##########################################################################
    return
  ############################################################################
  def PaintEditing                ( self , p , region , clip , color       ) :
    ##########################################################################
    """
    PaintRegion (p                 ) ;
    PaintBorder (p                 ) ;
    PaintName   (p,ScreenRect,false) ;
    """
    ##########################################################################
    return
  ############################################################################
  def PaintFrame       ( self , p , region , clip , color                  ) :
    ##########################################################################
    self . PaintRegion (        p                                            )
    ##########################################################################
    return
  ############################################################################
  def PaintRegion             ( self , p                                   ) :
    ##########################################################################
    self . Painter . drawRect ( p , "Default" , self . ScreenRect            )
    ##########################################################################
    return
  ############################################################################
  def Print          ( self , p , rect                                     ) :
    ##########################################################################
    self . PaintName (        p , rect , True                                )
    ##########################################################################
    return
  ############################################################################
  def PaintBorder ( self , p ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def PaintName ( self , p , rect , clip ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def setMargins ( self , left , top , right , bottom ) :
    ##########################################################################
    """
    Borders[Left  ] = left   ;
    Borders[Top   ] = top    ;
    Borders[Right ] = right  ;
    Borders[Bottom] = bottom ;
    """
    ##########################################################################
    return
  ############################################################################
  def Menu                    ( self , gview , pos , spos                  ) :
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
"""

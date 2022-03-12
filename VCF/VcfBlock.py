# -*- coding: utf-8 -*-
##############################################################################
## VcfBlock
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
from         . VcfNode                import VcfNode      as VcfNode
##############################################################################
class VcfBlock        ( VcfNode                                            ) :
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
class Q_COMPONENTS_EXPORT VcfBlock : public VcfNode
{
  Q_OBJECT
  public:

    QRectF ChildRect ;
    QRectF NameRect  ;

    enum { Type = UserType + VCF::Block } ;
    virtual int type(void) const { return Type; }

    explicit VcfBlock                 (QObject       * parent       ,
                                       QGraphicsItem * item         ,
                                       Plan          * plan = NULL) ;
    virtual ~VcfBlock                 (void) ;

    virtual QRectF childRect          (void) ;
    virtual QRectF nameRect           (void) ;

    virtual bool AttemptMelt          (VcfLinker * Linker,QPointF base) ;
    virtual bool AllowMelts           (int side) ;

  protected:

    virtual void Configure            (void) ;
    virtual void Hovering             (QPointF pos);
    virtual enum EditWays CastEditing (void) ;

    virtual void NewSize              (QRectF rect) ;
    virtual void FinalSize            (void) ;

  private:

  public slots:

    virtual void Compactified         (void) ;

    virtual bool FocusIn              (void) ;
    virtual bool FocusOut             (void) ;

    virtual void setRange             (QRectF rect) ;
    virtual void EnterEditor          (void) ;
    virtual bool doubleClicked        (QPointF pos) ;

  protected slots:

    virtual void nameFinished         (void) ;

  private slots:

  signals:

    void Update                       (VcfBlock * block,int item) ;

};


N::VcfBlock:: VcfBlock (QObject * parent,QGraphicsItem * item,Plan * p)
            : VcfNode  (          parent,                item,       p)
{
  Configure ( ) ;
}

N::VcfBlock::~VcfBlock(void)
{
}

void N::VcfBlock::Configure(void)
{
}

void N::VcfBlock::Hovering(QPointF pos)
{
  if (!Scaling) return                 ;
  setCornerCursor ( atCorner ( pos ) ) ;
}

enum N::VcfNode::EditWays N::VcfBlock::CastEditing(void)
{
  if (!Editable             ) return EditNothing ;
  if (!Markers.contains(999))                    {
    if (Scaling) return ScaleEditing             ;
    return EditNothing                           ;
  }                                              ;
  return (enum EditWays)Markers[999]             ;
}

QRectF N::VcfBlock::childRect(void)
{
  return toPaper(ChildRect) ;
}

QRectF N::VcfBlock::nameRect(void)
{
  return toPaper(NameRect) ;
}

void N::VcfBlock::NewSize(QRectF rect)
{
  if (IsNull(Options)) return                                       ;
  QRectF R = Options->Standard(rect)                                ;
  ///////////////////////////////////////////////////////////////////
  ChildRect . setLeft   (R.left  ()+Borders [ Left   ]            ) ;
  ChildRect . setTop    (R.top   ()+Borders [ Top    ]            ) ;
  ChildRect . setWidth  (R.width ()-Borders[Left]-Borders[Right ] ) ;
  ChildRect . setHeight (R.height()-Borders[Top ]-Borders[Bottom] ) ;
  NameRect  = ChildRect                                             ;
  ParagraphRect = toPaper (NameRect          )                      ;
  ///////////////////////////////////////////////////////////////////
  QPainterPath path                                                 ;
  path.addRect  ( rect )                                            ;
  Painter.pathes [1] = path                                         ;
  EnablePath  ( 1 , true )                                          ;
  MergePathes ( 0        )                                          ;
}

void N::VcfBlock::FinalSize(void)
{
  QPointF PS = PaperPos               ;
  QPointF PC = PaperRect . topLeft () ;
  QSizeF  RS = PaperRect . size    () ;
  PS += PC                            ;
  QRectF  RR      ( PS , RS  )        ;
  setRange        ( RR       )        ;
  emit Update     ( this , 2 )        ;
}

void N::VcfBlock::setRange(QRectF rect)
{
  QPointF pos = rect . topLeft (              )                                     ;
  QRectF  r ( 0,0,rect.width(),rect.height()  )                                     ;
  ChildRect . setLeft   ( Borders [ Left   ]                                      ) ;
  ChildRect . setTop    ( Borders [ Top    ]                                      ) ;
  ChildRect . setWidth  ( rect.width () - Borders [ Left   ] - Borders [ Right  ] ) ;
  ChildRect . setHeight ( rect.height() - Borders [ Top    ] - Borders [ Bottom ] ) ;
  NameRect  = ChildRect                                                             ;
  ParagraphRect = toPaper ( NameRect          )                                     ;
  VcfNode :: setPos    ( pos                  )                                     ;
  VcfNode :: setRect   ( r                    )                                     ;
}

void N::VcfBlock::EnterEditor(void)
{
  Editing = true                              ;
  QLineEdit * line = NewLineEdit ( 4 )        ;
  line -> setText ( name )                    ;
  if (Painter.fonts.contains(4))              {
    Painter.fonts[4].setDPI( Options -> DPI ) ;
    line -> setFont ( Painter . fonts [ 4 ] ) ;
  }                                           ;
  QRectF NR  = toPaper     ( NameRect  )      ;
  Proxys[4] -> setGeometry ( NR        )      ;
  line      -> setFrame    ( false     )      ;
  connect(line,SIGNAL(editingFinished())      ,
          this,SLOT  (nameFinished   ())    ) ;
  line -> setFocus ( Qt :: TabFocusReason   ) ;
}

void N::VcfBlock::nameFinished (void)
{
  QLineEdit * line = Casting(QLineEdit,Widgets[4]) ;
  if (NotNull(line)) name = line->text()           ;
  DeleteGadgets ( )                                ;
  Editing = false                                  ;
  switch (Mode)                                    {
    case 0                                         :
      emit Update ( this , 0 )                     ;
    break                                          ;
    default                                        :
      emit Update ( this , 1 )                     ;
    break                                          ;
  }                                                ;
}

bool N::VcfBlock::doubleClicked(QPointF pos)
{
  if (!Editable) return false       ;
  QRectF NR  = toPaper ( NameRect ) ;
  if (NR.contains(pos))             {
    EnterEditor ( )                 ;
    return true                     ;
  }                                 ;
  return true                       ;
}

void N::VcfBlock::Compactified(void)
{
  if (IsNull(Options)           ) return                             ;
  if (!Painter.fonts.contains(4)) return                             ;
  Painter.fonts[4].setDPI( Options -> DPI )                          ;
  ////////////////////////////////////////////////////////////////////
  QPointF       PP  = QGraphicsItem::pos()                           ;
  QPointF       PC  = PaperRect . center ()                          ;
  QFontMetricsF FMF = Painter.FontMetrics(4)                         ;
  QRectF        RT  = FMF.boundingRect(name)                         ;
  ////////////////////////////////////////////////////////////////////
  PP = Options->Standard(PP)                                         ;
  RT = Options->Standard(RT)                                         ;
  QPointF W(RT . width  () + Borders [ Left ] + Borders [ Right  ]   ,
            RT . height () + Borders [ Top  ] + Borders [ Bottom ] ) ;
  QPointF H = W                                                      ;
  H /= 2                                                             ;
  PC -= H                                                            ;
  PP += PC                                                           ;
  ////////////////////////////////////////////////////////////////////
  QRectF RC ( PP.x() , PP.y() , W.x() , W.y() )                      ;
  setRange  ( RC                              )                      ;
}

bool N::VcfBlock::FocusIn(void)
{
  if (Painter.pens   .contains(21))                 {
    Painter . pens    [ 1] = Painter . pens    [21] ;
    Painter . pens    [ 3] = Painter . pens    [23] ;
  }                                                 ;
  if (Painter.brushes.contains(21))                 {
    Painter . brushes [ 1] = Painter . brushes [21] ;
    Painter . brushes [ 3] = Painter . brushes [23] ;
  }                                                 ;
  update ( )                                        ;
  return true                                       ;
}

bool N::VcfBlock::FocusOut(void)
{
  if (Painter.pens   .contains(11))                 {
    Painter . pens    [21] = Painter . pens    [ 1] ;
    Painter . pens    [23] = Painter . pens    [ 3] ;
    Painter . pens    [ 1] = Painter . pens    [11] ;
    Painter . pens    [ 3] = Painter . pens    [11] ;
  }                                                 ;
  if (Painter.brushes.contains(11))                 {
    Painter . brushes [21] = Painter . brushes [ 1] ;
    Painter . brushes [23] = Painter . brushes [ 3] ;
    Painter . brushes [ 1] = Painter . brushes [11] ;
    Painter . brushes [ 3] = Painter . brushes [11] ;
  }                                                 ;
  update ( )                                        ;
  return false                                      ;
}

bool N::VcfBlock::AttemptMelt(VcfLinker * Linker,QPointF base)
{
  bool melt = false          ;
  if (Linker->isFirst(this)) {
    Linker->Melts[0] = base  ;
    melt = true              ;
  }                          ;
  if (Linker->isEnd  (this)) {
    Linker->Melts[1] = base  ;
    melt = true              ;
  }                          ;
  return melt                ;
}

bool N::VcfBlock::AllowMelts(int side)
{
  return true ;
}
"""

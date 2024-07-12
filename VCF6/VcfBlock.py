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
import PySide6
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
from           . VcfNode   import VcfNode as VcfNode
##############################################################################
class VcfBlock                 ( VcfNode                                   ) :
  ############################################################################
  def __init__                 ( self                                      , \
                                 parent = None                             , \
                                 item   = None                             , \
                                 plan   = None                             ) :
    ##########################################################################
    super ( ) . __init__       ( parent , item , plan                        )
    self . setVcfBlockDefaults (                                             )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfBlockDefaults     ( self                                       ) :
    ##########################################################################
    self . ChildRect = QRectF (                                              )
    self . NameRect  = QRectF (                                              )
    ##########################################################################
    return
  ############################################################################
  def Hovering             ( self , pos                                    ) :
    ##########################################################################
    if                     ( not self . Scaling                            ) :
      return
    ##########################################################################
    self . setCornerCursor ( self . atCorner ( pos )                         )
    ##########################################################################
    return
  ############################################################################
  def CastEditing ( self ) :
    ##########################################################################
    """
    if (!Editable             ) return EditNothing ;
    if (!Markers.contains(999))                    {
      if (Scaling) return ScaleEditing             ;
      return EditNothing                           ;
    }                                              ;
    return (enum EditWays)Markers[999]             ;
    """
    ##########################################################################
    return
  ############################################################################
  def childRect               ( self                                       ) :
    return self . rectToPaper ( self . ChildRect                             )
  ############################################################################
  def nameRect                ( self                                       ) :
    return self . rectToPaper ( self . NameRect                              )
  ############################################################################
  def NewSize ( self , rect ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def FinalSize                       ( self                               ) :
    ##########################################################################
    PS   = self . PaperPos
    PC   = self . PaperRect . topLeft (                                      )
    RS   = self . PaperRect . size    (                                      )
    PS   = PS   + PC
    RR   = QRectF                     ( PS , RS                              )
    self . setRange                   ( RR                                   )
    """
    emit Update     ( this , 2 )        ;
    """
    ##########################################################################
    return
  ############################################################################
  def setRange ( self , rect ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def EnterEditor ( self ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def nameFinished ( self ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def doubleClicked      ( self , pos                                      ) :
    ##########################################################################
    if                   ( not self . Editable                             ) :
      return False
    ##########################################################################
    NR = self . nameRect (                                                   )
    ##########################################################################
    if                   ( NR . contains ( pos )                           ) :
      self . EnterEditor (                                                   )
      return True
    ##########################################################################
    return True
  ############################################################################
  def Compactified ( self ) :
    ##########################################################################
    """
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
    """
    ##########################################################################
    return
  ############################################################################
  def FocusIn ( self ) :
    ##########################################################################
    if            ( 21 in self . Painter . pens                            ) :
      ########################################################################
      self . Painter . pens    [  1 ] = self . Painter . pens    [ 21 ]
      self . Painter . pens    [  3 ] = self . Painter . pens    [ 23 ]
    ##########################################################################
    if            ( 21 in self . Painter . brushes                         ) :
      ########################################################################
      self . Painter . brushes [  1 ] = self . Painter . brushes [ 21 ]
      self . Painter . brushes [  3 ] = self . Painter . brushes [ 23 ]
    ##########################################################################
    self . update (                                                          )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut    ( self                                                   ) :
    ##########################################################################
    if            ( 11 in self . Painter . pens                            ) :
      ########################################################################
      self . Painter . pens    [ 21 ] = self . Painter . pens    [  1 ]
      self . Painter . pens    [ 23 ] = self . Painter . pens    [  3 ]
      self . Painter . pens    [  1 ] = self . Painter . pens    [ 11 ]
      self . Painter . pens    [  3 ] = self . Painter . pens    [ 11 ]
    ##########################################################################
    if            ( 11 in self . Painter . brushes                         ) :
      ########################################################################
      self . Painter . brushes [ 21 ] = self . Painter . brushes [  1 ]
      self . Painter . brushes [ 23 ] = self . Painter . brushes [  3 ]
      self . Painter . brushes [  1 ] = self . Painter . brushes [ 11 ]
      self . Painter . brushes [  3 ] = self . Painter . brushes [ 11 ]
    ##########################################################################
    self . update (                                                          )
    ##########################################################################
    return False
  ############################################################################
  def AttemptMelt ( self , Linker , base                                   ) :
    ##########################################################################
    melt     = False
    ##########################################################################
    if            ( Linker . isFirst ( self )                              ) :
      ########################################################################
      Linker . Melts [ 0 ] = base
      melt   = True
    ##########################################################################
    if            ( Linker . isEnd   ( self )                              ) :
      ########################################################################
      Linker . Melts [ 1 ] = base
      melt   = True
    ##########################################################################
    return melt
  ############################################################################
  def AllowMelts ( self , side                                             ) :
    return True
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfBlock : public VcfNode
{
  Q_OBJECT
  public:
  signals:
    void Update                       (VcfBlock * block,int item) ;
} ;
"""

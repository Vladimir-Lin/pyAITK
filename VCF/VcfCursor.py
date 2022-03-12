# -*- coding: utf-8 -*-
##############################################################################
## VcfCursor
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
class VcfCursor       ( VcfRectangle                                       ) :
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
class Q_COMPONENTS_EXPORT VcfCursor : public VcfRectangle
{
  Q_OBJECT
  public:

    enum { Type = UserType + VCF::Cursor } ;
    virtual int type(void) const { return Type ; }

    explicit VcfCursor       (QObject       * parent        ,
                              QGraphicsItem * item          ,
                              Plan          * plan = NULL );
    virtual ~VcfCursor       (void);

    virtual void paint       (QPainter                       * painter      ,
                              const QStyleOptionGraphicsItem * option       ,
                              QWidget                        * widget = 0 ) ;

  protected:

    QTimer * Timer   ;
    bool     Showing ;

  private:

  public slots:

    virtual void Paint       (QPainter * painter,QRectF Region,bool clip,bool color) ;
    void         Start       (void);
    void         setInterval (int milliseconds) ;

  protected slots:

    void         Twinkling   (void);

  private slots:

  signals:

};

N::VcfCursor:: VcfCursor    ( QObject * parent , QGraphicsItem * item , Plan * p )
             : VcfRectangle (           parent ,                 item ,        p )
             , Timer        ( new QTimer ( this )                                )
             , Showing      ( false                                              )
{
  Printable = false                              ;
  Painter . addMap   ( "Default" , 0 )           ;
  Painter . addPen   ( 0 , QColor(  0,  0,255) ) ;
  Painter . addBrush ( 0 , QColor(224,224,224) ) ;
  setFlag (ItemIsSelectable,false)               ;
  setFlag (ItemIsFocusable ,false)               ;
  nConnect ( Timer , SIGNAL ( timeout   ( ) )    ,
             this  , SLOT   ( Twinkling ( ) ) )  ;
  Timer -> setInterval ( 1000 )                  ;
}

N::VcfCursor::~VcfCursor(void)
{
  Timer -> stop ( ) ;
}

void N::VcfCursor::setInterval(int milliseconds)
{
  Timer -> setInterval ( milliseconds ) ;
}

void N::VcfCursor::Start(void)
{
  Timer -> start ( ) ;
}

void N::VcfCursor::Twinkling(void)
{
  update();
}

void N::VcfCursor::paint(QPainter * painter,const QStyleOptionGraphicsItem * option,QWidget * widget)
{
  Paint(painter,ScreenRect,false,true) ;
}

void N::VcfCursor::Paint(QPainter * p,QRectF Region,bool clip,bool color)
{
  pushPainters (p)                  ;
  if (Showing)                      {
    Painter.setPainter(p,"Default") ;
    p -> drawRect (ScreenRect     ) ;
    Showing = false                 ;
  } else                            {
    Showing = true                  ;
  }                                 ;
  popPainters  (p)                  ;
}
"""

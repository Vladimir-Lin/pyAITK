# -*- coding: utf-8 -*-
##############################################################################
## VcfLines
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
from         . VcfPath                import VcfPath      as VcfPath
##############################################################################
class VcfLines        ( VcfPath                                            ) :
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
class Q_COMPONENTS_EXPORT VcfLines : public VcfPath
{
  Q_OBJECT
  public:

    Contour   contour ;
    QPolygonF lines   ;

    enum { Type = UserType + VCF::Lines };
    virtual int type(void) const { return Type; }

    explicit VcfLines            (QObject       * parent       ,
                                  QGraphicsItem * item         ,
                                  Plan          * plan = NULL) ;
    virtual ~VcfLines            (void);

  protected:

  private:

  public slots:

    virtual void Paint          (QPainter * painter,QRectF Region,bool clip,bool color) ;

    virtual void Prepare        (bool line = false,bool dot = false) ;
    virtual void ShowLines      (bool line = false) ;

  protected slots:

  private slots:

  signals:

};

N::VcfLines:: VcfLines (QObject * parent,QGraphicsItem * item,Plan * p)
            : VcfPath  (          parent,                item,       p)
{
  setBrushColor ( 1 , QColor ( 224 , 224 , 224 ) ) ;
  setBrushColor ( 2 , QColor ( 255 , 144 , 144 ) ) ;
}

N::VcfLines::~VcfLines (void)
{
}

void N::VcfLines::Paint(QPainter * p,QRectF Region,bool,bool)
{
  PaintPath  ( p , 1        ) ;
  PaintLines ( p , 3 ,lines ) ;
  PaintPath  ( p , 2        ) ;
}

void N::VcfLines::Prepare(bool line,bool dot)
{
  setLines     ( 1 , contour ) ;
  EnablePath   ( 1 , true    ) ;
  ShowLines    ( line        ) ;
  if (dot )                    {
    setPoints  ( 2 , contour ) ;
    EnablePath ( 2 , true    ) ;
  } else                       {
    EnablePath ( 2 , false   ) ;
  }                            ;
  MergePathes  ( 0           ) ;
}

void N::VcfLines::ShowLines(bool line)
{
  lines . clear              (                          ) ;
  if (line) lines = Polyline ( contour , contour.closed ) ;
  update                     (                          ) ;
}
"""

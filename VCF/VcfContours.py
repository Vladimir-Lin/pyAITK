# -*- coding: utf-8 -*-
##############################################################################
## VcfContours
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
class VcfContours     ( VcfPath                                            ) :
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
class Q_COMPONENTS_EXPORT VcfContours : public VcfPath
{
  Q_OBJECT
  public:

    Contour   contour ;
    QPolygonF lines   ;

    enum { Type = UserType + VCF::Contours };
    virtual int type(void) const { return Type; }

    explicit VcfContours          (QObject       * parent       ,
                                   QGraphicsItem * item         ,
                                   Plan          * plan = NULL) ;
    virtual ~VcfContours          (void);

  protected:

    virtual void contextMenuEvent (QGraphicsSceneContextMenuEvent * event);

    virtual bool dropColor        (QWidget * source,QPointF pos,const QColor & color) ;
    virtual bool dropTags         (QWidget * source,QPointF pos,const UUIDs & Uuids) ;
    virtual bool dropPen          (QWidget * source,QPointF pos,const SUID pen) ;
    virtual bool dropBrush        (QWidget * source,QPointF pos,const SUID brush) ;

  private:

  public slots:

    virtual void Paint            (QPainter * painter,QRectF Region,bool clip,bool color) ;

    virtual void Prepare          (bool line = false,bool dot = false) ;
    virtual void ShowLines        (bool line = false) ;

  protected slots:

  private slots:

  signals:

    void Menu                     (VcfContours * contour,QPointF pos);

};

N::VcfContours:: VcfContours (QObject * parent,QGraphicsItem * item,Plan * p)
               : VcfPath     (          parent,                item,       p)
{
  setDropFlag(DropText    ,false) ;
  setDropFlag(DropUrls    ,false) ;
  setDropFlag(DropImage   ,false) ;
  setDropFlag(DropHtml    ,false) ;
  setDropFlag(DropColor   ,true ) ;
  setDropFlag(DropTag     ,true ) ;
  setDropFlag(DropPicture ,false) ;
  setDropFlag(DropPeople  ,false) ;
  setDropFlag(DropVideo   ,false) ;
  setDropFlag(DropAlbum   ,false) ;
  setDropFlag(DropGender  ,false) ;
  setDropFlag(DropDivision,false) ;
  setDropFlag(DropURIs    ,false) ;
  setDropFlag(DropBookmark,false) ;
  setDropFlag(DropFont    ,false) ;
  setDropFlag(DropPen     ,true ) ;
  setDropFlag(DropBrush   ,true ) ;
  setDropFlag(DropGradient,false) ;
}

N::VcfContours::~VcfContours (void)
{
}

void N::VcfContours::contextMenuEvent(QGraphicsSceneContextMenuEvent * event)
{
  emit Menu(this,event->pos());
  event->accept();
}

void N::VcfContours::Paint(QPainter * p,QRectF Region,bool,bool)
{ Q_UNUSED   ( Region        ) ;
  PaintPath  ( p , 1         ) ;
  PaintLines ( p , 3 , lines ) ;
  PaintPath  ( p , 2         ) ;
}

void N::VcfContours::Prepare(bool line,bool dot)
{
  setContour   ( 1 , contour ) ;
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

void N::VcfContours::ShowLines(bool line)
{
  lines . clear              (                          ) ;
  if (line) lines = Polyline ( contour , contour.closed ) ;
  update                     (                          ) ;
}

bool N::VcfContours::dropColor(QWidget * source,QPointF pos,const QColor & color)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( pos    ) ;
  Q_UNUSED ( color  ) ;
  return true         ;
}

bool N::VcfContours::dropTags(QWidget * source,QPointF pos,const UUIDs & Uuids)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( pos    ) ;
  Q_UNUSED ( Uuids  ) ;
  return true         ;
}

bool N::VcfContours::dropPen(QWidget * source,QPointF pos,const SUID pen)
{ Q_UNUSED ( source )                                ;
  Q_UNUSED ( pos    )                                ;
  GraphicsManager GM (plan )                         ;
  EnterSQL ( SC , plan->sql )                        ;
    Painter . pens    [1] = GM . GetPen   (SC,pen  ) ;
  LeaveSQL ( SC , plan->sql )                        ;
  update   (                )                        ;
  return true                                        ;
}

bool N::VcfContours::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{ Q_UNUSED ( source )                                ;
  Q_UNUSED ( pos    )                                ;
  GraphicsManager GM (plan )                         ;
  EnterSQL ( SC , plan->sql )                        ;
    Painter . brushes [1] = GM . GetBrush (SC,brush) ;
  LeaveSQL ( SC , plan->sql )                        ;
  update   (                )                        ;
  return true                                        ;
}
"""

# -*- coding: utf-8 -*-
##############################################################################
## LineEdit
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
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QCompleter
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class LineEdit            ( QLineEdit , VirtualGui                         ) :
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
    ##########################################################################
    super ( QLineEdit  , self ) . __init__   ( parent                        )
    super ( VirtualGui , self ) . Initialize ( self                          )
    ##########################################################################
    self . setAttribute   ( Qt . WA_InputMethodEnabled                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(list)
  def updateCompleter       ( self , strings                               ) :
    ##########################################################################
    oc   = self . completer (                                                )
    lc   = QCompleter       ( strings , self                                 )
    self . setCompleter     ( lc                                             )
    ##########################################################################
    return oc
##############################################################################



"""


class Q_COMPONENTS_EXPORT LineEdit : public QLineEdit
                                   , public VirtualGui
                                   , public Thread
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    explicit     LineEdit        (StandardConstructor) ;
    virtual ~    LineEdit        (void               ) ;

  protected:

    virtual void paintEvent      (QPaintEvent     * event) ;

    virtual void focusInEvent    (QFocusEvent     * event) ;
    virtual void focusOutEvent   (QFocusEvent     * event) ;

    virtual void resizeEvent     (QResizeEvent    * event) ;

    virtual void dragEnterEvent  (QDragEnterEvent * event) ;
    virtual void dragLeaveEvent  (QDragLeaveEvent * event) ;
    virtual void dragMoveEvent   (QDragMoveEvent  * event) ;
    virtual void dropEvent       (QDropEvent      * event) ;

    virtual bool acceptDrop      (nDeclWidget,const QMimeData * mime);
    virtual bool dropNew         (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropMoving      (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropAppend      (nDeclWidget,const QMimeData * mime,QPoint pos);

    virtual bool dropFont        (nDeclWidget,QPointF pos,const SUID font ) ;
    virtual bool dropPen         (nDeclWidget,QPointF pos,const SUID pen  ) ;
    virtual bool dropBrush       (nDeclWidget,QPointF pos,const SUID brush) ;

    virtual void assignFont      (Font  & font ) ;
    virtual void assignPen       (Pen   & pen  ) ;
    virtual void assignBrush     (Brush & brush) ;

  private:

  public slots:

    QCompleter * updateCompleter (QStringList & list) ;

  protected slots:

  private slots:

  signals:

};




#include <qtcomponents.h>

N::LineEdit:: LineEdit   ( QWidget * parent , Plan * p     )
            : QLineEdit  (           parent                )
            , VirtualGui (           this   ,        p     )
            , Thread     (           0      ,        false )
{
  WidgetClass                                   ;
  setAttribute ( Qt::WA_InputMethodEnabled )    ;
  setDropFlag  ( DropFont  , true          )    ;
  setDropFlag  ( DropPen   , true          )    ;
  setDropFlag  ( DropBrush , true          )    ;
  ///////////////////////////////////////////////
  if ( NotNull ( plan ) )                       {
    Data . Controller = & ( plan->canContinue ) ;
  }                                             ;
}

N::LineEdit::~LineEdit(void)
{
}

QCompleter * N::LineEdit::updateCompleter(QStringList & list)
{
  QCompleter * oc = completer      (             ) ;
  QCompleter * lc = new QCompleter ( list , this ) ;
  setCompleter                     ( lc          ) ;
  return oc                                        ;
}

void N::LineEdit::paintEvent(QPaintEvent * event)
{
  nIsolatePainter(QLineEdit) ;
}

void N::LineEdit::focusInEvent(QFocusEvent * event)
{
  if (!focusIn (event)) QLineEdit::focusInEvent (event) ;
}

void N::LineEdit::focusOutEvent(QFocusEvent * event)
{
  if (!focusOut(event)) QLineEdit::focusOutEvent(event) ;
}

void N::LineEdit::resizeEvent(QResizeEvent * event)
{
  QLineEdit :: resizeEvent ( event ) ;
}

void N::LineEdit::dragEnterEvent(QDragEnterEvent * event)
{
  if (dragEnter(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QLineEdit::dragEnterEvent(event)       ;
    else event->ignore()                                     ;
  }                                                          ;
}

void N::LineEdit::dragLeaveEvent(QDragLeaveEvent * event)
{
  if (removeDrop()) event->accept() ; else             {
    if (PassDragDrop) QLineEdit::dragLeaveEvent(event) ;
    else event->ignore()                               ;
  }                                                    ;
}

void N::LineEdit::dragMoveEvent(QDragMoveEvent * event)
{
  if (dragMove(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QLineEdit::dragMoveEvent(event)       ;
    else event->ignore()                                    ;
  }                                                         ;
}

void N::LineEdit::dropEvent(QDropEvent * event)
{
  if (drop(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QLineEdit::dropEvent(event)       ;
    else event->ignore()                                ;
  }                                                     ;
}

bool N::LineEdit::acceptDrop(QWidget * source,const QMimeData * mime)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  return false        ;
}

bool N::LineEdit::dropNew(QWidget * source,const QMimeData * mime,QPoint pos)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::LineEdit::dropMoving(QWidget * source,const QMimeData * mime,QPoint pos)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::LineEdit::dropAppend(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return dropItems ( source , mime , pos ) ;
}

bool N::LineEdit::dropFont(QWidget * source,QPointF pos,const SUID font)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Font            f                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    f = GM.GetFont   ( SC , font            ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignFont         ( f                    ) ;
  return true                                 ;
}

bool N::LineEdit::dropPen(QWidget * source,QPointF pos,const SUID pen)
{ Q_UNUSED            ( source               ) ;
  Q_UNUSED            ( pos                  ) ;
  nKickOut            ( IsNull(plan) , false ) ;
  Pen             p                            ;
  GraphicsManager GM  ( plan                 ) ;
  EnterSQL            ( SC , plan->sql       ) ;
    p = GM.GetPen     ( SC , pen             ) ;
  LeaveSQL            ( SC , plan->sql       ) ;
  assignPen           ( p                    ) ;
  return true                                  ;
}

bool N::LineEdit::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{ Q_UNUSED            ( source               ) ;
  Q_UNUSED            ( pos                  ) ;
  nKickOut            ( IsNull(plan) , false ) ;
  Brush           b                            ;
  GraphicsManager GM  ( plan                 ) ;
  EnterSQL            ( SC , plan->sql       ) ;
    b = GM.GetBrush   ( SC , brush           ) ;
  LeaveSQL            ( SC , plan->sql       ) ;
  assignBrush         ( b                    ) ;
  return true                                  ;
}

void N::LineEdit::assignFont(Font & f)
{
  QLineEdit::setFont ( f ) ;
}

void N::LineEdit::assignPen(Pen & p)
{ Q_UNUSED ( p ) ;
}

void N::LineEdit::assignBrush(Brush & brush)
{
  QBrush   B   = brush                            ;
  QPalette P   = palette (                      ) ;
  P . setBrush           ( QPalette::Base , B   ) ;
  setPalette             ( P                    ) ;
}



"""




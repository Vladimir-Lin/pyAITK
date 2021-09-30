# -*- coding: utf-8 -*-
##############################################################################
## Widget
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
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
##############################################################################
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class Widget            ( QWidget , VirtualGui                             ) :
  ############################################################################
  def __init__          ( self , parent = None , plan = None               ) :
    ##########################################################################
    super ( QWidget     , self ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    ##########################################################################
    self . setAttribute ( Qt . WA_InputMethodEnabled                         )
    ##########################################################################
    return
##############################################################################



"""



class Q_COMPONENTS_EXPORT Widget : public QWidget
                                 , public VirtualGui
                                 , public Thread
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    explicit Widget (StandardConstructor) ;
    virtual ~Widget (void               ) ;

  protected:

    virtual bool event         (QEvent * event) ;

  private:

  public slots:

  protected slots:

     virtual void DropCommands (void) ;

  private slots:

  signals:

};



#include <qtcomponents.h>

N::Widget :: Widget     (QWidget * parent,Plan * p     )
           : QWidget    (          parent              )
           , VirtualGui (          this  ,       p     )
           , Thread     (          0     ,       false )
{
  WidgetClass                                   ;
  addIntoWidget ( parent , this             )   ;
  setAttribute  ( Qt::WA_InputMethodEnabled )   ;
  addConnector  ( "Commando"                    ,
                  Commando                      ,
                  SIGNAL ( timeout      ( ) )   ,
                  this                          ,
                  SLOT   ( DropCommands ( ) ) ) ;
  onlyConnector ( "Commando"                  ) ;
  ///////////////////////////////////////////////
  if ( NotNull ( plan ) )                       {
    Data . Controller = & ( plan->canContinue ) ;
  }                                             ;
}

N::Widget ::~Widget(void)
{
}

void N::Widget::DropCommands(void)
{
  LaunchCommands ( ) ;
}

bool N::Widget::event(QEvent * event)
{
  if (permitGesture() && gestureEvent(event)) return true ;
  return QWidget::event(event)                            ;
}


"""


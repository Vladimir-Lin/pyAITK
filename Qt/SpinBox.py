# -*- coding: utf-8 -*-
##############################################################################
## SpinBox
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class SpinBox  ( QSpinBox , VirtualGui                                     ) :
  ############################################################################
  def __init__ ( self , parent = None                                      ) :
    ##########################################################################
    super ( QSpinBox   , self ) . __init__   ( parent                        )
    super ( VirtualGui , self ) . Initialize ( self                          )
    ##########################################################################
    return
##############################################################################





"""




class Q_COMPONENTS_EXPORT SpinBox : public QSpinBox
                                  , public VirtualGui
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    int * External ;

    explicit SpinBox           (StandardConstructor) ;
    virtual ~SpinBox           (void               ) ;

  protected:

  private:

  public slots:

  protected slots:

     virtual void DropCommands (void) ;
     virtual void assignValue  (int value) ;

  private slots:

  signals:

};







#include <qtcomponents.h>

N::SpinBox :: SpinBox    (QWidget * parent,Plan * p)
            : QSpinBox   (          parent         )
            , VirtualGui (          this  ,       p)
            , External   (NULL                     )
{
  setAttribute  ( Qt::WA_InputMethodEnabled               ) ;
  addConnector  ( "Value"                                   ,
                  this    , SIGNAL ( valueChanged (int) )   ,
                  this    , SLOT   ( assignValue  (int) ) ) ;
  addConnector  ( "Commando"                                ,
                  Commando                                  ,
                  SIGNAL ( timeout      ( ) )               ,
                  this                                      ,
                  SLOT   ( DropCommands ( ) )             ) ;
  onlyConnector ( "Value"                                 ) ;
  onlyConnector ( "Commando"                              ) ;
}

N::SpinBox ::~SpinBox(void)
{
}

void N::SpinBox::DropCommands(void)
{
  LaunchCommands ( ) ;
}

void N::SpinBox::assignValue(int value)
{
  nDropOut ( IsNull(External) ) ;
  (*External) = value           ;
}




"""










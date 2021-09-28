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
from   PyQt5 . QtWidgets              import QDialog
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class Dialog   ( QDialog , VirtualGui                                      ) :
  ############################################################################
  def __init__ ( self , parent = None                                      ) :
    ##########################################################################
    super ( QDialog     , self ) . __init__   ( parent                       )
    super ( VirtualGui  , self ) . Initialize ( self                         )
    ##########################################################################
    return
##############################################################################


"""


class Q_COMPONENTS_EXPORT Dialog : public QDialog
                                 , public VirtualGui
                                 , public Thread
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    explicit Dialog (StandardConstructor) ;
    virtual ~Dialog (void               ) ;

  protected:

  private:

  public slots:

  protected slots:

  private slots:

  signals:

};




#include <qtcomponents.h>

N::Dialog :: Dialog     (QWidget * parent,Plan * p     )
           : QDialog    (          parent              )
           , VirtualGui (          this  ,       p     )
           , Thread     (          0     ,       false )
{
  WidgetClass                                   ;
  setAttribute ( Qt::WA_InputMethodEnabled    ) ;
  ///////////////////////////////////////////////
  if ( NotNull ( plan ) )                       {
    Data . Controller = & ( plan->canContinue ) ;
  }                                             ;
}

N::Dialog ::~Dialog(void)
{
}




"""




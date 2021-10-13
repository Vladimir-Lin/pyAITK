# -*- coding: utf-8 -*-
##############################################################################
## MdiSubWindow
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
from   PyQt5 . QtCore                 import QRect
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMdiSubWindow
##############################################################################
class MdiSubWindow              ( QMdiSubWindow                            ) :
  ############################################################################
  def __init__                  ( self , parent = None                     ) :
    ##########################################################################
    super ( ) . __init__        ( parent                                     )
    self      .  setAttribute   ( Qt . WA_InputMethodEnabled                 )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                ( self , event                             ) :
    ##########################################################################
    """
    if ( NULL != abstract )                                         {
      if ( ! abstract -> canStop ( ) )                              {
        e -> ignore ( )                                             ;
        return                                                      ;
      }                                                             ;
    } else                                                          {
      QWidget * w = widget ( )                                      ;
      if ( NULL != w )                                              {
        QVariant v = w -> property ( "AbstractGui" )                ;
        if ( v . isValid ( ) && v . toBool ( ) )                    {
          QVariant z = w -> property ( "CanStop" )                  ;
          if ( z . isValid ( ) && ( ! getAbstractStopable ( z ) ) ) {
            e -> ignore ( )                                         ;
            return                                                  ;
          }                                                         ;
        }                                                           ;
      }                                                             ;
    }                                                               ;
    """
    ##########################################################################
    super ( ) . closeEvent      (        event                               )
    ##########################################################################
    return
##############################################################################

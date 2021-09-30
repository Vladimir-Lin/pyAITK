# -*- coding: utf-8 -*-
##############################################################################
## InputTreeWidget
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
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
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
from         . Widget                 import Widget     as Widget
from         . TreeWidget             import TreeWidget as TreeWidget
##############################################################################
class InputTreeWidget ( Widget                                             ) :
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super ( Widget     , self ) . __init__   ( parent , plan                 )
    ##########################################################################
    return
  ############################################################################
  def Prepare                   ( self                                     ) :
    ##########################################################################
    self . EditorHeight = 28
    self . combo = QComboBox    ( self                                       )
    self . line  = QLineEdit    ( self                                       )
    self . tree  = TreeWidget   ( self                                       )
    ##########################################################################
    self . combo . setLineEdit  ( self . line                                )
    ##########################################################################
    self . combo . move         ( 0 , 0                                      )
    self . tree  . move         ( 0 , self . EditorHeight                    )
    ##########################################################################
    self . Prepared    = True
    ##########################################################################
    return
  ############################################################################
  def Configure                 ( self                                     ) :
    raise NotImplementedError   (                                            )
  ############################################################################
  def resizeEvent               ( self , event                             ) :
    ##########################################################################
    QWidget . resizeEvent       ( self , event                               )
    ##########################################################################
    if                          ( not self . Prepared                      ) :
      return
    ##########################################################################
    w       = self  . width     (                                            )
    h       = self  . height    (                                            )
    ##########################################################################
    self    . combo . resize    ( w ,     self . EditorHeight                )
    self    . tree  . resize    ( w , h - self . EditorHeight                )
    ##########################################################################
    return
##############################################################################

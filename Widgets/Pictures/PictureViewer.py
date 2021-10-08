# -*- coding: utf-8 -*-
##############################################################################
## PeopleView
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
from   PyQt5 . QtCore                 import QSize
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
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
from   PyQt5 . QtWidgets              import QScrollArea
from   PyQt5 . QtWidgets              import QLabel
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . VirtualGui        import VirtualGui  as VirtualGui
##############################################################################
class PictureViewer               ( QScrollArea , VirtualGui                               ) :
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super (                    ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    self . Image = None
    self . Ratio = QSize          ( 100 , 100                                )
    ##########################################################################
    return
  ############################################################################
  def AssignPixmap    ( self                                               ) :
    ##########################################################################
    if                ( self . Image == None                               ) :
      return
    ##########################################################################
    PIX   = QPixmap . fromImage ( self . Image )
    ##########################################################################
    if ( ( self . Ratio . width ( ) != 100 ) or ( self . Ratio . width ( ) != 100 ) ) :
      ws    = self . Image . size ( )
      W     = int ( ws . width  ( ) * self . Ratio . width  ( ) / 100 )
      H     = int ( ws . height ( ) * self . Ratio . height ( ) / 100 )
      PIX   = PIX . scaled ( QSize ( W , H ) )
    ##########################################################################
    label = QLabel    (                                                      )
    label . setPixmap ( PIX                                                  )
    self  . setWidget ( label                                                )
    ##########################################################################
    return
  ############################################################################
  def setImage          ( self , image                                     ) :
    ##########################################################################
    self . Image = image
    self . AssignPixmap (                                                    )
    ##########################################################################
    return
##############################################################################

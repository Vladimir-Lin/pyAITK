# -*- coding: utf-8 -*-
##############################################################################
## SplitterHandle
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
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QSplitterHandle
##############################################################################
from         . MenuManager            import MenuManager as MenuManager
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class SplitterHandle                       ( QSplitterHandle , VirtualGui  ) :
  ############################################################################
  assignOrientation = pyqtSignal           ( int                             )
  ############################################################################
  def __init__                             ( self                          , \
                                             orientation                   , \
                                             parent = None                 , \
                                             plan   = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( orientation , parent            )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . Menus =                         {                                 }
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ORI    = self . orientation       (                                      )
    ##########################################################################
    if                                ( ORI == Qt . Horizontal             ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Vertical"                           )
      mm   . addAction                ( 301 , msg                            )
    elif                              ( ORI  == Qt . Vertical              ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Horizontal"                         )
      mm   . addAction                ( 302 , msg                            )
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    if                                ( at == 301                          ) :
      self . assignOrientation . emit ( Qt . Vertical                        )
      return True
    ##########################################################################
    if                                ( at == 302                          ) :
      self . assignOrientation . emit ( Qt . Horizontal                      )
      return True
    ##########################################################################
    return True
##############################################################################

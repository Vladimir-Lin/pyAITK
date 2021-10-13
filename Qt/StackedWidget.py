# -*- coding: utf-8 -*-
##############################################################################
## StackedWidget
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
from   PyQt5 . QtWidgets              import QStackedWidget
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class StackedWidget             ( QStackedWidget , VirtualGui              ) :
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( QStackedWidget , self ) . __init__ ( parent                      )
    super ( VirtualGui     , self ) . __init__ (                             )
    self . Initialize                          ( self                        )
    self . setPlanFunction                     ( plan                        )
    self . setAttribute         ( Qt . WA_InputMethodEnabled                 )
    ##########################################################################
    self . menu  = None
    self . group = None
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def MenuAboutToShow           ( self                                     ) :
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     ( QAction                                    )
  def WindowActionId            ( self , action                            ) :
    ##########################################################################
    Ids  = action . data        (                                            )
    Id   = int                  ( Ids                                        )
    ##########################################################################
    w    = self . widget        ( Id                                         )
    if                          ( w == None                                ) :
      return
    ##########################################################################
    self . setCurrentIndex      ( Id                                         )
    ##########################################################################
    msg  = w    . windowTitle   (                                            )
    self . Go                   ( self . Talk                              , \
                                  ( msg , self . getLocality ( ) , )         )
    ##########################################################################
    return
  ############################################################################
  def PrepareMenu               ( self , menu                              ) :
    ##########################################################################
    self . menu  = menu
    self . group = QActionGroup ( menu                                       )
    ##########################################################################
    self . menu  . aboutToShow . connect ( self . MenuAboutToShow            )
    self . group . triggered   . connect ( self . WindowActionId             )
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  def AttachMenu                  ( self , menu , group                    ) :
    ##########################################################################
    menu    . clear               (                                          )
    ##########################################################################
    CI      = self . currentIndex (                                          )
    ##########################################################################
    for i in range                ( 0 , self . count ( )                   ) :
      ########################################################################
      w     = self . widget       ( i                                        )
      a     = menu . addAction    ( w . windowTitle  ( )                     )
      a     . setData             ( i                                        )
      a     . setCheckable        ( True                                     )
      ########################################################################
      if                          ( CI == i                                ) :
        a   . setChecked          ( True                                     )
      ########################################################################
      group . addAction           ( a                                        )
    ##########################################################################
    return
##############################################################################

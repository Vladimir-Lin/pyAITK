# -*- coding: utf-8 -*-
##############################################################################
## System Tray Icon GUI
##############################################################################
import os
import sys
import time
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
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
from   PyQt5 . QtWidgets              import QSystemTrayIcon
##############################################################################
from         . VirtualGui             import VirtualGui  as VirtualGui
from         . MenuManager            import MenuManager as MenuManager
##############################################################################
class SystemTrayIcon ( QSystemTrayIcon , VirtualGui ) :
  ############################################################################
  emitShowMessage = pyqtSignal       ( str , str                             )
  emitSetIcon     = pyqtSignal       ( str                                   )
  ############################################################################
  def __init__ ( self , icon , parent = None ) :
    ##########################################################################
    QSystemTrayIcon . __init__ ( self , icon , parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    self . activated       . connect ( self . doTrayActivated                )
    self . emitShowMessage . connect ( self . doShowMessage                  )
    self . emitSetIcon     . connect ( self . doSetIcon                      )
    ##########################################################################
    self . Configure ( parent )
    ##########################################################################
    return
  ############################################################################
  def Configure ( self , parent ) :
    raise NotImplementedError ( )
  ############################################################################
  def PrepareMenu                    ( self , parent                       ) :
    raise NotImplementedError        (                                       )
  ############################################################################
  def AboutToShow                    ( self                                ) :
    raise NotImplementedError        (                                       )
  ############################################################################
  def RaiseMenu                      ( self , action                       ) :
    raise NotImplementedError        (                                       )
  ############################################################################
  def DoubleClickIcon                ( self                                ) :
    raise NotImplementedError        (                                       )
  ############################################################################
  def TriggerIcon                    ( self                                ) :
    self . AboutToShow             (                                       )
    a = self . Menu . exec_        ( QCursor . pos ( )                     )
    self . RaiseMenu               ( a                                     )
    return
  ############################################################################
  def MiddleIcon                     ( self                                ) :
    raise NotImplementedError        (                                       )
  ############################################################################
  def doTrayActivated                ( self , reason                       ) :
    ## Context
    if                               ( reason == 1                         ) :
      self . AboutToShow             (                                       )
      a = self . Menu . exec_        ( QCursor . pos ( )                     )
      self . RaiseMenu               ( a                                     )
    ## DoubleClick
    elif                             ( reason == 2                         ) :
      self . DoubleClickIcon         (                                       )
    ## Trigger
    elif                             ( reason == 3                         ) :
      self . TriggerIcon             (                                       )
    ## MiddleClick
    elif                             ( reason == 4                         ) :
      self . MiddleIcon              (                                       )
    return True
  ############################################################################
  def SendMessage                    ( self , TITLE , MESSAGE              ) :
    self . emitShowMessage . emit    (        TITLE , MESSAGE                )
    return True
  ############################################################################
  def doShowMessage                  ( self , TITLE , MESSAGE              ) :
    self . showMessage               (        TITLE , MESSAGE                )
    return True
  ############################################################################
  def SetIcon                        ( self , iconfile                     ) :
    self . emitSetIcon . emit        (        iconfile                       )
    return True
  ############################################################################
  def doSetIcon                      ( self , iconfile                     ) :
    self . setIcon                   ( QIcon ( iconfile )                    )
    return True
##############################################################################

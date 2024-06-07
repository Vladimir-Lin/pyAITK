# -*- coding: utf-8 -*-
##############################################################################
## System Tray Icon GUI
##############################################################################
import os
import sys
import time
##############################################################################
import PySide6
from   PySide6               import QtCore
from   PySide6               import QtGui
from   PySide6               import QtWidgets
##############################################################################
from   PySide6 . QtCore      import *
from   PySide6 . QtGui       import *
from   PySide6 . QtWidgets   import *
##############################################################################
from           . AbstractGui import AbstractGui as AbstractGui
from           . VirtualGui  import VirtualGui  as VirtualGui
from           . MenuManager import MenuManager as MenuManager
##############################################################################
class SystemTrayIcon       ( QSystemTrayIcon , VirtualGui                  ) :
  ############################################################################
  emitShowMessage = Signal ( str , str                                       )
  emitSetIcon     = Signal ( str                                             )
  ############################################################################
  def __init__             ( self , icon , parent = None , plan = None     ) :
    ##########################################################################
    super (                   ) . __init__ ( icon , parent                   )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    ##########################################################################
    self . activated       . connect ( self . doTrayActivated                )
    self . emitShowMessage . connect ( self . doShowMessage                  )
    self . emitSetIcon     . connect ( self . doSetIcon                      )
    ##########################################################################
    self . Configure                 ( parent                                )
    ##########################################################################
    return
  ############################################################################
  def Configure               ( self , parent                              ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def PrepareMenu             ( self , parent                              ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def AboutToShow             ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def RaiseMenu               ( self , action                              ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def DoubleClickIcon         ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def TriggerIcon           ( self                                         ) :
    ##########################################################################
    self . AboutToShow      (                                                )
    a = self . Menu . exec_ ( QCursor . pos ( )                              )
    self . RaiseMenu        ( a                                              )
    ##########################################################################
    return
  ############################################################################
  def MiddleIcon              ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def doTrayActivated         ( self , reason                              ) :
    ##########################################################################
    ## Context
    ##########################################################################
    if                        ( reason == QSystemTrayIcon . Context        ) :
      ########################################################################
      self . AboutToShow      (                                              )
      a = self . Menu . exec_ ( QCursor . pos ( )                            )
      self . RaiseMenu        ( a                                            )
    ##########################################################################
    ## DoubleClick
    ##########################################################################
    elif                      ( reason == QSystemTrayIcon . DoubleClick    ) :
      ########################################################################
      self . DoubleClickIcon  (                                              )
    ##########################################################################
    ## Trigger
    ##########################################################################
    elif                      ( reason == QSystemTrayIcon . Trigger        ) :
      ########################################################################
      self . TriggerIcon      (                                              )
    ##########################################################################
    ## MiddleClick
    ##########################################################################
    elif                      ( reason == QSystemTrayIcon . MiddleClick    ) :
      ########################################################################
      self . MiddleIcon       (                                              )
    return True
  ############################################################################
  def SendMessage                 ( self , TITLE , MESSAGE                 ) :
    self . emitShowMessage . emit (        TITLE , MESSAGE                   )
    return True
  ############################################################################
  def doShowMessage    ( self , TITLE , MESSAGE                            ) :
    self . showMessage (        TITLE , MESSAGE                              )
    return True
  ############################################################################
  def SetIcon                 ( self , iconfile                            ) :
    self . emitSetIcon . emit (        iconfile                              )
    return True
  ############################################################################
  def doSetIcon    ( self , iconfile                                       ) :
    self . setIcon ( QIcon ( iconfile )                                      )
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## TextEdit
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
import PySide6
from   PySide6              import QtCore
from   PySide6              import QtGui
from   PySide6              import QtWidgets
##############################################################################
from   PySide6 . QtCore     import *
from   PySide6 . QtGui      import *
from   PySide6 . QtWidgets  import *
##############################################################################
from           . VirtualGui import VirtualGui as VirtualGui
from           . AttachDock import AttachDock as AttachDock
##############################################################################
class TextEdit        ( QTextEdit , VirtualGui , AttachDock                ) :
  ############################################################################
  attachNone = Signal ( QWidget                                              )
  attachDock = Signal ( QWidget , str , int , int                            )
  attachMdi  = Signal ( QWidget , int                                        )
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    super ( AttachDock , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . InitializeDock                  ( plan                            )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setAttribute ( Qt . WA_InputMethodEnabled                         )
    self . VoiceJSON =  {                                                    }
    ##########################################################################
    return
  ############################################################################
  def focusInEvent               ( self , event                            ) :
    if                           ( self . focusIn ( event )                ) :
      return
    super ( ) . focusInEvent     ( event                                     )
    return
  ############################################################################
  def focusOutEvent              ( self , event                            ) :
    if                           ( self . focusOut ( event )               ) :
      return
    super ( ) . focusOutEvent    ( event                                     )
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    super ( ) . contextMenuEvent ( event                                     )
    return
  ############################################################################
  def closeEvent                 ( self , event                            ) :
    ##########################################################################
    if                           ( self . Shutdown ( )                     ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . closeEvent       ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def DockIn        ( self , shown                                         ) :
    ##########################################################################
    self . ShowDock (        shown                                           )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    ##########################################################################
    self . Visiblity (        visible                                        )
    ##########################################################################
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu                    ( self , menu                         ) :
    ##########################################################################
    canDock = self . isFunction      ( self . FunctionDocking                )
    if                               ( not canDock                         ) :
      return
    ##########################################################################
    p       = self . parentWidget    (                                       )
    S       = False
    D       = False
    M       = False
    ##########################################################################
    if                               ( p == None                           ) :
      S     = True
    else                                                                     :
      ########################################################################
      if                             ( self . isDocking ( )                ) :
        D   = True
      else                                                                   :
        M   = True
    ##########################################################################
    menu    . addSeparator           (                                       )
    ##########################################################################
    if                               (     S or D                          ) :
      msg   = self . getLocalMessage ( self . AttachToMdi                    )
      menu  . addAction              ( self . AttachToMdi  , msg             )
    ##########################################################################
    if                               (     S or M                          ) :
      msg   = self . getLocalMessage ( self . AttachToDock                   )
      menu  . addAction              ( self . AttachToDock , msg             )
    ##########################################################################
    if                               ( not S                               ) :
      msg   = self . getLocalMessage ( self . AttachToNone                   )
      menu  . addAction              ( self . AttachToNone , msg             )
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == self . AttachToNone                 ) :
      self . attachNone . emit ( self                                        )
      return True
    ##########################################################################
    if                         ( at == self . AttachToMdi                  ) :
      self . attachMdi  . emit ( self , self . dockingOrientation            )
      return True
    ##########################################################################
    if                         ( at == self . AttachToDock                 ) :
      self . attachDock . emit ( self                                      , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  def Shutdown                ( self                                       ) :
    return True
##############################################################################

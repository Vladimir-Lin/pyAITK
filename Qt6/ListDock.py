# -*- coding: utf-8 -*-
##############################################################################
## ListWidget
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
from           . AttachDock import AttachDock as AttachDock
from           . ListWidget import ListWidget as ListWidget
##############################################################################
class ListDock        ( ListWidget , AttachDock                            ) :
  ############################################################################
  attachNone = Signal ( QWidget                                              )
  attachDock = Signal ( QWidget , str , int , int                            )
  attachMdi  = Signal ( QWidget , int                                        )
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    ## WidgetClass                                            ;
    self . setFunction     ( self . FunctionDocking , True                   )
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
  def Visible        ( self , visible                                      ) :
    self . Visiblity (        visible                                        )
    return
  ############################################################################
  def DockIn         ( self , shown                                        ) :
    self . ShowDock  (        shown                                          )
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
##############################################################################

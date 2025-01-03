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
class ListDock         ( ListWidget , AttachDock                           ) :
  ############################################################################
  attachNone  = Signal ( QWidget                                             )
  attachStack = Signal ( QWidget                                             )
  attachDock  = Signal ( QWidget                                           , \
                         str                                               , \
                         Qt . DockWidgetArea                               , \
                         Qt . DockWidgetAreas                                )
  attachMdi   = Signal ( QWidget , int                                       )
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
    IDPMSG = self . Translations [ "Docking" ] [ "None"                      ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock"                      ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"                       ]
    STKMSG = self . Translations [ "Docking" ] [ "Stack"                     ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone  , IDPMSG             )
    self   . setLocalMessage     ( self . AttachToMdi   , MDIMSG             )
    self   . setLocalMessage     ( self . AttachToDock  , DCKMSG             )
    self   . setLocalMessage     ( self . AttachToStack , STKMSG             )
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
  def DockingMenu                     ( self , menu                        ) :
    ##########################################################################
    if                                ( not self . HavingPlacement         ) :
      return
    ##########################################################################
    canDock  = self . isFunction      ( self . FunctionDocking               )
    if                                ( not canDock                        ) :
      return
    ##########################################################################
    p        = self . parentWidget    (                                      )
    S        = False
    D        = False
    M        = False
    ##########################################################################
    if                                ( p == None                          ) :
      S      = True
    else                                                                     :
      ########################################################################
      if                              ( self . isDocking ( )               ) :
        D    = True
      else                                                                   :
        M    = True
    ##########################################################################
    menu     . addSeparator           (                                      )
    ##########################################################################
    if                                ( self . HavingMDI                   ) :
      if                              (     S or D                         ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToMdi                   )
        ico  = QIcon                  ( ":/images/GUI.png"                   )
        menu . addActionWithIcon      ( self . AttachToMdi  , ico , msg      )
    ##########################################################################
    if                                ( self . HavingDOCK                  ) :
      if                              (     S or M                         ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToDock                  )
        ico  = QIcon                  ( ":/images/hidespeech.png"            )
        menu . addActionWithIcon      ( self . AttachToDock , ico , msg      )
    ##########################################################################
    ## if                                ( self . HavingSTACK                 ) :
    ##   if                              ( not S                              ) :
    ##     ######################################################################
    ##     msg  = self . getLocalMessage ( self . AttachToStack                 )
    ##     menu . addAction              ( self . AttachToStack , msg           )
    ##########################################################################
    if                                ( self . HavingALONE                 ) :
      if                              ( not S                              ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToNone                  )
        menu . addAction              ( self . AttachToNone , msg            )
    ##########################################################################
    return
  ############################################################################
  def RunDocking                ( self , menu , action                     ) :
    ##########################################################################
    if                          ( not self . HavingPlacement               ) :
      return False
    ##########################################################################
    at = menu . at              ( action                                     )
    ##########################################################################
    if                          ( at == self . AttachToNone                ) :
      self . attachNone  . emit ( self                                       )
      return True
    ##########################################################################
    if                          ( at == self . AttachToMdi                 ) :
      self . attachMdi   . emit ( self , self . dockingOrientation           )
      return True
    ##########################################################################
    if                          ( at == self . AttachToDock                ) :
      self . attachDock  . emit ( self                                     , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    if                          ( at == self . AttachToStack               ) :
      self . attachStack . emit ( self                                       )
      return True
    ##########################################################################
    return False
##############################################################################

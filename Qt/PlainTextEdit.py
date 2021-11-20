# -*- coding: utf-8 -*-
##############################################################################
## PlainTextEdit
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
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QPlainTextEdit
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
from         . AttachDock             import AttachDock as AttachDock
##############################################################################
class PlainTextEdit       ( QPlainTextEdit , VirtualGui , AttachDock       ) :
  ############################################################################
  attachNone = pyqtSignal ( QWidget                                          )
  attachDock = pyqtSignal ( QWidget , str , int , int                        )
  attachMdi  = pyqtSignal ( QWidget , int                                    )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
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
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
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
  def Relocation              ( self                                       ) :
    return False
  ############################################################################
  def Menu                    ( self , pos                                 ) :
    raise NotImplementedError (                                              )
##############################################################################

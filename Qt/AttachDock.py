# -*- coding: utf-8 -*-
##############################################################################
## Dock抽象介面
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
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Qt        . DockWidget  import DockWidget
##############################################################################
class AttachDock         (                                                 ) :
  ############################################################################
  FunctionDocking = 1271293849
  AttachToNone    = 1000000
  AttachToMdi     = 1000001
  AttachToDock    = 1000002
  ############################################################################
  def __init__           ( self                                            ) :
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def InitializeDock     ( self , plan = None                              ) :
    ##########################################################################
    self . Trigger    = None
    self . Dock       = None
    self . dockPlan   = plan
    self . Scope      = ""
    self . Mutex      = threading . Lock ( )
    self . DockLimits = { }
    ##########################################################################
    return
  ############################################################################
  def setDockPlanFunction   ( self , func                                  ) :
    ##########################################################################
    self . dockPlan   = func
    ##########################################################################
    return
  ############################################################################
  def hasDockPlan           ( self                                         ) :
    return                  ( self . dockPlan != None                        )
  ############################################################################
  def GetDockPlan           ( self                                         ) :
    ##########################################################################
    if                      ( not self . hasDockPlan ( )                   ) :
      return None
    ##########################################################################
    return self . dockPlan  (                                                )
  ############################################################################
  def isDocking                    ( self                                  ) :
    if                             ( self . Dock == None                   ) :
      return False
    return self . Dock . isVisible (                                         )
  ############################################################################
  def LockDock             ( self                                          ) :
    self . Mutex . acquire (                                                 )
    return
  ############################################################################
  def UnlockDock           ( self                                          ) :
    self . Mutex . release (                                                 )
    return
  ############################################################################
  def ShowDock                          ( self , shown                     ) :
    ##########################################################################
    if                                  ( self . Dock == None              ) :
      return
    ##########################################################################
    self   . LockDock                   (                                    )
    ##########################################################################
    w      = self . Dock . parentWidget (                                    )
    if ( ( w != None ) and ( not w . isMinimized ( ) ) )                     :
      self . Dock . blockSignals        ( True                               )
      self . Dock . setVisible          ( shown                              )
      self . Dock . blockSignals        ( False                              )
    ##########################################################################
    self   . UnlockDock                 (                                    )
    ##########################################################################
    return
  ############################################################################
  def Visiblity                         ( self , visible                   ) :
    ##########################################################################
    if                                  ( self . Trigger == None           ) :
      return
    ##########################################################################
    w      = self . Dock . parentWidget (                                    )
    if ( ( w != None ) and ( not w . isMinimized ( ) ) )                     :
      self . Trigger . setChecked       ( visible                            )
    ##########################################################################
    return
  ############################################################################
  def getAllowArea   ( self , AREAS , areas , area                         ) :
    ##########################################################################
    if               ( ( areas & area ) == area                            ) :
      AREAS = AREAS | area
    ##########################################################################
    return AREAS
  ############################################################################
  def assignAllowAreas            ( self , areas                           ) :
    ##########################################################################
    A = 0
    A = self . getAllowArea       ( A , areas , Qt . LeftDockWidgetArea      )
    A = self . getAllowArea       ( A , areas , Qt . RightDockWidgetArea     )
    A = self . getAllowArea       ( A , areas , Qt . TopDockWidgetArea       )
    A = self . getAllowArea       ( A , areas , Qt . BottomDockWidgetArea    )
    ##########################################################################
    self . Dock . setAllowedAreas ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def Store                   ( self , Main                                ) :
    ##########################################################################
    self . LockDock           (                                              )
    ##########################################################################
    """
      QRect     DR = Dock -> geometry                 (            ) ;
      QWidget * wx = Dock -> widget                   (            ) ;
      DockInformation DI                                             ;
      DI    . geometry = Dock -> saveGeometry         (            ) ;
      DI    . floating = Dock -> isFloating           (            ) ;
      DI    . show     = Dock -> isVisible            (            ) ;
      DI    . area     = (int) Main -> dockWidgetArea ( Dock       ) ;
      DI    . width    = DR    . width                (            ) ;
      DI    . height   = DR    . height               (            ) ;
      plan -> site . SaveDock                         ( Scope , DI ) ;
      if ( NotNull ( wx ) )                                          {
        QSize hs = wx -> size     (                                ) ;
        plan -> site . beginGroup ( Scope                          ) ;
        plan -> site . setValue   ( "HintWidth"  , hs . width  ( ) ) ;
        plan -> site . setValue   ( "HintHeight" , hs . height ( ) ) ;
        plan -> site . endGroup   (                                ) ;
      }                                                              ;
    """
    ##########################################################################
    self . UnlockDock         (                                              )
    ##########################################################################
    return
  ############################################################################
  def Docking                        ( self                                , \
                                       Main                                , \
                                       widget                              , \
                                       title                               , \
                                       area                                , \
                                       areas                               ) :
    ##########################################################################
    if                               ( not self . hasDockPlan ( )          ) :
      return
    ##########################################################################
    plan     = self . GetDockPlan    (                                       )
    ##########################################################################
    """
    int             w       = plan -> screen . widthPixels ( 40 ) 4公分             ;
    bool            restore = false                                            ;
    QSize           WS                                                         ;
    DockInformation DI                                                         ;
    """
    w        = 80
    Restore  = False
    DIW      = 0
    DIH      = 0
    Floating = False
    Show     = True
    ##########################################################################
    if   ( area in [ Qt . LeftDockWidgetArea , Qt . RightDockWidgetArea  ] ) :
      DIW    = w
      DIH    = Main . height         (                                       )
    elif ( area in [ Qt . TopDockWidgetArea  , Qt . BottomDockWidgetArea ] ) :
      DIW    = Main . width          (                                       )
      DIH    = w
    ##########################################################################
    ## plan -> site . LoadDock ( Scope , DI )
    ##########################################################################
    self     . Dock = DockWidget     ( Main , self . dockPlan                )
    self     . Dock . blockSignals   ( True                                  )
    ##########################################################################
    ## Dock -> setFont ( plan->fonts[N::Fonts::Default] )
    self     . Dock . setWindowTitle ( title                                 )
    self     . Dock . setWidget      ( widget                                )
    self     . Dock . setToolTip     ( title                                 )
    Main     . addDockWidget         ( area , self . Dock                    )
    widget   . setWindowTitle        ( title                                 )
    ## DockLimits [ 2 ] = widget -> minimumSize ( )
    ## DockLimits [ 3 ] = widget -> maximumSize ( )
    self     . assignAllowAreas      ( areas                                 )
    ## if ( DI . geometry . size ( ) > 0 )                                        {
    ##   Dock -> restoreGeometry          ( DI . geometry                       ) ;
    ## }                                                                          ;
    self     . Dock . setFloating    ( Floating                              )
    """
    WS               . setWidth        ( DI . width                          ) ;
    WS               . setHeight       ( DI . height                         ) ;
    if ( ( WS . width ( ) > 0 ) && ( WS . height ( ) > 0 ) ) restore = true    ;
    if ( restore )                                                             {
      QSize DS = Dock -> maximumSize   (       )                               ;
      widget          -> resize        ( WS    )                               ;
      plan      -> site . beginGroup   ( Scope )                               ;
      if ( plan -> site . contains ( "HintWidth" ) )                           {
        if ( plan -> site . contains ( "HintHeight" ) )                        {
          QSize         hs                                                     ;
          AbstractGui * ag = dynamic_cast<AbstractGui *>(widget)               ;
          hs . setWidth  ( plan -> site . value ( "HintWidth"  ) . toInt() )   ;
          hs . setHeight ( plan -> site . value ( "HintHeight" ) . toInt() )   ;
          if ( NotNull ( ag ) ) ag -> setSuggestion ( hs )                     ;
        }                                                                      ;
      }                                                                        ;
      plan            -> site . endGroup                 (    )                ;
      Dock            -> DockGeometry = Dock -> geometry (    )                ;
      Dock            -> DockGeometry . setSize          ( WS )                ;
      DockLimits [ 0 ] = WS                                                    ;
      DockLimits [ 1 ] = DS                                                    ;
    }                                                                          ;
    """
    ##########################################################################
    self     . Dock . setVisible     ( True                                  )
    self     . Dock . blockSignals   ( False                                 )
    ## plan -> setFont        ( Dock      )
    ##########################################################################
    Located  = getattr               ( widget , "DockLocationChanged" , None )
    if                               ( Located is not None                 ) :
      if                             ( callable ( Located )                ) :
        self . Dock . dockLocationChanged . connect ( Located                )
    ##########################################################################
    qApp     . processEvents         (                                       )
    ##########################################################################
    return
  ############################################################################
  def Detach                  ( self , Main                                ) :
    ##########################################################################
    if                        ( self . Dock == None                        ) :
      return
    ##########################################################################
    Main . removeDockWidget   ( self . Dock                                  )
    self . Dock . deleteLater (                                              )
    self . Dock = None
    qApp . processEvents      (                                              )
    ##########################################################################
    return
##############################################################################

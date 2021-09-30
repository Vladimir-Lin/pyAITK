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
##############################################################################
class AttachDock         (                                                 ) :
  ############################################################################
  FunctionDocking = 1271293849
  AttachToMdi     = 1000001
  AttachToDock    = 1000002
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    self . Trigger    = None
    self . Dock       = None
    self . dockPlan   = None
    self . Scope      = ""
    self . Mutex      = threading . Lock ( )
    self . DockLimits = { }
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
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
  def Store                   ( self , Main                                ) :
    ##########################################################################
    ##########################################################################
    """
    void N::AttachDock::Store(QMainWindow * Main)
    {
      LockDock                                        (            ) ;
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
      UnlockDock                                      (            ) ;
    }
    """
    ##########################################################################
    return
  ############################################################################
  def Docking                ( self , Main , widget , title , area , areas ) :
    ##########################################################################
    ##########################################################################
    """
    void N::AttachDock::Docking       (
           QMainWindow       * Main   ,
           QWidget           * widget ,
           QString             title  ,
           Qt::DockWidgetArea  area   ,
           Qt::DockWidgetAreas areas  )
    {
      if ( IsNull ( plan ) ) return                                              ;
      int             w       = plan -> screen . widthPixels ( 40 )              ;
      bool            restore = false                                            ;
      QSize           WS                                                         ;
      DockInformation DI                                                         ;
      ////////////////////////////////////////////////////////////////////////////
      switch ( area )                                                            {
        case Qt::LeftDockWidgetArea                                              :
        case Qt::RightDockWidgetArea                                             :
          DI . width    = w                                                      ;
          DI . height   = Main -> height ( )                                     ;
        break                                                                    ;
        case Qt::TopDockWidgetArea                                               :
        case Qt::BottomDockWidgetArea                                            :
          DI . width    = Main -> width  ( )                                     ;
          DI . height   = w                                                      ;
        break                                                                    ;
      }                                                                          ;
      ////////////////////////////////////////////////////////////////////////////
      DI    . floating = false                                                   ;
      DI    . show     = true                                                    ;
      DI    . area     = area                                                    ;
      plan -> site . LoadDock            ( Scope , DI                          ) ;
      Dock             = new DockWidget  ( Main                                ) ;
      Dock            -> blockSignals    ( true                                ) ;
      Dock            -> setFont         ( plan->fonts[N::Fonts::Default]      ) ;
      Dock            -> setWindowTitle  ( title                               ) ;
      Dock            -> setWidget       ( widget                              ) ;
      Dock            -> setToolTip      ( title                               ) ;
      Main            -> addDockWidget   ( (Qt::DockWidgetArea) DI.area , Dock ) ;
      widget          -> setWindowTitle  ( title                               ) ;
      DockLimits [ 2 ] = widget -> minimumSize (                               ) ;
      DockLimits [ 3 ] = widget -> maximumSize (                               ) ;
      ////////////////////////////////////////////////////////////////////////////
      Dock            -> setAllowedAreas ( areas                               ) ;
      if ( DI . geometry . size ( ) > 0 )                                        {
        Dock -> restoreGeometry          ( DI . geometry                       ) ;
      }                                                                          ;
      Dock            -> setFloating     ( DI . floating                       ) ;
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
      Dock -> setVisible     ( DI . show )                                       ;
      Dock -> blockSignals   ( false     )                                       ;
      plan -> setFont        ( Dock      )                                       ;
      plan -> processEvents  (           )                                       ;
    }
    """
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

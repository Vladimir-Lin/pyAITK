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
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Pair        import Pair
from   AITK . Database  . Columns     import Columns
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
##############################################################################
class AttachDock         (                                                 ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    self . Trigger  = None
    self . Dock     = None
    self . dockPlan = None
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def isPrepared         ( self                                            ) :
    return self . Prepared
  ############################################################################
  def setPrepared        ( self , prepared                                 ) :
    self . Prepared = prepared
    return self . Prepared
  ############################################################################
  def getLocality        ( self                                            ) :
    return self . Locality
  ############################################################################
  def setLocality        ( self , locality                                 ) :
    ##########################################################################
    self . Locality = locality
    ##########################################################################
    return self . Locality
  ############################################################################
  def Initialize         ( self , widget = None                            ) :
    ##########################################################################
    self . Gui          = widget
    ##########################################################################
    return
  ############################################################################
  def focusIn            ( self , event                                    ) :
    ##########################################################################
    if                   ( event . gotFocus ( )                            ) :
      if                 ( self  . FocusIn  ( )                            ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = True
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def focusOut           ( self , event                                    ) :
    ##########################################################################
    if                   ( event . lostFocus ( )                           ) :
      if                 ( self  . FocusOut  ( )                           ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = False
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def FocusIn                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def FocusOut                ( self                                       ) :
    raise NotImplementedError (                                              )
##############################################################################

"""

bool N::AttachDock::isDocking(void)
{
  nKickOut ( IsNull ( Dock ) , false ) ;
  return Dock -> isVisible ( )         ;
}

void N::AttachDock::Show(bool shown)
{
  nDropOut ( IsNull ( Dock ) )                       ;
  LockDock   ( )                                     ;
  QWidget * w = Dock -> parentWidget ( )             ;
  Dock -> blockSignals ( true  )                     ;
  if ( NotNull ( w ) && ( ! w -> isMinimized ( ) ) ) {
    Dock -> setVisible ( shown )                     ;
  }                                                  ;
  Dock -> blockSignals ( false )                     ;
  UnlockDock           (       )                     ;
}

void N::AttachDock::Visiblity(bool visible)
{
  nDropOut ( IsNull ( Trigger ) )                    ;
  QWidget * w = Dock -> parentWidget ( )             ;
  if ( NotNull ( w ) && ( ! w -> isMinimized ( ) ) ) {
    Trigger -> setChecked ( visible )                ;
  }                                                  ;
}

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

void N::AttachDock::LockDock   (void)
{
  Mutex . lock ( ) ;
}

void N::AttachDock::UnlockDock (void)
{
  Mutex . unlock ( ) ;
}

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

void N::AttachDock::Detach(QMainWindow * Main)
{
  nDropOut ( IsNull ( Dock ) )      ;
  Main -> removeDockWidget ( Dock ) ;
  Dock -> deleteLater      (      ) ;
  Dock  = NULL                      ;
  plan -> processEvents    (      ) ;
}

void N::AttachDock::Restrict(bool strict,QWidget * widget)
{
}

"""

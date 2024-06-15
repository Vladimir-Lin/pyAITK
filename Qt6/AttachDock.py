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
import PySide6
from   PySide6                          import QtCore
from   PySide6                          import QtGui
from   PySide6                          import QtWidgets
##############################################################################
from   PySide6 . QtCore                 import *
from   PySide6 . QtGui                  import *
from   PySide6 . QtWidgets              import *
##############################################################################
from   AITK    . Calendars . StarDate   import StarDate
from   AITK    . Qt6       . DockWidget import DockWidget
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
  def InitializeDock                     ( self , plan = None              ) :
    ##########################################################################
    self . Trigger    = None
    self . Dock       = None
    self . dockPlan   = plan
    self . Scope      = ""
    self . Mutex      = threading . Lock (                                   )
    self . DockLimits =                  {                                   }
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
  def getAllowArea ( self , AREAS , areas , area                           ) :
    ##########################################################################
    if             ( ( areas & area ) == area                              ) :
      AREAS = AREAS | area
    ##########################################################################
    return AREAS
  ############################################################################
  def assignAllowAreas            ( self , areas                           ) :
    ##########################################################################
    A = Qt   . NoDockWidgetArea
    A = self . getAllowArea       ( A , areas , Qt . LeftDockWidgetArea      )
    A = self . getAllowArea       ( A , areas , Qt . RightDockWidgetArea     )
    A = self . getAllowArea       ( A , areas , Qt . TopDockWidgetArea       )
    A = self . getAllowArea       ( A , areas , Qt . BottomDockWidgetArea    )
    ##########################################################################
    self . Dock . setAllowedAreas ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def LoadDockingSettings     ( self                                       ) :
    return                    {                                              }
  ############################################################################
  def SaveDockingSettings     ( self , JSON                                ) :
    return
  ############################################################################
  def ByteArrayToString  ( self , qbyte                                    ) :
    ##########################################################################
    if                   ( qbyte == None                                   ) :
      return ""
    ##########################################################################
    try                                                                      :
      BB = qbyte . data  (                                                   )
    except                                                                   :
      return ""
    ##########################################################################
    if                   ( BB == None                                      ) :
      return ""
    ##########################################################################
    if                   ( len ( BB ) <= 0                                 ) :
      return ""
    ##########################################################################
    try                                                                      :
      SS = BB . decode   ( "utf-8"                                           )
    except                                                                   :
      return ""
    ##########################################################################
    return SS
  ############################################################################
  def HexToByteArray            ( self , HEX                               ) :
    ##########################################################################
    try                                                                      :
      HH = HEX . encode         ( "utf-8"                                    )
      BX = QByteArray           ( HH                                         )
    except                                                                   :
      return QByteArray         (                                            )
    ##########################################################################
    return QByteArray . fromHex ( BX )
  ############################################################################
  def Store                       ( self , area                            ) :
    ##########################################################################
    self . LockDock               (                                          )
    ##########################################################################
    DR   = self . Dock . geometry (                                          )
    WX   = self . Dock . widget   (                                          )
    DI   =                        {                                          }
    SG   = self . Dock . saveGeometry (                                      )
    SGS  = self . ByteArrayToString   ( SG . toHex ( )                       )
    ##########################################################################
    DI [ "Geometry"   ] = SGS
    DI [ "Floating"   ] = self . Dock . isFloating   (                       )
    DI [ "Show"       ] = self . Dock . isVisible    (                       )
    DI [ "Area"       ] = area
    DI [ "Width"      ] = DR   . width               (                       )
    DI [ "Height"     ] = DR   . height              (                       )
    ##########################################################################
    DI [ "HintWidth"  ] = 0
    DI [ "HintHeight" ] = 0
    ##########################################################################
    if                            ( WX not in [ False , None ]             ) :
      ########################################################################
      hs = WX . size              (                                          )
      DI [ "HintWidth"  ] = hs . width  (                                    )
      DI [ "HintHeight" ] = hs . height (                                    )
    ##########################################################################
    self . SaveDockingSettings    ( DI                                       )
    ##########################################################################
    self . UnlockDock             (                                          )
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
    w        = 80
    WS       = QSize  ( )
    DI       = { }
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
    DI       = self . LoadDockingSettings (                                  )
    ##########################################################################
    self     . Dock = DockWidget     ( Main , self . dockPlan                )
    self     . Dock . blockSignals   ( True                                  )
    ##########################################################################
    self     . Dock . setWindowTitle ( title                                 )
    self     . Dock . setWidget      ( widget                                )
    self     . Dock . setToolTip     ( title                                 )
    Main     . addDockWidget         ( area , self . Dock                    )
    widget   . setWindowTitle        ( title                                 )
    self     . DockLimits [ 2 ] = widget . minimumSize (                     )
    self     . DockLimits [ 3 ] = widget . maximumSize (                     )
    self     . assignAllowAreas      ( areas                                 )
    self     . Dock . setFloating    ( Floating                              )
    ##########################################################################
    if                               ( "Geometry" in DI                    ) :
      HBA    = self . HexToByteArray ( DI [ "Geometry" ]                     )
      self   . Dock . restoreGeometry ( HBA                                  )
    ##########################################################################
    if                               ( "Width"  in DI                      ) :
      WS     . setWidth              ( DI [ "Width"  ]                       )
    ##########################################################################
    if                               ( "Height" in DI                      ) :
      WS     . setHeight             ( DI [ "Height" ]                       )
    ##########################################################################
    if ( ( WS . width ( ) > 0 ) and ( WS . height ( ) > 0 ) )                :
      Restore  = True
    ##########################################################################
    if                               ( Restore                             ) :
      ########################################################################
      DS     = self . Dock . maximumSize (                                   )
      widget . resize                ( WS                                    )
      HW     = DI                    [ "HintWidth"                           ]
      HH     = DI                    [ "HintHeight"                          ]
      hs     = QSize                 (                                       )
      hs     . setWidth              ( HW                                    )
      hs     . setHeight             ( HH                                    )
      widget . setSuggestion         ( hs                                    )
      self   . Dock . DockGeometry = self . Dock . geometry (                )
      self   . Dock . DockGeometry . setSize ( WS                            )
    ##########################################################################
    self     . Dock . setVisible     ( True                                  )
    self     . Dock . blockSignals   ( False                                 )
    ##########################################################################
    Located  = getattr               ( widget , "DockLocationChanged" , None )
    if                               ( Located is not None                 ) :
      if                             ( callable ( Located )                ) :
        self . Dock . dockLocationChanged . connect ( Located                )
    ##########################################################################
    VISIBLE  = getattr               ( widget , "DockVisibleChanged"  , None )
    if                               ( VISIBLE is not None                 ) :
      if                             ( callable ( VISIBLE )                ) :
        self . Dock . visibilityChanged   . connect ( VISIBLE                )
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

# -*- coding: utf-8 -*-
##############################################################################
## ControlPad
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
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QStackedWidget
from   PyQt5 . QtWidgets              import QSplitter
from   PyQt5 . QtWidgets              import QToolButton
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QLabel
##############################################################################
from         . AttachDock             import AttachDock as AttachDock
from         . Splitter               import Splitter   as Splitter
##############################################################################
class ControlPad             ( Splitter , AttachDock                       ) :
  ############################################################################
  attachNone    = pyqtSignal ( QWidget                                       )
  attachDock    = pyqtSignal ( QWidget , str , int , int                     )
  attachMdi     = pyqtSignal ( QWidget , int                                 )
  SendAdd       = pyqtSignal ( str , QWidget , QObject                       )
  SendLeave     = pyqtSignal ( QObject                                       )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super (                   ) . __init__ ( Qt . Vertical , parent , plan   )
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
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 280 , 640 )                       )
  ############################################################################
  def Prepare                           ( self                             ) :
    ##########################################################################
    sss  = "QStackedWidget { background: rgb(255,255,255) ; }"
    ##########################################################################
    self . ToolStack = None
    self . ViewStack = None
    self . Top       = None
    self . ButtonPad = None
    self . Close     = None
    self . Position  = None
    self . Tools     = None
    self . Empty     = None
    self . Lastest   = 1
    self . Parents   =                  {                                    }
    self . WidgetId  =                  {                                    }
    self . WidgetMap =                  {                                    }
    self . Titles    =                  {                                    }
    ##########################################################################
    self . ToolStack = QStackedWidget   ( self                               )
    self . ViewStack = QStackedWidget   ( self                               )
    self . Top       = QSplitter        ( Qt . Horizontal , self . ToolStack )
    self . ButtonPad = QWidget          ( self . Top                         )
    self . Close     = QToolButton      ( self . ButtonPad                   )
    self . Position  = QToolButton      ( self . ButtonPad                   )
    self . Tools     = QComboBox        ( self . Top                         )
    self . Empty     = QLabel           ( self . ViewStack                   )
    ##########################################################################
    self . ViewStack . setStyleSheet    ( sss                                )
    ##########################################################################
    self . ToolStack . setMinimumHeight ( 28                                 )
    self . ToolStack . setMaximumHeight ( 28                                 )
    self . addWidget                    ( self . ViewStack                   )
    self . addWidget                    ( self . ToolStack                   )
    self . ViewStack . addWidget        ( self . Empty                       )
    ##########################################################################
    self . Top       . setHandleWidth   ( 0                                  )
    self . Top       . setMinimumHeight ( 28                                 )
    self . Top       . setMaximumHeight ( 28                                 )
    self . ToolStack . addWidget        ( self . Top                         )
    ##########################################################################
    self . Top       . addWidget        ( self . ButtonPad                   )
    self . Top       . addWidget        ( self . Tools                       )
    self . ButtonPad . setMinimumWidth  ( 56                                 )
    self . ButtonPad . setMaximumWidth  ( 56                                 )
    ##########################################################################
    msg  = self      . getMenuItem      ( "Close"                            )
    ICON = QIcon                        ( ":/images/close.png"               )
    self . Close     . setGeometry      (  0 ,  0 , 28 , 28                  )
    self . Close     . setAutoRaise     ( True                               )
    self . Close     . setIcon          ( ICON                               )
    self . Close     . setToolTip       ( msg                                )
    ##########################################################################
    msg  = self      . getMenuItem      ( "ChangeDocking"                    )
    ICON = QIcon                        ( ":/images/hide.png"                )
    self . Position  . setGeometry      ( 28 ,  0 , 28 , 28                  )
    self . Position  . setAutoRaise     ( True                               )
    self . Position  . setIcon          ( ICON                               )
    self . Position  . setToolTip       ( msg                                )
    ##########################################################################
    self . setHandleWidth               (   1                                )
    self . setMinimumWidth              ( 160                                )
    self . setMinimumHeight             ( 160                                )
    ##########################################################################
    self . ToolStack . setCurrentWidget ( self . Top                         )
    self . ViewStack . setCurrentWidget ( self . Empty                       )
    ##########################################################################
    self . Close     . setEnabled       ( False                              )
    self . Tools     . setEnabled       ( False                              )
    self . Tools     . setEditable      ( True                               )
    ##########################################################################
    msg  = self      . getMenuItem      ( "NoController"                     )
    self . Empty     . setText          ( msg                                )
    self . Empty     . setAlignment     ( Qt . AlignCenter                   )
    ##########################################################################
    self . ViewStack . setMouseTracking ( True                               )
    self . ViewStack . setFocusPolicy   ( Qt . WheelFocus                    )
    ##########################################################################
    self . SendLeave             . connect ( self . ActualLeave              )
    self . SendAdd               . connect ( self . ActualAdd                )
    self . Tools     . activated . connect ( self . WidgetChanged            )
    self . Close     . clicked   . connect ( self . CloseWidget              )
    self . Position  . clicked   . connect ( self . ChangePosition           )
    ##########################################################################
    self . ToolStack . show             (                                    )
    self . ViewStack . show             (                                    )
    self . Top       . show             (                                    )
    self . ButtonPad . show             (                                    )
    self . Close     . show             (                                    )
    self . Position  . show             (                                    )
    self . Tools     . show             (                                    )
    self . Empty     . show             (                                    )
    ## self . plan      . setFont ( this )
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
  def Visible        ( self , visible                                      ) :
    self . Visiblity (        visible                                        )
    return
  ############################################################################
  def DockIn          ( self , shown                                       ) :
    ##########################################################################
    self . Show       (        shown                                         )
    self . Relocation (                                                      )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    super ( ) . resizeEvent (        event                                   )
    self . Relocation       (                                                )
    ##########################################################################
    return
  ############################################################################
  def Relocation ( self                                                    ) :
    return
  ############################################################################
  def Leave                 ( self , widget                                ) :
    self . SendLeave . emit (        widget                                  )
    return
  ############################################################################
  def Detach                ( self , widget                                ) :
    ##########################################################################
    if                      ( widget not in self . WidgetId                ) :
      return
    ##########################################################################
    index = self . WidgetId [ widget                                         ]
    if                      ( index < 0                                    ) :
      return
    ##########################################################################
    self . Delete           ( widget                                         )
    self . FindCurrent      ( index                                          )
    ##########################################################################
    return
  ############################################################################
  def Delete                         ( self , widget                       ) :
    ##########################################################################
    if                               ( widget not in self . WidgetId       ) :
      return
    ##########################################################################
    index  = self . WidgetId         [ widget                                ]
    if                               ( index < 0                           ) :
      return
    ##########################################################################
    del self . Parents               [ widget                                ]
    del self . WidgetId              [ widget                                ]
    del self . WidgetMap             [ index                                 ]
    del self . Titles                [ index                                 ]
    ##########################################################################
    pos    = -1
    ##########################################################################
    for i in range                   ( 0 , self . Tools . count ( )        ) :
      ########################################################################
      v    = self . Tools . itemData ( i                                     )
      v    = int                     ( v                                     )
      if                             ( v == index                          ) :
        pos = i
    ##########################################################################
    if                               ( pos < 0                             ) :
      return
    ##########################################################################
    self   . Tools . removeItem      ( pos                                   )
    widget . deleteLater             (                                       )
    ##########################################################################
    return
  ############################################################################
  def addControl               ( self , name , widget , parent             ) :
    ##########################################################################
    parent . Leave   . connect ( self . Leave                                )
    self   . SendAdd . emit    (        name , widget , parent               )
    ##########################################################################
    return
  ############################################################################
  def ActualLeave                        ( self , object                   ) :
    ##########################################################################
    index  = self . Tools . currentIndex (                                   )
    if                                   ( index < 0                       ) :
      return
    ##########################################################################
    wid    = self . Tools . itemData     ( index                             )
    wid    = int                         ( wid                               )
    if                                   ( wid < 0                         ) :
      return
    ##########################################################################
    Ws     = self . Parents . keys       (                                   )
    Ds     =                             [                                   ]
    ##########################################################################
    for w in Ws                                                              :
      if                                 ( object == self . Parents [ w ]  ) :
        Ds . append                      ( w                                 )
    ##########################################################################
    if                                   ( len ( Ds ) <= 0                 ) :
      return
    ##########################################################################
    for w in Ds                                                              :
      self . Delete                      ( w                                 )
    ##########################################################################
    self   . FindCurrent                 ( wid                               )
    ##########################################################################
    return
  ############################################################################
  def ActualAdd                           ( self , name , widget , parent  ) :
    ##########################################################################
    self . Lastest = self . Lastest + 1
    ##########################################################################
    widget . setParent                    ( self . ViewStack                 )
    self   . ViewStack . addWidget        ( widget                           )
    self   . ViewStack . setCurrentWidget ( widget                           )
    ##########################################################################
    self   . Parents   [ widget         ] = parent
    self   . WidgetId  [ widget         ] = self . Lastest
    self   . WidgetMap [ self . Lastest ] = widget
    self   . Titles    [ self . Lastest ] = name
    ##########################################################################
    index  = self . Tools . count         (                                  )
    ##########################################################################
    self   . Close . setEnabled           ( True                             )
    ##########################################################################
    self   . Tools . setEnabled           ( True                             )
    self   . Tools . addItem              ( name , self . Lastest            )
    self   . Tools . blockSignals         ( True                             )
    self   . Tools . setCurrentIndex      ( index                            )
    self   . Tools . blockSignals         ( False                            )
    ##########################################################################
    return
  ############################################################################
  def ChangePosition ( self                                                ) :
    ##########################################################################
    """
    QMdiSubWindow * mdi  = Casting(QMdiSubWindow,parent())      ;
    QDockWidget   * dock = Casting(QDockWidget  ,parent())      ;
    nIfSafe(dock) emit attachMdi  ( this , dockingOrientation ) ;
    nIfSafe(mdi ) emit attachDock ( this                        ,
                                    windowTitle ( )             ,
                                    dockingPlace                ,
                                    dockingPlaces             ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def FindCurrent                         ( self , index                   ) :
    ##########################################################################
    if                                    ( self . Tools . count ( ) <= 0  ) :
      ########################################################################
      self . ViewStack . setCurrentWidget ( self . Empty                     )
      self . Close     . setEnabled       ( False                            )
      self . Tools     . setEnabled       ( False                            )
      self . Notify                       ( 2                                )
      ########################################################################
      return
    ##########################################################################
    index  = self . Tools . currentIndex  (                                  )
    if                                    ( index < 0                      ) :
      return
    ##########################################################################
    wid    = int                          ( self . Tools . itemData(index)   )
    ##########################################################################
    if                                    ( wid < 0                        ) :
      return
    ##########################################################################
    if                                    ( wid not in self . WidgetMap    ) :
      return
    ##########################################################################
    w      = self . WidgetMap             [ wid                              ]
    self   . ViewStack . setCurrentWidget ( w                                )
    self   . Notify                       ( 5                                )
    ##########################################################################
    return
  ############################################################################
  def CloseWidget                       ( self                             ) :
    ##########################################################################
    index = self . Tools . currentIndex (                                    )
    if                                  ( index < 0                        ) :
      return
    ##########################################################################
    wid   = int                         ( self . Tools . itemData ( index )  )
    if                                  ( wid < 0                          ) :
      return
    ##########################################################################
    if                                  ( wid not in self . WidgetMap      ) :
      return
    ##########################################################################
    w     = self . WidgetMap            [ wid                                ]
    self  . Delete                      ( w                                  )
    self  . FindCurrent                 ( wid                                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                             (        int                         )
  def WidgetChanged                     ( self , index                     ) :
    ##########################################################################
    wid = int                           ( self . Tools . itemData ( index )  )
    if                                  ( wid <= 0                         ) :
      return
    ##########################################################################
    self . ViewStack . setCurrentWidget ( self . WidgetMap [ wid ]           )
    ##########################################################################
    return
  ############################################################################
  def Find                        ( self , accessibleNameWidget            ) :
    ##########################################################################
    IDs = self . WidgetMap . keys (                                          )
    if                            ( len ( IDs ) <= 0                       ) :
      return None
    ##########################################################################
    for ID in IDs                                                            :
      ########################################################################
      w = self . WidgetMap        [ ID                                       ]
      if                          ( w not in [ False , None ]              ) :
        ######################################################################
        anv = w . accessibleName  (                                          )
        if                        ( anv == accessibleNameWidget            ) :
          return w
    ##########################################################################
    return None
##############################################################################

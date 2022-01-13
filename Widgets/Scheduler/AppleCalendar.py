# -*- coding: utf-8 -*-
##############################################################################
## AppleCalendar
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
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
##############################################################################
from   AITK  . Calendars  . Apple     import Apple       as DAV
##############################################################################
class AppleCalendar                ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 3                                       )
    self . setColumnHidden         ( 2 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 480 , 640 )                       )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . startup                   )
    ##########################################################################
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut             ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked         ( self , item , column                         ) :
    ##########################################################################
    if                      ( self . isItemPicked ( )                      ) :
      if                    ( column != self . CurrentItem [ "Column" ]    ) :
        self . removeParked (                                                )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked ( self , item , column                                 ) :
    ##########################################################################
    if              ( column not in [ 0 ]                                  ) :
      return
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , JSON                                ) :
    ##########################################################################
    ID      = JSON            [ "Id"                                         ]
    Name    = JSON            [ "Name"                                       ]
    ##########################################################################
    IT      = QTreeWidgetItem (                                              )
    ##########################################################################
    IT      . setText         ( 0 , Name                                     )
    IT      . setText         ( 1 , ID                                       )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , CALENDARS                       ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in CALENDARS                                                       :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                      ( self                                  ) :
    ##########################################################################
    URL   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"        ]
    DSID  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"       ]
    USER  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"   ]
    PASS  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"   ]
    ##########################################################################
    APPLE = DAV                    ( URL , DSID , USER , PASS                )
    OKAY  = APPLE . FetchCalendars (                                         )
    ##########################################################################
    CALS  =                        [                                         ]
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      self . emitNamesShow . emit  (                                         )
      ########################################################################
      return
    ##########################################################################
    for calendar in APPLE . Calendars                                        :
      ########################################################################
      CID   = APPLE . CalendarId   ( calendar                                )
      NAME  = calendar.name
      ########################################################################
      J     =                      { "Id"      : CID                       , \
                                     "Name"    : NAME                        }
      CALS  . append               ( J                                       )
    ##########################################################################
    if                             ( len ( CALS ) <= 0                     ) :
      self  . emitNamesShow . emit (                                         )
      return
    ##########################################################################
    self    . emitAllNames  . emit ( CALS                                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot          (                                                       )
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 0 , 120                                   )
    self   . setColumnWidth      ( 2 ,   3                                   )
    LABELs = self . Translations [ "AppleCalendar" ] [ "Labels"              ]
    self   . setCentralLabels    ( LABELs                                    )
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( 1                                        )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    items  = self . selectedItems  (                                         )
    item   = self . currentItem    (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu    ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunColumnsMenu    ( at )       ) :
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    return True
##############################################################################

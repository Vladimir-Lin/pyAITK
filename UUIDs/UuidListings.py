# -*- coding: utf-8 -*-
##############################################################################
## UuidListings
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
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
defaultUuidListings = None
SystemUUIDs         = [                                                      ]
##############################################################################
def setUuidListings ( UUID                                                 ) :
  ############################################################################
  global defaultUuidListings
  ############################################################################
  defaultUuidListings = UUID
  ############################################################################
  return
##############################################################################
def getUuids (                                                             ) :
  ############################################################################
  global SystemUUIDs
  ############################################################################
  return SystemUUIDs
##############################################################################
def appendUuid                  ( UUID                                     ) :
  ############################################################################
  global defaultUuidListings
  global SystemUUIDs
  ############################################################################
  SystemUUIDs         . append  ( UUID                                       )
  defaultUuidListings . startup (                                            )
  ############################################################################
  return
##############################################################################
def appendUuids                 ( UUIDs                                    ) :
  ############################################################################
  global defaultUuidListings
  global SystemUUIDs
  ############################################################################
  for UUID in UUIDs                                                          :
    ##########################################################################
    SystemUUIDs       . append  ( UUID                                       )
  ############################################################################
  defaultUuidListings . startup (                                            )
  ############################################################################
  return
##############################################################################
class UuidListings         ( TreeDock                                      ) :
  ############################################################################
  HavingMenu = 1371434312
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
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                  (                                               )
  def startup                ( self                                        ) :
    ##########################################################################
    global SystemUUIDs
    ##########################################################################
    self   . clear           (                                               )
    ##########################################################################
    for UUID in SystemUUIDs                                                  :
      ########################################################################
      item = QTreeWidgetItem (                                               )
      item . setText         ( 0 , str ( UUID )                              )
      item . setData         ( 0 , Qt . UserRole , UUID                      )
      self . addTopLevelItem ( item                                          )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "UuidListings" , 1                               )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (                                          )
  def nameChanged                 ( self                                   ) :
    ##########################################################################
    global SystemUUIDs
    ##########################################################################
    if                            ( not self . isItemPicked ( )            ) :
      return False
    ##########################################################################
    item   = self . CurrentItem   [ "Item"                                   ]
    column = self . CurrentItem   [ "Column"                                 ]
    line   = self . CurrentItem   [ "Widget"                                 ]
    text   = self . CurrentItem   [ "Text"                                   ]
    msg    = line . text          (                                          )
    uuid   = self . itemUuid      ( item , 0                                 )
    ##########################################################################
    if                            ( len ( msg ) <= 0                       ) :
      ########################################################################
      if                          ( uuid <= 0                              ) :
        self . removeTopLevelItem ( item                                     )
        return
    ##########################################################################
    uuid   = int                  ( msg                                      )
    item   . setText              ( column ,                 msg             )
    item   . setData              ( column , Qt . UserRole , uuid            )
    ##########################################################################
    self   . removeParked         (                                          )
    ##########################################################################
    SystemUUIDs . append          ( uuid                                     )
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    global SystemUUIDs
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    ##########################################################################
    MSG    = self . getMenuItem    ( "Clear"                                 )
    mm     . addAction             ( 1201 , MSG                              )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      MSG  = self . getMenuItem    ( "Delete"                                )
      mm   . addAction             ( 1202 , MSG                              )
    ##########################################################################
    mm     . addSeparator          (                                         )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1201                            ) :
      ########################################################################
      SystemUUIDs =                [                                         ]
      ########################################################################
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1202                            ) :
      ########################################################################
      uxid        = atItem . text  ( 0                                       )
      uuid        = int            ( uxid                                    )
      ########################################################################
      SystemUUIDs . remove         ( uuid                                    )
      ########################################################################
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

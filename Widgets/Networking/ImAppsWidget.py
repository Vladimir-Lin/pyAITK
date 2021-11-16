# -*- coding: utf-8 -*-
##############################################################################
## ImAppsWidget
## 即時通種類
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
from   PyQt5 . QtCore                 import QUrl
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDesktopServices
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
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class ImAppsWidget                 ( TreeDock                              ) :
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
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    self . MountClicked            ( 9                                       )
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
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 280 , 400                               )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Insert"     , self . InsertItem        )
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                     ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    self . Notify             ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 2 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                column                                     , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def stateChanged                  ( self , item , column                 ) :
    ##########################################################################
    if                              ( column not in [ 0 ]                  ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    Uuid   = self . itemUuid        ( item , 0                               )
    CHK    = item . checkState      ( 0                                      )
    FOUND  =                        ( CHK == Qt . Checked                    )
    USED   = 1
    if                              ( not FOUND                            ) :
      USED = 0
    ##########################################################################
    IMATAB = self . Tables          [ "Main"                                 ]
    QQ     = f"""update {IMATAB}
                 set `used` = {USED}
                 where ( `uuid` = {Uuid} ) ;"""
    QQ     = " " . join             ( QQ . split ( )                         )
    DB     . Query                  ( QQ                                     )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , JSON                             ) :
    ##########################################################################
    Id     = int                 ( JSON [ 0 ]                                )
    Uuid   = str                 ( JSON [ 1 ]                                )
    Used   = int                 ( JSON [ 2 ]                                )
    Name   = str                 ( JSON [ 3 ]                                )
    ##########################################################################
    PICK   = Qt . Checked
    if                           ( Used == 0                               ) :
      PICK = Qt . Unchecked
    ##########################################################################
    IT     = QTreeWidgetItem     (                                           )
    IT     . setCheckState       ( 0 , PICK                                  )
    IT     . setData             ( 0 , Qt . UserRole , Uuid                  )
    ##########################################################################
    IT     . setText             ( 1 , str ( Id )                            )
    IT     . setTextAlignment    ( 1 , Qt.AlignRight                         )
    ##########################################################################
    IT     . setText             ( 2 , Name                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                        (        list                             )
  def refresh                      ( self , LISTS                          ) :
    ##########################################################################
    self    . clear                (                                         )
    ##########################################################################
    for L in LISTS                                                           :
      ########################################################################
      IT    = self . PrepareItem   ( L                                       )
      self  . addTopLevelItem      ( IT                                      )
    ##########################################################################
    self    . emitNamesShow . emit (                                         )
    ##########################################################################
    return
  ############################################################################
  def loading                      ( self                                  ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      self  . emitNamesShow . emit (                                         )
      return
    ##########################################################################
    IMATAB  = self . Tables        [ "Main"                                  ]
    QQ      = f"""select `id`,`uuid`,`used`,`english` from {IMATAB}
                  order by `id` asc ;"""
    QQ      = " " . join           ( QQ . split ( )                          )
    DB      . Query                ( QQ                                      )
    LISTS   = DB . FetchAll        (                                         )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( LISTS in [ False , None ] ) or ( len ( LISTS ) <= 0 ) )           :
      self  . emitNamesShow . emit (                                         )
      return
    ##########################################################################
    self    . emitAllNames  . emit ( LISTS                                   )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 0 ,  3                                    )
    self   . setColumnWidth      ( 1 , 60                                    )
    ##########################################################################
    LABELs = self . Translations [ "ImAppsWidget" ] [ "Labels"               ]
    self   . setCentralLabels    ( LABELs                                    )
    ##########################################################################
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                         (                                        )
  def InsertItem                    ( self                                 ) :
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    IMATAB = self . Tables          [ "Main"                                 ]
    Uuid   = DB   . LastUuid        ( IMATAB , "uuid" , 2300000000000000000  )
    Id     = int                    ( int ( Uuid ) % 1000000                 )
    QQ     = f"""insert into {IMATAB}
                 ( `id` , `uuid` , `used` )
                 values
                 ( {Id} , {Uuid} , 0 ) ;"""
    QQ     = " " . join             ( QQ . split ( )                         )
    DB     . Query                  ( QQ                                     )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . startup                (                                        )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def RenameItem                 ( self                                    ) :
    ##########################################################################
    IT = self . currentItem      (                                           )
    if                           ( IT is None                              ) :
      return
    ##########################################################################
    self . doubleClicked         ( IT , 2                                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def nameChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    line   = self . CurrentItem  [ "Widget"                                  ]
    text   = self . CurrentItem  [ "Text"                                    ]
    msg    = line . text         (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem              ( self , item , Uuid , name              ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    IMATAB = self . Tables        [ "Main"                                   ]
    Uuid   = int                  ( Uuid                                     )
    ##########################################################################
    DB     . LockWrites           ( [ IMATAB                               ] )
    ##########################################################################
    QQ     = f"""update {IMATAB}
                 set `english` = %s
                 where ( `uuid` = {Uuid} ) ;"""
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . QueryValues          ( QQ , ( name , )                          )
    ##########################################################################
    DB     . Close                (                                          )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( 2                                        )
    LID  = self . getLocality     (                                          )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    self . TtsTalk                ( MSG , LID                                )
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items  = self . selectedItems  (                                         )
    atItem = self . currentItem    (                                         )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1002                          )
    if                             ( atItem not in [ False , None ]        ) :
      MSG  = TRX                   [ "UI::Rename"                            ]
      mm   . addAction             ( 1003 ,  MSG                             )
    ##########################################################################
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1003                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    return True
##############################################################################

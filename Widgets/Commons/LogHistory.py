# -*- coding: utf-8 -*-
##############################################################################
## LogHistory
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
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Documents  . Notes     import Notes
##############################################################################
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Events    import Events      as Events
from   AITK  . Scheduler  . Event     import Event       as Event
##############################################################################
class LogHistory                   ( TreeDock                              ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitNamesShow  = pyqtSignal      (                                         )
  emitAllNames   = pyqtSignal      ( list                                    )
  OpenSmartNote  = pyqtSignal      ( str , str , str , int                   )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "LogHistory"
    self . Uuid               = 0
    self . Key                = ""
    self . SortOrder          = "desc"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 3 , True                                )
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
    return self . SizeSuggestion ( QSize ( 480 , 320 )                       )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . startup                   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem                )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    ##########################################################################
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    ##########################################################################
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setOwner                   ( self , UUID , KEY                       ) :
    ##########################################################################
    self . Uuid = UUID
    self . Key  = KEY
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent         ( self , IT , JSON                        ) :
    ##########################################################################
    TRX = self . Translations    [ self . ClassTag                           ]
    TZ  = self . Settings        [ "TimeZone"                                ]
    ##########################################################################
    NOW = StarDate               (                                           )
    ID  = int                    ( JSON [ "Prefer"                         ] )
    ID  = int                    ( ID                                        )
    LEN = int                    ( JSON [ "Length"                         ] )
    LEN = int                    ( LEN                                       )
    ##########################################################################
    NOW . Stardate = int         ( JSON [ "Lastest"                        ] )
    DT  = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"        )
    ##########################################################################
    IT  . setText                ( 0 , str ( ID )                            )
    IT  . setToolTip             ( 0 , str ( ID )                            )
    IT  . setData                ( 0 , Qt . UserRole , ID                    )
    IT  . setTextAlignment       ( 0 , Qt.AlignRight                         )
    ##########################################################################
    IT  . setText                ( 1 , str ( LEN )                           )
    IT  . setTextAlignment       ( 1 , Qt.AlignRight                         )
    ##########################################################################
    IT  . setText                ( 2 , DT                                    )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , JSON                                ) :
    ##########################################################################
    IT   = QTreeWidgetItem    (                                              )
    self . PrepareItemContent ( IT   , JSON                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot      (                                                           )
  def InsertItem ( self                                                    ) :
    ##########################################################################
    self . Go    ( self . AppendPrefer                                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot    (                                                             )
  def CopyNote ( self , Prefer                                             ) :
    ##########################################################################
    self . Go  ( self . AppendAndCopyPrefer , ( Prefer , )                   )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveNotes                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , NOTEs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for N in NOTEs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( N                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB in [ False , None ]             ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    NOW     = StarDate                (                                      )
    NOXTAB  = self . Tables           [ "Notes"                              ]
    KEY     = self . Key
    UUID    = self . Uuid
    ORDER   = self . SortOrder
    ITEMs   =                         [                                      ]
    ##########################################################################
    QQ      = f"""select `prefer`,length(`note`),`ltime` from {NOXTAB}
                  where ( `uuid` = '{UUID}' )
                    and ( `name` = '{KEY}' )
                  order by `prefer` {ORDER} ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    ##########################################################################
    ALL     = DB . FetchAll           (                                      )
    if ( ( ALL not in [ False , None ] ) and ( len ( ALL ) > 0 ) )           :
      ########################################################################
      for ITEM in ALL                                                        :
        ######################################################################
        PREFER = int                  ( ITEM [ 0 ]                           )
        LENGTH = int                  ( ITEM [ 1 ]                           )
        NOW . fromDateTime            ( ITEM [ 2 ]                           )
        ######################################################################
        J   =                         { "Prefer"  : PREFER                 , \
                                        "Length"  : LENGTH                 , \
                                        "Lastest" : NOW . Stardate           }
        ITEMs . append                ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( ITEMs ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . emitAllNames  . emit    ( ITEMs                                )
    ##########################################################################
    return
  ############################################################################
  def AppendPrefer            ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . appendNote       ( DB , NOXTAB                                  )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def AppendAndCopyPrefer     ( self , AT                                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    ##########################################################################
    NOX    . Obtains          ( DB , NOXTAB , AT                             )
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . appendNote       ( DB , NOXTAB                                  )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self    . setVacancy      (                                              )
    self    . GoRelax . emit  (                                              )
    DB      . Close           (                                              )
    ##########################################################################
    self    . loading         (                                              )
    ##########################################################################
    return
  ############################################################################
  def RemoveNotes             ( self , IDs                                 ) :
    ##########################################################################
    if                        ( len ( IDs ) <= 0                           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    IDZs   =                  [                                              ]
    ##########################################################################
    for ID in IDs                                                            :
      IDZs . append           ( str ( ID )                                   )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . RemovePrefers    ( DB , NOXTAB , IDZs                           )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def OrderingNumbers         ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    UUID          = self . Uuid
    KEY           = self . Key
    ##########################################################################
    IDs    = NOX . ObtainIDs  ( DB , NOXTAB , "prefer" , "asc"               )
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    ##########################################################################
    X      = 0
    for ID in IDs                                                            :
      ########################################################################
      QQ   = f"""update {NOXTAB}
                 set `prefer` = {X}
                 where ( `uuid` = {UUID} )
                   and ( `name` = '{KEY}' )
                   and ( `prefer` = {ID} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
      ########################################################################
      X    = X + 1
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 , 100                                          )
    self . setColumnWidth ( 1 , 100                                          )
    self . setColumnWidth ( 2 , 200                                          )
    self . defaultPrepare ( self . ClassTag , 3                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9003 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      msg  = self . getMenuItem    ( "Edit"                                  )
      icon = QIcon                 ( ":/images/coding.png"                   )
      mm   . addActionWithIcon     ( 2001 , icon , msg                       )
      mm   . addSeparator          (                                         )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      msg  = self . getMenuItem    ( "CopyNote"                              )
      icon = QIcon                 ( ":/images/plus.png"                     )
      mm   . addActionWithIcon     ( 1102 , icon , msg                       )
      ########################################################################
      self . AppendDeleteAction    ( mm , 1103                               )
    ##########################################################################
    msg    = self . getMenuItem    ( "OrderingNumbers"                       )
    mm     . addAction             ( 1104 , msg                              )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . CopyNote              ( uuid                                    )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1104                            ) :
      self . Go                    ( self . OrderingNumbers                  )
      return True
    ##########################################################################
    if                             ( at == 2001                            ) :
      ########################################################################
      TEXT = self . windowTitle    (                                         )
      UXID = str                   ( self . Uuid                             )
      KEY  = str                   ( self . Key                              )
      self . OpenSmartNote . emit  ( TEXT , UXID , KEY , int ( uuid )        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## TaskListings
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
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Events    import Events      as Events
from   AITK  . Scheduler  . Event     import Event       as Event
##############################################################################
class TaskListings                 ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  TaskEvents    = pyqtSignal       ( str , int , str                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "TaskListings"
    self . DefaultType        = 196833
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "desc"
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Task"                                  )
    self . Relation . setRelation  ( "Contains"                              )
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 7 , True                                )
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
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 640 )                      )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . restart                   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem                )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    self . LinkAction      ( "Rename"     , self . RenameItem                )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    self . LinkAction      ( "Home"       , self . PageHome                  )
    self . LinkAction      ( "End"        , self . PageEnd                   )
    self . LinkAction      ( "PageUp"     , self . PageUp                    )
    self . LinkAction      ( "PageDown"   , self . PageDown                  )
    ##########################################################################
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
    self . LinkAction      ( "Refresh"    , self . restart         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkVoice       ( None                                            )
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
    if                          ( column not in [ 1 , 5 ]                  ) :
      return
    ##########################################################################
    if                          ( column in [ 1 ]                          ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      return
    ##########################################################################
    if                          ( column in [ 5 ]                          ) :
      ########################################################################
      val  = item . data        ( column , Qt . UserRole                     )
      val  = int                ( val                                        )
      sb   = self . setSpinBox  ( item                                       ,
                                  column                                     ,
                                  0                                          ,
                                  1000000000                                 ,
                                  "editingFinished"                          ,
                                  self . spinChanged                         )
      sb   . setValue           ( val                                        )
      sb   . setAlignment       ( Qt . AlignRight                            )
      sb   . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent              ( self , IT , JSON                   ) :
    ##########################################################################
    TRX      = self . Translations    [ self . ClassTag                      ]
    TZ       = self . Settings        [ "TimeZone"                           ]
    NOW      = StarDate               (                                      )
    UUID     = int                    ( JSON [ "Uuid" ]                      )
    Id       = int                    ( UUID % 100000000                     )
    UXID     = str                    ( UUID                                 )
    Name     = self . assureString    ( JSON [ "Name" ]                      )
    TASK     = JSON                   [ "Task"                               ]
    STATES   = str                    ( TASK . Period . States               )
    SNAME    = TRX                    [ "PeriodStates" ] [ STATES            ]
    TYPE     = str                    ( TASK . Type                          )
    TOTAL    = len                    ( TASK . Events                        )
    ##########################################################################
    SDTIME   = ""
    SDSTAM   = "0"
    EDTIME   = ""
    EDSTAM   = "0"
    ##########################################################################
    if                                ( TASK . Period . isAllow ( )        ) :
      ########################################################################
      SDSTAM = TASK . Period . Start
      SDSTAM = f"{SDSTAM}"
      NOW    . Stardate = TASK . Period . Start
      SDTIME = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
      ########################################################################
      EDSTAM = TASK . Period . End
      EDSTAM = f"{EDSTAM}"
      NOW    . Stardate = TASK . Period . End
      EDTIME = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    ##########################################################################
    IT       . setText                ( 0 , str ( Id )                       )
    IT       . setToolTip             ( 0 , UXID                             )
    IT       . setData                ( 0 , Qt . UserRole , UXID             )
    IT       . setTextAlignment       ( 0 , Qt.AlignRight                    )
    ##########################################################################
    IT       . setText                ( 1 , Name                             )
    IT       . setText                ( 2 , SNAME                            )
    ##########################################################################
    IT       . setText                ( 3 , SDTIME                           )
    IT       . setData                ( 3 , Qt . UserRole , SDSTAM           )
    ##########################################################################
    IT       . setText                ( 4 , EDTIME                           )
    IT       . setData                ( 4 , Qt . UserRole , EDSTAM           )
    ##########################################################################
    IT       . setText                ( 5 , TYPE                             )
    IT       . setData                ( 5 , Qt . UserRole , TASK . Type      )
    IT       . setTextAlignment       ( 5 , Qt.AlignRight                    )
    ##########################################################################
    IT       . setText                ( 6 , str ( TOTAL )                    )
    IT       . setData                ( 6 , Qt . UserRole , TOTAL            )
    IT       . setTextAlignment       ( 6 , Qt.AlignRight                    )
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
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    item   = QTreeWidgetItem     (                                           )
    item   . setData             ( 0 , Qt . UserRole , 0                     )
    ##########################################################################
    if                           ( self . SortOrder == "asc"               ) :
      self . addTopLevelItem     ( item                                      )
    else                                                                     :
      self . insertTopLevelItem  ( 0 , item                                  )
    ##########################################################################
    line   = self . setLineEdit  ( item                                    , \
                                   1                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
    line   . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( self . RemoveTasks                           )
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
    self . doubleClicked         ( IT , 1                                    )
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
    if                           ( len ( msg ) <= 0                        ) :
      self . removeTopLevelItem  ( item                                      )
      return
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    return
  ############################################################################
  def spinChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    sb     = self . CurrentItem  [ "Widget"                                  ]
    v      = item . data         ( column , Qt . UserRole                    )
    v      = int                 ( v                                         )
    nv     = sb   . value        (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( ( v == nv ) or ( column not in [ 5 ] ) )  :
      item . setText             ( column , str ( v )                        )
      self . removeParked        (                                           )
      return
    ##########################################################################
    self . Go                    ( self . UpdateTypeItemValue              , \
                                   ( uuid , "type" , nv , )                  )
    ##########################################################################
    item . setText               ( column , str ( nv )                       )
    item . setData               ( column , Qt . UserRole , nv               )
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , TASKS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in TASKS                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids           ( self , DB                            ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables          [ "Relation"                             ]
    ##########################################################################
    if                              ( self . isSubordination ( )           ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    if                              ( self . isReverse       ( )           ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                          [                                        ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return   self . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      TABLE = self . Tables   [ "Names"                                      ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
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
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    TASKS   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      TASK  = Task                    (                                      )
      TASK  . Tables       = self . Tables
      TASK  . Translations = self . Translations
      TASK  . Uuid = U
      TASK  . load                    ( DB                                   )
      ########################################################################
      J     =                         { "Uuid" : U                         , \
                                        "Name" : ""                        , \
                                        "Task" : TASK                        }
      if                              ( U in NAMEs                         ) :
        J [ "Name" ] = NAMEs          [ U                                    ]
      ########################################################################
      TASKS . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( TASKS ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames  . emit     ( TASKS                                )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids                ( self , DB                            ) :
    ##########################################################################
    TABLE  = self . Tables          [ "Tasks"                                ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` > 0 )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    QQ     = " " . join             ( QQ . split ( )                         )
    ##########################################################################
    return DB . ObtainUuids         ( QQ , 0                                 )
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    TABLE = self . Tables       [ "Names"                                    ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self  . Total = 0
    ##########################################################################
    TABLE = self . Tables [ "Tasks"                                          ]
    ##########################################################################
    QQ    = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
    DB    . Query         ( QQ                                               )
    RR    = DB . FetchOne (                                                  )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) not in [ 1 ] )           :
      return
    ##########################################################################
    self  . Total = int   ( RR [ 0 ]                                         )
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "Tasks"                                     ]
    QQ     = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
    DB     . Query             ( QQ                                          )
    ONE    = DB . FetchOne     (                                             )
    ##########################################################################
    if                         ( ONE == None                               ) :
      return 0
    ##########################################################################
    if                         ( len ( ONE ) <= 0                          ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
  ############################################################################
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TSKTAB = self . Tables          [ "Tasks"                                ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TSKTAB}
                 where ( `used` > 0 )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def FetchSessionInformation ( self , DB                                  ) :
    ##########################################################################
    if                        ( self . isOriginal      ( )                 ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                        ( self . isReverse       ( )                 ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def dragMime                      ( self                                 ) :
    ##########################################################################
    mtype   = "task/uuids"
    message = self . getMenuItem    ( "TasksSelected"                        )
    ##########################################################################
    return self    . CreateDragMime ( self , 0 , mtype , message             )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    FMTs    =              [ "people/uuids"                                , \
                             "project/uuids"                               , \
                             "task/uuids"                                  , \
                             "event/uuids"                                   ]
    formats = ";" . join   ( FMTs                                            )
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def acceptPeopleDrop   ( self                                            ) :
    return True
  ############################################################################
  def acceptProjectsDrop ( self                                            ) :
    return True
  ############################################################################
  def acceptTasksDrop    ( self                                            ) :
    return True
  ############################################################################
  def acceptEventsDrop   ( self                                            ) :
    return True
  ############################################################################
  def dropNew                           ( self                             , \
                                          sourceWidget                     , \
                                          mimeData                         , \
                                          mousePos                         ) :
    ##########################################################################
    if                                  ( self == sourceWidget             ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew      ( mimeData                           )
    if                                  ( not RDN                          ) :
      return False
    ##########################################################################
    mtype  = self . DropInJSON          [ "Mime"                             ]
    UUIDs  = self . DropInJSON          [ "UUIDs"                            ]
    title  = sourceWidget . windowTitle (                                    )
    CNT    = len                        ( UUIDs                              )
    atItem = self . itemAt              ( mousePos                           )
    ##########################################################################
    if                                  ( mtype in [ "people/uuids"      ] ) :
      ########################################################################
      if                                ( atItem in [ False , None ]       ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus    ( "PeopleJoinTask"   , title , CNT   )
    ##########################################################################
    elif                                ( mtype in [ "project/uuids"     ] ) :
      ########################################################################
      if                                ( atItem in [ False , None ]       ) :
        return False
      ########################################################################
      title = atItem . text             ( 1                                  )
      self . ShowMenuItemTitleStatus    ( "TaskJoinProjects" , title , CNT   )
    ##########################################################################
    elif                                ( mtype in [ "task/uuids"        ] ) :
      self . ShowMenuItemTitleStatus    ( "JoinTasks"        , title , CNT   )
    ##########################################################################
    elif                                ( mtype in [ "event/uuids"       ] ) :
      ########################################################################
      if                                ( atItem in [ False , None ]       ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus    ( "JoinEvents"       , title , CNT   )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget == self                      ) :
      return False
    ##########################################################################
    mtype  = self . DropInJSON [ "Mime"                                      ]
    atItem = self . itemAt     ( mousePos                                    )
    ##########################################################################
    if                         ( mtype in [ "task/uuids"                 ] ) :
      return True
    ##########################################################################
    if                         ( atItem in [ False , None ]                ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def dropPeople                       ( self , source , pos , JSON        ) :
    ##########################################################################
    FUNC = self . PeopleJoinTask
    ##########################################################################
    return self . defaultDropInObjects ( source , pos , JSON , 0 , FUNC      )
  ############################################################################
  def dropProjects             ( self , source , pos , JSOX                ) :
    ##########################################################################
    FUNC = self . TaskJoinProjects
    ##########################################################################
    return self . defaultDropInObjects ( source , pos , JSON , 0 , FUNC      )
  ############################################################################
  def dropTasks                     ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . JoinTasks
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def dropEvents                       ( self , source , pos , JSON        ) :
    ##########################################################################
    FUNC = self . EventsJoinTask
    ##########################################################################
    return self . defaultDropInObjects ( source , pos , JSON , 0 , FUNC      )
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 ,  80                                          )
    self . setColumnWidth ( 1 , 280                                          )
    self . setColumnWidth ( 3 , 180                                          )
    self . setColumnWidth ( 4 , 180                                          )
    self . defaultPrepare ( self . ClassTag , 7                              )
    ##########################################################################
    return
  ############################################################################
  def PeopleJoinTask              ( self , UUID , UUIDs                    ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def TaskJoinProjects            ( self , UUID , UUIDs                    ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def JoinTasks                   ( self , UUIDs                           ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def EventsJoinTask              ( self , UUID , UUIDs                    ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem              ( self , item , uuid , name              ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    NEWONE   = False
    JSON     =                    {                                          }
    TSKTAB   = self . Tables      [ "Tasks"                                  ]
    PRDTAB   = self . Tables      [ "Periods"                                ]
    RELTAB   = self . Tables      [ "RelationGroups"                         ]
    NAMTAB   = self . Tables      [ "NamesLocal"                             ]
    ##########################################################################
    DB       . LockWrites         ( [ TSKTAB , PRDTAB , RELTAB , NAMTAB ]    )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      ########################################################################
      TASKS  = Tasks              (                                          )
      TASKS  . Tables      = self . Tables
      TASKS  . DefaultType = self . DefaultType
      uuid   = TASKS . AppendTask ( DB                                       )
      ########################################################################
      NEWONE = True
      TASK   = Task               (                                          )
      TASK   . Tables       = self . Tables
      TASK   . Translations = self . Translations
      TASK   . Uuid = uuid
      TASK   . load               ( DB                                       )
      ########################################################################
      JSON   =                    { "Uuid" : uuid                          , \
                                    "Name" : name                          , \
                                    "Task" : TASK                            }
      ########################################################################
      if                          ( self . isSubordination ( )             ) :
        ######################################################################
        self . Relation . set     ( "second" , uuid                          )
        self . Relation . Join    ( DB , RELTAB                              )
        ######################################################################
      elif                        ( self . isReverse ( )                   ) :
        ######################################################################
        self . Relation . set     ( "first" , uuid                           )
        self . Relation . Join    ( DB , RELTAB                              )
    ##########################################################################
    self     . AssureUuidName     ( DB , NAMTAB , uuid , name                )
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    item     . setData            ( 0 , Qt . UserRole , uuid                 )
    ##########################################################################
    if                            ( NEWONE                                 ) :
      ########################################################################
      self   . PrepareItemContent ( item , JSON                              )
      self   . emitAssignColumn . emit ( item , 1 , name                     )
    ##########################################################################
    ## 發送訊息給計畫管理後台
    ## SendWssBack
    ##########################################################################
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemValue     ( self , uuid , item , value                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    TSKTAB = self . Tables    [ "Tasks"                                      ]
    ##########################################################################
    DB     . LockWrites       ( [ TSKTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"""update {TSKTAB}
                 set `{item}` = {value}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    ## 發送訊息給計畫管理後台
    ## SendWssBack
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def RemoveTasks               ( self , UUIDs                             ) :
    ##########################################################################
    if                          ( not self . isGrouping ( )                ) :
      return
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( DB in [ False , None ]                   ) :
      return
    ##########################################################################
    RELTAB   = self . Tables    [ "Relation"                                 ]
    ##########################################################################
    DB       . LockWrites       ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "second" , UUID                            )
        QQ   = self . Relation . Delete ( RELTAB                             )
        DB   . Query            ( QQ                                         )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        QQ   = self . Relation . Delete ( RELTAB                             )
        DB   . Query            ( QQ                                         )
    ##########################################################################
    DB       . Close            (                                            )
    ##########################################################################
    ## 發送訊息給計畫管理後台
    ## SendWssBack
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def RecalculatePeriods          ( self , uuid                            ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    TASK   = Task                 (                                          )
    TASK   . Tables = self . Tables
    TASK   . Uuid   = uuid
    TASK   . load                 ( DB                                       )
    ##########################################################################
    EVENTs = Events               (                                          )
    EVENTs . Tables = self . Tables
    EVENTs . load                 ( DB , TASK . Events                       )
    ##########################################################################
    PRDTAB = self . Tables        [ "Periods"                                ]
    TSKTAB = self . Tables        [ "Tasks"                                  ]
    DB     . LockWrites           ( [ PRDTAB , TSKTAB                      ] )
    TASK   . Investigate          ( DB , EVENTs                              )
    DB     . UnlockTables         (                                          )
    ##########################################################################
    DB     . Close                (                                          )
    ##########################################################################
    self   . Notify               ( 5                                        )
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
    return self . DefaultColumnsMenu (        mm , 2                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9002 ) and ( at <= 9007 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu              ( self , mm , item                           ) :
    ##########################################################################
    msg  = self . getMenuItem ( "Details"                                    )
    LOM  = mm . addMenu       ( msg                                          )
    ##########################################################################
    msg  = self . getMenuItem ( "Events"                                     )
    mm   . addActionFromMenu  ( LOM , 1501 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Recalculate"                                )
    mm   . addActionFromMenu  ( LOM , 1502 , msg                             )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu            ( self , at , item                          ) :
    ##########################################################################
    if                         ( at == 1501                                ) :
      ########################################################################
      uuid = self . itemUuid   ( item , 0                                    )
      name = atItem . text     ( 1                                           )
      self . TaskEvents . emit ( name , 16 , str ( uuid )                    )
      ########################################################################
      return True
    ##########################################################################
    if                         ( at == 1502                                ) :
      ########################################################################
      uuid = self . itemUuid   ( item , 0                                    )
      self . Go                ( self . RecalculatePeriods , ( uuid , )      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    if                              ( self . isSearching ( )               ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Original"                             )
      mm   . addAction              ( 1002 , msg                             )
    ##########################################################################
    self   . AppendInsertAction     ( mm , 1101                              )
    if                              ( len ( items ) > 0                    ) :
      self . AppendDeleteAction     ( mm , 1102                              )
    if                              ( atItem not in [ False , None ]       ) :
      self . AppendRenameAction     ( mm , 1103                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      if                            ( self . doEditAllNames ( )            ) :
        self . AppendEditNamesAction ( mm , 1601                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      self . GroupsMenu             ( mm , atItem                            )
    ##########################################################################
    self   . ColumnsMenu            ( mm                                     )
    self   . SortingMenu            ( mm                                     )
    self   . LocalityMenu           ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunAmountIndexMenu ( )        ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( self . RunDocking    ( mm , aa )     ) :
      return True
    ##########################################################################
    if                              ( self . RunGroupsMenu ( at , atItem ) ) :
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      self . Grouping = self . OldGrouping
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      self . DeleteItems            (                                        )
      return True
    ##########################################################################
    if                              ( at == 1103                           ) :
      self . RenameItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( atItem , 0                             )
      NAM  = self . Tables          [ "NamesLocal"                           ]
      self . EditAllNames           ( self , "Tasks" , uuid , NAM            )
      return True
    ##########################################################################
    return True
##############################################################################

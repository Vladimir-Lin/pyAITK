# -*- coding: utf-8 -*-
##############################################################################
## PeriodeListings
## 時段列表
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
##############################################################################
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Events    import Events      as Events
from   AITK  . Scheduler  . Event     import Event       as Event
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
from   AITK  . Scheduler  . Task      import Task        as Task
##############################################################################
class PeriodeListings              ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  PeriodDetails = pyqtSignal       ( str , str                               )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "PeriodeListings"
    self . DefaultType        = 196833
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "desc"
    self . Editable           = True
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
    self . Relation . setT2        ( "Period"                                )
    self . Relation . setRelation  ( "Contains"                              )
    ##########################################################################
    self . setColumnCount          ( 13                                      )
    self . setColumnHidden         ( 10 , True                               )
    self . setColumnHidden         ( 11 , True                               )
    self . setColumnHidden         ( 12 , True                               )
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
  def sizeHint                     ( self                                  ) :
    return self . SizeSuggestion   ( QSize ( 1024 , 640 )                    )
  ############################################################################
  def setEditable                  ( self , edit                           ) :
    ##########################################################################
    self . Editable = edit
    ##########################################################################
    return
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
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( not self . Editable                        ) :
      return
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    self     . Notify         ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( not self . Editable                      ) :
      return
    ##########################################################################
    if                          ( column not in [ 1 ]                      ) :
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
    return
  ############################################################################
  def PrepareItemContent           ( self , IT , JSON                      ) :
    ##########################################################################
    TZ       = "Asia/Taipei"
    TRX      = self . Translations [ self . ClassTag                         ]
    NOW      = StarDate            (                                         )
    ##########################################################################
    UUID     = int                 ( JSON [ "Uuid" ]                         )
    Id       = int                 ( UUID % 100000000                        )
    UXID     = str                 ( UUID                                    )
    Name     = JSON                [ "Name"                                  ]
    TYPE     = JSON                [ "Type"                                  ]
    USED     = JSON                [ "Used"                                  ]
    START    = JSON                [ "Start"                                 ]
    ENDT     = JSON                [ "End"                                   ]
    REALM    = JSON                [ "Realm"                                 ]
    RNAME    = JSON                [ "RName"                                 ]
    ROLE     = JSON                [ "Role"                                  ]
    TNAME    = JSON                [ "TName"                                 ]
    ITEM     = JSON                [ "Item"                                  ]
    STATES   = JSON                [ "States"                                ]
    CREATION = JSON                [ "Creation"                              ]
    MODIFIED = JSON                [ "Modified"                              ]
    ##########################################################################
    IT       . setText             (  0 , str ( Id )                         )
    IT       . setToolTip          (  0 , UXID                               )
    IT       . setData             (  0 , Qt . UserRole , UXID               )
    IT       . setTextAlignment    (  0 , Qt . AlignRight                    )
    ##########################################################################
    IT       . setText             (  1 , Name                               )
    ##########################################################################
    DTS      = ""
    if                             ( START    > 0                          ) :
      NOW    . Stardate = START
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             (  2 , DTS                                )
    ##########################################################################
    DTS      = ""
    if                             ( ENDT     > 0                          ) :
      NOW    . Stardate = ENDT
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             (  3 , DTS                                )
    ##########################################################################
    IT       . setText             (  4 , TRX [ "Type" ] [ str ( TYPE  ) ]   )
    ##########################################################################
    IT       . setText             (  5 , TRX [ "Used" ] [ str ( USED  ) ]   )
    ##########################################################################
    IT       . setText             (  6 , str ( RNAME )                      )
    IT       . setToolTip          (  6 , str ( REALM )                      )
    ##########################################################################
    IT       . setText             (  7 , str ( TNAME )                      )
    IT       . setToolTip          (  7 , str ( ROLE  )                      )
    ##########################################################################
    IT       . setText             (  8 , str ( ITEM  )                      )
    IT       . setTextAlignment    (  8 , Qt . AlignRight                    )
    ##########################################################################
    TRXS     = TRX                 [ "States"                                ]
    IT       . setText             (  9 , TRXS [ str ( STATES ) ]            )
    ##########################################################################
    DTS      = ""
    if                             ( CREATION > 0                          ) :
      NOW    . Stardate = CREATION
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 10 , DTS                                )
    ##########################################################################
    DTS      = ""
    if                             ( MODIFIED > 0                          ) :
      NOW    . Stardate = MODIFIED
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 11 , DTS                                )
    ##########################################################################
    IT       . setData             ( 12 , Qt . UserRole , JSON               )
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
    item = QTreeWidgetItem       (                                           )
    item . setData               ( 0 , Qt . UserRole , 0                     )
    ##########################################################################
    if                           ( self . SortOrder == "asc"               ) :
      self . addTopLevelItem     ( item                                      )
    else                                                                     :
      self . insertTopLevelItem  ( 0 , item                                  )
    ##########################################################################
    line = self . setLineEdit    ( item                                    , \
                                   1                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
    line . setFocus              ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemovePeriods                     )
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
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , PERIODs                         ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for P in PERIODs                                                         :
      ########################################################################
      IT   = self . PrepareItem   ( P                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder ( )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables [ "Relation" ]
    ##########################################################################
    if                         ( self . isSubordination ( )                ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    if                         ( self . isReverse       ( )                ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "NamesLocal"                         ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainPeriodDetail             ( self , DB , NAMEs , U               ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "NamesLocal"                          ]
    GNATAB = self . Tables           [ "NamesPrivate"                        ]
    PRDTAB = self . Tables           [ "Periods"                             ]
    TYPTAB = self . Tables           [ "Types"                               ]
    ##########################################################################
    J      =                         { "Uuid"     : U                      , \
                                       "Name"     : ""                     , \
                                       "Type"     : 0                      , \
                                       "TName"    : ""                     , \
                                       "Used"     : 0                      , \
                                       "Start"    : 0                      , \
                                       "End"      : 0                      , \
                                       "Realm"    : 0                      , \
                                       "RName"    : ""                     , \
                                       "Role"     : 0                      , \
                                       "Item"     : 0                      , \
                                       "States"   : 0                      , \
                                       "Creation" : 0                      , \
                                       "Modified" : 0                        }
    ##########################################################################
    if                               ( U in NAMEs                          ) :
      J [ "Name" ] = self . assureString ( NAMEs [ U ]                       )
    ##########################################################################
    QQ     = f"""select
                 `type`,`used`,
                 `start`,`end`,
                 `realm`,`role`,
                 `item`,`states`,
                 `creation`,`modified`
                 from {PRDTAB}
                 where ( `uuid` = {U} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    RR     = DB . FetchOne           (                                       )
    ##########################################################################
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 10 ) )           :
      ########################################################################
      J [ "Type"     ] = int         ( RR [ 0 ]                              )
      J [ "Used"     ] = int         ( RR [ 1 ]                              )
      J [ "Start"    ] = int         ( RR [ 2 ]                              )
      J [ "End"      ] = int         ( RR [ 3 ]                              )
      J [ "Realm"    ] = int         ( RR [ 4 ]                              )
      J [ "Role"     ] = int         ( RR [ 5 ]                              )
      J [ "Item"     ] = int         ( RR [ 6 ]                              )
      J [ "States"   ] = int         ( RR [ 7 ]                              )
      J [ "Creation" ] = int         ( RR [ 8 ]                              )
      J [ "Modified" ] = int         ( RR [ 9 ]                              )
      ########################################################################
      RU   = J                       [ "Realm"                               ]
      if                             ( RU > 0                              ) :
        N  = self . GetName          ( DB , GNATAB , RU                      )
        J [ "RName" ] = N
      ########################################################################
      TU   = J                       [ "Role"                                ]
      TU   = 1100000000000000000 + TU
      if                             ( TU > 0                              ) :
        ######################################################################
        QQ = f"select `name` from {TYPTAB} where ( `uuid` = {TU} ) ;"
        DB . Query                   ( QQ                                    )
        RR = DB . FetchOne           (                                       )
        N  = str                     ( J [ "Role" ]                          )
        if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )        :
          N   = self . assureString  ( RR [ 0 ]                              )
        ## N = self . GetName          ( DB , GNATAB , TU                     )
        ####################################################################
        J [ "TName" ] = N
    ##########################################################################
    return J
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
    self    . FetchSessionInformation ( DB                                   )
    ##########################################################################
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    PERIODS =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J = self . ObtainPeriodDetail   ( DB , NAMEs , U                       )
      PERIODS . append                ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( PERIODS ) <= 0               ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . emitAllNames  . emit    ( PERIODS                              )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids                ( self , DB                            ) :
    ##########################################################################
    PRDTAB = self . Tables          [ "Periods"                              ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {PRDTAB}
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
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "Periods"                                   ]
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
    PRDTAB = self . Tables          [ "Periods"                              ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {PRDTAB}
                 where ( `used` > 0 )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def dragMime                      ( self                                 ) :
    ##########################################################################
    mtype   = "period/uuids"
    message = self . getMenuItem    ( "PeriodsSelected"                      )
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
                             "event/uuids"                                 , \
                             "period/uuids"                                  ]
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
  def acceptEventsDrop   ( self                                            ) :
    return True
  ############################################################################
  def acceptPeriodsDrop  ( self                                            ) :
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
      self . ShowMenuItemTitleStatus    ( "PeopleJoinPeriod" , title , CNT   )
    ##########################################################################
    elif                                ( mtype in [ "event/uuids"       ] ) :
      self . ShowMenuItemTitleStatus    ( "PeriodJoinEvents" , title , CNT   )
    ##########################################################################
    elif                                ( mtype in [ "period/uuids"      ] ) :
      ########################################################################
      if                                ( atItem in [ False , None ]       ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus    ( "JoinPeriods"      , title , CNT   )
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
    if                         ( mtype in [ "period/uuids"               ] ) :
      return True
    ##########################################################################
    if                         ( atItem in [ False , None ]                ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def dropPeople                       ( self , source , pos , JSON        ) :
    ##########################################################################
    FUNC = self . PeopleJoinPeriod
    ##########################################################################
    return self . defaultDropInObjects ( source , pos , JSON , 0 , FUNC      )
  ############################################################################
  def dropEvents                    ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . PeriodJoinEvents
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def dropPeriods                      ( self , source , pos , JSON        ) :
    ##########################################################################
    FUNC = self . JoinPeriods
    ##########################################################################
    return self . defaultDropInObjects ( source , pos , JSON , 0 , FUNC      )
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth (  0 , 120                                         )
    self . setColumnWidth (  1 , 280                                         )
    self . setColumnWidth (  2 , 180                                         )
    self . setColumnWidth (  3 , 180                                         )
    self . defaultPrepare ( self . ClassTag , 12                             )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def PeopleJoinPeriod            ( self , UUID , UUIDs                    ) :
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
  def PeriodJoinEvents        ( self , UUID , UUIDs                        ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    RELTAB = self . Tables    [ "RelationGroups"                             ]
    ##########################################################################
    DB     . LockWrites       ( [ RELTAB                                   ] )
    ##########################################################################
    for EUID in UUIDs                                                        :
      ########################################################################
      EVT  = Event            (                                              )
      EVT  . Uuid = TUID
      EVT  . JoinPeriods      ( DB , RELTAB , [ UUID ]                       )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def JoinPeriods               ( self , UUIDs                             ) :
    ##########################################################################
    RELTAB = self . Tables      [ "RelationGroups"                           ]
    OKAY   = self . JoinMembers ( RELTAB , UUIDs                             )
    if                          ( not OKAY                                 ) :
      return
    ##########################################################################
    self   . Notify             ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    DB       = self . ConnectDB    (                                         )
    if                             ( DB in [ False , None ]                ) :
      return
    ##########################################################################
    NEWONE   = False
    JSON     =                     {                                         }
    PRDTAB   = self . Tables       [ "Periods"                               ]
    RELTAB   = self . Tables       [ "RelationGroups"                        ]
    NAMTAB   = self . Tables       [ "NamesLocal"                            ]
    GNATAB   = self . Tables       [ "NamesPrivate"                          ]
    TYPTAB   = self . Tables       [ "Types"                                 ]
    TABLES   =                     [ PRDTAB , NAMTAB                         ]
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      TABLES . append              ( RELTAB                                  )
      TABLES . append              ( GNATAB                                  )
      TABLES . append              ( TYPTAB                                  )
    ##########################################################################
    DB       . LockWrites          ( TABLES                                  )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      EVTS   = Events              (                                         )
      EVTS   . Tables      = self . Tables
      EVTS   . DefaultType = self . DefaultType
      uuid   = EVTS . AppendPeriod ( DB                                      )
      ########################################################################
      NEWONE = True
      NAMEs  =                     { uuid : name                             }
      JSON   = self . ObtainPeriodDetail ( DB , NAMEs , uuid                 )
      ########################################################################
      if                           ( self . isSubordination ( )            ) :
        ######################################################################
        self . Relation . set      ( "second" , uuid                         )
        self . Relation . Join     ( DB , RELTAB                             )
        ######################################################################
      elif                         ( self . isReverse ( )                  ) :
        ######################################################################
        self . Relation . set      ( "first" , uuid                          )
        self . Relation . Join     ( DB , RELTAB                             )
    ##########################################################################
    self     . AssureUuidName      ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB       . UnlockTables        (                                         )
    DB       . Close               (                                         )
    ##########################################################################
    item     . setData             ( 0 , Qt . UserRole , uuid                )
    ##########################################################################
    if                            ( NEWONE                                 ) :
      ########################################################################
      self   . PrepareItemContent ( item , JSON                              )
      self   . emitAssignColumn . emit ( item , 1 , name                     )
    ##########################################################################
    ## 發送訊息給計畫管理後台
    ## SendWssBack
    ##########################################################################
    self     . Notify              ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def RemovePeriods             ( self , UUIDs                             ) :
    ##########################################################################
    OKAY = self . RemoveMembers (        UUIDs                               )
    if                          ( not OKAY                                 ) :
      return
    ##########################################################################
    ## 發送訊息給計畫管理後台
    ## SendWssBack
    ##########################################################################
    self . loading              (                                            )
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
    ##########################################################################
    return self . DefaultColumnsMenu (        mm , 4                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9004 ) and ( at <= 9012 )         :
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
    msg  = self . getMenuItem ( "Editor"                                     )
    mm   . addActionFromMenu  ( LOM , 1501 , msg                             )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu               ( self , at , item                       ) :
    ##########################################################################
    if                            ( at == 1501                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      name = item . text          ( 1                                        )
      self . PeriodDetails . emit ( name , str ( uuid )                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                           ( self , pos                          ) :
    ##########################################################################
    doMenu = self . isFunction       ( self . HavingMenu                     )
    if                               ( not doMenu                          ) :
      return False
    ##########################################################################
    self   . Notify                  ( 0                                     )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager             ( self                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu  ( mm                                    )
    ##########################################################################
    self   . AppendRefreshAction     ( mm , 1001                             )
    ##########################################################################
    if                               ( self . isSearching ( )              ) :
      ########################################################################
      msg  = self . getMenuItem      ( "Original"                            )
      mm   . addAction               ( 1002 , msg                            )
    ##########################################################################
    self   . AppendInsertAction      ( mm , 1101                             )
    if                               ( len ( items ) > 0                   ) :
      self . AppendDeleteAction      ( mm , 1102                             )
    if                               ( atItem not in [ False , None ]      ) :
      self . AppendRenameAction      ( mm , 1103                             )
    ##########################################################################
    if                               ( atItem not in [ False , None ]      ) :
      if                             ( self . doEditAllNames ( )           ) :
        self . AppendEditNamesAction ( mm , 1601                             )
    ##########################################################################
    mm     . addSeparator            (                                       )
    ##########################################################################
    if                               ( atItem not in [ False , None ]      ) :
      self . GroupsMenu              ( mm , atItem                           )
    ##########################################################################
    self   . ColumnsMenu             ( mm                                    )
    self   . SortingMenu             ( mm                                    )
    self   . LocalityMenu            ( mm                                    )
    self   . DockingMenu             ( mm                                    )
    ##########################################################################
    mm     . setFont                 ( self    . menuFont ( )                )
    aa     = mm . exec_              ( QCursor . pos      ( )                )
    at     = mm . at                 ( aa                                    )
    ##########################################################################
    if                               ( self   . RunAmountIndexMenu ( )     ) :
      ########################################################################
      self . restart                 (                                       )
      ########################################################################
      return
    ##########################################################################
    if                               ( self . RunDocking   ( mm , aa )     ) :
      return True
    ##########################################################################
    if                               ( self . RunGroupsMenu ( at,atItem )  ) :
      return True
    ##########################################################################
    if                               ( self . HandleLocalityMenu ( at )    ) :
      self . restart                 (                                       )
      return True
    ##########################################################################
    if                               ( self . RunColumnsMenu     ( at )    ) :
      return True
    ##########################################################################
    if                               ( self . RunSortingMenu     ( at )    ) :
      self . restart                 (                                       )
      return True
    ##########################################################################
    if                               ( at == 1001                          ) :
      self . restart                 (                                       )
      return True
    ##########################################################################
    if                               ( at == 1101                          ) :
      self . InsertItem              (                                       )
      return True
    ##########################################################################
    if                               ( at == 1102                          ) :
      self . DeleteItems             (                                       )
      return True
    ##########################################################################
    if                               ( at == 1103                          ) :
      self . RenameItem              (                                       )
      return True
    ##########################################################################
    if                               ( at == 1601                          ) :
      uuid = self . itemUuid         ( atItem , 0                            )
      NAM  = self . Tables           [ "NamesLocal"                          ]
      self . EditAllNames            ( self , "Periode" , uuid , NAM         )
      return True
    ##########################################################################
    return True
##############################################################################

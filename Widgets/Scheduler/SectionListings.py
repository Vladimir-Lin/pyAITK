# -*- coding: utf-8 -*-
##############################################################################
## SectionListings
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
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Event     import Event       as Event
from   AITK  . Scheduler  . Events    import Events      as Events
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
##############################################################################
class SectionListings              ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "desc"
    self . Editable           = True
    ##########################################################################
    self . Grouping           = "Original"
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
  def setGrouping                  ( self , group                          ) :
    self . Grouping = group
    return self . Grouping
  ############################################################################
  def getGrouping                  ( self                                  ) :
    return self . Grouping
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Insert"     , self . InsertItem        )
    self . LinkAction              ( "Delete"     , self . DeleteItems       )
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
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
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                  ( self , JSON                           ) :
    ##########################################################################
    TZ       = "Asia/Taipei"
    TRX      = self . Translations [ "PeriodeListings"                       ]
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
    IT       = QTreeWidgetItem     (                                         )
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
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    item = QTreeWidgetItem       (                                           )
    item . setData               ( 0 , Qt . UserRole , 0                     )
    self . addTopLevelItem       ( item                                      )
    line = self . setLineEdit    ( item                                    , \
                                   1                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
    line . setFocus              ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def DeleteItems                ( self                                    ) :
    ##########################################################################
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
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder ( )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables [ "Relation" ]
    ##########################################################################
    if                         ( self . Grouping == "Subordination"        ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                         ( self . Grouping == "Reverse"              ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids         ( self , DB                                 ) :
    ##########################################################################
    if                         ( self . Grouping == "Original"             ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
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
    NAMTAB  = self . Tables           [ "Names"                              ]
    PRDTAB  = self . Tables           [ "Periods"                            ]
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    PERIODS =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"     : U                     , \
                                        "Name"     : ""                    , \
                                        "Type"     : 0                     , \
                                        "TName"    : ""                    , \
                                        "Used"     : 0                     , \
                                        "Start"    : 0                     , \
                                        "End"      : 0                     , \
                                        "Realm"    : 0                     , \
                                        "RName"    : ""                    , \
                                        "Role"     : 0                     , \
                                        "Item"     : 0                     , \
                                        "States"   : 0                     , \
                                        "Creation" : 0                     , \
                                        "Modified" : 0                       }
      ########################################################################
      if                              ( U in NAMEs                         ) :
        J [ "Name" ] = self . assureString ( NAMEs [ U ]                     )
      ########################################################################
      QQ    = f"""select
                  `type`,`used`,`start`,`end`,
                  `realm`,`role`,
                  `item`,`states`,
                  `creation`,`modified`
                  from {PRDTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 10 ) )         :
        ######################################################################
        J [ "Type"     ] = int        ( RR [ 0 ]                             )
        J [ "Used"     ] = int        ( RR [ 1 ]                             )
        J [ "Start"    ] = int        ( RR [ 2 ]                             )
        J [ "End"      ] = int        ( RR [ 3 ]                             )
        J [ "Realm"    ] = int        ( RR [ 4 ]                             )
        J [ "Role"     ] = int        ( RR [ 5 ]                             )
        J [ "Item"     ] = int        ( RR [ 6 ]                             )
        J [ "States"   ] = int        ( RR [ 7 ]                             )
        J [ "Creation" ] = int        ( RR [ 8 ]                             )
        J [ "Modified" ] = int        ( RR [ 9 ]                             )
        ######################################################################
        RU  = J                       [ "Realm"                              ]
        if                            ( RU > 0                             ) :
          N = self . GetName          ( DB , NAMTAB , RU                     )
          J [ "RName" ] = N
        ######################################################################
        TU  = J                       [ "Role"                               ]
        TU  = 1100000000000000000 + TU
        if                            ( TU > 0                             ) :
          ####################################################################
          QQ    = f"select `name` from `types` where ( `uuid` = {TU} ) ;"
          DB    . Query               ( QQ                                   )
          RR    = DB . FetchOne       (                                      )
          N     = str                 ( J [ "Role" ]                         )
          if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )      :
            N   = self . assureString ( RR [ 0 ]                             )
          ## N = self . GetName          ( DB , NAMTAB , TU                     )
          ####################################################################
          J [ "TName" ] = N
      ########################################################################
      PERIODS . append                ( J                                    )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( PERIODS ) <= 0               ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( PERIODS                              )
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
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    TABLE   = self . Tables      [ "Periods"                                 ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TABLE   = self . Tables           [ "Periods"                            ]
    ##########################################################################
    QQ      = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
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
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TSKTAB  = self . Tables   [ "Periods"                                    ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `uuid` from {TSKTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    ##########################################################################
    if                                ( self . Grouping == "Original"      ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . Grouping == "Subordination" ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . Grouping == "Reverse"       ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    if                              ( self == sourceWidget                 ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle ( )
      CNT   = len                   ( UUIDs                                  )
      MSG   = f"從「{title}」複製{CNT}個人物"
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget != self                      ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    if                         ( atItem is None                            ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    if                         ( "UUIDs" not in JSOX                       ) :
      return True
    ##########################################################################
    UUIDs  = JSOX              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    if                         ( atItem is None                            ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      (  0 , 120                                  )
    self   . setColumnWidth      (  1 , 320                                  )
    self   . setColumnWidth      ( 12 ,   3                                  )
    LABELs = self . Translations [ "PeriodeListings" ] [ "Labels"            ]
    self   . setCentralLabels    ( LABELs                                    )
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def PageHome                     ( self                                  ) :
    ##########################################################################
    self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd                      ( self                                  ) :
    ##########################################################################
    self . StartId    = self . Total - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp                       ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown                     ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId + self . Amount
    if                             ( self . StartId > self . Total         ) :
      self . StartId  = self . Total
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    """
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TSKTAB  = self . Tables        [ "Tasks"                                 ]
    PRDTAB  = self . Tables        [ "Periods"                               ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    HEAD    = 5702000000000000000
    ##########################################################################
    DB      . LockWrites           ( [ PRJTAB , PRDTAB , NAMTAB ]            )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . LastUuid        ( PRJTAB , "uuid" , HEAD                  )
      DB    . AddUuid              ( PRJTAB , uuid   , 1                     )
      ########################################################################
      NOW   = StarDate             (                                         )
      NOW   . Now                  (                                         )
      CDT   = NOW . Stardate
      ########################################################################
      PRD   = Periode              (                                         )
      PRID  = PRD  . GetUuid       ( DB , PRDTAB                             )
      ########################################################################
      PRD   . Realm    = uuid
      PRD   . Role     = 71
      PRD   . Item     = 1
      PRD   . States   = 0
      PRD   . Creation = CDT
      PRD   . Modified = CDT
      Items =                      [ "realm"                               , \
                                     "role"                                , \
                                     "item"                                , \
                                     "states"                              , \
                                     "creation"                            , \
                                     "modified"                              ]
      PRD   . UpdateItems          ( DB , PRDTAB , Items                     )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    """
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( 0                                        )
    LID  = self . getLocality     (                                          )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    self . TtsTalk                ( MSG , LID                                )
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
      ## if                           ( ( at == 9001 ) and ( hid )            ) :
      ##   self . startup             (                                         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  @pyqtSlot                        (        int                              )
  def GotoId                       ( self , Id                             ) :
    ##########################################################################
    self . StartId    = Id
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(int)
  def AssignAmount                 ( self , Amount                         ) :
    ##########################################################################
    self . Amount    = Amount
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    uuid   = 0
    ##########################################################################
    if                              ( atItem != None                       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    mm     = self . AppendDeleteAction  ( mm , 1102                          )
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( len ( items ) == 1                   ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
        mm . addSeparator           (                                        )
    ##########################################################################
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunAmountIndexMenu ( )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
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
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "Periode" , uuid , NAM          )
      return True
    ##########################################################################
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## EMailsWidget
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
import dns   . resolver
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
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Telecom    . EMail     import EMail       as TelecomEMail
##############################################################################
class EMailsWidget                 ( TreeDock                              ) :
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
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "desc"
    self . DbProfile          = ""
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
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
    self . Relation . setT2        ( "EMail"                                 )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . OwnRel   = Relation     (                                         )
    self . OwnRel   . setT1        ( "People"                                )
    self . OwnRel   . setT2        ( "EMail"                                 )
    self . OwnRel   . setRelation  ( "Subordination"                         )
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
  def sizeHint                     ( self                                  ) :
    return self . SizeSuggestion   ( QSize ( 1024 , 640 )                    )
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
    self . LinkAction              ( "Paste"      , self . Paste             )
    self . LinkAction              ( "Search"     , self . Search            )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkVoice               ( self . CommandParser                    )
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
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 , 1 , 2 , 3 ]          ) :
      return
    ##########################################################################
    if                          ( column in [ 0 , 1 , 2 ]                  ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      return
    ##########################################################################
    if                          ( column in [ 3 ]                          ) :
      ########################################################################
      LL   = self . Translations [ "EMailsWidget" ] [ "Shareable"            ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . shareableChanged                   )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 5                                         )
      cb   . showPopup           (                                           )
    ##########################################################################
    return
  ############################################################################
  def getItemJson                  ( self , item                           ) :
    return item . data             ( 7 , Qt . UserRole                       )
  ############################################################################
  def PrepareItem                   ( self , JSON                          ) :
    ##########################################################################
    UUID      = int                 ( JSON [ "Uuid"                        ] )
    UXID      = str                 ( UUID                                   )
    ##########################################################################
    ACCOUNT   = JSON                [ "Account"                              ]
    HOSTNAME  = JSON                [ "Hostname"                             ]
    EMAIL     = JSON                [ "EMail"                                ]
    OWNERS    = JSON                [ "Owners"                               ]
    MX        = JSON                [ "MX"                                   ]
    SHAREABLE = JSON                [ "Shareable"                            ]
    CONFIRM   = JSON                [ "Confirm"                              ]
    ##########################################################################
    SHARELIST = self . Translations [ "EMailsWidget" ] [ "Shareable"         ]
    SHARECONF = self . Translations [ "EMailsWidget" ] [ "Confirm"           ]
    ##########################################################################
    SHRSTR    = ""
    if                              ( str ( SHAREABLE ) in SHARELIST       ) :
      SHRSTR  = SHARELIST           [ str ( SHAREABLE )                      ]
    ##########################################################################
    CMFSTR    = ""
    if                              ( str ( CONFIRM   ) in SHARECONF       ) :
      CMFSTR  = SHARECONF           [ str ( CONFIRM   )                      ]
    ##########################################################################
    IT        = QTreeWidgetItem     (                                        )
    IT        . setText             ( 0 , EMAIL                              )
    IT        . setToolTip          ( 0 , UXID                               )
    IT        . setData             ( 0 , Qt . UserRole , UXID               )
    ##########################################################################
    IT        . setText             ( 1 , ACCOUNT                            )
    IT        . setToolTip          ( 1 , UXID                               )
    ##########################################################################
    IT        . setText             ( 2 , HOSTNAME                           )
    IT        . setToolTip          ( 2 , UXID                               )
    ##########################################################################
    IT        . setText             ( 3 , SHRSTR                             )
    IT        . setData             ( 3 , Qt . UserRole , SHAREABLE          )
    ##########################################################################
    IT        . setText             ( 4 , CMFSTR                             )
    IT        . setData             ( 4 , Qt . UserRole , CONFIRM            )
    ##########################################################################
    IT        . setText             ( 5 , str ( MX )                         )
    IT        . setTextAlignment    ( 5 , Qt . AlignRight                    )
    ##########################################################################
    IT        . setText             ( 6 , str ( OWNERS )                     )
    IT        . setTextAlignment    ( 6 , Qt . AlignRight                    )
    ##########################################################################
    IT        . setData             ( 7 , Qt . UserRole , JSON               )
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
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
    line . setFocus              ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    return
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0 , 1 , 2 , 3                             ] )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (                                          )
  def nameChanged                 ( self                                   ) :
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
      else                                                                   :
        ######################################################################
        item . setText            ( column , text                            )
        self . Notify             ( 5                                        )
      ########################################################################
      return
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . UpdateEMail                      , \
                                   ( item , uuid , column , msg , )          )
    ##########################################################################
    return
  ############################################################################
  def shareableChanged           ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      uuid = self . itemUuid     ( item , 0                                  )
      LL   = self . Translations [ "ImWidget" ] [ "Shareable"                ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateShareable                  , \
                                   ( item , uuid , value , )                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def Paste                      ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot            (                                                     )
  def Finding          ( self                                              ) :
    ##########################################################################
    L    = self . SearchLine
    ##########################################################################
    if                 ( L in [ False , None ]                             ) :
      return
    ##########################################################################
    self . SearchLine = None
    T    = L . text    (                                                     )
    L    . deleteLater (                                                     )
    ##########################################################################
    if                 ( len ( T ) <= 0                                    ) :
      return
    ##########################################################################
    self . clear       (                                                     )
    self . Go          ( self . looking , ( T , )                            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                            (                                     )
  def Search                           ( self                              ) :
    ##########################################################################
    L      = LineEdit                  ( None , self . PlanFunc              )
    OK     = self . attacheStatusBar   ( L , 1                               )
    ##########################################################################
    if                                 ( not OK                            ) :
      ########################################################################
      L    . deleteLater               (                                     )
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . Finding                      )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "Search"                            )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , EMAILs                          ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in EMAILs                                                          :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( EMAILs )                           )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    if                            ( self . Grouping in [ "Searching" ]     ) :
      ########################################################################
      T    = self . Translations  [ "EMailsWidget" ] [ "Title"               ]
      K    = self . SearchKey
      T    = f"{T}:{K}"
      ########################################################################
      self . setWindowTitle       ( T                                        )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables     [ "Relation"                                  ]
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
  def looking                         ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    EMSTAB  = self . Tables           [ "EMails"                            ]
    LIKE    = f"%{name}%"
    ORDER   = self . getSortingOrder  (                                      )
    UUIDs   =                         [                                      ]
    ##########################################################################
    QQ      = f"""select `uuid` from {EMSTAB}
                  where ( `email` like %s )
                  order by `uuid` {ORDER} ;"""
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( ALL in [ False , None ] ) or ( len ( ALL ) <= 0 ) )               :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    for U in ALL                                                             :
      UUIDs . append                  ( U [ 0 ]                              )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    self . SearchKey   = name
    self . UUIDs       = UUIDs
    self . OldGrouping = self . Grouping
    self . setGrouping                ( "Searching"                          )
    ##########################################################################
    self . loading                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    if                                ( self . Grouping in [ "Searching" ] ) :
      UUIDs = self . UUIDs
    else                                                                     :
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    EMSTAB  = self . Tables           [ "EMails"                             ]
    PRZTAB  = self . Tables           [ "Properties"                         ]
    RELTAB  = self . Tables           [ "Relation"                           ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"      : U                    , \
                                        "Account"   : ""                   , \
                                        "Hostname"  : ""                   , \
                                        "EMail"     : ""                   , \
                                        "Owners"    : 0                    , \
                                        "MX"        : 0                    , \
                                        "Shareable" : 0                    , \
                                        "Confirm"   : 0                      }
      ########################################################################
      QQ    = f"""select
                  {EMSTAB}.`account`,
                  {EMSTAB}.`hostname`,
                  {EMSTAB}.`email`,
                  {PRZTAB}.`mx`,
                  {PRZTAB}.`shareable`,
                  {PRZTAB}.`confirm`
                  from {EMSTAB}
                  left join {PRZTAB}
                  on ( {PRZTAB}.`uuid` = {EMSTAB}.`uuid` )
                  where ( {EMSTAB}.`uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( RR not in [ False , None ] ) and ( len ( RR ) == 6 )              :
        ######################################################################
        J [ "Account"   ] = self . assureString ( RR [ 0 ]                   )
        J [ "Hostname"  ] = self . assureString ( RR [ 1 ]                   )
        J [ "EMail"     ] = self . assureString ( RR [ 2 ]                   )
        J [ "MX"        ] = int       (           RR [ 3 ]                   )
        J [ "Shareable" ] = int       (           RR [ 4 ]                   )
        J [ "Confirm"   ] = int       (           RR [ 5 ]                   )
      ########################################################################
      self . OwnRel . set             ( "second" , U                         )
      OWNED = self . OwnRel . CountFirst ( DB , RELTAB                       )
      J   [ "Owners"    ] = OWNED
      ########################################################################
      IMACT . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( IMACT ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( IMACT                                )
    self   . Notify                   ( 5                                    )
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Paste"      , self . Paste           , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
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
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    EMSTAB  = self . Tables           [ "EMails"                             ]
    ##########################################################################
    QQ      = f"select count(*) from {EMSTAB} ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( RR in [ False , None ] ) or ( len ( RR ) <= 0 )                     :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    EMSTAB = self . Tables     [ "EMails"                                    ]
    QQ     = f"select count(*) from {EMSTAB} ;"
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
    EMSTAB = self . Tables          [ "EMails"                               ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {EMSTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
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
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 , 280                                          )
    self . setColumnWidth ( 1 , 200                                          )
    self . defaultPrepare ( "EMailsWidget" , 7                               )
    ##########################################################################
    return
  ############################################################################
  def UpdateEMail                  ( self , item , uuid , column , name    ) :
    ##########################################################################
    EMAIL    = item . text         ( 0                                       )
    ACCOUNT  = item . text         ( 1                                       )
    HOST     = item . text         ( 2                                       )
    ##########################################################################
    TEM      = TelecomEMail        (                                         )
    ##########################################################################
    if                             ( column in [ 0 ]                       ) :
      ########################################################################
      if                           ( not TEM . isValidEMail    ( name )    ) :
        self . Notify              ( 1                                       )
        return
      ########################################################################
      TEM    . setEMail            ( name                                    )
    ##########################################################################
    if                             ( column in [ 1 ]                       ) :
      ########################################################################
      if                           ( not TEM . isValidAccount  ( name )    ) :
        self . Notify              ( 1                                       )
        return
      ########################################################################
      TEM    . setAccount          ( name                                    )
      TEM    . setHostname         ( HOST                                    )
    ##########################################################################
    if                             ( column in [ 2 ]                       ) :
      ########################################################################
      if                           ( not TEM . isValidHostname ( name )    ) :
        self . Notify              ( 1                                       )
        return
      ########################################################################
      TEM    . setAccount          ( ACCOUNT                                 )
      TEM    . setHostname         ( name                                    )
    ##########################################################################
    EMAIL    = TEM . EMail
    ACCOUNT  = TEM . Account
    HOST     = TEM . Hostname
    ##########################################################################
    DB       = self . ConnectDB    (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    EMSTAB   = self . Tables       [ "EMails"                                ]
    HEAD     = 3000000000000000000
    NEWON    = False
    ##########################################################################
    DB       . LockWrites          ( [ EMSTAB ]                              )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      EUID   = DB . LastUuid       ( EMSTAB , "uuid" , HEAD                  )
      DB     . AppendUuid          ( EMSTAB , EUID                           )
      uuid   = EUID
      NEWON  = True
    ##########################################################################
    QQ       = f"""update {EMSTAB}
                   set `account` = %s , `hostname` = %s , `email` = %s
                   where ( `uuid` = {uuid} ) ;"""
    QQ       = " " . join          ( QQ . split ( )                          )
    VAL      =                     ( ACCOUNT , HOST , EMAIL ,                )
    DB       . QueryValues         ( QQ , VAL                                )
    ##########################################################################
    DB       . Close               (                                         )
    ##########################################################################
    if                             ( NEWON                                 ) :
      ########################################################################
      SHARELIST = self . Translations [ "EMailsWidget" ] [ "Shareable"       ]
      SHARECONF = self . Translations [ "EMailsWidget" ] [ "Confirm"         ]
      ########################################################################
      SHRSTR = SHARELIST           [ "0"                                     ]
      CMFSTR = SHARECONF           [ "0"                                     ]
      ########################################################################
      JSON   =                     { "Uuid"      : uuid                    , \
                                     "Account"   : ACCOUNT                 , \
                                     "Hostname"  : HOST                    , \
                                     "EMail"     : EMAIL                   , \
                                     "Owners"    : 0                       , \
                                     "MX"        : 0                       , \
                                     "Shareable" : 0                       , \
                                     "Confirm"   : 0                         }
      ########################################################################
      IT     . setData             ( 7 , Qt . UserRole , JSON                )
      ########################################################################
      self   . emitAssignColumn . emit ( item , 3 , SHRSTR                   )
      self   . emitAssignColumn . emit ( item , 4 , CMFSTR                   )
      self   . emitAssignColumn . emit ( item , 5 , "0"                      )
      self   . emitAssignColumn . emit ( item , 6 , "0"                      )
    ##########################################################################
    item     . setData             ( 0 , Qt . UserRole , uuid                )
    self . emitAssignColumn . emit ( item , 0 , EMAIL                        )
    self . emitAssignColumn . emit ( item , 1 , ACCOUNT                      )
    self . emitAssignColumn . emit ( item , 2 , HOST                         )
    ##########################################################################
    self     . Notify              ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def UpdateShareable         ( self , item , uuid , shareable             ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    PRSTAB = self . Tables    [ "Properties"                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ PRSTAB ]                                   )
    ##########################################################################
    QQ     = f"""update {PRSTAB}
                 set `shareable` = {shareable}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
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
  def DetectMX                       ( self , item                         ) :
    ##########################################################################
    HOST   = item . text             ( 2                                     )
    MXes   =                         [                                       ]
    try                                                                      :
      MXes = dns  . resolver . resolve ( HOST , 'MX'                         )
    except                                                                   :
      pass
    ##########################################################################
    for MX in MXes                                                           :
      print ( MX . to_text ( ) )
    ##########################################################################
    return
  ############################################################################
  def DetectAllMXes               ( self                                   ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    plan     = None
    if                            ( self . hasPlan ( )                     ) :
      plan   = self . GetPlan     (                                          )
    ##########################################################################
    self     . OnBusy  . emit     (                                          )
    ##########################################################################
    EMSTAB   = self . Tables      [ "EMails"                                 ]
    PRZTAB   = self . Tables      [ "Properties"                             ]
    ##########################################################################
    QQ       = f"select `hostname` from {EMSTAB} group by `hostname` asc ;"
    HOSTs    = DB . ObtainUuids   ( QQ                                       )
    ##########################################################################
    if                            ( len ( HOSTs ) > 0                      ) :
      ########################################################################
      if                          ( plan not in [ False , None ]           ) :
        ######################################################################
        NAME = self . getMenuItem ( "QueryAllMXes"                           )
        cFmt = self . getMenuItem ( "SecsCounting"                           )
        rFmt = self . getMenuItem ( "ItemCounting"                           )
        FMT  = self . getMenuItem ( "Percentage"                             )
        PID  = plan . Progress    ( NAME , FMT                               )
        plan . setFrequency       ( PID  , cFmt , rFmt                       )
      ########################################################################
      plan   . setRange           ( PID , 0 , len ( HOSTs )                  )
      plan   . Start              ( PID , 0 , True                           )
      plan   . ProgressReady      ( PID , 300                                )
      ########################################################################
      K      = 0
      while ( K < len ( HOSTs ) ) and ( plan . isProgressRunning ( PID ) )   :
        ######################################################################
        HOST = self . assureString ( HOSTs [ K ]                             )
        plan . setProgressValue   ( PID , K                                  )
        plan . ProgressText       ( PID , str ( HOST )                       )
        ######################################################################
        MXes =                    [                                          ]
        if                        ( len ( HOST ) > 0                       ) :
          try                                                                :
            MXes = dns  . resolver . resolve ( HOST , 'MX'                   )
          except                                                             :
            pass
        ######################################################################
        CNT  = len                ( MXes                                     )
        ######################################################################
        if                        ( CNT <= 0                               ) :
          ####################################################################
          MQ = f"select `uuid` from {EMSTAB} where ( `hostname` = %s )"
          QQ = f"""update {PRZTAB}
                   set `mx` = 0 , `confirm` = 2
                   where ( `uuid` in ( {MQ} ) ) ;"""
          ####################################################################
        else                                                                 :
          ####################################################################
          MQ = f"select `uuid` from {EMSTAB} where ( `hostname` = %s )"
          QQ = f"""update {PRZTAB}
                   set `mx` = {CNT}
                   where ( `uuid` in ( {MQ} ) ) ;"""
        ######################################################################
        QQ   = " " . join         ( QQ . split ( )                           )
        DB   . QueryValues        ( QQ , ( HOST , )                          )
        ######################################################################
        K    = K + 1
      ########################################################################
      plan   . Finish             ( PID                                      )
    ##########################################################################
    self     . GoRelax . emit     (                                          )
    DB       . Close              (                                          )
    self     . Notify             ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    return          { "Match" : False                                        }
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9007 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PickDbMenu                   ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    MSG    = self . getMenuItem    ( "PickDB"                                )
    DBM    = mm . addMenu          ( MSG                                     )
    ##########################################################################
    DBs    = self . Hosts . keys   (                                         )
    i      = 121330001
    ##########################################################################
    for DBn in DBs                                                           :
      ########################################################################
      hid  =                       ( DBn == self . DbProfile                 )
      mm   . addActionFromMenu     ( DBM , i , DBn , True , hid              )
      ########################################################################
      i    = i + 1
    ##########################################################################
    return mm
  ############################################################################
  def RunPickDbMenu                ( self , at                             ) :
    ##########################################################################
    DBs    = self . Hosts . keys   (                                         )
    DBs    = list                  ( DBs                                     )
    b      = 121330001
    e      = b + len               ( DBs                                     )
    ##########################################################################
    if                             ( at <  b                               ) :
      return False
    ##########################################################################
    if                             ( at >= e                               ) :
      return False
    ##########################################################################
    e      = at - b
    N      = DBs                   [ e                                       ]
    ##########################################################################
    self   . DbProfile = N
    self   . DB = self . Hosts     [ N                                       ]
    ##########################################################################
    if                             ( N in [ "ERP" ]                        ) :
      ########################################################################
      self . OwnRel . set          ( "t1" , 103                              )
      self . OwnRel . set          ( "t2" , 119                              )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . OwnRel . setT1        ( "People"                                )
      self . OwnRel . setT2        ( "EMail"                                 )
    ##########################################################################
    return True
  ############################################################################
  def Menu                         ( self , pos                            ) :
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
    mm     . addAction             ( 13189121 , self . DbProfile             )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . AmountIndexMenu     ( mm                                 )
    ##########################################################################
    if                             ( self . Grouping in [ "Searching" ]    ) :
      ########################################################################
      msg  = self . getMenuItem    ( "NotSearch"                             )
      mm   . addAction             ( 2001 , msg                              )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    mm     = self . AppendDeleteAction  ( mm , 1102                          )
    mm     = self . AppendRenameAction  ( mm , 1103                          )
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      msg  = self . getMenuItem    ( "QueryMailDNS"                          )
      mm   . addAction             ( 4327 , msg                              )
    msg    = self . getMenuItem    ( "QueryAllMXes"                          )
    mm     . addAction             ( 4328 , msg                              )
    msg    = self . getMenuItem    ( "ListAllInvalid"                        )
    mm     . addAction             ( 4329 , msg                              )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . PickDbMenu     ( mm                                      )
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . SortingMenu    ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunAmountIndexMenu ( )         ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunPickDbMenu      ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                              ( at == 2001                           ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 4327                            ) :
      self . Go                    ( self . DetectMX , ( atItem , )          )
      return True
    ##########################################################################
    if                             ( at == 4328                            ) :
      self . Go                    ( self . DetectAllMXes                    )
      return True
    ##########################################################################
    if                             ( at == 4329                            ) :
      return True
    ##########################################################################
    return True
##############################################################################

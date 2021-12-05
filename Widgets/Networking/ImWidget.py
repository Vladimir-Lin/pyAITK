# -*- coding: utf-8 -*-
##############################################################################
## ImWidget
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
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . People     . People    import People
##############################################################################
class ImWidget                     ( TreeDock                              ) :
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
    self . ImsTypes           =    {                                         }
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "InstantMessage"                        )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . OwnRel   = Relation     (                                         )
    self . OwnRel   . setT1        ( "People"                                )
    self . OwnRel   . setT2        ( "InstantMessage"                        )
    self . OwnRel   . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 7                                       )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 5 , True                                )
    self . setColumnHidden         ( 6 , True                                )
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
    return QSize                   ( 800 , 640                               )
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
    self   . setActionLabel        ( "Label"      , self . windowTitle ( )   )
    self   . LinkAction            ( "Refresh"    , self . startup           )
    ##########################################################################
    if                             ( self . Grouping in [ "Original" ]     ) :
      self . LinkAction            ( "Insert"     , self . InsertItem        )
    ##########################################################################
    self   . LinkAction            ( "Delete"     , self . DeleteItems       )
    self   . LinkAction            ( "Rename"     , self . RenameItem        )
    self   . LinkAction            ( "Copy"       , self . CopyToClipboard   )
    self   . LinkAction            ( "Paste"      , self . Paste             )
    self   . LinkAction            ( "Search"     , self . Search            )
    self   . LinkAction            ( "Home"       , self . PageHome          )
    self   . LinkAction            ( "End"        , self . PageEnd           )
    self   . LinkAction            ( "PageUp"     , self . PageUp            )
    self   . LinkAction            ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self   . LinkAction            ( "SelectAll"  , self . SelectAll         )
    self   . LinkAction            ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self   . LinkVoice             ( self . CommandParser                    )
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
    if                          ( column not in [ 1 , 2 , 4 ]              ) :
      return
    ##########################################################################
    if                          ( column in [ 2 ]                          ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    if                          ( column in [ 1 ]                          ) :
      ########################################################################
      LL   = self . ImsTypes
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . imsChanged                         )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
    ##########################################################################
    if                          ( column in [ 4 ]                          ) :
      ########################################################################
      LL   = self . Translations [ "ImWidget" ] [ "Shareable"                ]
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
  def getItemJson                 ( self , item                            ) :
    return item . data            ( 6 , Qt . UserRole                        )
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    TRX     = self . Translations [ "ImWidget"                               ]
    ##########################################################################
    UUID    = int                 ( JSON [ "Uuid"      ]                     )
    UXID    = str                 ( UUID                                     )
    ID      = int                 ( UUID % 100000000                         )
    TID     = int                 ( JSON [ "Type"      ]                     )
    Name    = JSON                [ "Name"                                   ]
    OWNERS  = int                 ( JSON [ "Owners"    ]                     )
    SHARE   = int                 ( JSON [ "Shareable" ]                     )
    CONFIRM = int                 ( JSON [ "Confirm"   ]                     )
    ##########################################################################
    TNAM    = ""
    if                            ( TID             in self . ImsTypes     ) :
      TNAM  = self . ImsTypes     [ TID                                      ]
    ##########################################################################
    SNAME   = ""
    if                            ( str ( SHARE   ) in TRX [ "Shareable" ] ) :
      SNAME = TRX [ "Shareable" ] [ str ( SHARE   )                          ]
    ##########################################################################
    CNAME   = ""
    if                            ( str ( CONFIRM ) in TRX [ "Confirm"   ] ) :
      CNAME = TRX [ "Confirm"   ] [ str ( CONFIRM )                          ]
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    ##########################################################################
    IT      . setText             ( 0 , str ( ID )                           )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setTextAlignment    ( 0 , Qt . AlignRight                      )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    ##########################################################################
    IT      . setText             ( 1 , TNAM                                 )
    IT      . setToolTip          ( 1 , UXID                                 )
    IT      . setData             ( 1 , Qt . UserRole , TID                  )
    ##########################################################################
    IT      . setText             ( 2 , Name                                 )
    IT      . setToolTip          ( 2 , UXID                                 )
    ##########################################################################
    IT      . setText             ( 3 , str ( OWNERS )                       )
    IT      . setTextAlignment    ( 3 , Qt . AlignRight                      )
    ##########################################################################
    IT      . setText             ( 4 , SNAME                                )
    IT      . setData             ( 4 , Qt . UserRole , SHARE                )
    ##########################################################################
    IT      . setText             ( 5 , CNAME                                )
    IT      . setData             ( 5 , Qt . UserRole , CONFIRM              )
    ##########################################################################
    IT      . setData             ( 6 , Qt . UserRole , JSON                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot        (                                                         )
  def InsertItem   ( self                                                  ) :
    ##########################################################################
    if             ( self . Grouping in [ "Original" ]                     ) :
      self . clear (                                                         )
      self . Go    ( self . AppendNewItem                                    )
      return
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                          (                                       )
  def DeleteItems                    ( self                                ) :
    ##########################################################################
    items     = self . selectedItems (                                       )
    if                               ( len ( items ) <= 0                  ) :
      return
    ##########################################################################
    UUIDs     =                      [                                       ]
    for item in items                                                        :
      UUID    = self . itemUuid      ( item , 0                              )
      self    . pendingRemoveItem . emit ( item                              )
      if                             ( UUID not in UUIDs                   ) :
        UUIDs . append               ( UUID                                  )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      return
    ##########################################################################
    self      . Go                   ( self . RemoveItems , ( UUIDs , )      )
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
  def imsChanged                 ( self                                    ) :
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
    value  = int                 ( value                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      uuid = self . itemUuid     ( item , 0                                  )
      LL   = self . ImsTypes
      msg  = LL                  [ value                                     ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateIms                        , \
                                   ( item , uuid , value , )                 )
    ##########################################################################
    self   . removeParked        (                                           )
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
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , IMS                             ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for JSON in IMS                                                          :
      ########################################################################
      IT   = self . PrepareItem   ( JSON                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( IMS )                              )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    if                            ( self . Grouping in [ "Searching" ]     ) :
      ########################################################################
      T    = self . Translations  [ "ImWidget" ] [ "Title"                   ]
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
    IMSTAB  = self . Tables           [ "InstantMessage"                     ]
    LIKE    = f"%{name}%"
    ORDER   = self . getSortingOrder  (                                      )
    UUIDs   =                         [                                      ]
    ##########################################################################
    QQ      = f"""select `uuid` from {IMSTAB}
                  where ( `used` > 0 )
                  and ( `account` like %s )
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
    IMSTAB  = self . Tables           [ "InstantMessage"                     ]
    PRTTAB  = self . Tables           [ "Properties"                         ]
    RELTAB  = self . Tables           [ "Relation"                           ]
    ##########################################################################
    IMACT   =                         [                                      ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"      : U                    , \
                                        "Type"      : 0                    , \
                                        "Name"      : ""                   , \
                                        "Owners"    : 0                    , \
                                        "Shareable" : 0                    , \
                                        "Confirm"   : 0                      }
      ########################################################################
      QQ    = f"""select
                  {IMSTAB}.`imapp`,
                  {IMSTAB}.`account`,
                  {PRTTAB}.`shareable`,
                  {PRTTAB}.`confirm`
                  from {IMSTAB}
                  left join {PRTTAB}
                  on ( {PRTTAB}.`uuid` = {IMSTAB}.`uuid` )
                  where ( {IMSTAB}.`uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( RR not in [ False , None ] ) and ( len ( RR ) == 4 )              :
        ######################################################################
        J [ "Type"      ] = RR        [ 0                                    ]
        J [ "Name"      ] = self . assureString ( RR [ 1 ]                   )
        J [ "Shareable" ] = RR        [ 2                                    ]
        J [ "Confirm"   ] = RR        [ 3                                    ]
      ########################################################################
      self . OwnRel . set             ( "second" , U                         )
      OWNED = self . OwnRel . CountFirst ( DB , RELTAB                       )
      J [ "Owners"      ] = OWNED
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
    self   . LinkAction    ( "Refresh"    , self . startup         , False   )
    ##########################################################################
    if                     ( self . Grouping in [ "Original" ]             ) :
      self . LinkAction    ( "Insert"     , self . InsertItem      , False   )
    ##########################################################################
    self   . LinkAction    ( "Delete"     , self . DeleteItems     , False   )
    self   . LinkAction    ( "Rename"     , self . RenameItem      , False   )
    self   . LinkAction    ( "Copy"       , self . CopyToClipboard , False   )
    self   . LinkAction    ( "Paste"      , self . Paste           , False   )
    self   . LinkAction    ( "Search"     , self . Search          , False   )
    self   . LinkAction    ( "Home"       , self . PageHome        , False   )
    self   . LinkAction    ( "End"        , self . PageEnd         , False   )
    self   . LinkAction    ( "PageUp"     , self . PageUp          , False   )
    self   . LinkAction    ( "PageDown"   , self . PageDown        , False   )
    self   . LinkAction    ( "SelectAll"  , self . SelectAll       , False   )
    self   . LinkAction    ( "SelectNone" , self . SelectNone      , False   )
    self   . LinkVoice     ( None                                            )
    ##########################################################################
    self   . Leave . emit  ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    IMSTAB  = self . Tables           [ "InstantMessage"                     ]
    IMXTAB  = self . Tables           [ "ImApps"                             ]
    ##########################################################################
    self    . ImsTypes =              {                                      }
    QQ      = f"select `id`,`english` from {IMXTAB} order by `id` asc ;"
    DB      . Query                   ( QQ                                   )
    IMT     = DB . FetchAll           (                                      )
    ##########################################################################
    if ( IMT not in [ False , None ] ) and ( len ( IMT ) > 0 )               :
      ########################################################################
      for M in IMT                                                           :
        ######################################################################
        ID  = int                     ( M [ 0 ]                              )
        N   = self . assureString     ( M [ 1 ]                              )
        ######################################################################
        self . ImsTypes [ ID ] = N
    ##########################################################################
    QQ      = f"select count(*) from {IMSTAB} where ( `used` > 0 ) ;"
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
    IMSTAB = self . Tables     [ "InstantMessage"                            ]
    QQ     = f"select count(*) from {IMSTAB} where ( `used` > 0 ) ;"
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
    IMSTAB  = self . Tables   [ "InstantMessage"                             ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `uuid` from {IMSTAB}
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
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 1 , 100                                          )
    self . setColumnWidth ( 2 , 320                                          )
    self . defaultPrepare ( "ImWidget" , 6                                   )
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
  def Paste                        ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RemoveItem              ( self , DB , UUID                           ) :
    ##########################################################################
    IMSTAB = self . Tables    [ "InstantMessage"                             ]
    PRSTAB = self . Tables    [ "Properties"                                 ]
    ##########################################################################
    QQ     = f"""update {IMSTAB}
                 set `used` = 0 , `imapp` = 1 , `account` = ''
                 where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""update {PRSTAB}
                 set `shareable` = 0 , `confirm` = 0
                 where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems             ( self , UUIDs                               ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    IMSTAB = self . Tables    [ "InstantMessage"                             ]
    PRSTAB = self . Tables    [ "Properties"                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ IMSTAB , PRSTAB ]                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      self . RemoveItem       ( DB , UUID                                    )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AppendNewItem           ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    IMSTAB = self . Tables    [ "InstantMessage"                             ]
    ##########################################################################
    DB     . LockWrites       ( [ IMSTAB ]                                   )
    ##########################################################################
    UUID   = DB . UnusedUuid  ( IMSTAB , "`uuid`"                            )
    DB     . UseUuid          ( IMSTAB , UUID                                )
    ##########################################################################
    QQ     = f"""update {IMSTAB}
                 set `imapp` = 1
                 where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    IMSTAB = self . Tables    [ "InstantMessage"                             ]
    ##########################################################################
    DB     . LockWrites       ( [ IMSTAB ]                                   )
    ##########################################################################
    QQ     = f"""update {IMSTAB}
                 set `account` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . QueryValues      ( QQ , ( name , )                              )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateIms               ( self , item , uuid , ims                   ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    IMSTAB = self . Tables    [ "InstantMessage"                             ]
    ##########################################################################
    DB     . LockWrites       ( [ IMSTAB ]                                   )
    ##########################################################################
    QQ     = f"""update {IMSTAB}
                 set `imapp` = {ims}
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
    self . DoCopyToClipboard      (                                          )
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
    return self . DefaultColumnsMenu (        mm , 0                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9006 )         :
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
      self . OwnRel . set          ( "t2" , 113                              )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . OwnRel . setT1        ( "People"                                )
      self . OwnRel . setT2        ( "InstantMessage"                        )
    ##########################################################################
    return True
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
    if                              ( self . Grouping in [ "Searching" ]   ) :
      ########################################################################
      msg  = self . getMenuItem     ( "NotSearch"                            )
      mm   . addAction              ( 2001 , msg                             )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    if                              ( len ( items ) > 0                    ) :
      self . AppendDeleteAction     ( mm , 1102                              )
    ##########################################################################
    msg    = self . getMenuItem     ( "Search"                               )
    mm     . addAction              ( 1103 , msg                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    mm     = self . PickDbMenu      ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunAmountIndexMenu ( )        ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
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
    if                             ( self . RunPickDbMenu      ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
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
    if                              ( at == 1103                           ) :
      self . Search                 (                                        )
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
    return True
##############################################################################

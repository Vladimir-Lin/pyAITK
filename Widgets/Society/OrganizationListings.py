# -*- coding: utf-8 -*-
##############################################################################
## OrganizationListings
## 組織列表
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
class OrganizationListings         ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int                               )
  PeopleGroup       = pyqtSignal   ( str , int , str                         )
  AlbumGroup        = pyqtSignal   ( str , int , str                         )
  OpenVariantTables = pyqtSignal   ( str , str , int , str , dict            )
  OpenLogHistory    = pyqtSignal   ( str , str , str                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . GType              = 40
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "asc"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . FetchTableKey      = "OrganizationListings"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Organization"                          )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 3                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
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
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Insert"     , self . InsertItem                 )
    self . LinkAction     ( "Delete"     , self . DeleteItems                )
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    ##########################################################################
    self . LinkAction     ( "Search"     , self . Search                     )
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
    self . LinkAction     ( "Paste"      , self . Paste                      )
    self . LinkAction     ( "Import"     , self . Import                     )
    ##########################################################################
    self . LinkAction     ( "Home"       , self . PageHome                   )
    self . LinkAction     ( "End"        , self . PageEnd                    )
    self . LinkAction     ( "PageUp"     , self . PageUp                     )
    self . LinkAction     ( "PageDown"   , self . PageDown                   )
    ##########################################################################
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
    ##########################################################################
    self . LinkVoice      ( self . CommandParser                             )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Paste"      , self . Paste           , False   )
    self . LinkAction      ( "Import"     , self . Import          , False   )
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
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "OrganizationListings" , 2                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self , UUID , NAME                       ) :
    ##########################################################################
    IT = self . PrepareUuidItem ( 0    , UUID , NAME                         )
    IT . setTextAlignment       ( 1    , Qt . AlignRight                     )
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
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( self . RemoveItems                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot             (                                                    )
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , msg ,                        )
    self   . Go                 ( self . AssureUuidItem , VAL                )
    ##########################################################################
    return
  ############################################################################
  def Paste             ( self                                             ) :
    ##########################################################################
    self . defaultPaste ( self . ImportFromText                              )
    ##########################################################################
    return
  ############################################################################
  def Import             ( self                                            ) :
    ##########################################################################
    self . defaultImport ( self . ImportFromText                             )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        dict                              )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , NAMEs [ U ]                          )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( UUIDs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids                    ( self , DB                   ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder          (                               )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables                   [ "Relation"                    ]
    ##########################################################################
    if                                       ( self . isSubordination ( )  ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                                       ( self . isReverse       ( )  ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                                   [                               ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
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
  @pyqtSlot                (        str  , int                               )
  def AssignAmounts        ( self , UUID , Amounts                         ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( 1 , str ( Amounts )                             )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Organization"                       )
    REL    . setT2                    ( "People"                             )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT                   )
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "Organizations" , "NamesEditing"          )
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
    self    . Notify                  ( 3                                    )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    if                                ( self . Grouping in [ "Searching" ] ) :
      UUIDs = self . UUIDs
    else                                                                     :
      self  . UUIDs =                 [                                      ]
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 1 )    ) :
      self . Go                       ( self . ReportBelongings            , \
                                        ( UUIDs , )                          )
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
  def ObtainAllUuids                ( self , DB                            ) :
    ##########################################################################
    TABLE  = self . Tables          [ "Organizations"                        ]
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
    TABLE = self . Tables       [ "NamesEditing"                             ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    ORGTAB = self . Tables [ "Organizations"                                 ]
    ##########################################################################
    QQ     = f"select count(*) from {ORGTAB} where ( `used` > 0 ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( ( RR in [ False , None ] ) or ( len ( RR ) <= 0 ) )                 :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    ORGTAB = self . Tables   [ "Organizations"                               ]
    QQ     = f"select count(*) from {ORGTAB} where ( `used` > 0 ) ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                             ]
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
    ORGTAB = self . Tables          [ "Organizations"                        ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {ORGTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "organization/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , 0 , mtype , message                )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids;organization/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    if                               ( self == sourceWidget                ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( mtype in [ "people/uuids"         ] ) :
      ########################################################################
      if                             ( atItem in [ False , None ]          ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus ( "CopyFrom" , title , CNT              )
    elif                             ( mtype in [ "organization/uuids"   ] ) :
      self . ShowMenuItemTitleStatus ( "OrganizationFrom" , title , CNT      )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , source , mimeData , mousePos       ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( source == self                            ) :
      return False
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    mtype  = self . DropInJSON [ "Mime"                                      ]
    ##########################################################################
    if                         ( mtype in [ "people/uuids"               ] ) :
      ########################################################################
      if                       ( atItem in [ False , None ]                ) :
        return False
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def acceptOrganizationsDrop  ( self                                      ) :
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
    if                         ( atItem in [ False , None ]                ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinOrganization             , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def dropOrganizations ( self , source , pos , JSOX                       ) :
    ##########################################################################
    if                  ( "UUIDs" not in JSOX                              ) :
      return True
    ##########################################################################
    UUIDs  = JSOX       [ "UUIDs"                                            ]
    if                  ( len ( UUIDs ) <= 0                               ) :
      return True
    ##########################################################################
    self . Go           ( self . AppendingOrganizations , ( UUIDs , )        )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinOrganization        ( self , UUID , UUIDs                  ) :
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    COUNT   = len                   ( UUIDs                                  )
    if                              ( COUNT <= 0                           ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden ( 1                                      )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem    ( "JoinPeople"                           )
    MSG     = FMT  . format         ( COUNT                                  )
    self    . ShowStatus            ( MSG                                    )
    self    . TtsTalk               ( MSG , 1002                             )
    ##########################################################################
    TYPE    = "Organization"
    PER     = People                (                                        )
    RELTAB  = self . Tables         [ "RelationPeople"                       ]
    DB      . LockWrites            ( [ RELTAB                             ] )
    PER     . ConnectToPeople       ( DB , RELTAB , UUID , TYPE , UUIDs      )
    DB      . UnlockTables          (                                        )
    ##########################################################################
    if                              ( not Hide                             ) :
      TOTAL = PER . CountBelongs    ( DB , RELTAB , UUID , TYPE              )
    ##########################################################################
    DB      . Close                 (                                        )
    ##########################################################################
    self    . ShowStatus            ( ""                                     )
    ##########################################################################
    if                              ( Hide                                 ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem     ( UUID , 0                               )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    IT      . setText               ( 1 , str ( TOTAL )                      )
    self    . DoUpdate              (                                        )
    ##########################################################################
    return
  ############################################################################
  def AppendingOrganizations    ( self , UUIDs                             ) :
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    FMT    = self . getMenuItem ( "JoinOrganization"                         )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "Relation"                                 ]
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      self . Relation . Joins   ( DB , RELTAB                                )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        self . Relation . Join  ( DB      , RELTAB                           )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    self   . loading            (                                            )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
      SQLs . append                   ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    TITLE  = "RemoveOrganizationItems"
    self   . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    self   . loading                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    ORGTAB = self . Tables    [ "Organizations"                              ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ ORGTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( ORGTAB , "uuid" , 1600000000000000000        )
      DB   . AppendUuid       ( ORGTAB , uuid                                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def ImportFromText          ( self , text                                ) :
    ##########################################################################
    L      = text . split     ( "\n"                                         )
    if                        ( len ( L ) <= 0                             ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    ORGTAB = self . Tables    [ "Organizations"                              ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ ORGTAB , NAMTAB                          ] )
    ##########################################################################
    for N in L                                                               :
      ########################################################################
      name = N
      name = name .  strip    (                                              )
      name = name . rstrip    (                                              )
      ########################################################################
      if                      ( len ( name ) <= 0                          ) :
        continue
      ########################################################################
      uuid = DB . LastUuid    ( ORGTAB , "uuid" , 1600000000000000000        )
      DB   . AppendUuid       ( ORGTAB , uuid                                )
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
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
  def FunctionsMenu          ( self , mm , uuid , item                     ) :
    ##########################################################################
    msg = self . getMenuItem ( "Functions"                                   )
    LOM = mm   . addMenu     ( msg                                           )
    ##########################################################################
    msg = self . getMenuItem ( "AssignTables"                                )
    mm  . addActionFromMenu  ( LOM , 25351301 , msg                          )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 25351301                    ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      if                               ( self . isOriginal ( )             ) :
        ######################################################################
        UUID = "0"
        TYPE = 38
        ######################################################################
      elif                             ( self . isSubordination (        ) ) :
        ######################################################################
        UUID = self . Relation  . get  ( "first"                             )
        TYPE = self . Relation  . get  ( "t1"                                )
        TYPE = int                     ( TYPE                                )
        ######################################################################
      elif                             ( self . isReverse       (        ) ) :
        ######################################################################
        UUID = self . Relation  . get  ( "second"                            )
        TYPE = self . Relation  . get  ( "t2"                                )
        TYPE = int                     ( TYPE                                )
      ########################################################################
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         str ( UUID  )                     , \
                                         TYPE                              , \
                                         self . FetchTableKey              , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    return False
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
      if                           ( ( at == 9001 ) and ( hid )            ) :
        ######################################################################
        self . startup             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu              ( self , mm , item                           ) :
    ##########################################################################
    if                        ( self . NotOkay ( item )                    ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text        ( 0                                            )
    FMT  = TRX                [ "UI::Belongs"                                ]
    MSG  = FMT . format       ( NAME                                         )
    COL  = mm . addMenu       ( MSG                                          )
    ##########################################################################
    msg  = self . getMenuItem ( "Crowds"                                     )
    mm   . addActionFromMenu  ( COL , 38521001 , msg                         )
    ##########################################################################
    msg  = self . getMenuItem ( "Films"                                      )
    mm   . addActionFromMenu  ( COL , 38521002 , msg                         )
    ##########################################################################
    msg  = self . getMenuItem ( "Description"                                )
    mm   . addActionFromMenu  ( COL , 38521003 , msg                         )
    ##########################################################################
    msg  = self . getMenuItem ( "Address"                                    )
    mm   . addActionFromMenu  ( COL , 38521004 , msg                         )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , item                      ) :
    ##########################################################################
    if                             ( at == 38521001                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . PeopleGroup . emit  ( head , self . GType , str ( uuid )        )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521002                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . AlbumGroup  . emit    ( head , self . GType , str ( uuid )      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521003                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . OpenLogHistory . emit ( head , str ( uuid ) , "Description"     )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521004                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . OpenLogHistory . emit ( head , str ( uuid ) , "Address"         )
      ########################################################################
      return True
    ##########################################################################
    return False
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
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    ##########################################################################
    if                             ( self . Grouping in [ "Searching" ]    ) :
      ########################################################################
      msg  = self . getMenuItem    ( "Original"                              )
      mm   . addAction             ( 1002 , msg                              )
    ##########################################################################
    self   . AppendInsertAction    ( mm , 1101                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    self   . AppendDeleteAction    ( mm , 1103                               )
    ##########################################################################
    msg    = self . getMenuItem    ( "Search"                                )
    mm     . addAction             ( 1104 , msg                              )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      if                           ( self . EditAllNames != None           ) :
        ######################################################################
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
    ##########################################################################
    mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . FunctionsMenu         ( mm , uuid , atItem                      )
    self   . GroupsMenu            ( mm ,        atItem                      )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking     ( mm , aa                                 )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu  ( at , uuid , atItem                   )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu ( at                                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu ( at                                      )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu  ( at , atItem                             )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      ########################################################################
      self . Grouping = "Original"
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1104                            ) :
      self . Search                (                                         )
      return True
    ##########################################################################
    if                             ( at == 1201                            ) :
      head = atItem . text         ( 0                                       )
      self . PeopleGroup   . emit  ( head , 38 , str ( uuid )                )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Organization" , uuid , NAM      )
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
##############################################################################

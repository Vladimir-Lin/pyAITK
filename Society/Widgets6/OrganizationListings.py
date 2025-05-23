# -*- coding: utf-8 -*-
##############################################################################
## OrganizationListings
## 組織列表
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                              import QtCore
from   PySide6                              import QtGui
from   PySide6                              import QtWidgets
from   PySide6 . QtCore                     import *
from   PySide6 . QtGui                      import *
from   PySide6 . QtWidgets                  import *
from   AITK    . Qt6                        import *
##############################################################################
from   AITK    . Essentials . Relation      import Relation
from   AITK    . Calendars  . StarDate      import StarDate
from   AITK    . Calendars  . Periode       import Periode
from   AITK    . People     . People        import People
##############################################################################
from   AITK    . UUIDs      . UuidListings6 import appendUuid
from   AITK    . UUIDs      . UuidListings6 import appendUuids
from   AITK    . UUIDs      . UuidListings6 import assignUuids
from   AITK    . UUIDs      . UuidListings6 import getUuids
##############################################################################
class OrganizationListings     ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitAllNames        = Signal ( dict                                        )
  emitAssignAmounts   = Signal ( str , int , int                             )
  PeopleGroup         = Signal ( str , int , str                             )
  AlbumGroup          = Signal ( str , int , str                             )
  AlbumDepot          = Signal ( str , int , str , str                       )
  GalleryDepot        = Signal ( str , int , str , str                       )
  ShowWebPages        = Signal ( str , int , str , str , QIcon               )
  OpenVariantTables   = Signal ( str , str , int , str , dict                )
  OpenLogHistory      = Signal ( str , str , str , str , str                 )
  OpenIdentifiers     = Signal ( str , str , int                             )
  emitVendorDirectory = Signal ( str                                         )
  emitLog             = Signal ( str                                         )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . GType              = 38
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
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
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
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
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationNames             )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Search"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/search.png" )          )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . Search                            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Crowds"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/viewpeople.png" )      )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationCrowds            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Films"                                  )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/video.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationVideos            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Identifiers"                            )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/tag.png" )             )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationIdentifiers       )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "IdentWebPage"                           )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/webfind.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenIdentifierWebPages            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "OrganizationListingsParameter"              )
    FF   = self . Relation . First
    ST   = self . Relation . Second
    T1   = self . Relation . T1
    T2   = self . Relation . T2
    RT   = self . Relation . Relation
    LL   = f"{MM} {FF} {ST} ( {GG} : {T1} , {T2} , {RT} ) - {TT}"
    ##########################################################################
    if                        ( Enabled                                    ) :
      ########################################################################
      LL = f"{LL} Enter"
      ########################################################################
    else                                                                     :
      ########################################################################
      LL = f"{LL} Leave"
    ##########################################################################
    self . emitLog . emit     ( LL                                           )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . Paste           , Enabled      )
    self . LinkAction ( "Import"     , self . Import          , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ##########################################################################
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    ## self . TellStory  (                                         Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    self . LinkVoice         ( self . CommandParser                          )
    self . statusMessage     ( self . windowTitle (                        ) )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                 ( self                                      ) :
    ##########################################################################
    if                         ( not self . isPrepared ( )                 ) :
      return True
    ##########################################################################
    if                         ( not self . AtMenu                         ) :
      ########################################################################
      self . AttachActions     ( False                                       )
      self . detachActionsTool (                                             )
      self . LinkVoice         ( None                                        )
    ##########################################################################
    return False
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked            ( self , item , column                       ) :
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
    self . defaultPrepare ( "OrganizationListings" , 3                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self , UUID , NAME                       ) :
    ##########################################################################
    IT = self . PrepareUuidItem ( 0    , UUID , NAME                         )
    IT . setTextAlignment       ( 1    , Qt . AlignRight                     )
    IT . setTextAlignment       ( 2    , Qt . AlignRight                     )
    ##########################################################################
    return IT
  ############################################################################
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
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
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
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
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
    self   . setEnabled           ( True                                     )
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
  def AssignAmounts        ( self , UUID , Amounts , Column                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( Column , str ( Amounts )                        )
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
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 1               )
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def ReportVideos                    ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "RelationVideos"                     ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Organization"                       )
    REL    . setT2                    ( "Album"                              )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 2               )
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def looking                         ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    if                                ( self . isOriginal ( )              ) :
      self . SearchingForT2           ( name                                 ,
                                        "Organizations"                      ,
                                        "Names"                              )
      return
    ##########################################################################
    if                                ( not self . isGrouping ( )          ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    RELTAB  = self . Tables           [ "RelationEditing"                    ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    LIC     = self . getLocality      (                                      )
    LIKE    = f"%{name}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    T1      = self . Relation . get   ( "t1"                                 )
    T2      = self . Relation . get   ( "t2"                                 )
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      UUID  = self . Relation . get   ( "first"                              )
      ########################################################################
      RQ    = f"""select `second` from {RELTAB}
                  where ( `first` = {UUID} )
                       and ( `t1` = {T1} )
                       and ( `t2` = {T2} )"""
      ########################################################################
    elif                              ( self . isReverse       ( )         ) :
      ########################################################################
      UUID  = self . Relation . get   ( "second"                             )
      ########################################################################
      RQ    = f"""select `first` from {RELTAB}
                  where ( `second` = {UUID} )
                        and ( `t1` = {T1} )
                        and ( `t2` = {T2} )"""
    ##########################################################################
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( `name` like %s )
                  group by `uuid` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
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
    self . SearchKey = name
    self . UUIDs     = UUIDs
    self . Grouping  = "Searching"
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
      VAL  =                          ( UUIDs ,                              )
      self . Go                       ( self . ReportBelongings , VAL        )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 2 )    ) :
      VAL  =                          ( UUIDs ,                              )
      self . Go                       ( self . ReportVideos , VAL            )
    ##########################################################################
    self   . Notify                   ( 5                                    )
    ##########################################################################
    return
  ############################################################################
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
    self   . ReloadLocality           ( DB                                   )
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "first"                              )
      TYPE = self . Relation . get    ( "t1"                                 )
      self . Tables = self . ObtainsOwnerVariantTables                     ( \
                                        DB                                 , \
                                        str ( UUID )                       , \
                                        int ( TYPE )                       , \
                                        self . FetchTableKey               , \
                                        self . Tables                        )
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "second"                             )
      TYPE = self . Relation . get    ( "t2"                                 )
      self . Tables = self . ObtainsOwnerVariantTables                     ( \
                                        DB                                 , \
                                        str ( UUID )                       , \
                                        int ( TYPE )                       , \
                                        self . FetchTableKey               , \
                                        self . Tables                        )
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
    ##########################################################################
    formats = "people/uuids;organization/uuids"
    ##########################################################################
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
    if                               ( self == source                      ) :
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
    if                         ( mtype  in [ "people/uuids"              ] ) :
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
  def dropPeople           ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem in [ False , None ]                    ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    self . Go              ( self . PeopleJoinOrganization                 , \
                             ( UUID , UUIDs , )                              )
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
    RELTAB  = self . Tables         [ "RelationEditing"                      ]
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
    RELTAB = self . Tables      [ "RelationEditing"                          ]
    ##########################################################################
    if                          ( self . isReverse       ( )               ) :
      ########################################################################
      T2   = self . Relation . get ( "t2"                                    )
      ########################################################################
      if                        ( 76 == T2                                 ) :
        ######################################################################
        RELTAB = self . Tables  [ "RelationVideos"                           ]
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      self . Relation . Joins   ( DB , RELTAB , UUIDs                        )
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
    RELTAB = self . Tables            [ "RelationEditing"                    ]
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
    RELTAB = self . Tables    [ "RelationEditing"                            ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ ORGTAB , RELTAB , NAMTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( ORGTAB , "uuid" , 1600000000000000000        )
      DB   . AppendUuid       ( ORGTAB , uuid                                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      self . Relation . set   ( "second" , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
      ########################################################################
    elif                      ( self . isReverse       ( )                 ) :
      ########################################################################
      self . Relation . set   ( "first"  , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
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
  def ObtainFilmFilters           ( self , DB , UUID                       ) :
    ##########################################################################
    IDFTAB  = self . Tables       [ "Identifiers"                            ]
    ##########################################################################
    FILTERS =                     [                                          ]
    GTYPE   = self . GType
    ##########################################################################
    QQ      = f"""select `name` from {IDFTAB}
                  where ( `uuid` = {UUID} )
                    and ( `type` = {GTYPE} )
                    order by `id` asc ;"""
    QQ      = " " . join          ( QQ . split ( )                           )
    DB      . Query               ( QQ                                       )
    ALL     = DB . FetchAll       (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( ALL )                 ) :
      return FILTERS
    ##########################################################################
    if                            ( len ( ALL ) <= 0                       ) :
      return FILTERS
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      F     = self . assureString ( RR [ 0 ]                                 )
      if                          ( len ( F ) > 0                          ) :
        FILTERS . append          ( F                                        )
    ##########################################################################
    return FILTERS
  ############################################################################
  def CollectRemainingFilms   ( self , DB , UUID , FILTERS                 ) :
    ##########################################################################
    FILMs     =               [                                              ]
    if                        ( len ( FILTERS ) <= 0                       ) :
      return FILMs
    ##########################################################################
    IDFTAB    = self . Tables [ "Identifiers"                                ]
    VIDREL    = self . Tables [ "RelationVideos"                             ]
    GTYPE     = self . GType
    LIKEs     =               [                                              ]
    VAL       = tuple         ( FILTERS                                      )
    ##########################################################################
    for L in FILTERS                                                         :
      ########################################################################
      LIKEs   . append        ( "( `name` like %s )"                         )
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      UQ      = f"""select `second` from {VIDREL}
                    where ( `first` = {UUID} )
                      and ( `t1` = {GTYPE} )
                      and ( `t2` = 76 )
                      and ( `relation` = 1 )"""
      ########################################################################
    elif                      ( self . isReverse       ( )                 ) :
      ########################################################################
      UQ      = f"""select `first` from {VIDREL}
                    where ( `second` = {UUID} )
                      and ( `t1` = 76 )
                      and ( `t2` = {GTYPE} )
                      and ( `relation` = 1 )"""
      ########################################################################
    else                                                                     :
      ########################################################################
      return FILMs
    ##########################################################################
    QLIKE     = " or " . join ( LIKEs                                        )
    QQ        = f"""select `uuid` from {IDFTAB}
                    where ( `uuid` not in ( {UQ} ) )
                      and ( `type` = 76 )
                      and ( {QLIKE} )
                    group by `uuid` asc ;"""
    QQ        = " " . join    ( QQ . split ( )                               )
    DB        . QueryValues   ( QQ , VAL                                     )
    ##########################################################################
    ALL       = DB . FetchAll (                                              )
    ##########################################################################
    if                        ( self . NotOkay ( ALL )                     ) :
      return FILMs
    ##########################################################################
    if                        ( len ( ALL ) <= 0                           ) :
      return FILMs
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      try                                                                    :
        F     = int           ( RR [ 0 ]                                     )
        FILMs . append        ( F                                            )
      except                                                                 :
        pass
    ##########################################################################
    return FILMs
  ############################################################################
  def ImportOrganizationFilms   ( self , DB , UUID , FILMs                 ) :
    ##########################################################################
    VIDREL = self . Tables      [ "RelationVideos"                           ]
    SQLs   =                    [                                            ]
    ID     = -1
    ##########################################################################
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "Organization"                             )
    REL    . setT2              ( "Album"                                    )
    REL    . setRelation        ( "Subordination"                            )
    ##########################################################################
    QQ     = REL . Last         ( VIDREL                                     )
    DB     . Query              ( QQ                                         )
    RR     = DB . FetchOne      (                                            )
    if                          ( self . NotOkay ( RR )                    ) :
      pass
    else                                                                     :
      ID   = int                ( RR [ 0 ]                                   )
    ##########################################################################
    ID     = ID + 1
    ##########################################################################
    for FILM in FILMs                                                        :
      ########################################################################
      REL  . Position = ID
      REL  . set                ( "second" , FILM                            )
      ########################################################################
      QQ   = REL . Insert       ( VIDREL                                     )
      SQLs . append             ( QQ                                         )
      ########################################################################
      ID   = ID + 1
    ##########################################################################
    TITLE  = "ImportOrganizationFilms"
    self   . ExecuteSqlCommands ( TITLE , DB , SQLs , 100                    )
    ##########################################################################
    return
  ############################################################################
  def CollectFilms                    ( self , UUID                        ) :
    ##########################################################################
    if                                ( not self . isGrouping ( )          ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return False
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    IDFTAB  = self . Tables           [ "Identifiers"                        ]
    VIDREL  = self . Tables           [ "RelationVideos"                     ]
    GTYPE   = self . GType
    ##########################################################################
    FILTERS = self . ObtainFilmFilters     ( DB , UUID                       )
    FILMs   = self . CollectRemainingFilms ( DB , UUID , FILTERS             )
    ##########################################################################
    if                                ( len ( FILMs ) > 0                  ) :
      ########################################################################
      DB    . LockWrites              ( [ VIDREL                           ] )
      ########################################################################
      self  . ImportOrganizationFilms ( DB , UUID , FILMs                    )
      ########################################################################
      DB    . UnlockTables            (                                      )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage           ( self                                 ) :
    ##########################################################################
    if                              ( not self . isGrouping ( )            ) :
      return False
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return False
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    DB      . LockWrites            ( [ PAMTAB ]                             )
    ##########################################################################
    CUD     = False
    ##########################################################################
    if                              ( self . isOriginal      ( )           ) :
      ########################################################################
      UUID  = "0"
      TYPE  = self . GType
      CUD   = True
      ########################################################################
    elif                            ( self . isSubordination ( )           ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      CUD   = True
      ########################################################################
    elif                            ( self . isReverse       ( )           ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
      CUD   = True
    ##########################################################################
    if                              ( CUD                                  ) :
      ########################################################################
      SCOPE = self . Grouping
      SCOPE = f"OrganizationListings-{SCOPE}"
      self  . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    DB      . UnlockTables          (                                        )
    DB      . Close                 (                                        )
    self    . emitRestart . emit    (                                        )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    PAMTAB = self . Tables         [ "Parameters"                            ]
    ##########################################################################
    if                             ( self . isOriginal      ( )            ) :
      ########################################################################
      UUID = "0"
      TYPE = self . GType
      ########################################################################
    elif                           ( self . isSubordination ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t1"                                    )
      UUID = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                            ( self . isReverse       ( )           ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
      ########################################################################
    else                                                                     :
      return
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"OrganizationListings-{SCOPE}"
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
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
  def OpenOrganizationNames     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    NAM    = self . Tables      [ "NamesEditing"                             ]
    self   . EditAllNames       ( self , "Organization" , uuid , NAM         )
    ##########################################################################
    return
  ############################################################################
  def OpenOrganizationIdentifiers   ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    uuid   = atItem . data          ( 0 , Qt . UserRole                      )
    uuid   = int                    ( uuid                                   )
    head   = atItem . text          ( 0                                      )
    self   . OpenIdentifiers . emit ( head , str ( uuid ) , self . GType     )
    ##########################################################################
    return
  ############################################################################
  def OpenOrganizationCrowds    ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    self   . PeopleGroup . emit ( head , self . GType , str ( uuid )         )
    ##########################################################################
    return
  ############################################################################
  def OpenOrganizationVideos    ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    self   . AlbumGroup  . emit ( head , self . GType , str ( uuid )         )
    ##########################################################################
    return
  ############################################################################
  def OpenIdentifierWebPages    ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self . OpenWebPageListings  ( atItem , "Equivalent"                      )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageListings      ( self , item , Related                     ) :
    ##########################################################################
    text = item . text         ( 0                                           )
    uuid = item . data         ( 0    , Qt . UserRole                        )
    uuid = int                 ( uuid                                        )
    xsid = str                 ( uuid                                        )
    Typi = int                 ( self . GType                                )
    icon = self . windowIcon   (                                             )
    ##########################################################################
    self . ShowWebPages . emit ( text , Typi , xsid , Related , icon         )
    ##########################################################################
    return
  ############################################################################
  def FunctionsMenu                  ( self , mm , uuid , item             ) :
    ##########################################################################
    msg  = self . getMenuItem        ( "Functions"                           )
    LOM  = mm   . addMenu            ( msg                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "AssignTables"                        )
    mm   . addActionFromMenu         ( LOM , 25351301 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "GroupsToCLI"                         )
    mm   . addActionFromMenu         ( LOM , 25351302 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "Search"                              )
    ICON = QIcon                     ( ":/images/search.png"                 )
    mm   . addActionFromMenuWithIcon ( LOM , 25351401 , ICON , msg           )
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
        TYPE = self . GType
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
        ######################################################################
      else                                                                   :
        return False
      ########################################################################
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         str ( UUID  )                     , \
                                         TYPE                              , \
                                         self . FetchTableKey              , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351302                    ) :
      ########################################################################
      self . EmitRelateParameters      (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351401                    ) :
      self . Search                    (                                     )
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9003 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at in [ 9001 , 9002 ] ) and ( hid ) ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                ( self , mm , item                         ) :
    ##########################################################################
    if                          ( self . NotOkay ( item )                  ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text          ( 0                                          )
    FMT  = TRX                  [ "UI::Belongs"                              ]
    MSG  = FMT . format         ( NAME                                       )
    COL  = mm . addMenu         ( MSG                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "CopyOrganizationUuid"                     )
    mm   . addActionFromMenu    ( COL , 38521001 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "Crowds"                                   )
    ICON = QIcon                ( ":/images/viewpeople.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 38521002 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem   ( "AlbumDepot"                               )
    mm   . addActionFromMenu    ( COL , 38521003 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "GalleryDepot"                             )
    mm   . addActionFromMenu    ( COL , 38521004 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "Films"                                    )
    ICON = QIcon                ( ":/images/video.png"                       )
    mm   . addActionFromMenuWithIcon ( COL , 38521005 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem   ( "CreateVendorDirectory"                    )
    mm   . addActionFromMenu    ( COL , 38521006 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "CollectFilms"                             )
    mm   . addActionFromMenu    ( COL , 38521007 , msg                       )
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "Description"                              )
    mm   . addActionFromMenu    ( COL , 38522001 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "Address"                                  )
    mm   . addActionFromMenu    ( COL , 38522002 , msg                       )
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "Identifiers"                              )
    ICON = QIcon                ( ":/images/tag.png"                         )
    mm   . addActionFromMenuWithIcon ( COL , 38523001 , ICON , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "WebPages"                                 )
    mm   . addActionFromMenu    ( COL , 38524001 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "IdentWebPage"                             )
    ICON = QIcon                ( ":/images/webfind.png"                     )
    mm   . addActionFromMenuWithIcon ( COL , 38524002 , ICON , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , item                      ) :
    ##########################################################################
    if                             ( at == 38521001                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521002                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . PeopleGroup . emit    ( head , self . GType , str ( uuid )      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521003                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      rr   = "Capable"
      ########################################################################
      self . AlbumDepot   . emit   ( head , self . GType , str ( uuid ) , rr )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521004                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      rr   = "Contains"
      ########################################################################
      self . GalleryDepot . emit   ( head , self . GType , str ( uuid ) , rr )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521005                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . AlbumGroup  . emit    ( head , self . GType , str ( uuid )      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521006                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      self . emitVendorDirectory . emit ( str ( uuid )                       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38521007                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      VAL  =                       ( uuid ,                                  )
      self . Go                    ( self . CollectFilms , VAL               )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38522001                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      nx   = ""
      ########################################################################
      if                           ( "Notes" in self . Tables              ) :
        nx = self . Tables         [ "Notes"                                 ]
      ########################################################################
      self . OpenLogHistory . emit ( head                                    ,
                                     str ( uuid )                            ,
                                     "Description"                           ,
                                     nx                                      ,
                                     ""                                      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38522002                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      nx   = ""
      ########################################################################
      if                           ( "Notes" in self . Tables              ) :
        nx = self . Tables         [ "Notes"                                 ]
      ########################################################################
      self . OpenLogHistory . emit ( head                                    ,
                                     str ( uuid )                            ,
                                     "Address"                               ,
                                     nx                                      ,
                                     ""                                      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38523001                        ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . OpenIdentifiers . emit ( head , str ( uuid ) , self . GType     )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38524001                        ) :
      ########################################################################
      self . OpenWebPageListings   ( item , "Subordination"                  )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 38524002                        ) :
      ########################################################################
      self . OpenWebPageListings   ( item , "Equivalent"                     )
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    if                             ( self . isSearching ( )                ) :
      ########################################################################
      msg  = self . getMenuItem    ( "NotSearch"                             )
      mm   . addAction             ( 1002 , msg                              )
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    self   . AppendDeleteAction    ( mm , 1103                               )
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    self   . AppendTranslateAllAction (          mm , 3001                   )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . FunctionsMenu         ( mm , uuid , atItem                      )
    self   . GroupsMenu            ( mm ,        atItem                      )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
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
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu ( at                                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu ( at                                      )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu  ( at , atItem                             )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart               (                                         )
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
    if                             ( at == 1601                            ) :
      ########################################################################
      uuid = self . itemUuid       ( atItem , 0                              )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Organization" , uuid , NAM      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
##############################################################################

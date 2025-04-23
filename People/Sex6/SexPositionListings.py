# -*- coding: utf-8 -*-
##############################################################################
## SexPositionListings
## 性愛姿勢列表
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                                   import QtCore
from   PySide6                                   import QtGui
from   PySide6                                   import QtWidgets
from   PySide6 . QtCore                          import *
from   PySide6 . QtGui                           import *
from   PySide6 . QtWidgets                       import *
from   AITK    . Qt6                             import *
##############################################################################
from   AITK    . Essentials . Relation           import Relation
from   AITK    . Calendars  . StarDate           import StarDate
from   AITK    . Calendars  . Periode            import Periode
from   AITK    . People     . People             import People
from   AITK    . People     . Sex . SexPositions import SexPositions as SexPositionsItem
##############################################################################
class SexPositionListings      ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitAllNames        = Signal ( dict                                        )
  ShowPersonalGallery = Signal ( str , int , str  ,       QIcon              )
  ShowPersonalIcons   = Signal ( str , int , str  , str , QIcon              )
  ShowGalleries       = Signal ( str , int , str  ,       QIcon              )
  ShowVideoAlbums     = Signal ( str , int , str  ,       QIcon              )
  OpenLogHistory      = Signal ( str , str , str  , str , str                )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "SexPositionListings"
    self . FetchTableKey      = self . ClassTag
    self . GType              = 210
    self . SortOrder          = "asc"
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 45
    ##########################################################################
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . POSTURE            = SexPositionsItem (                           )
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "SexPosition"                           )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
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
    self . setMinimumSize          ( 80 , 80                                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendToolNamingAction   (                                        )
    self . AppendSideActionWithIcon ( "Search"                             , \
                                      ":/images/search.png"                , \
                                      self . Search                        , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "PersonalGallery"                    , \
                                      ":/images/gallery.png"               , \
                                      self . OpenPersonalGallery             )
    self . AppendSideActionWithIcon ( "Galleries"                          , \
                                      ":/images/galleries.png"             , \
                                      self . OpenPersonalGalleries           )
    ##########################################################################
    self . AppendSideActionWithIcon ( "Videos"                             , \
                                      ":/images/video.png"                 , \
                                      self . OpenPersonalAlbums              )
    ##########################################################################
    self . AppendSideActionWithIcon ( "Description"                        , \
                                      ":/images/notes.png"                 , \
                                      self . GotoItemNote                    )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . restart         , Enabled      )
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
    return
  ############################################################################
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked              ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 ]                      ) :
      return
    ##########################################################################
    line = self . setLineEdit   ( item                                     , \
                                  0                                        , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
    line . setFocus             ( Qt . TabFocusReason                        )
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "SexPositionListings" , 1                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                 ( self , UUID , NAME , BRUSH             ) :
    ##########################################################################
    IT   = self . PrepareUuidItem ( 0    , UUID , NAME                       )
    ##########################################################################
    for COL in range              ( 0 , self . columnCount (             ) ) :
      ########################################################################
      IT . setBackground          ( COL , BRUSH                              )
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
    CNT    = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U                                      , \
                                    NAMEs [ U ]                            , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
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
    RELTAB = self . Tables                   [ "RelationGroups"              ]
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
  def looking                         ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    if                                ( self . isOriginal ( )              ) :
      self . SearchingForT2           ( name                                 ,
                                        "SexPosition"                        ,
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
    RELTAB  = self . Tables           [ "RelationGroups"                     ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    LIC     = self . getLocality      (                                      )
    LNAME   = name . lower            (                                      )
    LIKE    = f"%{LNAME}%"
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
                  and ( lower ( convert ( `name` using utf8 ) ) like %s )
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
  def FetchRegularDepotCount             ( self , DB                       ) :
    ##########################################################################
    SEXTAB = self . Tables               [ "SexPosition"                     ]
    ##########################################################################
    return self . POSTURE . CountOptions (        DB , SEXTAB                )
  ############################################################################
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "RelationGroups"                  ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "RelationGroups"                  ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery                  ( self                             ) :
    ##########################################################################
    SEXTAB = self . Tables              [ "SexPosition"                      ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder     (                                    )
    ##########################################################################
    return self . POSTURE . QuerySyntax ( SEXTAB , ORDER , STID , AMOUNT     )
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
    mtype   = "sexposition/uuids"
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
    formats = "sexposition/uuids"
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
    if                               ( mtype in [ "sexposition/uuids"    ] ) :
      self . ShowMenuItemTitleStatus ( "SexPositionFrom" , title , CNT       )
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
    ## atItem = self . itemAt     ( mousePos                                    )
    ## mtype  = self . DropInJSON [ "Mime"                                      ]
    ##########################################################################
    return True
  ############################################################################
  def acceptSexPositionsDrop ( self                                        ) :
    return True
  ############################################################################
  def dropSexPositions ( self , source , pos , JSOX                        ) :
    ##########################################################################
    if                 ( "UUIDs" not in JSOX                               ) :
      return True
    ##########################################################################
    UUIDs  = JSOX      [ "UUIDs"                                             ]
    if                 ( len ( UUIDs ) <= 0                                ) :
      return True
    ##########################################################################
    self . Go          ( self . AppendingSexPositions , ( UUIDs , )          )
    ##########################################################################
    return True
  ############################################################################
  def AppendingSexPositions     ( self , UUIDs                             ) :
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
    FMT    = self . getMenuItem ( "JoinSexPosition"                          )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationGroups"                           ]
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
    RELTAB = self . Tables            [ "RelationGroups"                     ]
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
    TITLE  = "RemoveSexPositionItems"
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
    SEXTAB = self . Tables    [ "SexPosition"                                ]
    RELTAB = self . Tables    [ "RelationGroups"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ SEXTAB , RELTAB , NAMTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( SEXTAB , "uuid" , 5431236238719400000        )
      DB   . AppendUuid       ( SEXTAB , uuid                                )
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
    SEXTAB = self . Tables    [ "SexPosition"                                ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ SEXTAB , NAMTAB                          ] )
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
      uuid = DB . LastUuid    ( SEXTAB , "uuid" , 5431236238719400000        )
      DB   . AppendUuid       ( SEXTAB , uuid                                )
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
      SCOPE = f"SexPositionListings-{SCOPE}"
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
    SCOPE  = f"SexPositionListings-{SCOPE}"
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
  def OpenItemGalleries         ( self , item                              ) :
    ##########################################################################
    uuid = item . data          ( 0 , Qt . UserRole                          )
    uuid = int                  ( uuid                                       )
    text = item . text          ( 0                                          )
    icon = self . windowIcon    (                                            )
    xsid = str                  ( uuid                                       )
    ##########################################################################
    self . ShowGalleries . emit ( text , self . GType , xsid , icon          )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalGalleries     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self . OpenItemGalleries    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenGalleryItem                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( 0 , Qt . UserRole                    )
    uuid = int                        ( uuid                                 )
    text = item . text                ( 0                                    )
    icon = self . windowIcon          (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , self . GType , xsid , icon    )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalGallery       ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenGalleryItem    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalGalleries     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self . OpenItemGalleries    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenAlbumItem               ( self , item                            ) :
    ##########################################################################
    uuid = item . data            ( 0 , Qt . UserRole                        )
    uuid = int                    ( uuid                                     )
    text = item . text            ( 0                                        )
    icon = self . windowIcon      (                                          )
    xsid = str                    ( uuid                                     )
    ##########################################################################
    self . ShowVideoAlbums . emit ( text , self . GType , xsid , icon        )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalAlbums        ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenAlbumItem      ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNote               ( self , item                             ) :
    ##########################################################################
    uuid = item . data           ( 0 , Qt . UserRole                         )
    uuid = int                   ( uuid                                      )
    head = item . text           ( 0                                         )
    nx   = ""
    ##########################################################################
    if                           ( "Notes" in self . Tables                ) :
      nx = self . Tables         [ "Notes"                                   ]
    ##########################################################################
    self . OpenLogHistory . emit ( head                                    , \
                                   str ( uuid )                            , \
                                   "Description"                           , \
                                   nx                                      , \
                                   str ( self . getLocality ( ) )            )
    ##########################################################################
    return
  ############################################################################
  def GotoItemNote              ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemNote       ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "SexPosition"                      , \
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def FunctionsMenu                  ( self , mm , uuid , item             ) :
    ##########################################################################
    msg  = self . getMenuItem        ( "Functions"                           )
    LOM  = mm   . addMenu            ( msg                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Search"                              )
    ICON = QIcon                     ( ":/images/search.png"                 )
    mm   . addActionFromMenuWithIcon ( LOM , 25351401 , ICON , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
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
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                     ( self , mm , item                    ) :
    ##########################################################################
    if                               ( self . NotOkay ( item )             ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text               ( 0                                     )
    FMT  = TRX                       [ "UI::Belongs"                         ]
    msg  = FMT . format              ( NAME                                  )
    icon = QIcon                     ( ":/images/graphics.png"               )
    COL  = mm . addMenuWithIcon      ( icon , msg                            )
    ##########################################################################
    msg  = self . getMenuItem        ( "CopySexPositionUuid"                 )
    icon = QIcon                     ( ":/images/copy.png"                   )
    mm   . addActionFromMenuWithIcon ( COL , 38521001 , icon , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Icons"                               )
    icon = QIcon                     ( ":/images/pictures.png"               )
    mm   . addActionFromMenuWithIcon ( COL , 38522001 , icon , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem        ( "PersonalGallery"                     )
    icon = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38522002 , icon , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Galleries"                           )
    icon = QIcon                     ( ":/images/galleries.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 38522003 , icon , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Videos"                              )
    icon = QIcon                     ( ":/images/video.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 38522004 , icon , MSG           )
    ##########################################################################
    msg  = self . getMenuItem        ( "Description"                         )
    icon = QIcon                     ( ":/images/documents.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 38523001 , icon , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                   ( self , at , item                   ) :
    ##########################################################################
    if                                ( at == 38521001                     ) :
      ########################################################################
      uuid = item . data              ( 0 , Qt . UserRole                    )
      uuid = int                      ( uuid                                 )
      qApp . clipboard ( ). setText   ( f"{uuid}"                            )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 38522001                     ) :
      ########################################################################
      uuid = item . data              ( 0 , Qt . UserRole                    )
      uuid = int                      ( uuid                                 )
      text = item . text              ( 0                                    )
      icon = self . windowIcon        (                                      )
      ########################################################################
      tail = self . getMenuItem       ( "(Icons)"                            )
      text = f"{text}{tail}"
      ########################################################################
      self . ShowPersonalIcons . emit ( text                                 ,
                                        self . GType                         ,
                                        "Using"                              ,
                                        str ( uuid )                         ,
                                        icon                                 )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 38522002                     ) :
      ########################################################################
      self . OpenGalleryItem          ( item                                 )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 38522003                     ) :
      ########################################################################
      self . OpenItemGalleries        ( item                                 )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 38522004                     ) :
      ########################################################################
      self . OpenAlbumItem            ( item                                 )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 38523001                     ) :
      ########################################################################
      self . OpenItemNote             ( item                                 )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared ( )         ) :
      return False
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager               ( self                                )
    ##########################################################################
    if                                 ( self . isSearching ( )            ) :
      ########################################################################
      msg  = self . getMenuItem        ( "NotSearch"                         )
      mm   . addAction                 ( 1002 , msg                          )
    ##########################################################################
    mm     = self . AmountIndexMenu    ( mm , True                           )
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1101                           )
    self   . AppendRenameAction        ( mm , 1102                           )
    self   . AppendDeleteAction        ( mm , 1103                           )
    self   . TryAppendEditNamesAction  ( atItem , mm , 1601                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . FunctionsMenu             ( mm , uuid , atItem                  )
    self   . GroupsMenu                ( mm ,        atItem                  )
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    ##########################################################################
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu   ( at , uuid , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu      ( at , atItem                         )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1002                        ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1101                        ) :
      self . InsertItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      self . RenameItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1103                        ) :
      self . DeleteItems               (                                     )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    return True
##############################################################################

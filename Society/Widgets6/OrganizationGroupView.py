# -*- coding: utf-8 -*-
##############################################################################
## OrganizationGroupView
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
from   PySide6                          import QtCore
from   PySide6                          import QtGui
from   PySide6                          import QtWidgets
from   PySide6 . QtCore                 import *
from   PySide6 . QtGui                  import *
from   PySide6 . QtWidgets              import *
from   AITK    . Qt6                    import *
##############################################################################
from   AITK    . Qt6 . IconDock         import IconDock    as IconDock
##############################################################################
from   AITK    . Qt6 . MenuManager      import MenuManager as MenuManager
from   AITK    . Qt6 . LineEdit         import LineEdit    as LineEdit
from   AITK    . Qt6 . ComboBox         import ComboBox    as ComboBox
from   AITK    . Qt6 . SpinBox          import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation  import Relation
from   AITK    . Calendars  . StarDate  import StarDate
from   AITK    . Calendars  . Periode   import Periode
from   AITK    . People     . People    import People
##############################################################################
class OrganizationGroupView     ( IconDock                                 ) :
  ############################################################################
  HavingMenu           = 1371434312
  ############################################################################
  OrganizationSubgroup = Signal ( str , int , str                            )
  OrganizationGroup    = Signal ( str , int , str , str , QIcon              )
  OpenVariantTables    = Signal ( str , str , int , str , dict               )
  emitLog              = Signal ( str                                        )
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( ) . __init__        (        parent        , plan                )
    ##########################################################################
    self . ClassTag      = "OrganizationGroupView"
    self . FetchTableKey = self . ClassTag
    self . GTYPE         = 38
    self . SortOrder     = "asc"
    self . PrivateIcon   = True
    self . PrivateGroup  = True
    self . ExtraINFOs    = True
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace  = Qt . RightDockWidgetArea
    self . dockingPlaces = Qt . TopDockWidgetArea                          | \
                           Qt . BottomDockWidgetArea                       | \
                           Qt . LeftDockWidgetArea                         | \
                           Qt . RightDockWidgetArea
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
    ##########################################################################
    self . Grouping     = "Tag"
    self . OldGrouping  = "Tag"
    ## self . Grouping = "Catalog"
    ## self . Grouping = "Subgroup"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . set         ( "first" , 0                              )
    self . Relation . setT1       ( "Tag"                                    )
    self . Relation . setT2       ( "Subgroup"                               )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . MountClicked           ( 1                                        )
    self . MountClicked           ( 2                                        )
    ##########################################################################
    self . setFunction            ( self . HavingMenu      , True            )
    ##########################################################################
    self . setDragEnabled         ( True                                     )
    self . setAcceptDrops         ( True                                     )
    self . setDragDropMode        ( QAbstractItemView . DragDrop             )
    ##########################################################################
    self . setMinimumSize         ( 180 , 200                                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def PrepareFetchTableKey      ( self                                     ) :
    ##########################################################################
    self . catalogFetchTableKey (                                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions               ( self                               ) :
    ##########################################################################
    ISLIST = ( self . isSubgroup ( ) or self . isReverse ( )                 )
    ##########################################################################
    self   . PrepareFetchTableKey     (                                      )
    self   . AppendToolNamingAction   (                                      )
    self   . AppendSideActionWithIcon ( "Subgroup"                         , \
                                        ":/images/catalog.png"             , \
                                        self . OpenCurrentSubgroup           )
    if                                ( ISLIST                             ) :
      self . AppendSideActionWithIcon ( "SIG"                              , \
                                        ":/images/lists.png"               , \
                                        self . OpenOrganizationGroup         )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "OrganizationGroupParameter"                 )
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
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Font"       , self . ChangeItemFont  , Enabled      )
    ##########################################################################
    ## self . TellStory  (                                         Enabled      )
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
    self . setActionLabel    ( "Label" , ""                                  )
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item                              ) :
    ##########################################################################
    self . defaultSingleClicked (        item                                )
    ##########################################################################
    return True
  ############################################################################
  def doubleClicked                ( self , item                           ) :
    return self . OpenItemSubgroup (        item                             )
  ############################################################################
  def GetUuidIcon                    ( self , DB , Uuid                    ) :
    ##########################################################################
    TABLE = "RelationPictures"
    ##########################################################################
    return self . catalogGetUuidIcon (        DB , Uuid , TABLE              )
  ############################################################################
  def ObtainUuidsQuery                    ( self                           ) :
    return self . catalogObtainUuidsQuery (                                  )
  ############################################################################
  def ObtainSubgroupUuids                  ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `position` {ORDER}"
    RELTAB = self . Tables                 [ "Relation"                      ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainReverseUuids                   ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `reverse` {ORDER}"
    RELTAB = self . Tables                 [ "Relation"                      ]
    ##########################################################################
    return self . Relation . GetOwners     ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isTagging ( )         ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    if                                      ( self . isReverse ( )         ) :
      return self . ObtainReverseUuids      ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "organizationgroup/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , mtype , message                    )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    if                        ( self . isTagging ( )                       ) :
      ########################################################################
      formats = "picture/uuids;organizationgroup/uuids"
      ########################################################################
    else                                                                     :
      ########################################################################
      formats = "picture/uuids;organization/uuids;organizationgroup/uuids"
    ##########################################################################
    if                        ( len ( formats ) <= 0                       ) :
      return False
    ##########################################################################
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    atItem  = self . itemAt         ( mousePos                               )
    CNT     = len                   ( UUIDs                                  )
    title   = sourceWidget . windowTitle (                                   )
    ##########################################################################
    if                              ( mtype in [ "picture/uuids"         ] ) :
      ########################################################################
      self  . ShowMenuItemMessage   ( "AssignTagIcon"                        )
    ##########################################################################
    elif                            ( mtype in [ "organization/uuids" ]    ) :
      ########################################################################
      if                            ( self . isTagging ( )                 ) :
        return False
    ##########################################################################
    elif                            ( mtype in ["organizationgroup/uuids"] ) :
      ########################################################################
      if                            ( self == sourceWidget                 ) :
        self . ShowMenuItemCountStatus ( "MoveCatalogues" ,         CNT      )
      else                                                                   :
        self . ShowMenuItemTitleStatus ( "JoinCatalogues" , title , CNT      )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                                ( self . droppingAction              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON       [ "Mime"                               ]
    UUIDs   = self . DropInJSON       [ "UUIDs"                              ]
    atItem  = self . itemAt           ( mousePos                             )
    CNT     = len                     ( UUIDs                                )
    title   = sourceWidget . windowTitle (                                   )
    ##########################################################################
    if                                ( mtype in [ "organization/uuids" ]  ) :
      ########################################################################
      if                              ( self . isTagging ( )               ) :
        return False
      ########################################################################
      if                              ( self . NotOkay ( atItem )          ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus ( "JoinOrganization"  , title , CNT    )
      ########################################################################
      return True
    ##########################################################################
    if                                ( sourceWidget != self               ) :
      return True
    ##########################################################################
    if                                ( self . NotOkay      ( atItem     ) ) :
      return True
    ##########################################################################
    if                                ( atItem . isSelected (            ) ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def acceptOrganizationGroupsDrop ( self                                  ) :
    return True
  ############################################################################
  def acceptOrganizationsDrop      ( self                                  ) :
    return True
  ############################################################################
  def acceptPictureDrop            ( self                                  ) :
    return True
  ############################################################################
  def dropOrganizationGroups        ( self , source , pos , JSON           ) :
    MF   = self . OrganizationGroupsMoving
    AF   = self . OrganizationGroupsAppending
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def dropOrganizations                 ( self , source , pos , JSON       ) :
    FUNC = self . OrganizationAppending
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def dropPictures                      ( self , source , pos , JSON       ) :
    FUNC = self . AssignTaggingIcon
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def GetLastestPosition                      ( self , DB , LUID           ) :
    ##########################################################################
    RELTAB = "Relation"
    ##########################################################################
    if                                        ( self . isReverse ( )       ) :
      return self . GetReverseLastestPosition ( DB , RELTAB , LUID           )
    return   self . GetNormalLastestPosition  ( DB , RELTAB , LUID           )
  ############################################################################
  def GenerateMovingSQL                   ( self   , LAST , UUIDs          ) :
    ##########################################################################
    RELTAB = "Relation"
    R      = self . isReverse             (                                  )
    ##########################################################################
    return self . GenerateNormalMovingSQL ( RELTAB , LAST , UUIDs , R        )
  ############################################################################
  def OrganizationGroupsMoving ( self , atUuid , NAME , JSON               ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    DB     . LockWrites       ( [ RELTAB                                   ] )
    ##########################################################################
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs            [ -1                                           ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteSqlCommands ( "OrganizePositions" , DB , SQLs , 100      )
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
  def OrganizationGroupsAppending ( self , atUuid , NAME , JSON            ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( DB == None                                ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "Relation"                                  ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . Relation  . Joins ( DB , RELTAB , UUIDs                         )
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs             [ -1                                          ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteSqlCommands ( "OrganizePositions" , DB , SQLs , 100      )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . loading           (                                             )
    ##########################################################################
    return
  ############################################################################
  def OrganizationAppending ( self , atUuid , NAME , JSON                  ) :
    ##########################################################################
    T1   = "Subgroup"
    TAB  = "RelationEditing"
    ##########################################################################
    OK   = self . AppendingOrganizationIntoT1 ( atUuid                     , \
                                                NAME                       , \
                                                JSON                       , \
                                                TAB                        , \
                                                T1                           )
    if                      ( not OK                                       ) :
      return
    ##########################################################################
    self . loading          (                                                )
    ##########################################################################
    return
  ############################################################################
  def AssignTaggingIcon             ( self , atUuid , NAME , JSON          ) :
    ##########################################################################
    TABLE = "RelationPictures"
    self . catalogAssignTaggingIcon (        atUuid , NAME , JSON , TABLE    )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems             ( self , UUIDs                               ) :
    ##########################################################################
    self . catalogRemoveItems (        UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( self . isTagging ( )                       ) :
      return
    ##########################################################################
    self . defaultDeleteItems (                                              )
    ##########################################################################
    return
  ############################################################################
  def AppendGroupsFromLINEs         ( self , LINEs                         ) :
    ##########################################################################
    if                              ( len ( LINEs ) <= 0                   ) :
      return
    ##########################################################################
    GROUPs     =                    [                                        ]
    ##########################################################################
    for L in LINEs                                                           :
      ########################################################################
      L        = L . replace        ( "\r" , ""                              )
      L        = L . replace        ( "\n" , ""                              )
      L        = L . strip          (                                        )
      ########################################################################
      if                            ( len ( L ) > 0                        ) :
        GROUPs . append             ( L                                      )
    ##########################################################################
    if                              ( len ( GROUPs ) <= 0                  ) :
      return
    ##########################################################################
    DB         = self . ConnectDB   (                                        )
    if                              ( DB in self . EmptySet                ) :
      return
    ##########################################################################
    self       . OnBusy  . emit     (                                        )
    self       . setBustle          (                                        )
    ##########################################################################
    for L in GROUPs                                                          :
      ########################################################################
      self     . AppendItemNameToDB ( DB , L                                 )
    ##########################################################################
    self       . setVacancy         (                                        )
    self       . GoRelax . emit     (                                        )
    DB         . Close              (                                        )
    ##########################################################################
    self       . loading            (                                        )
    ##########################################################################
    return
  ############################################################################
  def AppendGroupsFromText        ( self , TEXT                            ) :
    ##########################################################################
    if                            ( len ( TEXT ) <= 0                      ) :
      return
    ##########################################################################
    self  . AppendGroupsFromLINEs ( TEXT . splitlines (                    ) )
    ##########################################################################
    return
  ############################################################################
  def PasteItems                       ( self                              ) :
    ##########################################################################
    TEXT = qApp . clipboard ( ) . text (                                     )
    self . Go                          ( self . AppendGroupsFromText       , \
                                         ( TEXT                          , ) )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard                 ( self                               ) :
    ##########################################################################
    ITEMs   = self . selectedItems    (                                      )
    UXIDs   =                         [                                      ]
    ##########################################################################
    for IT in ITEMs                                                          :
      ########################################################################
      UUID  = IT . data               ( Qt . UserRole                        )
      UUID  = int                     ( UUID                                 )
      UXIDs . append                  ( f"{UUID}"                            )
    ##########################################################################
    ULEN    = len                     ( UXIDs                                )
    ##########################################################################
    if                                ( ULEN <= 0                          ) :
      return
    ##########################################################################
    TEXT    = "\n" . join             ( UXIDs                                )
    qApp    . clipboard ( ) . setText ( TEXT                                 )
    ##########################################################################
    FMT     = self    . getMenuItem   ( "CopyUuidsToClipboard"               )
    MSG     = FMT     . format        ( ULEN                                 )
    self    . emitLog . emit          ( MSG                                  )
    self    . statusMessage           ( MSG                                  )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemName             ( self ,           item , uuid , name     ) :
    ##########################################################################
    self . UpdateItemNameByTable ( "NamesEditing" , item , uuid , name       )
    ##########################################################################
    return
  ############################################################################
  def AppendTagItem          ( self , DB                                   ) :
    ##########################################################################
    TAGTAB = self . Tables   [ "Tags"                                        ]
    uuid   = DB   . LastUuid ( TAGTAB , "uuid" , 2800000000000000000         )
    DB     . AddUuid         ( TAGTAB ,  uuid  , self . GTYPE                )
    ##########################################################################
    return uuid
  ############################################################################
  def AppendSubgroupItem     ( self , DB                                   ) :
    ##########################################################################
    SUBTAB = self . Tables   [ "Subgroups"                                   ]
    uuid   = DB   . LastUuid ( SUBTAB , "uuid" , 2800004000000000000         )
    DB     . AddUuid         ( SUBTAB ,  uuid  , self . GTYPE                )
    ##########################################################################
    return uuid
  ############################################################################
  def AppendItemNameToDB                 ( self , DB , name                ) :
    ##########################################################################
    TAGTAB   = self . Tables             [ "Tags"                            ]
    SUBTAB   = self . Tables             [ "Subgroups"                       ]
    NAMTAB   = self . Tables             [ "NamesEditing"                    ]
    RELTAB   = self . Tables             [ "RelationEditing"                 ]
    TABLES   =                           [ NAMTAB , RELTAB                   ]
    ##########################################################################
    if                                   ( self . isTagging ( )            ) :
      ########################################################################
      TABLES . append                    ( TAGTAB                            )
      T1     =  75
      T2     = 158
      RR     =   1
      ########################################################################
    else                                                                     :
      ########################################################################
      TABLES . append                    ( SUBTAB                            )
      T1     = self . Relation . get     ( "t1"                              )
      T2     = self . Relation . get     ( "t2"                              )
      RR     = self . Relation . get     ( "relation"                        )
    ##########################################################################
    DB       . LockWrites                ( TABLES                            )
    ##########################################################################
    if                                   ( self . isTagging ( )            ) :
      uuid   = self . AppendTagItem      ( DB                                )
    else                                                                     :
      ########################################################################
      uuid   = self . AppendSubgroupItem ( DB                                )
      ########################################################################
      REL    = Relation                  (                                   )
      REL    . set                       ( "relation" , RR                   )
      ########################################################################
      if                                 ( self . isSubgroup ( )           ) :
        ######################################################################
        PUID = self . Relation . get     ( "first"                           )
        REL  . set                       ( "first"    , PUID                 )
        REL  . set                       ( "second"   , uuid                 )
        REL  . set                       ( "t1"       , T1                   )
        REL  . set                       ( "t2"       , 158                  )
        ######################################################################
      elif                               ( self . isReverse  ( )           ) :
        ######################################################################
        PUID = self . Relation . get     ( "second"                          )
        REL  . set                       ( "first"    , uuid                 )
        REL  . set                       ( "second"   , PUID                 )
        REL  . set                       ( "t1"       , 158                  )
        REL  . set                       ( "t2"       , T2                   )
      ########################################################################
      REL    . Join                      ( DB , RELTAB                       )
    ##########################################################################
    self     . AssureUuidNameByLocality  ( DB                              , \
                                           NAMTAB                          , \
                                           uuid                            , \
                                           name                            , \
                                           self . getLocality ( )            )
    ##########################################################################
    DB       . UnlockTables              (                                   )
    ##########################################################################
    FMT      = self . getMenuItem        ( "AppendCatalogue"                 )
    MSG      = FMT  . format             ( name , uuid                       )
    self     . emitLog . emit            ( MSG                               )
    ##########################################################################
    return uuid
  ############################################################################
  def AppendItemName                 ( self , item , name                  ) :
    ##########################################################################
    DB    = self . ConnectDB         (                                       )
    if                               ( DB in self . EmptySet               ) :
      return
    ##########################################################################
    uuid = self . AppendItemNameToDB ( DB   ,        name                    )
    ##########################################################################
    DB   . Close                     (                                       )
    ##########################################################################
    self . PrepareItemContent        ( item , uuid , name                    )
    self . assignToolTip             ( item , str ( uuid )                   )
    self . Notify                    ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def FetchExtraInformations           ( self , UUIDs                      ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return
    ##########################################################################
    FMT        = self . getMenuItem    ( "LoadExtras"                        )
    SFMT       = self . getMenuItem    ( "SubgroupCount"                     )
    GFMT       = self . getMenuItem    ( "OrganizationCount"                 )
    ##########################################################################
    DBA        = self . ConnectDB      (                  True               )
    ##########################################################################
    if                                 ( DBA == None                       ) :
      return
    ##########################################################################
    DBG        = self . ConnectHost    ( self . GroupDB , True               )
    ##########################################################################
    if                                 ( DBG == None                       ) :
      DBA      . Close                 (                                     )
      return
    ##########################################################################
    RELTAB     = self . Tables         [ "Relation"                          ]
    REL        = Relation              (                                     )
    REL        . setRelation           ( "Subordination"                     )
    T2         = self . Relation . get ( "t2"                                )
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . StayAlive              ) :
        continue
      ########################################################################
      if                               ( U not in self . UuidItemMaps      ) :
        continue
      ########################################################################
      item     = self . UuidItemMaps   [ U                                   ]
      JSOX     = self . itemJson       ( item                                )
      ########################################################################
      if                               ( "Name" in JSOX                    ) :
        ######################################################################
        title  = JSOX                  [ "Name"                              ]
        ######################################################################
        if                             ( len ( title ) > 0                 ) :
          ####################################################################
          MSG  = FMT . format          ( title                               )
          self . ShowStatus            ( MSG                                 )
      ########################################################################
      REL      . set                   ( "first" , U                         )
      ########################################################################
      REL      . set                   ( "t1"    , T2                        )
      REL      . set                   ( "t2"    , 158                       )
      SCNT     = REL  . CountSecond    ( DBA     , RELTAB                    )
      SMSG     = SFMT . format         ( SCNT                                )
      ########################################################################
      REL      . set                   ( "t1"    , T2                        )
      REL      . setT2                 ( "Organization"                      )
      GCNT     = REL  . CountSecond    ( DBG     , RELTAB                    )
      GMSG     = GFMT . format         ( GCNT                                )
      ########################################################################
      tooltip  = f"{U}\n{SMSG}\n{GMSG}"
      self     . assignToolTip         ( item    , tooltip                   )
    ##########################################################################
    DBG        . Close                 (                                     )
    DBA        . Close                 (                                     )
    self       . Notify                ( 2                                   )
    self       . ShowStatus            ( ""                                  )
    ##########################################################################
    return
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage             ( self                               ) :
    ##########################################################################
    OKAY = catalogUpdateLocalityUsage (                                      )
    self . emitRestart . emit         (                                      )
    ##########################################################################
    return OKAY
  ############################################################################
  def ReloadLocality                    ( self , DB                        ) :
    return self . catalogReloadLocality (        DB                          )
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Organizations" , "NamesEditing" )
    ##########################################################################
    return
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
      ########################################################################
      if                               ( self . isTagging  (             ) ) :
        ######################################################################
        UUID = self . Relation  . get  ( "first"                             )
        TYPE = self . Relation  . get  ( "t1"                                )
        TYPE = int                     ( TYPE                                )
        ######################################################################
      elif                             ( self . isSubgroup (             ) ) :
        ######################################################################
        UUID = self . Relation  . get  ( "first"                             )
        TYPE = self . Relation  . get  ( "t1"                                )
        TYPE = int                     ( TYPE                                )
        ######################################################################
      elif                             ( self . isReverse  (             ) ) :
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
  def OpenItemSubgroup            ( self , item                            ) :
    ##########################################################################
    uuid  = item . data           ( Qt . UserRole                            )
    uuid  = int                   ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return False
    ##########################################################################
    title = item . text           (                                          )
    tid   = self . Relation . get ( "t2"                                     )
    self  . OrganizationSubgroup . emit  ( title , tid , str ( uuid )        )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentSubgroup          ( self                                  ) :
    ##########################################################################
    atItem = self . currentItem    (                                         )
    ##########################################################################
    if                             ( atItem == None                        ) :
      return False
    ##########################################################################
    return self . OpenItemSubgroup ( atItem                                  )
  ############################################################################
  def OpenOrganizationGroup          ( self                                ) :
    ##########################################################################
    atItem = self . currentItem      (                                       )
    if                               ( self . NotOkay ( atItem )           ) :
      return
    ##########################################################################
    self . OpenItemOrganizationGroup ( atItem                                )
    ##########################################################################
    return
  ############################################################################
  def OpenItemOrganizationGroup   ( self , item                            ) :
    ##########################################################################
    uuid  = item . data           ( Qt . UserRole                            )
    uuid  = int                   ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return False
    ##########################################################################
    icon    = item . icon         (                                          )
    title   = item . text         (                                          )
    tid     = self . Relation   . get ( "t2"                                 )
    related = "Subordination"
    self    . OrganizationGroup . emit ( title                             , \
                                         tid                               , \
                                         str ( uuid )                      , \
                                         related                           , \
                                         icon                                )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentOrganizationGroup          ( self                         ) :
    ##########################################################################
    atItem = self . currentItem             (                                )
    ##########################################################################
    if                                      ( atItem == None               ) :
      return False
    ##########################################################################
    return self . OpenItemOrganizationGroup ( atItem                         )
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
    if ( self . WithinCommand ( language , "UI::OpenSubgroup" , message )  ) :
      if            ( self . OpenCurrentSubgroup ( )                       ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::OpenAlbums"   , message )  ) :
      if            ( self . OpenCurrentCrowd ( )                          ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    ##########################################################################
    return          { "Match" : False                                        }
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    if                                ( not self . isPrepared ( )          ) :
      return False
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                    )
    if                                ( not doMenu                         ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu             ( mm                                   )
    ##########################################################################
    if                                ( uuid > 0                           ) :
      ########################################################################
      ic   = QIcon                    ( ":/images/catalog.png"               )
      mg   = self . getMenuItem       ( "Subgroup"                           )
      mm   . addActionWithIcon        ( 2001 , ic , mg                       )
      ########################################################################
      if                              ( self . isSubgroup ( )              ) :
        ######################################################################
        ic = QIcon                    ( ":/images/lists.png"                 )
        mg = self . getMenuItem       ( "SIG"                                )
        mm . addActionWithIcon        ( 2002 , ic , mg                       )
      ########################################################################
      mm   . addSeparator             (                                      )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    if                                ( uuid > 0                           ) :
      ########################################################################
      self . AppendRenameAction       ( mm , 1102                            )
      self . AssureEditNamesAction    ( mm , 1601 , atItem                   )
    ##########################################################################
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . FunctionsMenu            ( mm , uuid , atItem                   )
    self   . SortingMenu              ( mm                                   )
    self   . LocalityMenu             ( mm                                   )
    self   . ScrollBarMenu            ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunDocking        ( mm , aa                              )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu  ( at , uuid , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu    ( at                                   )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunScrollBarMenu  ( at                                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu   ( at                                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1101                         ) :
      self . InsertItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1102                         ) :
      self . RenameItem               (                                      )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor ( at , 1601 , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                                ( at == 2001                         ) :
      ########################################################################
      self . OpenItemSubgroup         ( atItem                               )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 2002                         ) :
      ########################################################################
      self . OpenItemOrganizationGroup ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

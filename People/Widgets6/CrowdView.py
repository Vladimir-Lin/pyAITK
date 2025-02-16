# -*- coding: utf-8 -*-
##############################################################################
## CrowdView
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
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Qt6        . IconDock    import IconDock    as IconDock
##############################################################################
from   AITK    . Qt6        . MenuManager import MenuManager as MenuManager
from   AITK    . Qt6        . LineEdit    import LineEdit    as LineEdit
from   AITK    . Qt6        . ComboBox    import ComboBox    as ComboBox
from   AITK    . Qt6        . SpinBox     import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation    import Relation
from   AITK    . Calendars  . StarDate    import StarDate
from   AITK    . Calendars  . Periode     import Periode
from   AITK    . People     . People      import People      as PeopleItem
##############################################################################
class CrowdView              ( IconDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  CrowdSubgroup     = Signal ( str , int , str                               )
  PeopleGroup       = Signal ( str , int , str                               )
  OpenVariantTables = Signal ( str , str , int , str , dict                  )
  OpenLogHistory    = Signal ( str , str , str , str , str                   )
  emitLog           = Signal ( str                                           )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . ClassTag     = "CrowdView"
    self . GTYPE        = 7
    self . SortOrder    = "asc"
    self . PrivateIcon  = True
    self . PrivateGroup = True
    self . ExtraINFOs   = True
    ##########################################################################
    self . GroupBtn     = None
    self . PeopleBtn    = None
    self . NameBtn      = None
    ##########################################################################
    self . dockingPlace = Qt . RightDockWidgetArea
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
    ##########################################################################
    self . Grouping     = "Tag"
    self . OldGrouping  = "Tag"
    ## self . Grouping     = "Catalog"
    ## self . Grouping     = "Subgroup"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . FetchTableKey = "CrowdView"
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . set         ( "first" , 0                              )
    self . Relation . set         ( "t1"    , 75                             )
    self . Relation . set         ( "t2"    , 158                            )
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
  def PrepareForActions                     ( self                         ) :
    ##########################################################################
    self . PrepareFetchTableKey             (                                )
    ##########################################################################
    msg    = self . getMenuItem             ( "Subgroup"                     )
    A      = QAction                        (                                )
    IC     = QIcon                          ( ":/images/catalog.png"         )
    A      . setIcon                        ( IC                             )
    A      . setToolTip                     ( msg                            )
    A      . triggered . connect            ( self . OpenCurrentSubgroup     )
    A      . setEnabled                     ( False                          )
    ##########################################################################
    self   . GroupBtn  = A
    ##########################################################################
    self   . WindowActions . append         ( A                              )
    ##########################################################################
    if                                      ( self . isCatalogue (       ) ) :
      ########################################################################
      msg  = self . getMenuItem             ( "Crowds"                       )
      A    = QAction                        (                                )
      ICON = QIcon                          ( ":/images/buddy.png"           )
      A    . setIcon                        ( ICON                           )
      A    . setToolTip                     ( msg                            )
      A    . triggered . connect            ( self . OpenCurrentCrowd        )
      A    . setEnabled                     ( False                          )
      ########################################################################
      self . PeopleBtn = A
      ########################################################################
      self . WindowActions . append         ( A                              )
    ##########################################################################
    self   . AppendToolNamingAction         (                                )
    self   . NameBtn = self . WindowActions [ -1                             ]
    self   . NameBtn . setEnabled           ( False                          )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "CrowdViewParameter"                         )
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
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Copy"       , self . DoCopyItemText  , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    self . LinkAction ( "Font"       , self . ChangeItemFont  , Enabled      )
    ##########################################################################
    self . TellStory  (                                         Enabled      )
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
    ## self . LinkVoice         ( self . CommandParser                          )
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
      ## self . LinkVoice         ( None                                        )
    ##########################################################################
    return False
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    ## self . LinkVoice         ( None                                          )
    self . defaultCloseEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def setGrouping ( self , group                                           ) :
    ##########################################################################
    self . Grouping      = group
    self . OldGrouping   = group
    self . FetchTableKey = f"CrowdView-{group}"
    ##########################################################################
    return self . Grouping
  ############################################################################
  def GetUuidIcon                    ( self , DB , Uuid                    ) :
    ##########################################################################
    TABLE = "RelationPictures"
    ##########################################################################
    return self . catalogGetUuidIcon (        DB , Uuid , TABLE              )
  ############################################################################
  def SwitchSideTools ( self , Enabled                                     ) :
    ##########################################################################
    if                ( self . GroupBtn  not in self . EmptySet            ) :
      ########################################################################
      self . GroupBtn  . setEnabled ( Enabled                                )
    ##########################################################################
    if                ( self . PeopleBtn not in self . EmptySet            ) :
      ########################################################################
      self . PeopleBtn . setEnabled ( Enabled                                )
    ##########################################################################
    if                ( self . NameBtn   not in self . EmptySet            ) :
      ########################################################################
      self . NameBtn   . setEnabled ( Enabled                                )
    ##########################################################################
    return
  ############################################################################
  def singleClicked        ( self , item                                   ) :
    ##########################################################################
    self . Notify          ( 0                                               )
    self . SwitchSideTools ( True                                            )
    ##########################################################################
    return True
  ############################################################################
  def selectionsChanged            ( self                                  ) :
    ##########################################################################
    OKAY = self . isEmptySelection (                                         )
    self . SwitchSideTools         ( OKAY                                    )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked                ( self , item                           ) :
    return self . OpenItemSubgroup (        item                             )
  ############################################################################
  def ObtainUuidsQuery                    ( self                           ) :
    return self . catalogObtainUuidsQuery (                                  )
  ############################################################################
  def ObtainSubgroupUuids                  ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `position` {ORDER}"
    RELTAB = self . Tables                 [ "RelationGroup"                 ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainReverseUuids                   ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `reverse` {ORDER}"
    RELTAB = self . Tables                 [ "RelationGroup"                 ]
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
    mtype   = "crowd/uuids"
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
      formats = "picture/uuids;crowd/uuids"
      ########################################################################
    else                                                                     :
      ########################################################################
      formats = "picture/uuids;people/uuids;crowd/uuids"
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
    elif                            ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      if                            ( self . isTagging ( )                 ) :
        return False
    ##########################################################################
    elif                            ( mtype in [ "crowd/uuids" ]           ) :
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
    if                                ( mtype in [ "people/uuids" ]        ) :
      ########################################################################
      if                              ( self . isTagging ( )               ) :
        return False
      ########################################################################
      if                              ( self . NotOkay ( atItem )          ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus ( "JoinPeople"  , title , CNT          )
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
  def acceptCrowdsDrop  ( self                                             ) :
    return True
  ############################################################################
  def acceptPeopleDrop  ( self                                             ) :
    return True
  ############################################################################
  def acceptPictureDrop ( self                                             ) :
    return True
  ############################################################################
  def dropCrowds                    ( self , source , pos , JSON           ) :
    MF   = self . CrowdsMoving
    AF   = self . CrowdsAppending
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def dropPeople                        ( self , source , pos , JSON       ) :
    FUNC = self . PeopleAppending
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
  def CrowdsMoving            ( self , atUuid , NAME , JSON                ) :
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
  def CrowdsAppending         ( self , atUuid , NAME , JSON               ) :
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
  def PeopleAppending                  ( self , atUuid , NAME , JSON       ) :
    ##########################################################################
    T1  = "Subgroup"
    TAB = "RelationPeople"
    ##########################################################################
    OK  = self . AppendingPeopleIntoT1 ( atUuid , NAME , JSON , TAB , T1     )
    if                                 ( not OK                            ) :
      return
    ##########################################################################
    self   . loading                   (                                     )
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
  def PasteItems                   ( self                                  ) :
    ##########################################################################
    print("PasteItems")
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard              ( self                                  ) :
    ##########################################################################
    print("CopyToClipboard")
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
  def AppendItemName                     ( self , item , name              ) :
    ##########################################################################
    DB       = self . ConnectDB          (                                   )
    if                                   ( DB == None                      ) :
      return
    ##########################################################################
    TAGTAB   = self . Tables             [ "Tags"                            ]
    SUBTAB   = self . Tables             [ "Subgroups"                       ]
    NAMTAB   = self . Tables             [ "NamesEditing"                    ]
    RELTAB   = self . Tables             [ "RelationGroup"                   ]
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
    DB       . Close                     (                                   )
    ##########################################################################
    self     . PrepareItemContent        ( item , uuid , name                )
    self     . assignToolTip             ( item , str ( uuid )               )
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
    GFMT       = self . getMenuItem    ( "PeopleCount"                       )
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
    self       . OnBusy  . emit        (                                     )
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
      REL      . setT2                 ( "People"                            )
      GCNT     = REL  . CountSecond    ( DBG     , RELTAB                    )
      GMSG     = GFMT . format         ( GCNT                                )
      ########################################################################
      tooltip  = f"{U}\n{SMSG}\n{GMSG}"
      self     . assignToolTip         ( item    , tooltip                   )
    ##########################################################################
    self       . GoRelax . emit        (                                     )
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
    self  . CrowdSubgroup . emit  ( title , tid , str ( uuid )               )
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
  def OpenItemCrowd               ( self , item                            ) :
    ##########################################################################
    uuid  = item . data           ( Qt . UserRole                            )
    uuid  = int                   ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return False
    ##########################################################################
    title = item . text           (                                          )
    tid   = self . Relation . get ( "t2"                                     )
    self  . PeopleGroup . emit    ( title , tid , str ( uuid )               )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentCrowd          ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( atItem == None                           ) :
      return False
    ##########################################################################
    return self . OpenItemCrowd ( atItem                                     )
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Crowds" , "NamesEditing"     )
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
  def FunctionsMenu          ( self , mm , uuid , item                     ) :
    ##########################################################################
    msg = self . getMenuItem ( "Functions"                                   )
    LOM = mm   . addMenu     ( msg                                           )
    ##########################################################################
    msg = self . getMenuItem ( "AssignTables"                                )
    mm  . addActionFromMenu  ( LOM , 25351301 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "LogHistory"                                  )
    mm  . addActionFromMenu  ( LOM , 25351302 , msg                          )
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
    if                                 ( at == 25351302                    ) :
      ########################################################################
      name = item . text               (                                     )
      nx   = ""
      ########################################################################
      if                               ( "Notes" in self . Tables          ) :
        nx = self . Tables             [ "Notes"                             ]
      ########################################################################
      self . OpenLogHistory . emit     ( name                                ,
                                         str ( uuid )                        ,
                                         "Description"                       ,
                                         nx                                  ,
                                         str ( self . getLocality ( ) )      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared ( )        ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu               ( mm                                 )
    ##########################################################################
    if                                  ( uuid > 0                         ) :
      ########################################################################
      mg   = self . getMenuItem         ( "Subgroup"                         )
      mm   . addAction                  ( 2001      , mg                     )
      ########################################################################
      if                                ( self . isSubgroup ( )            ) :
        mg = self . getMenuItem         ( "Crowds"                           )
        ic = QIcon                      ( ":/images/buddy.png"               )
        mm . addActionWithIcon          ( 2002 , ic , mg                     )
      ########################################################################
      mg   = self . getMenuItem         ( "CopyGroupUuid"                    )
      mm   . addAction                  ( 2003      , mg                     )
      ########################################################################
      mm   . addSeparator               (                                    )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    if                                  ( self . IsOkay ( atItem )         ) :
      ########################################################################
      mm   = self . AppendRenameAction  ( mm , 1102                          )
      self . AssureEditNamesAction      ( mm , 1601 , atItem                 )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    self   . FunctionsMenu              ( mm , uuid , atItem                 )
    self   . SortingMenu                ( mm                                 )
    self   . LocalityMenu               ( mm                                 )
    self   . ScrollBarMenu              ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunDocking          ( mm , aa                            )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu    ( at , uuid , atItem                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu  ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu      ( at                                 )
    if                                  ( OKAY                             ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunScrollBarMenu    ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu     ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1101                       ) :
      self . InsertItem                 (                                    )
      return True
    ##########################################################################
    if                                  ( at == 1102                       ) :
      self . RenameItem                 (                                    )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor   ( at , 1601 , atItem                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    if                                  ( at == 2001                       ) :
      ########################################################################
      head = atItem . text              (                                    )
      tid  = self . Relation . get      ( "t2"                               )
      self . CrowdSubgroup . emit       ( head , tid , str ( uuid )          )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 2002                       ) :
      ########################################################################
      head = atItem . text              (                                    )
      tid  = self . Relation . get      ( "t2"                               )
      self . PeopleGroup   . emit       ( head , tid , str ( uuid )          )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 2003                       ) :
      ########################################################################
      qApp . clipboard ( ). setText     ( f"{uuid}"                          )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

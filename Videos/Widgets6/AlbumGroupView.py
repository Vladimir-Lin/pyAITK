# -*- coding: utf-8 -*-
##############################################################################
## AlbumGroupView
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
from   AITK    . Qt6                   import *
##############################################################################
from   AITK    . Essentials . Relation import Relation
from   AITK    . Calendars  . StarDate import StarDate
from   AITK    . Calendars  . Periode  import Periode
from   AITK    . Pictures   . Picture  import Picture     as PictureItem
from   AITK    . Videos     . Album    import Album       as AlbumItem
from   AITK    . Videos     . Film     import Film        as FilmItem
##############################################################################
class AlbumGroupView         ( IconDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  AlbumSubgroup     = Signal ( str , int , str                               )
  AlbumGroup        = Signal ( str , int , str                               )
  ShowPersonalIcons = Signal ( str , int , str , str , QIcon                 )
  OpenVariantTables = Signal ( str , str , int , str , dict                  )
  emitLog           = Signal ( str                                           )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . ClassTag      = "AlbumGroup"
    self . FetchTableKey = "AlbumGroupView"
    self . GTYPE         = 76
    self . SortOrder     = "asc"
    self . PrivateIcon   = True
    self . PrivateGroup  = True
    self . ExtraINFOs    = True
    self . FetchingINFO  = False
    ##########################################################################
    self . Grouping      = "Tag"
    self . OldGrouping   = "Tag"
    ## self . Grouping     = "Catalog"
    ## self . Grouping     = "Subgroup"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace  = Qt . RightDockWidgetArea
    self . dockingPlaces = Qt . TopDockWidgetArea                          | \
                           Qt . BottomDockWidgetArea                       | \
                           Qt . LeftDockWidgetArea                         | \
                           Qt . RightDockWidgetArea
    ##########################################################################
    self . ALBUM    = AlbumItem   (                                          )
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . setT1       ( "Tag"                                    )
    self . Relation . setT2       ( "Subgroup"                               )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . MountClicked           ( 1                                        )
    self . MountClicked           ( 2                                        )
    ##########################################################################
    self . setFunction            ( self . HavingMenu , True                 )
    ##########################################################################
    self . setDragEnabled         ( True                                     )
    self . setAcceptDrops         ( True                                     )
    self . setDragDropMode        ( QAbstractItemView . DragDrop             )
    ##########################################################################
    self . setMinimumSize         ( 144 , 200                                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 660 , 800 )                       )
  ############################################################################
  def PrepareFetchTableKey      ( self                                     ) :
    ##########################################################################
    self . catalogFetchTableKey (                                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions                      ( self                        ) :
    ##########################################################################
    self   . PrepareFetchTableKey            (                               )
    self   . AppendToolNamingAction          (                               )
    self   . AppendSideActionWithIcon        ( "Icons"                     , \
                                               ":/images/foldericon.png"   , \
                                               self . OpenCurrentAlbumIcon   )
    self   . AppendWindowToolSeparatorAction (                               )
    self   . AppendSideActionWithIcon        ( "Subgroup"                  , \
                                               ":/images/filmfolder.png"   , \
                                               self . OpenCurrentSubgroup    )
    if                                       ( self . isCatalogue (      ) ) :
      self . AppendSideActionWithIcon        ( "Albums"                    , \
                                               ":/images/episode.png"      , \
                                               self . OpenCurrentAlbum       )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "AlbumGroupParameter"                        )
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
  def AttachActions   ( self         ,                         Enabled     ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . restart        , Enabled       )
    self . LinkAction ( "Insert"     , self . InsertItem     , Enabled       )
    self . LinkAction ( "Delete"     , self . DeleteItems    , Enabled       )
    self . LinkAction ( "Rename"     , self . RenameItem     , Enabled       )
    self . LinkAction ( "Paste"      , self . PasteItems     , Enabled       )
    self . LinkAction ( "Copy"       , self . DoCopyItemText , Enabled       )
    self . LinkAction ( "Select"     , self . SelectOne      , Enabled       )
    self . LinkAction ( "SelectAll"  , self . SelectAll      , Enabled       )
    self . LinkAction ( "SelectNone" , self . SelectNone     , Enabled       )
    self . LinkAction ( "Font"       , self . ChangeItemFont , Enabled       )
    ##########################################################################
    self . TellStory  (                                        Enabled       )
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
    if                       ( self . AnythingRunning (                  ) ) :
      return False
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . FetchingINFO                         ) :
      return False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , ""                                  )
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    self . clear             (                                               )
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
  def setGrouping ( self , group                                           ) :
    ##########################################################################
    self . Grouping      = group
    self . OldGrouping   = group
    self . FetchTableKey = f"AlbumGroupView-{group}"
    ##########################################################################
    return self . Grouping
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
    RELTAB = self . Tables                 [ "RelationGroup"                 ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainReverseUuids                   ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `reverse` {ORDER}"
    RELTAB = self . Tables                 [ "Relation"                      ]
    ## RELTAB = self . Tables                 [ "RelationGroup"                 ]
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
    mtype   = "albumgroup/uuids"
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
  def allowedMimeTypes     ( self , mime                                   ) :
    ##########################################################################
    FMTs    =              [ "picture/uuids" , "albumgroup/uuids"            ]
    ##########################################################################
    if                     ( not self . isTagging ( )                      ) :
      ########################################################################
      FMTs  . append       ( "album/uuids"                                   )
    ##########################################################################
    if                     ( len ( FMTs ) <= 0                             ) :
      return False
    ##########################################################################
    formats = ";" . join   ( FMTs                                            )
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                            ( self                            , \
                                           sourceWidget                    , \
                                           mimeData                        , \
                                           mousePos                        ) :
    ##########################################################################
    RDN     = self . RegularDropNew      ( mimeData                          )
    if                                   ( not RDN                         ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON          [ "Mime"                            ]
    UUIDs   = self . DropInJSON          [ "UUIDs"                           ]
    atItem  = self . itemAt              ( mousePos                          )
    CNT     = len                        ( UUIDs                             )
    title   = sourceWidget . windowTitle (                                   )
    ##########################################################################
    if                                   ( mtype in [ "picture/uuids"    ] ) :
      ########################################################################
      self  . ShowMenuItemMessage        ( "AssignTagIcon"                   )
    ##########################################################################
    elif                                 ( mtype in [ "album/uuids"      ] ) :
      ########################################################################
      if                                 ( self . isTagging (            ) ) :
        return False
      ########################################################################
      if                                 ( atItem in self . EmptySet       ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus    ( "JoinAlbums"  , title , CNT       )
    ##########################################################################
    elif                                 ( mtype in [ "albumgroup/uuids" ] ) :
      ########################################################################
      if                                 ( self == sourceWidget            ) :
        self . ShowMenuItemCountStatus   ( "MoveCatalogues" ,         CNT    )
      else                                                                   :
        self . ShowMenuItemTitleStatus   ( "JoinCatalogues" , title , CNT    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving                        ( self                             , \
                                          sourceWidget                     , \
                                          mimeData                         , \
                                          mousePos                         ) :
    ##########################################################################
    if                                  ( self . droppingAction            ) :
      return False
    ##########################################################################
    mtype  = self . DropInJSON          [ "Mime"                             ]
    UUIDs  = self . DropInJSON          [ "UUIDs"                            ]
    CNT    = len                        ( UUIDs                              )
    atItem = self . itemAt              ( mousePos                           )
    title  = sourceWidget . windowTitle (                                    )
    ##########################################################################
    if                                  ( mtype in [ "picture/uuids"     ] ) :
      ########################################################################
      if                                ( self == sourceWidget             ) :
        return False
      ########################################################################
      if                                ( atItem in self . EmptySet        ) :
        return False
      ########################################################################
      tname     = atItem . text         (                                    )
      FMT       = self . getMenuItem    ( "AssignTagIconTo"                  )
      MSG       = FMT  . format         ( tname                              )
      self      . ShowStatus            ( MSG                                )
      ########################################################################
      return True
    ##########################################################################
    elif                                ( mtype in [ "album/uuids"       ] ) :
      ########################################################################
      if                                ( self . isTagging (             ) ) :
        return False
      ########################################################################
      if                                ( atItem in self . EmptySet        ) :
        return False
      ########################################################################
      tname     = atItem . text         (                                    )
      FMT       = self . getMenuItem    ( "JoinAlbumsTo"                     )
      MSG       = FMT  . format         ( title , CNT , tname                )
      self      . ShowStatus            ( MSG                                )
      ########################################################################
      return True
    ##########################################################################
    elif                                ( mtype in [ "albumgroup/uuids"  ] ) :
      ########################################################################
      if                                ( self == sourceWidget             ) :
        ######################################################################
        if                              ( atItem in self . EmptySet        ) :
          ####################################################################
          FMT   = self . getMenuItem    ( "MovingEnd"                        )
          MSG   = FMT  . format         ( CNT                                )
          ####################################################################
        else                                                                 :
          ####################################################################
          if                            ( atItem . isSelected (          ) ) :
            return False
          ####################################################################
          tname = atItem . text         (                                    )
          FMT   = self   . getMenuItem  ( "MoveBefore"                       )
          MSG   = FMT    . format       ( CNT , tname                        )
        ######################################################################
      else                                                                   :
        ######################################################################
        if                              ( atItem in self . EmptySet        ) :
          ####################################################################
          FMT   = self . getMenuItem    ( "Appending"                        )
          MSG   = FMT  . format         ( title , CNT                        )
          ####################################################################
        else                                                                 :
          ####################################################################
          tname = atItem . text         (                                    )
          FMT   = self . getMenuItem    ( "AppendBefore"                     )
          MSG   = FMT  . format         ( title , CNT , tname                )
      ########################################################################
      self      . ShowStatus            ( MSG                                )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def acceptAlbumGroupsDrop ( self                                         ) :
    return True
  ############################################################################
  def acceptAlbumsDrop      ( self                                         ) :
    return True
  ############################################################################
  def acceptPictureDrop     ( self                                         ) :
    return True
  ############################################################################
  def dropAlbumGroups               ( self , source , pos , JSON           ) :
    ##########################################################################
    MF   = self . AlbumGroupsMoving
    AF   = self . AlbumGroupsAppending
    ##########################################################################
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def dropAlbums                        ( self , source , pos , JSON       ) :
    ##########################################################################
    FUNC = self . AlbumAppending
    ##########################################################################
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def dropPictures                      ( self , source , pos , JSON       ) :
    FUNC = self . AssignTaggingIcon
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def GetLastestPosition                      ( self , DB , LUID           ) :
    ##########################################################################
    RELTAB = "RelationGroup"
    ##########################################################################
    if                                        ( self . isReverse ( )       ) :
      return self . GetReverseLastestPosition ( DB , RELTAB , LUID           )
    return   self . GetNormalLastestPosition  ( DB , RELTAB , LUID           )
  ############################################################################
  def GenerateMovingSQL                   ( self   , LAST , UUIDs          ) :
    ##########################################################################
    RELTAB = "RelationGroup"
    R      = self . isReverse             (                                  )
    ##########################################################################
    return self . GenerateNormalMovingSQL ( RELTAB , LAST , UUIDs , R        )
  ############################################################################
  def AlbumGroupsMoving       ( self , atUuid , NAME , JSON                ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ "RelationGroup"                              ]
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
  def AlbumGroupsAppending     ( self , atUuid , NAME , JSON               ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "RelationGroup"                             ]
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
  def AlbumAppending                   ( self , atUuid , NAME , JSON       ) :
    ##########################################################################
    T1   = "Subgroup"
    TAB  = "RelationVideos"
    ##########################################################################
    OK   = self . AppendingAlbumIntoT1 ( atUuid , NAME , JSON , TAB , T1     )
    if                                 ( not OK                            ) :
      return
    ##########################################################################
    self . loading                     (                                     )
    M    = self    . getMenuItem       ( "AlbumsJoined"                      )
    self . emitLog . emit              ( M                                   )
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
    if                                   ( self . NotOkay ( DB )           ) :
      return
    ##########################################################################
    self     . OnBusy  . emit            (                                   )
    ##########################################################################
    TAGTAB   = self . Tables             [ "Tags"                            ]
    SUBTAB   = self . Tables             [ "Subgroups"                       ]
    NAMTAB   = self . Tables             [ "Names"                           ]
    RELTAB   = self . Tables             [ "RelationGroup"                   ]
    TABLES   =                           [ NAMTAB , RELTAB                   ]
    ##########################################################################
    if                                   ( self . Grouping in [ "Tag" ]    ) :
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
    if                                   ( self . Grouping in [ "Tag" ]    ) :
      uuid   = self . AppendTagItem      ( DB                                )
    else                                                                     :
      ########################################################################
      uuid   = self . AppendSubgroupItem ( DB                                )
      ########################################################################
      REL    = Relation                  (                                   )
      REL    . set                       ( "relation" , RR                   )
      ########################################################################
      if                                 ( self . Grouping == "Subgroup"   ) :
        ######################################################################
        PUID = self . Relation . get     ( "first"                           )
        REL  . set                       ( "first"    , PUID                 )
        REL  . set                       ( "second"   , uuid                 )
        REL  . set                       ( "t1"       , T1                   )
        REL  . set                       ( "t2"       , 158                  )
        ######################################################################
      elif                               ( self . Grouping == "Reverse"    ) :
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
    self     . GoRelax . emit            (                                   )
    DB       . UnlockTables              (                                   )
    DB       . Close                     (                                   )
    ##########################################################################
    self     . PrepareItemContent        ( item , uuid , name                )
    self     . assignToolTip             ( item , str ( uuid )               )
    self     . Notify                    ( 5                                 )
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
    GFMT       = self . getMenuItem    ( "AlbumCount"                        )
    ##########################################################################
    DBA        = self . ConnectDB      (                  True               )
    ##########################################################################
    if                                 ( self . NotOkay ( DBA )            ) :
      return
    ##########################################################################
    DBG        = self . ConnectHost    ( self . GroupDB , True               )
    ##########################################################################
    if                                 ( self . NotOkay ( DBG )            ) :
      DBA      . Close                 (                                     )
      return
    ##########################################################################
    self       . PushRunnings          (                                     )
    self       . OnBusy  . emit        (                                     )
    ##########################################################################
    self       . FetchingINFO = True
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
      REL      . setT2                 ( "Album"                             )
      GCNT     = REL  . CountSecond    ( DBG     , RELTAB                    )
      GMSG     = GFMT . format         ( GCNT                                )
      ########################################################################
      tooltip  = f"{U}\n{SMSG}\n{GMSG}"
      ########################################################################
      if                               ( self . StayAlive                  ) :
        self   . assignToolTip         ( item    , tooltip                   )
    ##########################################################################
    self       . GoRelax . emit        (                                     )
    self       . FetchingINFO = False
    ##########################################################################
    DBG        . Close                 (                                     )
    DBA        . Close                 (                                     )
    ##########################################################################
    if                                 ( self . StayAlive                  ) :
      ########################################################################
      self     . Notify                ( 2                                   )
      self     . ShowStatus            ( ""                                  )
    ##########################################################################
    self       . PopRunnings           (                                     )
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
  def OpenItemSubgroup             ( self , item                           ) :
    ##########################################################################
    uuid  = item . data            ( Qt . UserRole                           )
    uuid  = int                    ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return False
    ##########################################################################
    title = item . text            (                                         )
    tid   = self . Relation . get  ( "t2"                                    )
    self  . AlbumSubgroup   . emit ( title , tid , str ( uuid )              )
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
  def OpenItemAlbum                ( self , item                           ) :
    ##########################################################################
    uuid  = item . data            ( Qt . UserRole                           )
    uuid  = int                    ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return False
    ##########################################################################
    title = item . text            (                                         )
    tid   = self . Relation . get  ( "t2"                                    )
    self  . AlbumGroup      . emit ( title , tid , str ( uuid )              )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentAlbum          ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( atItem == None                           ) :
      return False
    ##########################################################################
    return self . OpenItemAlbum ( atItem                                     )
  ############################################################################
  def OpenAlbumIcon                 ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    relz = "Using"
    FMT  = self . getMenuItem       ( "IconsFormat"                          )
    tt   = FMT  . format            ( text                                   )
    ##########################################################################
    self . ShowPersonalIcons . emit ( tt                                   , \
                                      158                                  , \
                                      relz                                 , \
                                      xsid                                 , \
                                      icon                                   )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentAlbumIcon      ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenAlbumIcon      ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    ## self . defaultOpenItemNamesEditor ( item , "Albums" , "NamesEditing"     )
    self . defaultOpenItemNamesEditor ( item , "Albums" , "NamesLocal"       )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
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
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu              ( mm                                  )
    ##########################################################################
    if                                 ( uuid > 0                          ) :
      ########################################################################
      mg   = self . getMenuItem        ( "Subgroup"                          )
      ic   = QIcon                     ( ":/images/filmfolder.png"           )
      mm   . addActionWithIcon         ( 2001 , ic , mg                      )
      ########################################################################
      if                               ( self . Grouping == "Subgroup"     ) :
        ######################################################################
        ic = QIcon                     ( ":/images/episode.png"              )
        mg = self . getMenuItem        ( "Albums"                            )
        mm . addActionWithIcon         ( 2002 , ic , mg                      )
      ########################################################################
      mg   = self . getMenuItem        ( "Icons"                             )
      ic   = QIcon                     ( ":/images/foldericon.png"           )
      mm   . addActionWithIcon         ( 2003 , ic , mg                      )
      ########################################################################
      mm   . addSeparator              (                                     )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1101                           )
    ##########################################################################
    if                                 ( uuid > 0                          ) :
      self . AppendRenameAction        ( mm , 1102                           )
      self . AssureEditNamesAction     ( mm , 1601 , atItem                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . FunctionsMenu             ( mm , uuid , atItem                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . ScrollBarMenu             ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont (              ) )
    aa     = mm . exec_                ( QCursor . pos      (              ) )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
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
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunScrollBarMenu   ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu    ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1101                        ) :
      ########################################################################
      self . InsertItem                (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      ########################################################################
      self . RenameItem                (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 2001                        ) :
      self . OpenItemSubgroup          ( atItem                              )
      return True
    ##########################################################################
    if                                 ( at == 2002                        ) :
      ########################################################################
      self . OpenItemAlbum             ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 2003                        ) :
      ########################################################################
      self . OpenAlbumIcon             ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

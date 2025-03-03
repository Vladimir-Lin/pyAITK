# -*- coding: utf-8 -*-
##############################################################################
## PeopleView
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
from   PySide6                               import QtCore
from   PySide6                               import QtGui
from   PySide6                               import QtWidgets
from   PySide6 . QtCore                      import *
from   PySide6 . QtGui                       import *
from   PySide6 . QtWidgets                   import *
from   AITK    . Qt6                         import *
##############################################################################
from   AITK    . Essentials . Relation       import Relation       as Relation
from   AITK    . Calendars  . StarDate       import StarDate       as StarDate
from   AITK    . Calendars  . Periode        import Periode        as Periode
from   AITK    . Documents  . Variables      import Variables      as VariableItem
from   AITK    . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK    . Pictures   . Gallery        import Gallery        as GalleryItem
from   AITK    . People     . People         import People         as PeopleItem
##############################################################################
from   AITK    . UUIDs      . UuidListings6  import appendUuid
from   AITK    . UUIDs      . UuidListings6  import appendUuids
from   AITK    . UUIDs      . UuidListings6  import assignUuids
from   AITK    . UUIDs      . UuidListings6  import getUuids
##############################################################################
class PeopleView                 ( IconDock                                ) :
  ############################################################################
  HavingMenu            = 1371434312
  ############################################################################
  AssignCurrentPeople   = Signal ( dict                                      )
  ShowPeopleDetails     = Signal ( str , str ,             QIcon             )
  ShowPersonalGallery   = Signal ( str , int , str ,       QIcon             )
  ShowPersonalIcons     = Signal ( str , int , str , str , QIcon             )
  ShowPersonalFaces     = Signal ( str , str                                 )
  ShowGalleries         = Signal ( str , int , str ,       QIcon             )
  ShowGalleriesRelation = Signal ( str , int , str , str , QIcon             )
  ShowVideoAlbums       = Signal ( str , int , str ,       QIcon             )
  ShowWebPages          = Signal ( str , int , str , str , QIcon             )
  ShowPeopleSources     = Signal ( str , str , str ,       QIcon             )
  OwnedOccupation       = Signal ( str , int , str , str , QIcon             )
  OpenBodyShape         = Signal ( str , str , dict                          )
  OpenPickSexuality     = Signal ( str , str ,             QIcon             )
  OpenPickEyeColors     = Signal ( str , str ,             QIcon             )
  OpenPickHairColors    = Signal ( str , str ,             QIcon             )
  OpenPickBloodTypes    = Signal ( str , str ,             QIcon             )
  OpenPickRaceTypes     = Signal ( str , str ,             QIcon             )
  OpenPickNationalites  = Signal ( str , str ,             QIcon             )
  ShowLodListings       = Signal ( str , str             , QIcon             )
  OpenVariantTables     = Signal ( str , str , int , str , dict              )
  emitOpenSmartNote     = Signal ( str                                       )
  OpenLogHistory        = Signal ( str , str , str , str , str               )
  emitLog               = Signal ( str                                       )
  ############################################################################
  def __init__                   ( self , parent = None , plan = None      ) :
    ##########################################################################
    super ( ) . __init__         (        parent        , plan               )
    ##########################################################################
    self . ClassTag           = "PeopleView"
    self . FetchTableKey      = self . ClassTag
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . GType              = 7
    self . SortOrder          = "asc"
    self . SortByName         = False
    self . ExtraINFOs         = True
    self . RefreshOpts        = True
    self . Watermarking       = False
    self . UsedOptions        = [ 1 , 2 , 3 , 4 , 5 , 6 , 7                  ]
    self . PeopleOPTs         = {                                            }
    ##########################################################################
    self . Favourite          = 0
    self . Favourites         = {                                            }
    ##########################################################################
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingPlace       = Qt . BottomDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( "People"                                )
    self . Relation . setT2        ( "People"                                )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    self . setMinimumSize          ( 180 , 200                               )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def PrepareFetchTableKey       ( self                                    ) :
    ##########################################################################
    ## self . subgroupFetchTableKey (                                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions                    ( self                          ) :
    ##########################################################################
    self . PrepareFetchTableKey            (                                 )
    self . AppendToolNamingAction          (                                 )
    ##########################################################################
    self . AppendSideActionWithIcon        ( "PeopleDetails"               , \
                                             ":/images/actor.png"          , \
                                             self . OpenPeopleDetails        )
    self . AppendSideActionWithIcon        ( "Search"                      , \
                                             ":/images/search.png"         , \
                                             self . Search                 , \
                                             True                          , \
                                             False                           )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "Galleries"                   , \
                                             ":/images/galleries.png"      , \
                                             self . OpenPersonalGalleries    )
    self . AppendSideActionWithIcon        ( "PersonalGallery"             , \
                                             ":/images/gallery.png"        , \
                                             self . OpenPersonalGallery      )
    self . AppendSideActionWithIcon        ( "Icons"                       , \
                                             ":/images/foldericon.png"     , \
                                             self . OpenPersonalIcons        )
    self . AppendSideActionWithIcon        ( "Videos"                      , \
                                             ":/images/video.png"          , \
                                             self . OpenPeopleVideos         )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "BodyShapes"                  , \
                                             ":/images/android.png"        , \
                                             self . DoOpenBodyShape          )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "IdentWebPage"                , \
                                             ":/images/webfind.png"        , \
                                             self . OpenIdentifierWebPages   )
    self . AppendSideActionWithIcon        ( "OpenIdentWebPage"            , \
                                             ":/images/bookmarks.png"      , \
                                             self . OpenIdentWebPages        )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "LogHistory"                  , \
                                             ":/images/notes.png"          , \
                                             self . OpenCurrentLogHistory    )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "Sexuality"                   , \
                                             ":/images/sexuality.png"      , \
                                             self . OpenCurrentSexuality     )
    self . AppendSideActionWithIcon        ( "EyeColors"                   , \
                                             ":/images/eye.png"            , \
                                             self . OpenCurrentEyeColors     )
    self . AppendSideActionWithIcon        ( "HairColors"                  , \
                                             ":/images/hairs.png"          , \
                                             self . OpenCurrentHairColors    )
    self . AppendSideActionWithIcon        ( "BloodTypes"                  , \
                                             ":/images/ebloods.png"        , \
                                             self . OpenCurrentBloodTypes    )
    self . AppendSideActionWithIcon        ( "RaceTypes"                   , \
                                             ":/images/remoteuser.png"     , \
                                             self . OpenCurrentRaceTypes     )
    self . AppendSideActionWithIcon        ( "Nationalites"                , \
                                             ":/images/networkconnected.png" , \
                                             self . OpenCurrentNationalites  )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "PeopleViewParameter"                        )
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
  def AttachActions   ( self         ,                            Enabled  ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup           , Enabled    )
    self . LinkAction ( "Load"       , self . AppendingPeople   , Enabled    )
    self . LinkAction ( "Import"     , self . ImportPeople      , Enabled    )
    self . LinkAction ( "Export"     , self . ExportSameNames   , Enabled    )
    self . LinkAction ( "Insert"     , self . InsertItem        , Enabled    )
    self . LinkAction ( "Rename"     , self . RenamePeople      , Enabled    )
    self . LinkAction ( "Delete"     , self . DeleteItems       , Enabled    )
    self . LinkAction ( "Cut"        , self . DeleteItems       , Enabled    )
    self . LinkAction ( "Copy"       , self . DoCopyItemTexts   , Enabled    )
    self . LinkAction ( "Paste"      , self . PasteItems        , Enabled    )
    self . LinkAction ( "Search"     , self . Search            , Enabled    )
    self . LinkAction ( "Home"       , self . PageHome          , Enabled    )
    self . LinkAction ( "End"        , self . PageEnd           , Enabled    )
    self . LinkAction ( "PageUp"     , self . PageUp            , Enabled    )
    self . LinkAction ( "PageDown"   , self . PageDown          , Enabled    )
    self . LinkAction ( "Select"     , self . SelectByClipboard , Enabled    )
    self . LinkAction ( "Reversal"   , self . ReversalSelect    , Enabled    )
    self . LinkAction ( "SelectAll"  , self . SelectAll         , Enabled    )
    self . LinkAction ( "SelectNone" , self . SelectNone        , Enabled    )
    self . LinkAction ( "Font"       , self . ChangeItemFont    , Enabled    )
    ##########################################################################
    self . TellStory  (                                           Enabled    )
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
  def GetUuidIcon                    ( self , DB , UUID                    ) :
    ##########################################################################
    RELTAB = self . Tables           [ "Relation"                            ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "People" , UUID         )
  ############################################################################
  def FetchBaseINFO                  ( self , DB , UUID , PUID             ) :
    ##########################################################################
    ICZ    = self . FetchEntityImage (        DB , PUID                      )
    ##########################################################################
    if                               ( ICZ in self . EmptySet              ) :
      return
    ##########################################################################
    if                               ( UUID in self . PeopleOPTs           ) :
      ########################################################################
      self . PeopleOPTs [ UUID ] [ "Image" ] = ICZ
      self . PeopleOPTs [ UUID ] [ "PUID"  ] = PUID
      ########################################################################
    else                                                                     :
      ########################################################################
      self . PeopleOPTs [ UUID ] =   { "Image" : ICZ                       , \
                                       "PUID"  : PUID                        }
    ##########################################################################
    self   . EmitInfoIcon            ( UUID                                  )
    ##########################################################################
    return
  ############################################################################
  def EmitInfoIcon                    ( self , UUID                        ) :
    ##########################################################################
    if                                ( UUID not in self . UuidItemMaps    ) :
      return
    ##########################################################################
    if                                ( UUID not in self . PeopleOPTs      ) :
      return
    ##########################################################################
    GOPTs     = self . PeopleOPTs     [ UUID                                 ]
    item      = self . UuidItemMaps   [ UUID                                 ]
    ##########################################################################
    if                                ( "Image" in GOPTs                   ) :
      ########################################################################
      IMG     = GOPTs                 [ "Image"                              ]
      ########################################################################
    else                                                                     :
      ########################################################################
      ICON    = self . windowIcon     (                                      )
      PIX     = ICON . pixmap         ( 128 , 128                            )
      IMG     = PIX  . toImage        (                                      )
    ##########################################################################
    TIW       = 16
    TIH       = 16
    USED      = -1
    FAV       = -1
    DINFO     = False
    ##########################################################################
    if                                ( "Used"     in GOPTs                ) :
      ########################################################################
      USED    = GOPTs                 [ "Used"                               ]
      ########################################################################
      if                              ( USED in [ 2 , 3 , 4 , 5 , 6 , 7 ]  ) :
        DINFO = True
    ##########################################################################
    if                                ( UUID in self . Favourites          ) :
      ########################################################################
      FAV     = self . Favourites     [ UUID                                 ]
      DINFO   = True
    ##########################################################################
    if                                ( not self . Watermarking            ) :
      ########################################################################
      DINFO   = False
    ##########################################################################
    if                                ( DINFO                              ) :
      ########################################################################
      ISIZE   = IMG . size            (                                      )
      ICZ     = QImage                ( ISIZE , QImage . Format_ARGB32       )
      ICZ     . fill                  ( QColor ( 255 , 255 , 255 )           )
      ########################################################################
      PTS     = QPoint                ( 0 , 0                                )
      ########################################################################
      p       = QPainter              (                                      )
      p       . begin                 ( ICZ                                  )
      ########################################################################
      p       . drawImage             ( PTS , IMG                            )
      ########################################################################
      if                              ( 2 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/help.png"                  )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      elif                            ( 3 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/flowend.png"               )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      elif                            ( 4 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/geography.png"             )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      elif                            ( 5 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/astrophysics.png"          )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      elif                            ( 6 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/apprentice.png"            )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      elif                            ( 7 == USED                          ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/stars.png"                 )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW           , \
                                        ISIZE . height ( ) - TIH             )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      if                              ( FAV > 0                            ) :
        ######################################################################
        CLR   = QColor                ( 255 , 0 , 0 , 192                    )
        FNT   = self . font           (                                      )
        FNT   . setPixelSize          ( TIW - 6                              )
        FNT   . setBold               ( True                                 )
        RTS   = QRectF                ( 2                                  , \
                                        ISIZE . height ( ) - TIH           , \
                                        ISIZE . width  ( ) / 2             , \
                                        TIH                                  )
        p     . setFont               ( FNT                                  )
        p     . setPen                ( CLR                                  )
        p     . setBrush              ( CLR                                  )
        p     . drawText              ( RTS , f"{FAV}"                       )
      ########################################################################
      p       . end                   (                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      ICZ     = IMG
    ##########################################################################
    icon      = self . ImageToIcon    ( ICZ                                  )
    ##########################################################################
    self      . emitAssignIcon . emit ( item , icon                          )
    ##########################################################################
    return
  ############################################################################
  def ParallelFetchIcons      ( self , ID , UUIDs                          ) :
    ##########################################################################
    self . ParallelFetchINFOs (        ID , UUIDs                            )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item                              ) :
    ##########################################################################
    self . defaultSingleClicked (        item                                )
    ##########################################################################
    return True
  ############################################################################
  def doubleClicked              ( self , item                             ) :
    ##########################################################################
    self . OpenItemPeopleDetails (        item                               )
    ##########################################################################
    return True
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "People"                                    ]
    QQ     = f"select count(*) from {TABLE} where ( `used` = 1 ) ;"
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
    TABLE  = self . Tables          [ "People"                               ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` = 1 )
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables     [ "Relation"                                  ]
    ##########################################################################
    if                         ( self . isSubordination ( )                ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                         ( self . isReverse       ( )                ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isSearching (       ) ) :
      return self . UUIDs
    ##########################################################################
    if                                      ( self . isOriginal  (       ) ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . PeopleOPTs =                   {                                  }
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def GenerateItemToolTip             ( self , UUID                        ) :
    ##########################################################################
    if                                ( UUID not in self . UuidItemMaps    ) :
      return
    ##########################################################################
    if                                ( UUID not in self . PeopleOPTs      ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem       ( "PeopleToolTip"                      )
    USAGE  = self . Translations      [ self . ClassTag ] [ "Usage"          ]
    STATEs = self . Translations      [ self . ClassTag ] [ "States"         ]
    ##########################################################################
    FAV    = "0.00"
    USD    = self . PeopleOPTs        [ UUID ] [ "Used"                      ]
    SSS    = self . PeopleOPTs        [ UUID ] [ "State"                     ]
    PICs   = self . PeopleOPTs        [ UUID ] [ "Pictures"                  ]
    GALs   = self . PeopleOPTs        [ UUID ] [ "Galleries"                 ]
    SGPs   = self . PeopleOPTs        [ UUID ] [ "Subgroups"                 ]
    VIDs   = self . PeopleOPTs        [ UUID ] [ "Albums"                    ]
    ##########################################################################
    if                                ( UUID in self . Favourites          ) :
      ########################################################################
      PFAV = self . Favourites        [ UUID                                 ]
      ########################################################################
      DFAV = int                      ( PFAV / 100                           )
      RFAV = int                      ( PFAV % 100                           )
      ########################################################################
      SF   = f"{RFAV}"
      ########################################################################
      if                              ( len ( SF ) < 2                     ) :
        SF = f"0{SF}"
      ########################################################################
      FAV  = f"{DFAV}.{SF}"
    ##########################################################################
    UMSG   = ""
    ##########################################################################
    if                                ( f"{USD}" in USAGE                  ) :
      ########################################################################
      UMSG = USAGE                    [ f"{USD}"                             ]
    ##########################################################################
    text   = FMT . format             ( UUID                               , \
                                        FAV                                , \
                                        PICs                               , \
                                        GALs                               , \
                                        SGPs                               , \
                                        VIDs                               , \
                                        UMSG                                 )
    ##########################################################################
    if                                ( UUID in self . UuidItemNames       ) :
      ########################################################################
      TIT  = self . UuidItemNames     [ UUID                                 ]
      text = f"{TIT}\n\n{text}"
    ##########################################################################
    item   = self . UuidItemMaps      [ UUID                                 ]
    self   . emitAssignToolTip . emit ( item , text                          )
    self   . EmitInfoIcon             ( UUID                                 )
    ##########################################################################
    return
  ############################################################################
  def FetchExtraInformations           ( self , UUIDs                      ) :
    ##########################################################################
    DB           = self . ConnectDB    (                                     )
    if                                 ( self . NotOkay ( DB )             ) :
      return
    ##########################################################################
    PEOTAB       = self . Tables       [ "People"                            ]
    PICTAB       = self . Tables       [ "Relation"                          ]
    ## PICTAB       = self . Tables       [ "RelationPictures"                  ]
    GALTAB       = self . Tables       [ "Relation"                          ]
    RELTAB       = self . Tables       [ "Relation"                          ]
    SGPTAB       = self . Tables       [ "Relation"                          ]
    ## VIDTAB       = self . Tables       [ "RelationVideos"                    ]
    ALMTAB       = self . Tables       [ "Relation"                          ]
    ## ALMTAB       = self . Tables       [ "RelationPeople"                    ]
    VIDTAB       = self . Tables       [ "Relation"                          ]
    ## VIDTAB       = self . Tables       [ "RelationPeople"                    ]
    REL          = Relation            (                                     )
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . StayAlive              ) :
        continue
      ########################################################################
      GJSON      =                     { "Used"      : 1                   , \
                                         "State"     : 0                   , \
                                         "Pictures"  : 0                   , \
                                         "Galleries" : 0                   , \
                                         "Subgroups" : 0                   , \
                                         "Albums"    : 0                     }
      ########################################################################
      if                               ( U in self . PeopleOPTs            ) :
        ######################################################################
        GOPTs    = self . PeopleOPTs   [ U                                   ]
        ######################################################################
        if                             ( "Image" in GOPTs                  ) :
          ####################################################################
          GJSON [ "Image" ] = GOPTs    [ "Image"                             ]
      ########################################################################
      self       . PeopleOPTs [ U ] = GJSON
      ########################################################################
      QQ         = f"""select `used` , `state` from {PEOTAB}
                       where ( `uuid` = {U} ) ;"""
      DB         . Query               ( " " . join ( QQ . split (       ) ) )
      RR         = DB . FetchOne       (                                     )
      ########################################################################
      if                               ( RR not in self . EmptySet         ) :
        ######################################################################
        if                             ( 2 == len ( RR )                   ) :
          ####################################################################
          USD    = int                 ( RR [ 0                            ] )
          SSS    = int                 ( RR [ 1                            ] )
          ####################################################################
          self   . PeopleOPTs [ U ] [ "Used"   ] = USD
          self   . PeopleOPTs [ U ] [ "State" ] = SSS
      ########################################################################
      REL        . set                 ( "first" , U                         )
      REL        . setT1               ( "People"                            )
      REL        . setT2               ( "Picture"                           )
      REL        . setRelation         ( "Subordination"                     )
      PICs       = REL . CountSecond   ( DB , PICTAB                         )
      ########################################################################
      self       . PeopleOPTs [ U ] [ "Pictures" ] = PICs
      ########################################################################
      REL        . setT2               ( "Gallery"                           )
      GALs       = REL . CountSecond   ( DB , GALTAB                         )
      ########################################################################
      self       . PeopleOPTs [ U ] [ "Galleries" ] = GALs
      ########################################################################
      REL        . setT2               ( "Album"                             )
      VIDs       = REL . CountSecond   ( DB , ALMTAB                         )
      ########################################################################
      self       . PeopleOPTs [ U ] [ "Albums" ] = VIDs
      ########################################################################
      REL        . set                 ( "second" , U                        )
      REL        . setT2               ( "People"                            )
      ########################################################################
      REL        . setT1               ( "Subgroup"                          )
      SGPs       = REL . CountFirst    ( DB , SGPTAB                         )
      ########################################################################
      self       . PeopleOPTs [ U ] [ "Subgroups" ] = SGPs
      ########################################################################
      self       . GenerateItemToolTip ( U                                   )
    ##########################################################################
    DB           . Close               (                                     )
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent       ( self , item , UUID , NAME                 ) :
    ##########################################################################
    favor  = self . Favourites [ UUID                                        ]
    UXID   = str               ( UUID                                        )
    FAV    = str               ( favor                                       )
    ##########################################################################
    FT     = self . iconFont   (                                             )
    ##########################################################################
    if                         ( self . UsingName                          ) :
      item . setText           ( NAME                                        )
    ##########################################################################
    item   . setToolTip        ( str ( UUID )                                )
    item   . setTextAlignment  ( Qt   . AlignCenter                          )
    item   . setData           ( Qt   . UserRole        , UXID               )
    item   . setData           ( Qt   . UserRole + 1001 , FAV                )
    item   . setIcon           ( self . defaultIcon (                      ) )
    item   . setFont           ( FT                                          )
    ##########################################################################
    JSOX   = self . itemJson   ( item                                        )
    ##########################################################################
    JSOX [ "Uuid"      ] = UUID
    JSOX [ "Name"      ] = NAME
    JSOX [ "Favourite" ] = favor
    ##########################################################################
    self . setItemJson         ( item , JSOX                                 )
    ##########################################################################
    return item
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    self    . LoopRunning = False
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self  . emitIconsShow . emit    (                                      )
      self  . LoopRunning = True
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
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    PAMTAB  = self . Tables           [ "Parameters"                         ]
    PQ      = ParameterQuery          ( 7 , 113 , "Features" , PAMTAB        )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      favor = PQ . Value              ( DB , UUID , "Favourite"              )
      ########################################################################
      if                              ( len ( f"{favor}" ) > 0             ) :
        ######################################################################
        favor = int                   ( favor                                )
        ######################################################################
      else                                                                   :
        ######################################################################
        favor = 0
      ########################################################################
      self . Favourites [ UUID ] = favor
    ##########################################################################
    if                                ( self . UsingName                   ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    self    . LoopRunning = True
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self  . emitIconsShow . emit    (                                      )
    ##########################################################################
    JSON               =              {                                      }
    JSON   [ "UUIDs" ] = UUIDs
    if                                ( self . UsingName                   ) :
      JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self    . emitAllIcons . emit     ( JSON                                 )
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "people/uuids"
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
    FMTs    = [ "people/uuids"                                             , \
                "picture/uuids"                                            , \
                ## "album/uuids"                                              , \
                ## "albumgroup/uuids"                                         , \
                "face/uuids"                                                 ]
    formats = ";" . join   ( FMTs                                            )
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
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
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      if                            ( self . OldGrouping in ["Searching"]  ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        FMT = self . getMenuItem    ( "Moving"                               )
        MSG = FMT  . format         ( CNT                                    )
      else                                                                   :
        FMT = self . getMenuItem    ( "Copying"                              )
        MSG = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        return False
      ########################################################################
      FMT   = self . getMenuItem    ( "GetPictures"                          )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "face/uuids" ]            ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        return False
      ########################################################################
      FMT   = self . getMenuItem    ( "GetFaces"                             )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople                   ( self , source , pos , JSOX            ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                             ( self == source                        ) :
      ########################################################################
      self . Go ( self . PeopleMoving    , ( ATID , NAME , JSOX , )          )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    self   . Go ( self . PeopleAppending , ( ATID , NAME , JSOX , )          )
    ##########################################################################
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures                 ( self , source , pos , JSON            ) :
    ##########################################################################
    PUID , NAME = self . itemAtPos ( pos                                     )
    if                             ( int ( PUID ) <= 0                     ) :
      return True
    ##########################################################################
    self . Go ( self . PicturesAppending , ( PUID , NAME , JSON , )          )
    ##########################################################################
    return True
  ############################################################################
  def acceptFacesDrop          ( self                                      ) :
    return True
  ############################################################################
  def dropFaces                    ( self , source , pos , JSON            ) :
    ##########################################################################
    PUID , NAME = self . itemAtPos ( pos                                     )
    if                             ( int ( PUID ) <= 0                     ) :
      return True
    ##########################################################################
    self . Go ( self . FacesAppending , ( PUID , NAME , JSON , )             )
    ##########################################################################
    return True
  ############################################################################
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationPeople" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationPeople" , LAST , UUIDs   )
  ############################################################################
  def PeopleMoving     ( self , atUuid , NAME , JSON                       ) :
    ##########################################################################
    TK   = "Relation"
    ## TK   = "RelationPeople"
    MK   = "OrganizePeople"
    ##########################################################################
    self . MajorMoving (        atUuid ,        JSON , TK , MK               )
    ##########################################################################
    return
  ############################################################################
  def PeopleAppending     ( self , atUuid , NAME , JSON                    ) :
    ##########################################################################
    TK   = "RelationPeople"
    MK   = "OrganizePeople"
    ##########################################################################
    self . MajorAppending (        atUuid ,        JSON , TK , MK            )
    ##########################################################################
    return
  ############################################################################
  def PicturesAppending            ( self , atUuid , NAME , JSON           ) :
    ##########################################################################
    T1  = "People"
    TAB = "RelationPeople"
    ##########################################################################
    OK  = self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1  )
    if                             ( not OK                                ) :
      return
    ##########################################################################
    self   . loading               (                                         )
    ##########################################################################
    return
  ############################################################################
  def FacesAppending           ( self , atUuid , NAME , JSON               ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    FRNTAB = self . Tables     [ "FaceRegions"                               ]
    FRXTAB = self . Tables     [ "FaceRecognitions"                          ]
    ##########################################################################
    DB     . LockWrites        ( [ FRNTAB , FRXTAB                         ] )
    ##########################################################################
    UXIDs  =                   [                                             ]
    for UUID in UUIDs                                                        :
      UXIDs . append           ( f"{UUID}"                                   )
    UXIDX  = " , " . join      ( UXIDs                                       )
    ##########################################################################
    QQ     = f"""update {FRNTAB}
                 set `owner` = {atUuid}
                 where ( `uuid` in ( {UXIDX} ) ) ;"""
    ##########################################################################
    QQ     = " " . join        ( QQ . split ( )                              )
    DB     . Query             ( QQ                                          )
    ##########################################################################
    QQ     = f"""update {FRXTAB}
                 set `owner` = {atUuid}
                 where ( `face` in ( {UXIDX} ) ) ;"""
    ##########################################################################
    QQ     = " " . join        ( QQ . split ( )                              )
    DB     . Query             ( QQ                                          )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . Notify            ( 5                                           )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "People" , "Names"                        )
    ##########################################################################
    return
  ############################################################################
  ## 從剪貼簿取得MIME列表貼上
  ############################################################################
  def PasteItems                   ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RenamePeople    ( self                                               ) :
    ##########################################################################
    self . RenameItem (                                                      )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    if                                ( not self . isGrouping (          ) ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    SQLs   =                          [                                      ]
    ##########################################################################
    RV     = self . isReverse         (                                      )
    ##########################################################################
    if                                ( RV                                 ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set         ( "first" , UUID                       )
        QQ   = self . Relation . Delete ( RELTAB                             )
        SQLs . append                 ( QQ                                   )
      ########################################################################
    else                                                                     :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set         ( "second" , UUID                      )
        QQ   = self . Relation . Delete ( RELTAB                             )
        SQLs . append                 ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    TITLE  = "RemovePeopleItems"
    self   . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    self   . loading                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def AppendItemName                     ( self , item , name              ) :
    ##########################################################################
    DB       = self . ConnectDB          ( UsePure = True                    )
    if                                   ( self . NotOkay ( DB )           ) :
      return
    ##########################################################################
    uuid     = item . data               ( Qt . UserRole                     )
    uuid     = int                       ( uuid                              )
    ##########################################################################
    PHID     = 1400000000000000000
    ##########################################################################
    if                                   ( "Heading" in self . Tables      ) :
      ########################################################################
      PHID   = self . Tables             [ "Heading"                         ]
      PHID   = int                       ( PHID                              )
    ##########################################################################
    PEOTAB   = self . Tables             [ "People"                          ]
    NAMTAB   = self . Tables             [ "NamesEditing"                    ]
    RELTAB   = self . Tables             [ "RelationPeople"                  ]
    TABLES   =                           [ PEOTAB , NAMTAB                   ]
    ##########################################################################
    if                                   (  self . isGrouping ( )          ) :
      TABLES . append                    ( RELTAB                            )
      T1     = self . Relation . get     ( "t1"                              )
      T2     = self . Relation . get     ( "t2"                              )
      RR     = self . Relation . get     ( "relation"                        )
    ##########################################################################
    DB       . LockWrites                ( TABLES                            )
    ##########################################################################
    if                                   ( uuid <= 0                       ) :
      ########################################################################
      PI     = PeopleItem                (                                   )
      PI     . Settings [ "Head"   ] = PHID
      PI     . Tables   [ "People" ] = PEOTAB
      ########################################################################
      uuid   = PI . NewPeople            ( DB                                )
    ##########################################################################
    REL      = Relation                  (                                   )
    REL      . set                       ( "relation" , RR                   )
    ##########################################################################
    if                                   ( self . isSubordination ( )      ) :
      ########################################################################
      PUID   = self . Relation . get     ( "first"                           )
      REL    . set                       ( "first"    , PUID                 )
      REL    . set                       ( "second"   , uuid                 )
      REL    . set                       ( "t1"       , T1                   )
      REL    . setT2                     ( "People"                          )
      REL    . Join                      ( DB , RELTAB                       )
      ########################################################################
    elif                                 ( self . isReverse       ( )      ) :
      ########################################################################
      PUID   = self . Relation . get     ( "second"                          )
      REL    . set                       ( "first"    , uuid                 )
      REL    . set                       ( "second"   , PUID                 )
      REL    . setT1                     ( "People"                          )
      REL    . set                       ( "t2"       , T2                   )
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
  def ListAllNames                  ( self                                 ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def JoiningPeople            ( self , UUIDs                              ) :
    ##########################################################################
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
    RELTAB = self . Tables     [ "RelationPeople"                            ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . Relation  . Joins ( DB , RELTAB , UUIDs                         )
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
  def JoinPeopleFromFile             ( self , Filename                     ) :
    ##########################################################################
    UUIDs = self . LoadUuidsFromFile (        Filename                       )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      return
    ##########################################################################
    self  . JoiningPeople            ( UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def AppendingPeople             ( self                                   ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "TextFilters"                            )
    Name , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    ""                                     , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    VAL      =                    ( Name ,                                   )
    self     . Go                 ( self . JoinPeopleFromFile , VAL          )
    ##########################################################################
    return
  ############################################################################
  def ImportPeople                  ( self                                 ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "TextFilters"                            )
    Name , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    ""                                     , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    VAL      =                    ( Name ,                                   )
    self     . Go                 ( self . ImportPeopleFromFile , VAL        )
    ##########################################################################
    return
  ############################################################################
  def ImportPeopleFromFile           ( self , Filename                     ) :
    ##########################################################################
    UUIDs = self . LoadUuidsFromFile (        Filename                       )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      return False
    ##########################################################################
    self  . SearchKey = ""
    self  . UUIDs     = UUIDs
    self  . Grouping  = "Searching"
    ##########################################################################
    self  . loading                  (                                       )
    ##########################################################################
    return True
  ############################################################################
  def ImportPeopleFromClipboard         ( self                             ) :
    ##########################################################################
    BODY  = qApp . clipboard ( ) . text (                                    )
    UUIDs = self . GetUuidsFromText     ( BODY                               )
    ##########################################################################
    if                                  ( len ( UUIDs ) <= 0               ) :
      return False
    ##########################################################################
    self  . SearchKey = ""
    self  . UUIDs     = UUIDs
    self  . Grouping  = "Searching"
    ##########################################################################
    self  . loading                     (                                    )
    ##########################################################################
    return True
  ############################################################################
  def ExportSameNames ( self                                               ) :
    ##########################################################################
    self . Go         ( self . ExportSameNamesListings                       )
    ##########################################################################
    return
  ############################################################################
  def ExportSameNamesListings      ( self                                  ) :
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NAMTAB = self . Tables         [ "Names"                                 ]
    RELTAB = self . Tables         [ "Relation"                              ]
    ##########################################################################
    UUID   = self . Relation . get ( "first"                                 )
    T1     = self . Relation . get ( "t1"                                    )
    T2     = self . Relation . get ( "t2"                                    )
    REL    = self . Relation . get ( "relation"                              )
    ##########################################################################
    LISTS  =                       [                                         ]
    FF     = f"""select `second` from {RELTAB}
                 where ( `first` = {UUID} )
                 and ( `t1` = {T1} )
                 and ( `t2` = {T2} )
                 and ( `relation` = {REL} )"""
    QQ     = f"""select `uuid`,`name` from {NAMTAB}
                 where ( `uuid` in ( {FF} ) )
                 and ( `relevance` = 0 )
                 order by `name` asc , `uuid` asc ;"""
    QQ     = " " . join            ( QQ . split ( )                          )
    DB     . Query                 ( QQ                                      )
    ALL    = DB . FetchAll         (                                         )
    TOTAL  = len                   ( ALL                                     )
    PREV   = 0
    AT     = 1
    CC     = False
    ##########################################################################
    PVID   = ALL                   [ PREV ] [ 0                              ]
    NAME   = ALL                   [ PREV ] [ 1                              ]
    ##########################################################################
    while                          ( AT < TOTAL                            ) :
      ########################################################################
      U    = ALL                   [ AT ] [ 0                                ]
      N    = ALL                   [ AT ] [ 1                                ]
      ########################################################################
      if                           ( ( N == NAME ) and ( PVID != U )       ) :
        ######################################################################
        if                         ( not CC                                ) :
          ####################################################################
          CC = True
          L  = f"{PVID}"
          LISTS . append ( L )
        ######################################################################
        L  = f"{U}"
        LISTS . append ( L )
        ######################################################################
      else                                                                   :
        ######################################################################
        CC   = False
        NAME = N
      ########################################################################
      PVID = U
      AT   = AT + 1
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) > 0                  ) :
      ########################################################################
      NOTE = "\n" . join              ( LISTS                                )
      self . emitOpenSmartNote . emit ( NOTE                                 )
    ##########################################################################
    return
  ############################################################################
  def SearchForSameNames           ( self                                  ) :
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NAMTAB = self . Tables         [ "Names"                                 ]
    RELTAB = self . Tables         [ "Relation"                              ]
    ##########################################################################
    UUID   = self . Relation . get ( "first"                                 )
    T1     = self . Relation . get ( "t1"                                    )
    T2     = self . Relation . get ( "t2"                                    )
    REL    = self . Relation . get ( "relation"                              )
    ##########################################################################
    LISTS  =                       [                                         ]
    FF     = f"""select `second` from {RELTAB}
                 where ( `first` = {UUID} )
                 and ( `t1` = {T1} )
                 and ( `t2` = {T2} )
                 and ( `relation` = {REL} )"""
    QQ     = f"""select `uuid`,`name` from {NAMTAB}
                 where ( `uuid` in ( {FF} ) )
                 and ( `relevance` = 0 )
                 order by `name` asc , `uuid` asc ;"""
    QQ     = " " . join            ( QQ . split ( )                          )
    DB     . Query                 ( QQ                                      )
    ALL    = DB . FetchAll         (                                         )
    TOTAL  = len                   ( ALL                                     )
    PREV   = 0
    AT     = 1
    CC     = False
    ##########################################################################
    PVID   = ALL                   [ PREV ] [ 0                              ]
    NAME   = ALL                   [ PREV ] [ 1                              ]
    ##########################################################################
    while                          ( AT < TOTAL                            ) :
      ########################################################################
      U    = ALL                   [ AT ] [ 0                                ]
      N    = ALL                   [ AT ] [ 1                                ]
      ########################################################################
      if                           ( ( N == NAME ) and ( PVID != U )       ) :
        ######################################################################
        if                         ( not CC                                ) :
          ####################################################################
          CC = True
          L  = f"{PVID} {NAME}"
          LISTS . append ( L )
        ######################################################################
        L  = f"{U} {NAME}"
        LISTS . append ( L )
        ######################################################################
      else                                                                   :
        ######################################################################
        CC   = False
        NAME = N
      ########################################################################
      PVID = U
      AT   = AT + 1
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) > 0                  ) :
      ########################################################################
      NOTE = "\n" . join              ( LISTS                                )
      self . emitOpenSmartNote . emit ( NOTE                                 )
    ##########################################################################
    return
  ############################################################################
  def DoFetchOpenWebPages        ( self , uuid , related                   ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( self . NotOkay ( DB )                   ) :
      return False
    ##########################################################################
    RELTAB = "`cios`.`relations`"
    WEBTAB = "`cios`.`webpages`"
    ##########################################################################
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , uuid                            )
    REL    . setT1               ( "People"                                  )
    REL    . setT2               ( "WebPage"                                 )
    REL    . setRelation         ( related                                   )
    UUIDs  = REL . Subordination ( DB      , RELTAB                          )
    ##########################################################################
    if                           ( len ( UUIDs ) > 0                       ) :
      self . OpenUrlsByUuids     ( DB , WEBTAB , UUIDs                       )
    ##########################################################################
    DB     . Close               (                                           )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage          ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      self . emitRestart . emit    (                                         )
      return False
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( self . NotOkay ( DB )                 ) :
      return False
    ##########################################################################
    PAMTAB = self . Tables         [ "Parameters"                            ]
    DB     . LockWrites            ( [ PAMTAB ]                              )
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t1"                                    )
      UUID = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                           ( self . isReverse       ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"PeopleView-{SCOPE}-{TYPE}-{UUID}"
    self   . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    self   . emitRestart . emit    (                                         )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    if                             ( not self . isGrouping  ( )            ) :
      return
    ##########################################################################
    PAMTAB = self . Tables         [ "Parameters"                            ]
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t1"                                    )
      UUID = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                            ( self . isReverse       ( )           ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"PeopleView-{SCOPE}-{TYPE}-{UUID}"
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    return
  ############################################################################
  def OptimizePeopleOrder               ( self                             ) :
    ##########################################################################
    TKEY = "Relation"
    MKEY = "OrganizePeople"
    ##########################################################################
    self . DoRepositionMembershipOrders ( TKEY , MKEY , self . ProgressMin   )
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
  def UpdateFavourite           ( self , uuid , favor                      ) :
    ##########################################################################
    self   . LoopRunning = False
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      self . LoopRunning = True
      return
    ##########################################################################
    self   . Notify             ( 3                                          )
    ##########################################################################
    msg    = self . getMenuItem ( "UpdateFavourite..."                       )
    self   . ShowStatus         ( msg                                        )
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    PAMTAB = self . Tables      [ "Parameters"                               ]
    PQ     = ParameterQuery     ( 7  , 113  , "Features"  , PAMTAB           )
    PQ     . assureValue        ( DB , uuid , "Favourite" , favor            )
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    self   . ShowStatus         ( ""                                         )
    DB     . Close              (                                            )
    self   . Notify             ( 5                                          )
    ##########################################################################
    self   . LoopRunning = True
    ##########################################################################
    return
  ############################################################################
  def UpdatePeopleUsage              ( self , uuid , usage                 ) :
    ##########################################################################
    if                               ( uuid <= 0                           ) :
      return
    ##########################################################################
    UUIDs  = self . getSelectedUuids (                                       )
    UUIDz  =                         [ str ( u ) for u in UUIDs              ]
    ##########################################################################
    if                               ( len ( UUIDz ) <= 0                  ) :
      return
    ##########################################################################
    UUIDw  = "," . join              ( UUIDz                                 )
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( self . NotOkay ( DB )               ) :
      return
    ##########################################################################
    PEOTAB = self . Tables           [ "People"                              ]
    ##########################################################################
    DB     . LockWrites              ( [ PEOTAB                            ] )
    ##########################################################################
    QQ     = f"""update {PEOTAB}
                 set `used` = {usage}
                 where ( `uuid` = {uuid} ) ; """
    DB     . Query                   ( " " . join ( QQ . split (         ) ) )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    DB     . Close                   (                                       )
    ##########################################################################
    for u in UUIDs                                                           :
      ########################################################################
      self . PeopleOPTs              [ u ] [ "Used" ] = usage
      self . GenerateItemToolTip     ( u                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenIdentifierWebPages        ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    uuid   = atItem . data          ( Qt . UserRole                          )
    uuid   = int                    ( uuid                                   )
    self   . OpenWebPageBelongings  ( uuid , atItem , "Equivalent"           )
    ##########################################################################
    return
  ############################################################################
  def OpenIdentWebPageURLs ( self , item , related                         ) :
    ##########################################################################
    uuid = item . data     ( Qt . UserRole                                   )
    uuid = int             ( uuid                                            )
    ##########################################################################
    if                     ( uuid <= 0                                     ) :
      return
    ##########################################################################
    VAL  =                 ( uuid , related ,                                )
    self . Go              ( self . DoFetchOpenWebPages , VAL                )
    ##########################################################################
    return
  ############################################################################
  def OpenIdentWebPages           ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    self   . OpenIdentWebPageURLs ( atItem , "Equivalent"                    )
    ##########################################################################
    return
  ############################################################################
  def OpenPeopleVideos              ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    uuid   = atItem . data          ( Qt . UserRole                          )
    uuid   = int                    ( uuid                                   )
    text   = atItem . text          (                                        )
    icon   = atItem . icon          (                                        )
    xsid   = str                    ( uuid                                   )
    ##########################################################################
    self   . ShowVideoAlbums . emit ( text , 7 , xsid , icon                 )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "People" , "NamesEditing"     )
    ##########################################################################
    return
  ############################################################################
  def OpenSexualityItem             ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    self . OpenPickSexuality . emit ( text , xsid , icon                     )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentSexuality      ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenSexualityItem  ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenEyeColorsItem             ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    self . OpenPickEyeColors . emit ( text , xsid , icon                     )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentEyeColors      ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenEyeColorsItem  ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenHairColorsItem             ( self , item                         ) :
    ##########################################################################
    uuid = item . data               ( Qt . UserRole                         )
    uuid = int                       ( uuid                                  )
    text = item . text               (                                       )
    icon = item . icon               (                                       )
    xsid = str                       ( uuid                                  )
    ##########################################################################
    self . OpenPickHairColors . emit ( text , xsid , icon                    )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentHairColors     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenHairColorsItem ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenBloodTypesItem             ( self , item                         ) :
    ##########################################################################
    uuid = item . data               ( Qt . UserRole                         )
    uuid = int                       ( uuid                                  )
    text = item . text               (                                       )
    icon = item . icon               (                                       )
    xsid = str                       ( uuid                                  )
    ##########################################################################
    self . OpenPickBloodTypes . emit ( text , xsid , icon                    )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentBloodTypes     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenBloodTypesItem ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenRaceTypesItem             ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    self . OpenPickRaceTypes . emit ( text , xsid , icon                     )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentRaceTypes      ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenRaceTypesItem  ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenNationalitesItem             ( self , item                       ) :
    ##########################################################################
    uuid = item . data                 ( Qt . UserRole                       )
    uuid = int                         ( uuid                                )
    text = item . text                 (                                     )
    icon = item . icon                 (                                     )
    xsid = str                         ( uuid                                )
    ##########################################################################
    self . OpenPickNationalites . emit ( text , xsid , icon                  )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentNationalites     ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    self   . OpenNationalitesItem ( atItem                                   )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGalleries         ( self , item                              ) :
    ##########################################################################
    uuid = item . data          ( Qt . UserRole                              )
    uuid = int                  ( uuid                                       )
    text = item . text          (                                            )
    icon = item . icon          (                                            )
    xsid = str                  ( uuid                                       )
    ##########################################################################
    self . ShowGalleries . emit ( text , 7 , xsid , icon                     )
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
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    text = item . text                (                                      )
    icon = item . icon                (                                      )
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
  def OpenGalleryIcon               ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    relz = "Using"
    ##########################################################################
    self . ShowPersonalIcons . emit ( text                                 , \
                                      self . GType                         , \
                                      relz                                 , \
                                      xsid                                 , \
                                      icon                                   )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalIcons         ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenGalleryIcon    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemPeopleDetails         ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    self . ShowPeopleDetails . emit ( text , xsid , icon                     )
    ##########################################################################
    return
  ############################################################################
  def OpenPeopleDetails            ( self                                  ) :
    ##########################################################################
    atItem = self . currentItem    (                                         )
    ##########################################################################
    if                             ( self . NotOkay ( atItem )             ) :
      return
    ##########################################################################
    self   . OpenItemPeopleDetails ( atItem                                  )
    ##########################################################################
    return
  ############################################################################
  def DoOpenBodyShape             ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    uuid   = atItem . data        ( Qt . UserRole                            )
    uuid   = int                  ( uuid                                     )
    text   = atItem . text        (                                          )
    xsid   = str                  ( uuid                                     )
    ##########################################################################
    self   . OpenBodyShape . emit ( text , xsid , { }                        )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageListings          ( self , Related                        ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      return
    ##########################################################################
    text   = self . windowTitle    (                                         )
    icon   = self . windowIcon     (                                         )
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      Typi = self . Relation . get ( "t1"                                    )
      uuid = self . Relation . get ( "first"                                 )
    elif                           ( self . isReverse       ( )            ) :
      Typi = self . Relation . get ( "t2"                                    )
      uuid = self . Relation . get ( "second"                                )
    ##########################################################################
    Typi   = int                   ( Typi                                    )
    uuid   = int                   ( uuid                                    )
    xsid   = str                   ( uuid                                    )
    ##########################################################################
    self   . ShowWebPages . emit   ( text , Typi , xsid , Related , icon     )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageBelongings    ( self , uuid , item , Related              ) :
    ##########################################################################
    text = item . text         (                                             )
    icon = item . icon         (                                             )
    ##########################################################################
    uuid = int                 ( uuid                                        )
    xsid = str                 ( uuid                                        )
    ##########################################################################
    self . ShowWebPages . emit ( text , 7 , xsid , Related , icon            )
    ##########################################################################
    return
  ############################################################################
  def OpenPeopleSources             ( self , website , item                ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    ##########################################################################
    if                              ( uuid <= 0                            ) :
      return
    ##########################################################################
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    self . ShowPeopleSources . emit ( website , text , xsid , icon           )
    ##########################################################################
    return
  ############################################################################
  def IndexingMenu               ( self , mm , menu , uuid , item          ) :
    ##########################################################################
    MSG = self . getMenuItem     ( "Indexing"                                )
    LOM = mm   . addMenuFromMenu ( menu , MSG                                )
    ##########################################################################
    msg = self . getMenuItem     ( "AppendLists"                             )
    mm  . addActionFromMenu      ( LOM , 25355001 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "ImportLists"                             )
    mm  . addActionFromMenu      ( LOM , 25355002 , msg                      )
    ##########################################################################
    msg = self . getMenuItem     ( "ImportListsFromClipboard"                )
    mm  . addActionFromMenu      ( LOM , 25355003 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "ExportSameNames"                         )
    mm  . addActionFromMenu      ( LOM , 25355004 , msg                      )
    ##########################################################################
    msg = self . getMenuItem     ( "AllNames"                                )
    mm  . addActionFromMenu      ( LOM , 25355005 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "LocateSameNames"                         )
    mm  . addActionFromMenu      ( LOM , 25355006 , msg                      )
    ##########################################################################
    return mm
  ############################################################################
  def FunctionsMenu               ( self , mm , uuid , item                ) :
    ##########################################################################
    MSG   = self . getMenuItem    ( "Functions"                              )
    LOM   = mm   . addMenu        ( MSG                                      )
    ##########################################################################
    msg   = self . accessibleName (                                          )
    if                            ( len ( msg ) > 0                        ) :
      mm  . addActionFromMenu     ( LOM , 25351201 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "AssignAccessibleName"                   )
    mm    . addActionFromMenu     ( LOM , 25351202 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "Panel"                                  )
    mm    . addActionFromMenu     ( LOM , 25351203 , msg                     )
    ##########################################################################
    if                            ( self . isSubordination ( )             ) :
      ########################################################################
      msg = self . getMenuItem    ( "AssignTables"                           )
      mm  . addActionFromMenu     ( LOM , 25351301 , msg                     )
      ########################################################################
      msg = self . getMenuItem    ( "GroupsToCLI"                            )
      mm  . addActionFromMenu     ( LOM , 25351302 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "DoReposition"                           )
    mm    . addActionFromMenu     ( LOM                                    , \
                                    25351303                               , \
                                    msg                                    , \
                                    True                                   , \
                                    self . DoReposition                      )
    ##########################################################################
    msg   = self . getMenuItem    ( "Watermarking"                           )
    mm    . addActionFromMenu     ( LOM                                    , \
                                    25351304                               , \
                                    msg                                    , \
                                    True                                   , \
                                    self . Watermarking                      )
    ##########################################################################
    msg   = self . getMenuItem    ( "ReportTables"                           )
    mm    . addActionFromMenu     ( LOM , 25351305 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "SortByName"                             )
    mm    . addActionFromMenu     ( LOM                                    , \
                                    25351306                               , \
                                    msg                                    , \
                                    True                                   , \
                                    self . SortByName                        )
    ##########################################################################
    mm    = self . IndexingMenu   ( mm , LOM , uuid , item                   )
    ##########################################################################
    mm    . addSeparatorFromMenu  ( LOM                                      )
    ##########################################################################
    MSG   = self . getMenuItem    ( "WebPages"                               )
    mm    . addActionFromMenu     ( LOM , 25351221 , MSG                     )
    ##########################################################################
    MSG   = self . getMenuItem    ( "IdentWebPage"                           )
    mm    . addActionFromMenu     ( LOM , 25351222 , MSG                     )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 25351202                    ) :
      ########################################################################
      self . ConfigureAccessibleName   (                                     )
      ########################################################################
      return
    ##########################################################################
    if                                 ( at == 25351203                    ) :
      ########################################################################
      ########################################################################
      return
    ##########################################################################
    if                                 ( at == 25351301                    ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      UUID  = self . Relation  . get   ( "first"                             )
      TYPE  = self . Relation  . get   ( "t1"                                )
      TYPE  = int                      ( TYPE                                )
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
    if                                 ( at == 25351303                    ) :
      ########################################################################
      self . DoReposition = not self . DoReposition
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351304                    ) :
      ########################################################################
      self . Watermarking = not self . Watermarking
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351305                    ) :
      ########################################################################
      self . emitLog . emit            ( json . dumps ( self . Tables      ) )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351306                    ) :
      ########################################################################
      if                               ( self . SortByName                 ) :
        self . SortByName = False
      else                                                                   :
        self . SortByName = True
      ########################################################################
      self   . restart                 (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355001                    ) :
      ########################################################################
      self . AppendingPeople           (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355002                    ) :
      ########################################################################
      self . ImportPeople              (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355003                    ) :
      ########################################################################
      self . ImportPeopleFromClipboard (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355004                    ) :
      ########################################################################
      self . ExportSameNames           (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355005                    ) :
      ########################################################################
      self . ListAllNames              (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355006                    ) :
      ########################################################################
      self . Go                        ( self . SearchForSameNames           )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351221                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Subordination"                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351222                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Equivalent"                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def RelatedGalleriesMenu            ( self , mm , uuid , item            ) :
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    MSG  = self . getMenuItem         ( "RelatedGalleries"                   )
    LOM  = mm   . addMenu             ( MSG                                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Galleries"                           )
    icon = QIcon                     ( ":/images/galleries.png"              )
    mm   . addActionFromMenuWithIcon ( LOM , 24231310 , icon , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem        ( "PersonalGallery"                     )
    icon = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( LOM , 24231311 , icon , MSG           )
    ##########################################################################
    msg  = self . getMenuItem        ( "LOD"                                 )
    mm   . addActionFromMenu         ( LOM , 24231312 , msg                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Icons"                               )
    icon = QIcon                     ( ":/images/foldericon.png"             )
    mm   . addActionFromMenuWithIcon ( LOM , 24231313 , icon , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Faces"                               )
    mm   . addActionFromMenu         ( LOM , 24231314 , MSG                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( LOM                                   )
    ##########################################################################
    MSG  = self . getMenuItem        ( "BodyPictures"                        )
    mm   . addActionFromMenu         ( LOM , 24231399 , MSG                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( LOM                                   )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Mouth"                               )
    mm   . addActionFromMenu         ( LOM , 24231315 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Eyes"                                )
    mm   . addActionFromMenu         ( LOM , 24231316 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Iris"                                )
    mm   . addActionFromMenu         ( LOM , 24231317 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Nose"                                )
    mm   . addActionFromMenu         ( LOM , 24231318 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Tits"                                )
    mm   . addActionFromMenu         ( LOM , 24231319 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Umbilicus"                           )
    mm   . addActionFromMenu         ( LOM , 24231320 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Pussy"                               )
    mm   . addActionFromMenu         ( LOM , 24231321 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Asshole"                             )
    mm   . addActionFromMenu         ( LOM , 24231322 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Tattoo"                              )
    mm   . addActionFromMenu         ( LOM , 24231323 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Piercings"                           )
    mm   . addActionFromMenu         ( LOM , 24231324 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Texture"                             )
    mm   . addActionFromMenu         ( LOM , 24231325 , MSG                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunRelatedGalleriesMenu           ( self , at , uuid , item          ) :
    ##########################################################################
    if                                  ( at == 24231310                   ) :
      ########################################################################
      self . OpenItemGalleries          ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231311                   ) :
      ########################################################################
      self . OpenGalleryItem            ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231312                   ) :
      ########################################################################
      icon = item . icon                (                                    )
      head = item . text                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowLodListings . emit     ( head , str ( uuid ) , icon         )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231313                   ) :
      ########################################################################
      self . OpenGalleryIcon            ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231314                   ) :
      ########################################################################
      text = item . text                (                                    )
      ## icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ## relz = "Face"
      ########################################################################
      self . ShowPersonalFaces . emit   ( text , xsid                        )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231315                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Mouth"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231316                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Eye"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231317                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Iris"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231318                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Nose"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231319                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Tit"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231320                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Umbilicus"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231321                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Pussy"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231322                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Asshole"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231323                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Tattoo"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231324                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Piercings"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231325                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Texture"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231399                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      rels =                            [ "Mouth"                          , \
                                          "Eye"                            , \
                                          "Iris"                           , \
                                          "Nose"                           , \
                                          "Tit"                            , \
                                          "Umbilicus"                      , \
                                          "Pussy"                          , \
                                          "Asshole"                        , \
                                          "Tattoo"                         , \
                                          "Piercings"                        ]
      ########################################################################
      for relz in rels                                                       :
        ######################################################################
        self . ShowPersonalIcons . emit ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                    ( self , mm , uuid , item              ) :
    ##########################################################################
    if                              ( uuid <= 0                            ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem        ( "Belongs"                              )
    MSG = FMT  . format             ( item . text ( )                        )
    LOM = mm   . addMenu            ( MSG                                    )
    ##########################################################################
    msg = self . getMenuItem        ( "CopyPeopleUuid"                       )
    mm  . addActionFromMenu         ( LOM , 24231101 , msg                   )
    ##########################################################################
    msg = self . getMenuItem        ( "AssignCurrentPeople"                  )
    mm  . addActionFromMenu         ( LOM , 24231102 , msg                   )
    ##########################################################################
    mm  . addSeparatorFromMenu      ( LOM                                    )
    ##########################################################################
    MSG = self . getMenuItem        ( "LogHistory"                           )
    ICO = QIcon                     ( ":/images/notes.png"                   )
    mm  . addActionFromMenuWithIcon ( LOM , 24231103 , ICO , MSG             )
    ##########################################################################
    MSG = self . getMenuItem        ( "Occupations"                          )
    mm  . addActionFromMenu         ( LOM , 24231201 , MSG                   )
    ##########################################################################
    MSG = self . getMenuItem        ( "Videos"                               )
    ICO = QIcon                     ( ":/images/video.png"                   )
    mm  . addActionFromMenuWithIcon ( LOM , 24231411 , ICO , MSG             )
    ##########################################################################
    mm  . addSeparatorFromMenu      ( LOM                                    )
    ##########################################################################
    MSG = self . getMenuItem        ( "WebPages"                             )
    mm  . addActionFromMenu         ( LOM , 24231511 , MSG                   )
    ##########################################################################
    MSG = self . getMenuItem        ( "IdentWebPage"                         )
    ICO = QIcon                     ( ":/images/webfind.png"                 )
    mm  . addActionFromMenuWithIcon ( LOM , 24231512 , ICO , MSG             )
    ##########################################################################
    MSG = self . getMenuItem        ( "OpenIdentWebPage"                     )
    ICO = QIcon                     ( ":/images/bookmarks.png"               )
    mm  . addActionFromMenuWithIcon ( LOM , 24231513 , ICO , MSG             )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                     ( self , at , uuid , item          ) :
    ##########################################################################
    if                                  ( at == 24231101                   ) :
      ########################################################################
      qApp . clipboard ( ) . setText    ( f"{uuid}"                          )
      ########################################################################
      return
    ##########################################################################
    if                                  ( at == 24231102                   ) :
      ########################################################################
      t    = item . text                (                                    )
      J    =                            { "Uuid" : uuid , "Name" : t         }
      self . AssignCurrentPeople . emit ( J                                  )
      ########################################################################
      return
    ##########################################################################
    if                                  ( at == 24231103                   ) :
      ########################################################################
      self . OpenLogHistoryItem         ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231201                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      rela = "Subordination"
      ########################################################################
      self . OwnedOccupation     . emit ( text , 7 , xsid , rela , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231411                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowVideoAlbums . emit     ( text , 7 , xsid , icon             )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231511                   ) :
      ########################################################################
      self . OpenWebPageBelongings      ( uuid , item , "Subordination"      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231512                   ) :
      ########################################################################
      self . OpenWebPageBelongings      ( uuid , item , "Equivalent"         )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231513                   ) :
      ########################################################################
      self . OpenIdentWebPageURLs       (        item , "Equivalent"         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def FeaturesMenu                   ( self , mm , item                    ) :
    ##########################################################################
    if                               ( self . NotOkay ( item             ) ) :
      return mm
    ##########################################################################
    uuid = item  . data              ( Qt . UserRole                         )
    uuid = int                       ( uuid                                  )
    ##########################################################################
    if                               ( uuid not in self . PeopleOPTs       ) :
      return mm
    ##########################################################################
    MSG  = self . getMenuItem        ( "BodyFeatures"                        )
    COL  = mm   . addMenu            ( MSG                                   )
    ##########################################################################
    MSG  = self . getMenuItem        ( "BodyShapes"                          )
    mm   . addActionFromMenu         ( COL , 29436301 , MSG                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Sexuality"                           )
    ICO  = QIcon                     ( ":/images/sexuality.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 29436311 , ICO , MSG            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "EyeColors"                           )
    ICO  = QIcon                     ( ":/images/eye.png"                    )
    mm   . addActionFromMenuWithIcon ( COL , 29436312 , ICO , MSG            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "HairColors"                          )
    ICO  = QIcon                     ( ":/images/hairs.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 29436313 , ICO , MSG            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "BloodTypes"                          )
    ICO  = QIcon                     ( ":/images/ebloods.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 29436314 , ICO , MSG            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "RaceTypes"                           )
    ICO  = QIcon                     ( ":/images/remoteuser.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 29436315 , ICO , MSG            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Nationalites"                        )
    ICO  = QIcon                     ( ":/images/networkconnected.png"       )
    mm   . addActionFromMenuWithIcon ( COL , 29436316 , ICO , MSG            )
    ##########################################################################
    return mm
  ############################################################################
  def RunFeaturesMenu             ( self , at , item                       ) :
    ##########################################################################
    if                            ( 29436301 == at == 24231351             ) :
      ########################################################################
      text = item . text          (                                          )
      xsid = str                  ( uuid                                     )
      ########################################################################
      self . OpenBodyShape . emit ( text , xsid , {                        } )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436311 == at                         ) :
      ########################################################################
      self . OpenSexualityItem    (             item                         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436312 == at                         ) :
      ########################################################################
      self . OpenEyeColorsItem    (             item                         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436313 == at                         ) :
      ########################################################################
      self . OpenHairColorsItem   (             item                         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436314 == at                         ) :
      ########################################################################
      self . OpenBloodTypesItem   (             item                         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436315 == at                         ) :
      ########################################################################
      self . OpenRaceTypesItem    (             item                         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( 29436316 == at                         ) :
      ########################################################################
      self . OpenNationalitesItem (             item                         )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def PeopleFavourite                 ( self , mm , uuid , item            ) :
    ##########################################################################
    favr = item . data                ( Qt   . UserRole + 1001               )
    self . Favourite = int            ( favr                                 )
    ##########################################################################
    msg  = self . getMenuItem         ( "Favourite:"                         )
    ##########################################################################
    self . FavouriteId = SpinBox      ( None , self . PlanFunc               )
    self . FavouriteId . setPrefix    ( msg                                  )
    self . FavouriteId . setRange     ( 0 , 10000                            )
    self . FavouriteId . setValue     ( self . Favourite                     )
    self . FavouriteId . setAlignment ( Qt . AlignRight                      )
    mm   . addWidget                  ( 9999191 , self . FavouriteId         )
    ##########################################################################
    mm   . addSeparator               (                                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunPeopleFavourite                ( self , uuid , item               ) :
    ##########################################################################
    if                                  ( self . FavouriteId == None       ) :
      return False
    ##########################################################################
    SID    = self . FavouriteId . value (                                    )
    ##########################################################################
    self   . FavouriteId = None
    ##########################################################################
    if                                  ( SID != self . Favourite          ) :
      ########################################################################
      self . Favourite = SID
      item . setData                    ( Qt . UserRole + 1001 , SID         )
      self . Go                         ( self . UpdateFavourite           , \
                                          ( uuid , SID , )                   )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def PeopleSourcesMenu       ( self , mm , item                           ) :
    ##########################################################################
    if                        ( self . NotOkay ( item                    ) ) :
      return mm
    ##########################################################################
    uuid = item  . data       ( Qt . UserRole                                )
    uuid = int                ( uuid                                         )
    ##########################################################################
    if                        ( uuid not in self . PeopleOPTs              ) :
      return mm
    ##########################################################################
    MSG  = self . getMenuItem ( "PeopleSources"                              )
    COL  = mm   . addMenu     ( MSG                                          )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchADE"                                  )
    mm   . addActionFromMenu  ( COL , 29436051 , MSG                         )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchIAFD"                                 )
    mm   . addActionFromMenu  ( COL , 29436052 , MSG                         )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchPrivate"                              )
    mm   . addActionFromMenu  ( COL , 29436053 , MSG                         )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchBANG"                                 )
    mm   . addActionFromMenu  ( COL , 29436054 , MSG                         )
    ##########################################################################
    return mm
  ############################################################################
  def RunPeopleSourcesMenu     ( self , at , item                          ) :
    ##########################################################################
    if                         ( 29436051 == at                            ) :
      ########################################################################
      self . OpenPeopleSources ( "ADE"     , item                            )
      ########################################################################
      return True
    ##########################################################################
    if                         ( 29436052 == at                            ) :
      ########################################################################
      self . OpenPeopleSources ( "IAFD"    , item                            )
      ########################################################################
      return True
    ##########################################################################
    if                         ( 29436053 == at                            ) :
      ########################################################################
      self . OpenPeopleSources ( "Private" , item                            )
      ########################################################################
      return True
    ##########################################################################
    if                         ( 29436054 == at                            ) :
      ########################################################################
      self . OpenPeopleSources ( "BANG"    , item                            )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def WebSearchMenu            ( self , mm , item                          ) :
    ##########################################################################
    if                         ( self . NotOkay ( item                   ) ) :
      return
    ##########################################################################
    uuid = item  . data        ( Qt . UserRole                               )
    uuid = int                 ( uuid                                        )
    ##########################################################################
    if                         ( uuid not in self . PeopleOPTs             ) :
      return
    ##########################################################################
    MSG  = self  . getMenuItem ( "WebSearchPeople"                           )
    COL  = mm    . addMenu     ( MSG                                         )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SearchADE"                                 )
    mm   . addActionFromMenu   ( COL , 29436001 , MSG                        )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SearchIAFD"                                )
    mm   . addActionFromMenu   ( COL , 29436002 , MSG                        )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SearchPrivate"                             )
    mm   . addActionFromMenu   ( COL , 29436003 , MSG                        )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SearchBANG"                                )
    mm   . addActionFromMenu   ( COL , 29436004 , MSG                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunWebSearchMenu           ( self , at , item                        ) :
    ##########################################################################
    if                           ( 29436001 == at                          ) :
      ########################################################################
      ubase = "https://www.adultdvdempire.com/allsearch/search?q="
      pname = item  . text       (                                           )
      pname = pname . replace    ( " " , "%20"                               )
      PURL  = f"{ubase}{pname}"
      ########################################################################
      QDesktopServices . openUrl ( PURL                                      )
      ########################################################################
      return True
    ##########################################################################
    if                           ( 29436002 == at                          ) :
      ########################################################################
      ubase = "https://www.iafd.com/results.asp?searchtype=comprehensive&searchstring="
      pname = item  . text       (                                           )
      pname = pname . replace    ( " " , "+"                                 )
      PURL  = f"{ubase}{pname}"
      ########################################################################
      QDesktopServices . openUrl ( PURL                                      )
      ########################################################################
      return True
    ##########################################################################
    if                           ( 29436003 == at                          ) :
      ########################################################################
      ubase = "https://www.private.com/search.php?query="
      pname = item  . text       (                                           )
      pname = pname . replace    ( " " , "+"                                 )
      PURL  = f"{ubase}{pname}"
      ########################################################################
      QDesktopServices . openUrl ( PURL                                      )
      ########################################################################
      return True
    ##########################################################################
    if                           ( 29436004 == at                          ) :
      ########################################################################
      ubase = "https://www.bang.com/videos?term="
      pname = item  . text       (                                           )
      pname = pname . replace    ( " " , "+"                                 )
      PURL  = f"{ubase}{pname}"
      ########################################################################
      QDesktopServices . openUrl ( PURL                                      )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def UsageMenu                  ( self , mm , item                        ) :
    ##########################################################################
    if                           ( self . NotOkay ( item                 ) ) :
      return
    ##########################################################################
    uuid  = item  . data         ( Qt . UserRole                             )
    uuid  = int                  ( uuid                                      )
    ##########################################################################
    if                           ( uuid not in self . PeopleOPTs           ) :
      return
    ##########################################################################
    MSG   = self  . getMenuItem  ( "PeopleUsage"                             )
    COL   = mm    . addMenu      ( MSG                                       )
    USAGE = self  . Translations [ self . ClassTag ] [ "Usage"               ]
    KEYs  = USAGE . keys         (                                           )
    USED  = self  . PeopleOPTs   [ uuid ] [ "Used"                           ]
    BAID  = 29431000
    ##########################################################################
    for ID in KEYs                                                           :
      ########################################################################
      VID = int                  ( ID                                        )
      CHK =                      ( USED == VID                               )
      MSG = USAGE                [ ID                                        ]
      BXD = int                  ( VID + BAID                                )
      ########################################################################
      mm  . addActionFromMenu    ( COL , BXD , MSG , True , CHK              )
    ##########################################################################
    return mm
  ############################################################################
  def RunUsageMenu               ( self , at , item                        ) :
    ##########################################################################
    if                           ( at < 29431000                           ) :
      return False
    ##########################################################################
    if                           ( at > 29431100                           ) :
      return False
    ##########################################################################
    uuid  = item  . data         ( Qt . UserRole                             )
    uuid  = int                  ( uuid                                      )
    ##########################################################################
    if                           ( uuid not in self . PeopleOPTs           ) :
      return
    ##########################################################################
    VID   = int                  ( at - 29431000                             )
    VSD   = f"{VID}"
    USAGE = self  . Translations [ self . ClassTag ] [ "Usage"               ]
    ##########################################################################
    if                           ( VSD not in USAGE                        ) :
      return False
    ##########################################################################
    VP    =                      ( uuid , VID ,                              )
    self  . Go                   ( self . UpdatePeopleUsage , VP             )
    ##########################################################################
    return True
  ############################################################################
  def DisplayMenu                ( self , mm                               ) :
    ##########################################################################
    MSG   = self  . getMenuItem  ( "DisplayUsage"                            )
    COL   = mm    . addMenu      ( MSG                                       )
    USAGE = self  . Translations [ self . ClassTag ] [ "Usage"               ]
    KEYs  = USAGE . keys         (                                           )
    ##########################################################################
    MSG   = self  . getMenuItem  ( "RefreshOptions"                          )
    mm    . addActionFromMenu    ( COL                                     , \
                                   29432101                                , \
                                   MSG                                     , \
                                   True                                    , \
                                   self . RefreshOpts                        )
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    BAID  = 29432000
    ##########################################################################
    for ID in KEYs                                                           :
      ########################################################################
      VID = int                  ( ID                                        )
      CHK =                      ( VID in self . UsedOptions                 )
      MSG = USAGE                [ ID                                        ]
      BXD = int                  ( VID + BAID                                )
      ########################################################################
      mm  . addActionFromMenu    ( COL , BXD , MSG , True , CHK              )
    ##########################################################################
    return mm
  ############################################################################
  def RunDisplayMenu              ( self , at                              ) :
    ##########################################################################
    if                            ( at == 29432101                         ) :
      ########################################################################
      if                          ( self . RefreshOpts                     ) :
        self . RefreshOpts = False
      else                                                                   :
        self . RefreshOpts = True
      ########################################################################
      return True
    ##########################################################################
    if                            ( at < 29432000                          ) :
      return False
    ##########################################################################
    if                            ( at > 29432100                          ) :
      return False
    ##########################################################################
    VID    = int                  ( at - 29432000                            )
    VSD    = f"{VID}"
    USAGE  = self  . Translations [ self . ClassTag ] [ "Usage"              ]
    ##########################################################################
    if                            ( VSD not in USAGE                       ) :
      return False
    ##########################################################################
    if                            ( VID in self . UsedOptions              ) :
      ########################################################################
      ROP  =                      [                                          ]
      ########################################################################
      for ID in self . UsedOptions                                           :
        ######################################################################
        if                        ( VID != ID                              ) :
          ROP . append            ( ID                                       )
      ########################################################################
      self . UsedOptions = ROP
      ########################################################################
    else                                                                     :
      ########################################################################
      self . UsedOptions . append ( VID                                      )
    ##########################################################################
    if                            ( self . RefreshOpts                     ) :
      self   . restart            (                                          )
    ##########################################################################
    return True
  ############################################################################
  def Menu                               ( self , pos                      ) :
    ##########################################################################
    doMenu = self . isFunction           ( self . HavingMenu                 )
    if                                   ( not doMenu                      ) :
      return False
    ##########################################################################
    self   . Notify                      ( 0                                 )
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager                 ( self                              )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                                   ( self . isSearching (          ) ) :
      ########################################################################
      msg  = self . getMenuItem          ( "NotSearch"                       )
      mm   . addAction                   ( 7401 , msg                        )
    ##########################################################################
    self   . StopIconMenu                ( mm                                )
    self   . AmountIndexMenu             ( mm , True                         )
    ##########################################################################
    if                                   ( uuid > 0                        ) :
      ########################################################################
      self . PeopleFavourite             ( mm , uuid , atItem                )
      ########################################################################
      msg  = self . getMenuItem          ( "PeopleDetails"                   )
      icon = QIcon                       ( ":/images/actor.png"              )
      mm   . addActionWithIcon           ( 5001 , icon , msg                 )
      ########################################################################
      mm   . addSeparator                (                                   )
    ##########################################################################
    self   . AppendRefreshAction         ( mm , 1001                         )
    self   . AppendInsertAction          ( mm , 1101                         )
    self   . AppendSearchAction          ( mm , 1102                         )
    ##########################################################################
    if                                   ( len ( items ) > 0               ) :
      ########################################################################
      self . AppendDeleteAction          ( mm , 1103                         )
    ##########################################################################
    if                                   ( uuid > 0                        ) :
      ########################################################################
      self . AppendRenameAction          ( mm , 1104                         )
      self . AssureEditNamesAction       ( mm , 1601 , atItem                )
    ##########################################################################
    mm     . addSeparator                (                                   )
    ##########################################################################
    self   . FunctionsMenu               ( mm , uuid , atItem                )
    self   . GroupsMenu                  ( mm , uuid , atItem                )
    self   . RelatedGalleriesMenu        ( mm , uuid , atItem                )
    self   . FeaturesMenu                ( mm ,        atItem                )
    self   . PeopleSourcesMenu           ( mm ,        atItem                )
    self   . WebSearchMenu               ( mm ,        atItem                )
    self   . UsageMenu                   ( mm ,        atItem                )
    self   . DisplayMenu                 ( mm                                )
    self   . SortingMenu                 ( mm                                )
    self   . LocalityMenu                ( mm                                )
    self   . ScrollBarMenu               ( mm                                )
    self   . DockingMenu                 ( mm                                )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                     ( self    . menuFont (            ) )
    aa     = mm . exec_                  ( QCursor . pos      (            ) )
    at     = mm . at                     ( aa                                )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu   ( at                                )
    ##########################################################################
    if                                   ( OKAY                            ) :
      ########################################################################
      self . restart                     (                                   )
      ########################################################################
      return True
    ##########################################################################
    if                                   ( uuid > 0                        ) :
      ########################################################################
      OKAY = self . RunPeopleFavourite   ( uuid , atItem                     )
      ########################################################################
      if                                 ( OKAY                            ) :
        ######################################################################
        return True
    ##########################################################################
    OKAY   = self . RunDocking           ( mm , aa                           )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu     ( at , uuid , atItem                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu        ( at , uuid , atItem                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunRelatedGalleriesMenu ( at , uuid , atItem             )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunFeaturesMenu      ( at ,        atItem                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunPeopleSourcesMenu ( at , atItem                       )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunWebSearchMenu     ( at , atItem                       )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunUsageMenu         ( at , atItem                       )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunDisplayMenu       ( at                                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu       ( at                                )
    if                                   ( OKAY                            ) :
      ########################################################################
      self . restart                     (                                   )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu   ( at                                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunScrollBarMenu     ( at                                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu      ( at                                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    if                                   ( at == 5001                      ) :
      ########################################################################
      self . OpenItemPeopleDetails       ( atItem                            )
      ########################################################################
      return True
    ##########################################################################
    if                                   ( at == 1001                      ) :
      ########################################################################
      self . restart                     (                                   )
      ########################################################################
      return True
    ##########################################################################
    if                                   ( at == 1101                      ) :
      ########################################################################
      self . InsertItem                  (                                   )
      ########################################################################
      return True
    ##########################################################################
    if                                   ( at == 1102                      ) :
      self . Search                      (                                   )
      return True
    ##########################################################################
    if                                   ( at == 1103                      ) :
      ########################################################################
      self . DeleteItems                 (                                   )
      ########################################################################
      return True
    ##########################################################################
    if                                   ( at == 1104                      ) :
      ########################################################################
      self . RenamePeople                (                                   )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor    ( at , 1601 , atItem                )
    if                                   ( OKAY                            ) :
      return True
    ##########################################################################
    if                                   ( at == 7401                      ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart                     (                                   )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

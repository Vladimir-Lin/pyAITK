# -*- coding: utf-8 -*-
##############################################################################
## VideoAlbumsView
##############################################################################
import os
import sys
import time
import requests
import threading
import json
import glob
import shutil
import pathlib
##############################################################################
from   PySide6                              import QtCore
from   PySide6                              import QtGui
from   PySide6                              import QtWidgets
from   PySide6 . QtCore                     import *
from   PySide6 . QtGui                      import *
from   PySide6 . QtWidgets                  import *
from   AITK    . Qt6                        import *
##############################################################################
from   AITK    . Qt6        . IconDock      import IconDock    as IconDock
##############################################################################
from   AITK    . Qt6        . MenuManager   import MenuManager as MenuManager
from   AITK    . Qt6        . LineEdit      import LineEdit    as LineEdit
from   AITK    . Qt6        . ComboBox      import ComboBox    as ComboBox
from   AITK    . Qt6        . SpinBox       import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation      import Relation
from   AITK    . Calendars  . StarDate      import StarDate
from   AITK    . Calendars  . Periode       import Periode
from   AITK    . Documents  . Name          import Name        as NameItem
from   AITK    . Documents  . JSON          import Load        as LoadJson
from   AITK    . Documents  . JSON          import Save        as SaveJson
from   AITK    . Documents  . Identifier    import Identifier  as IdentifierItem
from   AITK    . Pictures   . Picture       import Picture     as PictureItem
from   AITK    . Pictures   . Gallery       import Gallery     as GalleryItem
from   AITK    . People     . People        import People      as PeopleItem
from   AITK    . Videos     . Album         import Album       as AlbumItem
from   AITK    . Videos     . Film          import Film        as FilmItem
##############################################################################
from   AITK    . UUIDs      . UuidListings6 import appendUuid
from   AITK    . UUIDs      . UuidListings6 import appendUuids
from   AITK    . UUIDs      . UuidListings6 import assignUuids
from   AITK    . UUIDs      . UuidListings6 import getUuids
##############################################################################
class VideoAlbumsView             ( IconDock                               ) :
  ############################################################################
  HavingMenu             = 1371434312
  ############################################################################
  OwnedPeopleGroup       = Signal ( str ,       int , str                    )
  OwnedPeopleGroupRelate = Signal ( str ,       int , str , str              )
  ShowPersonalGallery    = Signal ( str ,       int , str ,       QIcon      )
  ShowPersonalIcons      = Signal ( str ,       int , str , str , QIcon      )
  GalleryGroup           = Signal ( str ,       int , str                    )
  ShowGalleriesRelation  = Signal ( str ,       int , str , str , QIcon      )
  OwnedOrganizationGroup = Signal ( str ,       int , str , str , QIcon      )
  OwnedEpisodesSubgroup  = Signal ( str ,       int , str                    )
  emitConnectAlbum       = Signal ( str                                      )
  emitOpenVideoGroup     = Signal ( str ,       int , str , str , QIcon      )
  emitFragmentEditor     = Signal ( str , str , int , str , str , QIcon      )
  ShowAlbumDateEvents    = Signal ( str , str ,                   QIcon      )
  ShowWebPages           = Signal ( str ,       int , str , str , QIcon      )
  ShowAlbumSources       = Signal ( str ,       str , str ,       QIcon      )
  OpenVariantTables      = Signal ( str ,       str , int , str , dict       )
  emitOpenSmartNote      = Signal ( str                                      )
  OpenLogHistory         = Signal ( str , str , str  , str , str             )
  emitLog                = Signal ( str                                      )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . ClassTag           = "VideoAlbums"
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . GType              = 76
    self . SortOrder          = "asc"
    self . ShowIdentifier     = False
    ##########################################################################
    self . FetchTableKey      = "VideoAlbums"
    self . SortByName         = False
    self . ExtraINFOs         = True
    self . RefreshOpts        = True
    self . Watermarking       = True
    self . UsedOptions        = [ 1 , 2 , 3 , 4 , 5 , 6 , 7                  ]
    self . AlbumOPTs          = {                                            }
    ##########################################################################
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    self . PickedUuid         = 0
    self . PickedUuids        = [                                            ]
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
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
    self . Relation . setT1        ( "Album"                                 )
    self . Relation . setT2        ( "Album"                                 )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( True                                    )
    self . setAcceptDrops          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    self . setMinimumSize          ( 144 , 200                               )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 660 , 800 )                       )
  ############################################################################
  def PrepareFetchTableKey       ( self                                    ) :
    ##########################################################################
    self . subgroupFetchTableKey (                                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . PrepareFetchTableKey            (                                 )
    ##########################################################################
    self . AppendToolNamingAction          (                                 )
    self . AppendSideActionWithIcon        ( "ConnectAlbum"                , \
                                             ":/images/sqltable.png"       , \
                                             self . ConnectDirectoryToAlbum  )
    self . AppendSideActionWithIcon        ( "AlbumGallery"                , \
                                             ":/images/pictures.png"       , \
                                             self . OpenCurrentGallery       )
    self . AppendSideActionWithIcon        ( "GalleriesGroups"             , \
                                             ":/images/galleries.png"      , \
                                             self . OpenCurrentGalleries     )
    self . AppendSideActionWithIcon        ( "Crowds"                      , \
                                             ":/images/peoplegroups.png"   , \
                                             self . OpenCurrentCrowds        )
    self . AppendSideActionWithIcon        ( "AlbumSubgroups"              , \
                                             ":/images/modifyproject.png"  , \
                                             self . OpenEpisodesSubgroup     )
    self . AppendSideActionWithIcon        ( "VideoFragments"              , \
                                             ":/images/vfragments.png"     , \
                                             self . OpenVFragments           )
    self . AppendSideActionWithIcon        ( "AssignIdentifier"            , \
                                             ":/images/jointag.png"        , \
                                             self . OpenAlbumIdentifier      )
    self . AppendSideActionWithIcon        ( "DateEvents"                  , \
                                             ":/images/calendars.png"      , \
                                             self . OpenAlbumDateEvents      )
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
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    if                        ( not self . isGrouping (                  ) ) :
      return
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "ViewAlbumParameter"                         )
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
    self . LinkAction ( "Refresh"    , self . startup        , Enabled       )
    self . LinkAction ( "Insert"     , self . InsertItem     , Enabled       )
    self . LinkAction ( "Rename"     , self . RenameVideo    , Enabled       )
    self . LinkAction ( "Delete"     , self . DeleteItems    , Enabled       )
    self . LinkAction ( "Cut"        , self . DeleteItems    , Enabled       )
    self . LinkAction ( "Copy"       , self . DoCopyItemText , Enabled       )
    self . LinkAction ( "Paste"      , self . PasteItems     , Enabled       )
    self . LinkAction ( "Search"     , self . Search         , Enabled       )
    self . LinkAction ( "Home"       , self . PageHome       , Enabled       )
    self . LinkAction ( "End"        , self . PageEnd        , Enabled       )
    self . LinkAction ( "PageUp"     , self . PageUp         , Enabled       )
    self . LinkAction ( "PageDown"   , self . PageDown       , Enabled       )
    self . LinkAction ( "SelectAll"  , self . SelectAll      , Enabled       )
    self . LinkAction ( "SelectNone" , self . SelectNone     , Enabled       )
    self . LinkAction ( "Font"       , self . ChangeItemFont , Enabled       )
    ##########################################################################
    ## self . TellStory  (                                        Enabled       )
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
    self . clear             (                                               )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def GetUuidIcon                    ( self , DB , UUID                    ) :
    ##########################################################################
    RELTAB   = self . Tables         [ "Relation"                            ]
    ##########################################################################
    if                               ( "RelationIcons" in self . Tables    ) :
      RELTAB = self . Tables         [ "RelationIcons"                       ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "Album" , UUID          )
  ############################################################################
  def FetchBaseINFO                  ( self , DB , UUID , PUID             ) :
    ##########################################################################
    ICZ    = self . FetchEntityImage (        DB , PUID                      )
    ##########################################################################
    if                               ( ICZ in self . EmptySet              ) :
      return
    ##########################################################################
    if                               ( UUID in self . AlbumOPTs            ) :
      ########################################################################
      self . AlbumOPTs [ UUID ] [ "Image" ] = ICZ
      self . AlbumOPTs [ UUID ] [ "PUID"  ] = PUID
      ########################################################################
    else                                                                     :
      ########################################################################
      self . AlbumOPTs [ UUID ] =    { "Image" : ICZ                       , \
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
    if                                ( UUID not in self . AlbumOPTs       ) :
      return
    ##########################################################################
    GOPTs     = self . AlbumOPTs      [ UUID                                 ]
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
    DINFO     = False
    ##########################################################################
    if                                ( "Used"     in GOPTs                ) :
      ########################################################################
      USED    = GOPTs                 [ "Used"                               ]
      ########################################################################
      if                              ( USED in [ 2 , 3 , 4 , 5 , 6 , 7 ]  ) :
        DINFO = True
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
  def doubleClicked                   ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return False
    ##########################################################################
    text = item . text                (                                      )
    icon = item . icon                (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    ## self . ShowPersonalGallery . emit ( text , 64 , xsid , icon              )
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
  def FetchRegularDepotCount        ( self , DB                            ) :
    ##########################################################################
    ALMTAB = self . Tables          [ "Albums"                               ]
    UOPTS  = " , " . join           ( str(x) for x in self . UsedOptions     )
    QQ     = f"""select count(*) from {ALMTAB}
                 where ( `used` in ( {UOPTS} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def FetchGroupMembersCount ( self , DB                                   ) :
    ##########################################################################
    ALMTAB = self . Tables   [ "Albums"                                      ]
    RELTAB = self . Tables   [ "Relation"                                    ]
    UOPTS  = " , " . join    ( str(x) for x in self . UsedOptions            )
    RQ     = self . Relation . GetSecondUuidsSqlSyntax ( RELTAB              )
    ##########################################################################
    QQ     = f"""select count(*) from {ALMTAB}
                 where ( `used` in ( {UOPTS} ) )
                   and ( `uuid` in ( {RQ} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def FetchGroupOwnersCount ( self , DB                                    ) :
    ##########################################################################
    ALMTAB = self . Tables  [ "Albums"                                       ]
    RELTAB = self . Tables  [ "Relation"                                     ]
    UOPTS  = " , " . join   ( str(x) for x in self . UsedOptions             )
    RQ     = self . Relation . GetFirstUuidsSqlSyntax ( RELTAB               )
    ##########################################################################
    QQ     = f"""select count(*) from {ALMTAB}
                 where ( `used` in ( {UOPTS} ) )
                   and ( `uuid` in ( {RQ} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    ALMTAB = self . Tables [ "Albums"                                        ]
    UOPTS  = " , " . join  ( str(x) for x in self . UsedOptions              )
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"""select `uuid` from {ALMTAB}
                 where ( `used` in ( {UOPTS} ) )
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def ObtainSubgroupUuids                    ( self , DB                   ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ASC    =                        ( ORDER . lower in [ "asc"             ] )
    LMTS   = f"limit {SID} , {AMOUNT}"
    ALMTAB = self . Tables          [ "Albums"                               ]
    RELTAB = self . Tables          [ "Relation"                             ]
    ## RELTAB = self . Tables          [ "RelationVideos"                       ]
    NAMTAB = self . Tables          [ "Names"                                ]
    UOPTS  = " , " . join           ( str(x) for x in self . UsedOptions     )
    ##########################################################################
    if                              ( self . isSubordination (           ) ) :
      ########################################################################
      RQ   = self . Relation . GetSecondUuidsSqlSyntax ( RELTAB              )
      EQ   = f"""select `uuid` from {ALMTAB}
                 where ( `uuid` in ( {RQ} ) )
                   and ( `used` in ( {UOPTS} ) )"""
      VQ   = f"and ( `second` in ( {EQ} ) )"
      SQ   = f"order by `position` {ORDER} , `reverse` {ORDER}"
      QQ   = f"{RQ} {VQ} {SQ} {LMTS} ;"
      QQ   = " " . join             ( QQ . split ( )                         )
      UIDs = DB . ObtainUuids       ( QQ                                     )
      ########################################################################
      if                            ( len ( UIDs ) <= 0                    ) :
        return UIDs
      if                            ( not self . SortByName                ) :
        return UIDs
      ########################################################################
      UXDs = " , " . join           ( str(x) for x in UIDs                   )
      LC   = self . getLocality     (                                        )
      QQ   = f"""select distinct(`uuid`) from {NAMTAB}
                 where ( `uuid` in ( {UXDs} ) )
                   and ( `locality` = {LC} )
                 order by `name` {ORDER} {LMTS} ;"""
      QQ   = " " . join             ( QQ . split ( )                         )
      ########################################################################
      UNDs = DB . ObtainUuids       ( QQ                                     )
      ########################################################################
      return self . JoinPrimaryUuidsInOrder ( UNDs , UIDs  , ASC             )
    ##########################################################################
    if                              ( self . isReverse       (           ) ) :
      ########################################################################
      RQ   = self . Relation . GetFirstUuidsSqlSyntax ( RELTAB               )
      EQ   = f"""select `uuid` from {ALMTAB}
                 where ( `uuid` in ( {RQ} ) )
                   and ( `used` in ( {UOPTS} ) )"""
      VQ   = f"and ( `first` in ( {EQ} ) )"
      SQ   = f"order by `reverse` {ORDER} , `position` {ORDER}"
      QQ   = f"{RQ} {VQ} {SQ} {LMTS} ;"
      QQ   = " " . join             ( QQ . split ( )                         )
      ########################################################################
      UIDs = DB . ObtainUuids       ( QQ                                     )
      ########################################################################
      if                            ( len ( UIDs ) <= 0                    ) :
        return UIDs
      if                            ( not self . SortByName                ) :
        return UIDs
      ########################################################################
      UXDs = " , " . join           ( str(x) for x in UIDs                   )
      LC   = self . getLocality     (                                        )
      QQ   = f"""select distinct(`uuid`) from {NAMTAB}
                 where ( `uuid` in ( {UXDs} ) )
                   and ( `locality` = {LC} )
                 order by `name` {ORDER} {LMTS} ;"""
      QQ   = " " . join             ( QQ . split ( )                         )
      ########################################################################
      UNDs = DB . ObtainUuids       ( QQ                                     )
      ########################################################################
      return self . JoinPrimaryUuidsInOrder ( UNDs , UIDs  , ASC             )
    ##########################################################################
    return                          [                                        ]
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
  def ObtainsUuidNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    NAMEs     =                        {                                     }
    ##########################################################################
    if                                 ( len ( UUIDs ) > 0                 ) :
      ########################################################################
      TABLE   = self . Tables          [ "Names"                             ]
      NAMEs   = self . GetNames        ( DB , TABLE , UUIDs                  )
    ##########################################################################
    if                                 ( self . ShowIdentifier             ) :
      ########################################################################
      NKs     =                        {                                     }
      ALBUM   = AlbumItem              (                                     )
      ALBUM   . Settings = self . Settings
      ALBUM   . Tables   = self . Tables
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        N     = NAMEs                  [ UUID                                ]
        ALBUM . Uuid = UUID
        IDs   = ALBUM . GetIdentifiers ( DB                                  )
        ######################################################################
        if                             ( len ( IDs ) > 0                   ) :
          ####################################################################
          ID  = " , " . join           ( IDs                                 )
          ####################################################################
          if                           ( len ( ID ) > 0                    ) :
            ##################################################################
            if                         ( len ( IDs ) == 1                  ) :
              ################################################################
              N = f"[{ID}] {N}"
              ################################################################
            elif                       ( len ( ID ) > 1                    ) :
              ################################################################
              N = f"[ {ID} ] {N}"
        ######################################################################
        NKs [ UUID ] = N
      ########################################################################
      NAMEs   = NKs
    ##########################################################################
    return NAMEs
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . AlbumOPTs =                    {                                  }
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def GenerateItemToolTip             ( self , UUID                        ) :
    ##########################################################################
    if                                ( not self . StayAlive               ) :
      return
    ##########################################################################
    if                                ( UUID not in self . UuidItemMaps    ) :
      return
    ##########################################################################
    if                                ( UUID not in self . AlbumOPTs       ) :
      return
    ##########################################################################
    VAKEY  = "VideoAlbumsView"
    FMT    = self . getMenuItem       ( "AlbumToolTip"                       )
    USAGE  = self . Translations      [ VAKEY ] [ "Usage"                    ]
    STATEs = self . Translations      [ VAKEY ] [ "States"                   ]
    ##########################################################################
    USD    = self . AlbumOPTs         [ UUID ] [ "Used"                      ]
    SSS    = self . AlbumOPTs         [ UUID ] [ "States"                    ]
    PICs   = self . AlbumOPTs         [ UUID ] [ "Pictures"                  ]
    GALs   = self . AlbumOPTs         [ UUID ] [ "Galleries"                 ]
    SGPs   = self . AlbumOPTs         [ UUID ] [ "Subgroups"                 ]
    PEOs   = self . AlbumOPTs         [ UUID ] [ "People"                    ]
    VIDs   = self . AlbumOPTs         [ UUID ] [ "Videos"                    ]
    URLs   = self . AlbumOPTs         [ UUID ] [ "URLs"                      ]
    IDz    = self . AlbumOPTs         [ UUID ] [ "Identifiers"               ]
    ##########################################################################
    UMSG   = ""
    IDKz   = self . getMenuItem       ( "NoIdentifier"                       )
    ##########################################################################
    if                                ( len ( IDz ) > 0                    ) :
      ########################################################################
      IDKz = " , " . join             ( IDz                                  )
    ##########################################################################
    if                                ( f"{USD}" in USAGE                  ) :
      ########################################################################
      UMSG = USAGE                    [ f"{USD}"                             ]
    ##########################################################################
    text   = FMT . format             ( UUID                               , \
                                        VIDs                               , \
                                        PEOs                               , \
                                        PICs                               , \
                                        GALs                               , \
                                        SGPs                               , \
                                        URLs                               , \
                                        IDKz                               , \
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
    VAKEY        = "VideoAlbumsView"
    FMT          = self . getMenuItem  ( "AlbumToolTip"                      )
    USAGE        = self . Translations [ VAKEY ] [ "Usage"                   ]
    STATEs       = self . Translations [ VAKEY ] [ "States"                  ]
    ##########################################################################
    DB           = self . ConnectDB    (                                     )
    if                                 ( self . NotOkay ( DB )             ) :
      return
    ##########################################################################
    self         . PushRunnings        (                                     )
    self         . OnBusy . emit       (                                     )
    self         . FetchingINFO = True
    ##########################################################################
    ALMTAB       = self . Tables       [ "Albums"                            ]
    IDFTAB       = self . Tables       [ "Identifiers"                       ]
    PICTAB       = self . Tables       [ "Relation"                          ]
    ## PICTAB       = self . Tables       [ "RelationPictures"                  ]
    GALTAB       = self . Tables       [ "Relation"                          ]
    SGPTAB       = self . Tables       [ "Relation"                          ]
    RELTAB       = self . Tables       [ "Relation"                          ]
    PEOTAB       = self . Tables       [ "Relation"                          ]
    URLTAB       = self . Tables       [ "Relation"                          ]
    ## PEOTAB       = self . Tables       [ "RelationPeople"                    ]
    ## VIDTAB       = self . Tables       [ "RelationVideos"                    ]
    ## VIDTAB       = self . Tables       [ "RelationPeople"                    ]
    VIDTAB       = self . Tables       [ "Relation"                          ]
    REL          = Relation            (                                     )
    ALBUM        = AlbumItem           (                                     )
    ALBUM        . Settings = self . Settings
    ALBUM        . Tables   = self . Tables
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . StayAlive              ) :
        continue
      ########################################################################
      GJSON      =                     { "Used"      : 1                   , \
                                         "States"    : 0                   , \
                                         "Pictures"  : 0                   , \
                                         "Galleries" : 0                   , \
                                         "Subgroups" : 0                   , \
                                         "People"    : 0                   , \
                                         "Videos"    : 0                   , \
                                         "URLs"      : 0                     }
      ########################################################################
      if                               ( U in self . AlbumOPTs             ) :
        ######################################################################
        GOPTs    = self . AlbumOPTs    [ U                                   ]
        ######################################################################
        if                             ( "Image" in GOPTs                  ) :
          ####################################################################
          GJSON [ "Image" ] = GOPTs    [ "Image"                             ]
      ########################################################################
      self       . AlbumOPTs [ U ] = GJSON
      ########################################################################
      UMSG       = ""
      QQ         = f"""select `used` , `states` from {ALMTAB}
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
          self   . AlbumOPTs [ U ] [ "Used"   ] = USD
          self   . AlbumOPTs [ U ] [ "States" ] = SSS
          ####################################################################
          if                           ( f"{USD}" in USAGE                 ) :
            UMSG = USAGE               [ f"{USD}"                            ]
      ########################################################################
      REL        . set                 ( "first" , U                         )
      REL        . setT1               ( "Album"                             )
      REL        . setRelation         ( "Subordination"                     )
      ########################################################################
      REL        . setT2               ( "Picture"                           )
      PICs       = REL . CountSecond   ( DB , PICTAB                         )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "Pictures"  ] = PICs
      ########################################################################
      REL        . setT2               ( "Gallery"                           )
      GALs       = REL . CountSecond   ( DB , GALTAB                         )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "Galleries" ] = GALs
      ########################################################################
      REL        . setT2               ( "WebPage"                           )
      REL        . setRelation         ( "Equivalent"                        )
      URLs       = REL . CountSecond   ( DB , URLTAB                         )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "URLs" ] = URLs
      ########################################################################
      REL        . setRelation         ( "Subordination"                     )
      ########################################################################
      QQ         = f"""select count(*) from {VIDTAB}
                       where ( `t1` = 76 )
                         and ( `t2` = 11 )
                         and ( `relation` in ( 1 , 11 ) )
                         and ( `first` = {U} ) ;"""
      VIDs       = DB . GetOne         ( QQ , 0                              )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "Videos"    ] = VIDs
      ########################################################################
      REL        . set                 ( "second" , U                        )
      REL        . setT2               ( "Album"                             )
      ########################################################################
      REL        . setT1               ( "Subgroup"                          )
      SGPs       = REL . CountFirst    ( DB , SGPTAB                         )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "Subgroups" ] = SGPs
      ########################################################################
      REL        . setT1               ( "People"                            )
      PEOs       = REL . CountFirst    ( DB , PEOTAB                         )
      ########################################################################
      self       . AlbumOPTs [ U ] [ "People"    ] = PEOs
      ########################################################################
      ALBUM      . Uuid = U
      IDz        = ALBUM . GetIdentifiers ( DB                               )
      self       . AlbumOPTs [ U ] [ "Identifiers" ] = IDz
      ########################################################################
      self       . GenerateItemToolTip ( U                                   )
    ##########################################################################
    self         . GoRelax . emit      (                                     )
    self         . FetchingINFO = False
    DB           . Close               (                                     )
    ##########################################################################
    if                                 ( self . StayAlive                  ) :
      ########################################################################
      self       . Notify              ( 2                                   )
      self       . ShowStatus          ( ""                                  )
    ##########################################################################
    self         . PopRunnings         (                                     )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "album/uuids"
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
    FMTs    =              [ "album/uuids"                                 , \
                             "people/uuids"                                , \
    ##                         "gallery/uuids"                               , \
    ##                         "video/uuids"                                 , \
                             "picture/uuids"                                 ]
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
    atItem  = self . itemAt         ( mousePos                               )
    ##########################################################################
    if                              ( mtype in [ "album/uuids" ]           ) :
      ########################################################################
      if                            ( self . OldGrouping in ["Searching"]  ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        FMT = self . getMenuItem    ( "MoveAlbums"                           )
        MSG = FMT  . format         ( CNT                                    )
      else                                                                   :
        FMT = self . getMenuItem    ( "JoinAlbums"                           )
        MSG = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      if                            ( atItem in [ False , None ]           ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      FMT   = self . getMenuItem    ( "JoinPeople"                           )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      if                            ( atItem in [ False , None ]           ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      FMT   = self . getMenuItem    ( "CopyPicturesFrom"                     )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
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
    mtype  = self . DropInJSON [ "Mime"                                      ]
    UUIDs  = self . DropInJSON [ "UUIDs"                                     ]
    atItem = self . itemAt     ( mousePos                                    )
    ##########################################################################
    if                         ( mtype      in [ "people/uuids" ]          ) :
      if                       ( atItem     in self . EmptySet             ) :
        return False
      return True
    ##########################################################################
    if                         ( mtype      in [ "picture/uuids" ]         ) :
      if                       ( atItem     in self . EmptySet             ) :
        return False
      return True
    ##########################################################################
    if                         ( atItem not in self . EmptySet             ) :
      if                       ( atItem . isSelected ( )                   ) :
        return False
    ##########################################################################
    return True
  ############################################################################
  def acceptAlbumsDrop ( self                                              ) :
    return True
  ############################################################################
  def dropAlbums                   ( self , source , pos , JSOX            ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                             ( self == source                        ) :
      ########################################################################
      self . Go ( self . AlbumMoving    , ( ATID , NAME , JSOX , )           )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    self   . Go ( self . AlbumAppending , ( ATID , NAME , JSOX , )           )
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop ( self                                              ) :
    return True
  ############################################################################
  def dropPeople                   ( self , source , pos , JSOX            ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ##########################################################################
    VAL         =                  ( ATID , NAME , JSOX ,                    )
    self . Go                      ( self . PeopleAppending , VAL            )
    ##########################################################################
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures                 ( self , source , pos , JSOX            ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ##########################################################################
    VAL         =                  ( ATID , NAME , JSOX ,                    )
    self . Go                      ( self . PicturesAppending , VAL          )
    ##########################################################################
    return True
  ############################################################################
  def CopyItems ( self                                                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PasteItems ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RenameVideo     ( self                                               ) :
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
    TITLE  = "RemoveVideoItems"
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
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationVideos" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationVideos" , LAST , UUIDs   )
  ############################################################################
  def AlbumMoving      ( self , atUuid , NAME , JSON                       ) :
    ##########################################################################
    TK   = "Relation"
    ## TK   = "RelationPeople"
    MK   = "OrganizeAlbums"
    ##########################################################################
    self . MajorMoving (        atUuid ,        JSON , TK , MK               )
    ##########################################################################
    return
  ############################################################################
  def AlbumAppending      ( self , atUuid , NAME , JSON                    ) :
    ##########################################################################
    TK   = "RelationVideos"
    MK   = "OrganizeAlbums"
    ##########################################################################
    self . MajorAppending (        atUuid ,        JSON , TK , MK            )
    ##########################################################################
    return
  ############################################################################
  def PeopleAppending          ( self , atUuid , NAME , JSON               ) :
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
    RELTAB = self . Tables     [ "RelationVideos"                            ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    ##########################################################################
    REL    = Relation          (                                             )
    REL    . set               ( "second" , atUuid                           )
    REL    . setT1             ( "People"                                    )
    REL    . setT2             ( "Album"                                     )
    REL    . setRelation       ( "Subordination"                             )
    ##########################################################################
    for PUID in UUIDs                                                        :
      ########################################################################
      REL  . set               ( "first"  , PUID                             )
      REL  . Join              ( DB       , RELTAB                           )
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
  def PicturesAppending            ( self , atUuid , NAME , JSON           ) :
    ##########################################################################
    ## T1  = "People"
    ## TAB = "RelationPeople"
    ##########################################################################
    ## OK  = self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1  )
    ## if                             ( not OK                                ) :
    ##   return
    ##########################################################################
    ## self   . loading               (                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyDirectory                 ( self , DIR , path                    ) :
    ##########################################################################
    if                              ( not os . path . isdir ( path )       ) :
      ########################################################################
      try                                                                    :
        shutil . copytree           ( DIR , path                             )
      except                                                                 :
        return False
      ########################################################################
      return True
    ##########################################################################
    names    = os . listdir         ( DIR                                    )
    for name in names                                                        :
      ########################################################################
      SRC    = os . path . join     ( DIR  , name                            )
      DST    = os . path . join     ( path , name                            )
      ########################################################################
      if                            ( os . path . isdir ( SRC )            ) :
        ######################################################################
        OK   = self . CopyDirectory ( SRC , DST                              )
        if                          ( not OK                               ) :
          return False
        ######################################################################
      else                                                                   :
        ######################################################################
        if                          ( not os . path . isfile ( DST )       ) :
          if                        ( "Folder.pri" not in name             ) :
            ##################################################################
            try                                                              :
              shutil . copy2        ( SRC , DST                              )
            except                                                           :
              return False
    ##########################################################################
    return True
  ############################################################################
  def BuildAlbum                 ( self , templDIR , path                  ) :
    ##########################################################################
    OK = self . CopyDirectory    (        templDIR , path                    )
    if                           ( not OK                                  ) :
      self . Notify              ( 1                                         )
      return
    ##########################################################################
    VIDPATH    = f"{path}/videos"
    TAILs      =                 [ "*.mp4"                                 , \
                                   "*.mkv"                                 , \
                                   "*.avi"                                 , \
                                   "*.wmv"                                 , \
                                   "*.vob"                                 , \
                                   "*.rmvb"                                  ]
    ##########################################################################
    for suffix in TAILs                                                      :
      ########################################################################
      for file in glob . glob    ( f"{path}/{suffix}"                      ) :
        shutil . move            ( file , VIDPATH                            )
    ##########################################################################
    IMGPATH    = f"{path}/images"
    TAILs      =                 [ "*.jpg"                                 , \
                                   "*.jpeg"                                , \
                                   "*.png"                                   ]
    ##########################################################################
    for suffix in TAILs                                                      :
      ########################################################################
      for file in glob . glob    ( f"{path}/{suffix}"                      ) :
        shutil . move            ( file , IMGPATH                            )
    ##########################################################################
    return
  ############################################################################
  def ExportAlbumM3U             ( self , path                             ) :
    ##########################################################################
    VIDPATH     = f"{path}/videos"
    SUFFIXs     =                [ ".mp4"                                  , \
                                   ".mkv"                                  , \
                                   ".avi"                                  , \
                                   ".wmv"                                  , \
                                   ".vob"                                  , \
                                   ".rmvb"                                   ]
    FILEs       =                [                                           ]
    ##########################################################################
    LISTS       = os . listdir   ( VIDPATH                                   )
    for FILE in LISTS                                                        :
      ########################################################################
      SUFFIX    = pathlib . Path ( FILE                                      )
      SUFFIX    = SUFFIX . suffix
      SUFFIX    = SUFFIX . lower (                                           )
      ########################################################################
      if                         ( SUFFIX   in SUFFIXs                     ) :
        ######################################################################
        if                       ( FILE not in FILEs                       ) :
          FILEs . append         ( FILE                                      )
    ##########################################################################
    if                           ( len ( FILEs ) <= 0                      ) :
      return                     [                                           ]
    ##########################################################################
    M3UF        = f"{path}/Album.m3u"
    M3U         =                [ "#EXTM3U"                                 ]
    ##########################################################################
    PTAG        = "# Playlist created by CIOS/AITK Video Tools"
    M3U         . append         ( PTAG                                      )
    ##########################################################################
    for FILE in FILEs                                                        :
      ########################################################################
      M3U       . append         ( f"#EXTINF:0,{FILE}"                       )
      M3U       . append         ( f"videos/{FILE}"                          )
    ##########################################################################
    M3UX        = "\r\n" . join  ( M3U                                       )
    with open                    ( M3UF , 'w' , encoding = "utf-8" ) as f    :
      f         . write          ( M3UX                                      )
    ##########################################################################
    return FILEs
  ############################################################################
  def GetAlbumNames                 ( self , DB , uuid                     ) :
    ##########################################################################
    NAMTAB   = self . Tables        [ "Names"                                ]
    NAMEs    =                      [                                        ]
    ##########################################################################
    NIT      = NameItem             (                                        )
    NIT      . Uuid      = uuid
    NIT      . Relevance = 0
    ##########################################################################
    IDs      = NIT . ObtainsIDs     ( DB , NAMTAB                            )
    ##########################################################################
    for ID in IDs                                                            :
      ########################################################################
      NIT    . Id = ID
      ########################################################################
      if                            ( NIT . ObtainsById ( DB , NAMTAB )    ) :
        ######################################################################
        X    = NIT . Name
        ######################################################################
        try                                                                  :
          X  = X . decode           ( "utf-8"                                )
        except                                                               :
          pass
        ######################################################################
        J    =                      { "Name"     : X                       , \
                                      "Locality" : NIT . Locality          , \
                                      "Priority" : NIT . Priority            }
        NAMEs . append              ( J                                      )
    ##########################################################################
    return NAMEs
  ############################################################################
  def UpdateAlbumName    ( self , path , IDs , NAMEs                       ) :
    ##########################################################################
    if                   ( len ( IDs   ) <= 0                              ) :
      return
    ##########################################################################
    if                   ( len ( NAMEs ) <= 0                              ) :
      return
    ##########################################################################
    NFILE    = f"{path}/scripts/name.txt"
    TEXT     = ""
    ##########################################################################
    try                                                                      :
      with open          ( NFILE , "rb" ) as f                               :
        TEXT = f . read  (                                                   )
    except                                                                   :
      pass
    ##########################################################################
    if                   ( len ( TEXT ) > 0                                ) :
      return
    ##########################################################################
    NAME     = ""
    if                   ( len ( IDs ) > 0                                 ) :
      NAME   = IDs       [ 0                                                 ]
    if                   ( ( len ( NAME ) <= 0 ) and ( len ( NAMEs ) > 0 ) ) :
        NAME = NAMEs     [ 0 ] [ "Name"                                      ]
    ##########################################################################
    if                   ( len ( NAME ) <= 0                               ) :
      return
    ##########################################################################
    with open            ( NFILE , 'w' , encoding = "utf-8" ) as f           :
      f      . write     ( NAME                                              )
    ##########################################################################
    return
  ############################################################################
  def ExportAlbumCovers              ( self , DB , uuid , path             ) :
    ##########################################################################
    RELTAB   = self . Tables         [ "Relation"                            ]
    PICTAB   = "`pictures_covers`"
    DPOTAB   = "`pictures_depot_covers`"
    ##########################################################################
    GALM     = GalleryItem           (                                       )
    COVERS   = GALM . GetPictures    ( DB , RELTAB , uuid , 76 , 12          )
    ##########################################################################
    AT       = 0
    PIC      = PictureItem           (                                       )
    ##########################################################################
    for COVER in COVERS                                                      :
      ########################################################################
      PIC    . UUID = COVER
      FILE   = COVER
      SUFFIX = ""
      if                             ( AT == 0                             ) :
        FILE = "Cover"
      ########################################################################
      INFO   = PIC . GetInformation  ( DB , PICTAB , COVER                   )
      if                             ( INFO not in [ False , None ]        ) :
        ######################################################################
        SUFFIX = INFO                [ "Suffix"                              ]
      ########################################################################
      if                             ( len ( SUFFIX ) > 0                  ) :
        ######################################################################
        FNAM = f"{path}/images/{FILE}.{SUFFIX}"
        PIC  . Export                ( DB , DPOTAB , FNAM                    )
      ########################################################################
      AT     = AT + 1
    ##########################################################################
    return COVERS
  ############################################################################
  def ExportGalleries                 ( self , DB , GUID , path            ) :
    ##########################################################################
    RELTAB     = self . Tables        [ "Relation"                           ]
    PICTAB     = "`pictures`"
    DPOTAB     = "`picturedepot`"
    GALM       = GalleryItem          (                                      )
    PICTURES   = GALM . GetPictures   ( DB , RELTAB , GUID , 64 , 1          )
    ##########################################################################
    if                                ( len ( PICTURES ) <= 0              ) :
      return                          [                                      ]
    ##########################################################################
    GDIR       = f"{path}/images/{GUID}"
    if                                ( not os . path . isdir ( GDIR )     ) :
      os       . mkdir                ( GDIR                                 )
    ##########################################################################
    AT         = 1
    PIC        = PictureItem          (                                      )
    ##########################################################################
    for PCID in PICTURES                                                     :
      ########################################################################
      PIC      . UUID = PCID
      SUFFIX   = ""
      ########################################################################
      INFO     = PIC . GetInformation ( DB , PICTAB , PCID                   )
      if                              ( INFO not in [ False , None ]       ) :
        ######################################################################
        SUFFIX = INFO                 [ "Suffix"                             ]
      ########################################################################
      if                              ( len ( SUFFIX ) > 0                 ) :
        ######################################################################
        ORDER  = f"{AT}" . zfill      ( 4                                    )
        ######################################################################
        FNAM   = f"{path}/images/{GUID}/{ORDER}-{PCID}.{SUFFIX}"
        PIC    . Export               ( DB , DPOTAB , FNAM                   )
      ########################################################################
      AT       = AT + 1
    ##########################################################################
    return PICTURES
  ############################################################################
  def ExportAlbumGalleries               ( self , DB , uuid , path         ) :
    ##########################################################################
    RELTAB    = self . Tables            [ "Relation"                        ]
    PICTAB    = "`pictures_covers`"
    DPOTAB    = "`pictures_depot_covers`"
    ##########################################################################
    GALM      = GalleryItem              (                                   )
    GALLERIES = GALM . GetOwnerGalleries ( DB , RELTAB , "Album" , uuid      )
    ##########################################################################
    JGALM     =                          { "Galleries" : GALLERIES           }
    ##########################################################################
    for GALLERY in GALLERIES                                                 :
      ########################################################################
      PICS    = self . ExportGalleries   ( DB , GALLERY , path               )
      JGALM [ GALLERY ] = PICS
    ##########################################################################
    return JGALM
  ############################################################################
  def ExportActorThumbnails           ( self , DB , PUID , path            ) :
    ##########################################################################
    RELTAB     = self . Tables        [ "Relation"                           ]
    PICTAB     = "`pictures_faces`"
    DPOTAB     = "`pictures_depot_faces`"
    ##########################################################################
    PEOW       = PeopleItem           (                                      )
    ICONs      = PEOW . GetIcons      ( DB , RELTAB , PUID                   )
    ##########################################################################
    if                                ( len ( ICONs ) <= 0                 ) :
      return                          [                                      ]
    ##########################################################################
    AT         = 1
    THUMBS     =                      [                                      ]
    PIC        = PictureItem          (                                      )
    ##########################################################################
    for PCID in ICONs                                                        :
      ########################################################################
      PIC      . UUID = PCID
      SUFFIX   = ""
      ########################################################################
      INFO     = PIC . GetInformation ( DB , PICTAB , PCID                   )
      if                              ( INFO not in [ False , None ]       ) :
        ######################################################################
        SUFFIX = INFO                 [ "Suffix"                             ]
      ########################################################################
      if                              ( len ( SUFFIX ) > 0                 ) :
        ######################################################################
        ORDER  = f"{AT}" . zfill      ( 4                                    )
        ######################################################################
        PID    = f"{PUID}-{ORDER}-{PCID}.{SUFFIX}"
        FNAM   = f"{path}/roles/{PID}"
        THUMBS . append               ( PID                                  )
        PIC    . Export               ( DB , DPOTAB , FNAM                   )
      ########################################################################
      AT       = AT + 1
    ##########################################################################
    return THUMBS
  ############################################################################
  def ExportAlbumActors             ( self , DB , uuid , path              ) :
    ##########################################################################
    RELTAB  = self . Tables         [ "Relation"                             ]
    ##########################################################################
    PEOW    = PeopleItem            (                                        )
    CROWDS  = PEOW . GetOwners      ( DB                                   , \
                                      RELTAB                               , \
                                      uuid                                 , \
                                      "Album"                              , \
                                      "Subordination"                        )
    ##########################################################################
    LISTS   =                       [                                        ]
    for PUID in CROWDS                                                       :
      ########################################################################
      NAMEs = self . GetAlbumNames  ( DB , PUID                              )
      THUMB = self . ExportActorThumbnails ( DB , PUID , path                )
      J     =                       { "Uuid"   : PUID                      , \
                                      "Names"  : NAMEs                     , \
                                      "Thumbs" : THUMB                       }
      LISTS . append                ( J                                      )
    ##########################################################################
    return LISTS
  ############################################################################
  def InvestigateFilms                ( self                               , \
                                        DB                                 , \
                                        uuid                               , \
                                        name                               , \
                                        path                               , \
                                        FILEs                              ) :
    ##########################################################################
    RELTAB           = self . Tables  [ "RelationVideos"                     ]
    VIDTAB           = self . Tables  [ "Videos"                             ]
    NAMTAB           = self . Tables  [ "NamesVideo"                         ]
    ##########################################################################
    FILMs            =                {                                      }
    CNT              = 1
    LOC              = self . getLocality (                                  )
    ##########################################################################
    for FILE in FILEs                                                        :
      ########################################################################
      FVM            = FilmItem       (                                      )
      VFILE          = f"{path}/videos/{FILE}"
      DETAILs        = FVM . Probe    ( VFILE                                )
      ########################################################################
      try                                                                    :
        ######################################################################
        FSECS        = float          ( DETAILs [ "format" ] [ "duration" ]  )
        SECONDS      = int            ( FSECS                                )
        HOURS        = int            ( SECONDS / 3600                       )
        REMAINS      = int            ( SECONDS - ( HOURS   * 3600 )         )
        MINUTES      = int            ( REMAINS / 60                         )
        SECONDS      = int            ( REMAINS - ( MINUTES *   60 )         )
        ######################################################################
        if                            ( SECONDS < 10                       ) :
          ####################################################################
          if                          ( ( HOURS > 0 ) or ( MINUTES > 0 )   ) :
            SS       = f"0{SECONDS}"
          else                                                               :
            SS       = f"{SECONDS}"
        ######################################################################
        else                                                                 :
          SS         = f"{SECONDS}"
        ######################################################################
        if                            ( MINUTES < 10                       ) :
          ####################################################################
          if                          ( HOURS > 0                          ) :
            SS       = f"0{MINUTES}:{SS}"
          else                                                               :
            SS       = f"{MINUTES}:{SS}"
          ####################################################################
        else                                                                 :
          SS         = f"{MINUTES}:{SS}"
        ######################################################################
        if                            ( HOURS > 0                          ) :
          SS         = f"{HOURS}:{SS}"
        ######################################################################
        DETAILs [ "Length" ] = SS
        ######################################################################
      except                                                                 :
        pass
      ########################################################################
      NN   = f"{name} #{CNT}"
      FVM  . Parse                    ( NN , DETAILs                         )
      GOT  = FVM . Locate             ( DB , VIDTAB                          )
      OKAY = False
      ########################################################################
      if                              ( not GOT                            ) :
        ######################################################################
        DB   . LockWrites             ( [ VIDTAB                           ] )
        OKAY = FVM . Assure           ( DB , VIDTAB                          )
        DB   . UnlockTables           (                                      )
        ######################################################################
      else                                                                   :
        ######################################################################
        OKAY = True
      ########################################################################
      if                              ( OKAY                               ) :
        ######################################################################
        if                            ( not GOT                            ) :
          ####################################################################
          DB   . LockWrites           ( [ NAMTAB                           ] )
          self . AssureUuidName       ( DB , NAMTAB , FVM . Uuid , NN        )
          DB   . UnlockTables         (                                      )
        ######################################################################
        REL = Relation                (                                      )
        REL . setT1                   ( "Album"                              )
        REL . setT2                   ( "Video"                              )
        REL . setRelation             ( "Subordination"                      )
        ######################################################################
        REL . set                     ( "first"  , uuid                      )
        REL . set                     ( "second" , FVM . Uuid                )
        ######################################################################
        DB  . LockWrites              ( [ RELTAB                           ] )
        REL . Join                    ( DB , RELTAB                          )
        DB  . UnlockTables            (                                      )
      ########################################################################
      FILMs [ FILE ] = FVM . Details
      ########################################################################
      CNT = CNT + 1
    ##########################################################################
    return FILMs
  ############################################################################
  def ExportAlbumHTML ( self , DB , uuid , path , JSON                     ) :
    ##########################################################################
    IDF     = ""
    AUID    = JSON    [ "Uuid"                                               ]
    ##########################################################################
    if                ( len ( JSON [ "Identifiers" ] ) > 0                 ) :
      ########################################################################
      IDF = "," . join ( JSON [ "Identifiers" ]                              )
    ##########################################################################
    TITLE   = ""
    if                ( len ( JSON [ "NAMEs" ] ) > 0                       ) :
      ########################################################################
      TITLE = JSON    [ "NAMEs" ] [ 0 ] [ "Name"                             ]
      ########################################################################
      if              ( len ( IDF ) > 0                                    ) :
        ######################################################################
        TITLE = f"[{IDF}] {TITLE}"
    ##########################################################################
    CONTENT = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" />
  <link rel="stylesheet" type="text/css" href="projects/album.css" />
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
  <script src="projects/album.js"></script>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
  <title>{TITLE}</title>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
</head>
<body><main class="container">
"""
    ##########################################################################
    ALLNAMES = ""
    NAMEX    =        [                                                      ]
    ##########################################################################
    for N in JSON     [ "NAMEs"                                            ] :
      ########################################################################
      K   = N         [ "Name"                                               ]
      if              ( len ( IDF ) > 0                                    ) :
        ######################################################################
        K = f"[{IDF}] {K}"
      ########################################################################
      NAMEX . append  ( f"<label>{K}</label>"                                )
    ##########################################################################
    ALLNAMES = "\n" . join ( NAMEX                                           )
    ##########################################################################
    CONTENT = f"""{CONTENT}
<div class="row">
  <div class="col-12">
    <div class="form-group AlbumTitle">
      {ALLNAMES}
    </div>
  </div>
</div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
  <div class="row">
"""
    ##########################################################################
    if                ( len ( JSON [ "Covers" ] ) > 0                      ) :
      ########################################################################
      CONTENT = f"""{CONTENT}
    <div class="col-12 col-sm-8 col-xl-8">
      <img src="images/Cover.jpg">
    </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
    <div class="col-12 col-sm-4 col-xl-4">
"""
    ##########################################################################
    if                ( len ( IDF ) > 0                                    ) :
      ########################################################################
      CONTENT = f"""{CONTENT}
      <div>
        <span>識別碼</span>
        <span> : </span>
        <span>{IDF}</span>
      </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
      <div>
        <span>影片長編號</span>
        <span> : </span>
        <span>{AUID}</span>
      </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
    </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
  </div>
"""
    ##########################################################################
    if                ( len ( JSON [ "Actors" ] ) > 0                      ) :
      ########################################################################
      CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
"""
      ########################################################################
      CONTENT = f"""{CONTENT}
  <div class="row">
"""
      ########################################################################
      for ACTOR in JSON [ "Actors" ]                                         :
        ######################################################################
        CONTENT = f"""{CONTENT}
    <div class="col-12 col-sm-6 col-xl-2">
"""
        ######################################################################
        if            ( len ( ACTOR [ "Thumbs" ] ) > 0                     ) :
          ####################################################################
          THUMB = ACTOR [ "Thumbs" ] [ 0                                     ]
          CONTENT = f"""{CONTENT}
      <img src="roles/{THUMB}">
"""
        ######################################################################
        for NAME in ACTOR [ "Names" ]                                        :
          ####################################################################
          N = NAME    [ "Name"                                               ]
          if          ( len ( N ) > 0                                      ) :
            ##################################################################
            CONTENT = f"""{CONTENT}
        <div>{N}</div>
"""
        ######################################################################
        CONTENT = f"""{CONTENT}
    </div>
"""
      ########################################################################
      CONTENT = f"""{CONTENT}
  </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
"""
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    VIDEOs    = JSON  [ "VIDEOs"                                             ]
    if                ( len ( VIDEOs ) > 0                                 ) :
      ########################################################################
      CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
  <div class="row">
"""
      ########################################################################
      for VIDEO in VIDEOs                                                    :
        ######################################################################
        FILM  = JSON  [ "FILMs" ] [ VIDEO                                    ]
        if            ( "Length" in FILM                                   ) :
          ####################################################################
          VLE = FILM  [ "Length"                                             ]
          CONTENT = f"""{CONTENT}
      <div class="col-12">
        <span><a href="videos/{VIDEO}">{VIDEO}</a></span>
        <span> : </span>
        <span>{VLE}</span>
      </div>
"""
      ########################################################################
      CONTENT = f"""{CONTENT}
  </div>
"""
    ##########################################################################
    GALLERIES = JSON  [ "Galleries" ] [ "Galleries"                          ]
    if                ( len ( GALLERIES ) > 0                              ) :
      ########################################################################
      for GALLERY in GALLERIES                                               :
        ######################################################################
        PICTURES = JSON [ "Galleries" ] [ GALLERY                            ]
        if            ( len ( PICTURES ) > 0                               ) :
          ####################################################################
          CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
  <div class="row">
    <div class="col-12">
      <div>
        <span>圖庫</span>
        <span> : </span>
        <span>{GALLERY}</span>
      </div>
"""
          ####################################################################
          AT     = 0
          ####################################################################
          ## 應該修改為抓取實際檔案
          ####################################################################
          for PIC in PICTURES                                                :
            ##################################################################
            AT   = AT + 1
            ZAT  = f"{AT}"
            ZAT  = ZAT . zfill ( 4                                           )
            ##################################################################
            CONTENT = f"""{CONTENT}
        <img src="images/{GALLERY}/{ZAT}-{PIC}.jpg">
"""
          ####################################################################
          CONTENT = f"""{CONTENT}
    </div>
  </div>
"""
    ##########################################################################
    CONTENT = f"""{CONTENT}
  <div class="row">&nbsp;</div>
"""
    ##########################################################################
    ##########################################################################
    CONTENT = f"""{CONTENT}
</main></body>
</html>
"""
    ##########################################################################
    HTML    = f"{path}/index.html"
    with open         ( HTML , 'w' , encoding = "utf-8" ) as f               :
      f     . write   ( CONTENT                                              )
    ##########################################################################
    return
  ############################################################################
  def UpdateAlbumInformation              ( self , DB , uuid , name , path ) :
    ##########################################################################
    FILEs   = self . ExportAlbumM3U       (                    path          )
    NAMEs   = self . GetAlbumNames        (        DB , uuid                 )
    ##########################################################################
    ALBUM   = AlbumItem                   (                                  )
    ALBUM   . Uuid     = uuid
    ALBUM   . Settings = self . Settings
    ALBUM   . Tables   = self . Tables
    IDs     = ALBUM . GetIdentifiers      ( DB                               )
    ##########################################################################
    self    . UpdateAlbumName             ( path , IDs  , NAMEs              )
    ##########################################################################
    COVERS  = self . ExportAlbumCovers    ( DB   , uuid , path               )
    CROWDS  = self . ExportAlbumActors    ( DB   , uuid , path               )
    JGALM   = self . ExportAlbumGalleries ( DB   , uuid , path               )
    FILMs   = self . InvestigateFilms     ( DB                             , \
                                            uuid                           , \
                                            name                           , \
                                            path                           , \
                                            FILEs                            )
    ##########################################################################
    CONF    = f"{path}/Album.json"
    JSON    =                             { "Uuid"        : uuid           , \
                                            "NAMEs"       : NAMEs          , \
                                            "VIDEOs"      : FILEs          , \
                                            "FILMs"       : FILMs          , \
                                            "Identifiers" : IDs            , \
                                            "Covers"      : COVERS         , \
                                            "Galleries"   : JGALM          , \
                                            "Actors"      : CROWDS           }
    ##########################################################################
    self . ExportAlbumHTML                ( DB , uuid , path , JSON          )
    SaveJson                              ( CONF , JSON                      )
    ##########################################################################
    return
  ############################################################################
  def GenerateVideoAlbum           ( self , uuid , name , path             ) :
    ##########################################################################
    CONFs = self . Settings        [ "Albums"                                ]
    DIR   = CONFs                  [ "Template"                              ]
    ##########################################################################
    ALBUM = AlbumItem              (                                         )
    ALBUM . Uuid     = uuid
    ALBUM . Settings = self . Settings
    ALBUM . Tables   = self . Tables
    ##########################################################################
    self  . BuildAlbum             ( DIR , path                              )
    ##########################################################################
    DB    = self . ConnectDB       ( UsePure = True                          )
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    self  . OnBusy  . emit         (                                         )
    ##########################################################################
    self  . UpdateAlbumInformation ( DB , uuid , name , path                 )
    ##########################################################################
    self  . GoRelax . emit         (                                         )
    DB    . Close                  (                                         )
    ##########################################################################
    self  . Notify                 ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def CreateAlbum               ( self , VIDEO , NAME                      ) :
    ##########################################################################
    MSG    = self . getMenuItem ( "CreateAlbum"                              )
    path   = QFileDialog . getExistingDirectory                            ( \
                                  self                                     , \
                                  MSG                                      , \
                                  ""                                       , \
                                  QFileDialog . ShowDirsOnly               | \
                                  QFileDialog . DontResolveSymlinks          )
    if                          ( not path                                 ) :
      return
    ##########################################################################
    PARAMs =                    ( VIDEO , NAME , path ,                      )
    self . Go                   ( self . GenerateVideoAlbum , PARAMs         )
    ##########################################################################
    return
  ############################################################################
  def UpdateVideoAlbum             ( self , uuid , name , path             ) :
    ##########################################################################
    CONFs = self . Settings        [ "Albums"                                ]
    DIR   = CONFs                  [ "Template"                              ]
    ##########################################################################
    ALBUM = AlbumItem              (                                         )
    ALBUM . Uuid     = uuid
    ALBUM . Settings = self . Settings
    ALBUM . Tables   = self . Tables
    ##########################################################################
    DB    = self . ConnectDB       ( UsePure = True                          )
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    self  . OnBusy  . emit         (                                         )
    ##########################################################################
    self  . UpdateAlbumInformation ( DB , uuid , name , path                 )
    ##########################################################################
    self  . GoRelax . emit         (                                         )
    DB    . Close                  (                                         )
    ##########################################################################
    self  . Notify                 ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def UpdateAlbum               ( self , VIDEO , NAME                      ) :
    ##########################################################################
    MSG    = self . getMenuItem ( "UpdateAlbum"                              )
    path   = QFileDialog . getExistingDirectory                            ( \
                                  self                                     , \
                                  MSG                                      , \
                                  ""                                       , \
                                  QFileDialog . ShowDirsOnly               | \
                                  QFileDialog . DontResolveSymlinks          )
    if                          ( not path                                 ) :
      return
    ##########################################################################
    PARAMs =                    ( VIDEO , NAME , path ,                      )
    self . Go                   ( self . UpdateVideoAlbum , PARAMs           )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "Albums" , "Names"                        )
    ##########################################################################
    return
  ############################################################################
  def FindProducts                    ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    FMT     = self . Translations     [ "UI::SearchKey"                      ]
    MSG     = FMT . format            ( name                                 )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    ##########################################################################
    ALMTAB  = self . Tables           [ "Albums"                             ]
    IDFTAB  = self . Tables           [ "Identifiers"                        ]
    RELTAB  = self . Tables           [ "Relation"                           ]
    LIKE    = f"{name}"
    UUIDs   =                         [                                      ]
    ##########################################################################
    if                                ( self . isOriginal      (         ) ) :
      ########################################################################
      PEQ   = f"""select `uuid` from {ALMTAB} where ( `used` > 0 )"""
      ########################################################################
    elif                              ( self . isSubordination (         ) ) :
      ########################################################################
      FIRST = self . Relation . get   ( "first"                              )
      T1    = self . Relation . get   ( "t1"                                 )
      T2    = self . Relation . get   ( "t2"                                 )
      REL   = self . Relation . get   ( "relation"                           )
      ########################################################################
      REQ   = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `t2` = {T2} )
                    and ( `relation` = {REL} )
                    and ( `first` = {FIRST} )"""
      PEQ   = f"""select `uuid` from {ALMTAB}
                  where ( `used` > 0 )
                  and ( `uuid` in ( {REQ} ) )"""
      ########################################################################
    elif                              ( self . isReverse       (         ) ) :
      ########################################################################
      SECID = self . Relation . get   ( "second"                             )
      T1    = self . Relation . get   ( "t1"                                 )
      T2    = self . Relation . get   ( "t2"                                 )
      REL   = self . Relation . get   ( "relation"                           )
      ########################################################################
      REQ   = f"""select `first` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `t2` = {T2} )
                    and ( `relation` = {REL} )
                    and ( `second` = {SECID} )"""
      PEQ   = f"""select `uuid` from {ALMTAB}
                  where ( `used` > 0 )
                  and ( `uuid` in ( {REQ} ) )"""
    ##########################################################################
    IDQ     = f"""select `uuid` from {IDFTAB}
                  where ( `type` = 76 )
                    and ( `name` like %s )
                    and ( `uuid` in ( {PEQ} ) )
                  group by `uuid`"""
    QQ      = f"""select `uuid` from {IDFTAB}
                  where ( `uuid` in ( {IDQ} ) )
                  order by `name` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
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
  def FindIdentifiers  ( self                                              ) :
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
    self . Go          ( self . FindProducts , ( T , )                       )
    ##########################################################################
    return
  ############################################################################
  def SearchIdentifier                 ( self                              ) :
    ##########################################################################
    L      = LineEdit                  ( None , self . PlanFunc              )
    L      . setMinimumWidth           ( 120                                 )
    L      . setMaximumWidth           ( 120                                 )
    p      = self      . GetPlan       (                                     )
    p      . statusBar . addPermanentWidget ( L                              )
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . FindIdentifiers              )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "SearchIdentifier"                  )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  def UpdateIdentifier                ( self , UUID , identifier           ) :
    ##########################################################################
    IDz     = identifier
    IDz     . strip                   (                                      )
    IDz     . lstrip                  (                                      )
    IDz     . rstrip                  (                                      )
    ##########################################################################
    if                                ( len ( IDz ) <= 0                   ) :
      self  . Notify                  ( 1                                    )
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self  . Notify                  ( 1                                    )
      return
    ##########################################################################
    MSG     = self . getMenuItem      ( "UpdateIdentifier"                   )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    ##########################################################################
    IDFTAB  = self . Tables           [ "Identifiers"                        ]
    IDF     = IdentifierItem          (                                      )
    IDF     . Uuid = UUID
    IDF     . Type = 76
    IDF     . Name = IDz
    ##########################################################################
    IDF     . Assure                  ( DB , IDFTAB                          )
    ##########################################################################
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def AssignIdentifier ( self                                              ) :
    ##########################################################################
    UUID = self . PickedUuid
    L    = self . SearchLine
    ##########################################################################
    if                 ( UUID == 0                                         ) :
      return
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
    self . Go          ( self . UpdateIdentifier , ( UUID , T , )            )
    ##########################################################################
    return
  ############################################################################
  def AssignAlbumIdentifier            ( self , uuid                       ) :
    ##########################################################################
    self   . PickedUuid = uuid
    L      = LineEdit                  ( None , self . PlanFunc              )
    L      . setMinimumWidth           ( 120                                 )
    L      . setMaximumWidth           ( 120                                 )
    p      = self      . GetPlan       (                                     )
    p      . statusBar . addPermanentWidget ( L                              )
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . AssignIdentifier             )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "AssignIdentifier"                  )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  def ObtainAlbumNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    IDFTAB   = self . Tables           [ "Identifiers"                       ]
    NAMTAB   = self . Tables           [ "Names"                             ]
    ##########################################################################
    NAMEs    =                         {                                     }
    if                                 ( len ( UUIDs ) <= 0                ) :
      return NAMEs
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME   = self . GetName          ( DB , NAMTAB , UUID                  )
      ########################################################################
      QQ     = f"""select `name` from {IDFTAB}
                 where ( `type` = 76 )
                 and ( `uuid` = {UUID} ) ;"""
      QQ     = " " . join              ( QQ . split ( )                      )
      DB     . Query                   ( QQ                                  )
      RR     = DB . FetchOne           (                                     )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )          :
        ######################################################################
        IDEF = RR                      [ 0                                   ]
        SS   = ""
        ######################################################################
        try                                                                  :
          SS = IDEF . decode           ( "utf-8"                             )
        except                                                               :
          pass
        ######################################################################
        if                             ( len ( SS ) > 0                    ) :
          NAME = f"{SS} {NAME}"
      ########################################################################
      NAMEs [ UUID ] = NAME
    ##########################################################################
    return NAMEs
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
    PHID     = 2800002000000000000
    ##########################################################################
    if                                   ( "Heading" in self . Tables      ) :
      ########################################################################
      PHID   = self . Tables             [ "Heading"                         ]
      PHID   = int                       ( PHID                              )
    ##########################################################################
    ALMTAB   = self . Tables             [ "Albums"                          ]
    NAMTAB   = self . Tables             [ "NamesEditing"                    ]
    RELTAB   = self . Tables             [ "RelationEditing"                 ]
    TABLES   =                           [ ALMTAB , NAMTAB                   ]
    ##########################################################################
    if                                   (  self . isGrouping ( )          ) :
      ########################################################################
      TABLES . append                    ( RELTAB                            )
      T1     = self . Relation . get     ( "t1"                              )
      T2     = self . Relation . get     ( "t2"                              )
      RR     = self . Relation . get     ( "relation"                        )
    ##########################################################################
    DB       . LockWrites                ( TABLES                            )
    ##########################################################################
    if                                   ( uuid <= 0                       ) :
      ########################################################################
      PI     = AlbumItem                 (                                   )
      PI     . Settings [ "Head"   ] = PHID
      PI     . Tables   [ "Albums" ] = ALMTAB
      ########################################################################
      uuid   = PI . NewAlbum             ( DB                                )
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
      REL    . setT2                     ( "Album"                           )
      REL    . Join                      ( DB , RELTAB                       )
      ########################################################################
    elif                                 ( self . isReverse       ( )      ) :
      ########################################################################
      PUID   = self . Relation . get     ( "second"                          )
      REL    . set                       ( "first"    , uuid                 )
      REL    . set                       ( "second"   , PUID                 )
      REL    . setT1                     ( "Album"                          )
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
  def UpdateItemName             ( self ,           item , uuid , name     ) :
    ##########################################################################
    self . UpdateItemNameByTable ( "NamesEditing" , item , uuid , name       )
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
    REL    . setT1               ( "Album"                                   )
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
  def UpdateLocalityUsage                     ( self                       ) :
    return self . subgroupUpdateLocalityUsage (                              )
  ############################################################################
  def ReloadLocality                     ( self , DB                       ) :
    return self . subgroupReloadLocality (        DB                         )
  ############################################################################
  def UpdateAlbumUsage           ( self , uuid , usage                     ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( self . NotOkay ( DB )                   ) :
      return
    ##########################################################################
    ALMTAB = self . Tables       [ "Albums"                                  ]
    ##########################################################################
    DB     . LockWrites          ( [ ALMTAB                                ] )
    ##########################################################################
    QQ     = f"""update {ALMTAB}
                 set `used` = {usage}
                 where ( `uuid` = {uuid} ) ; """
    DB     . Query               ( " " . join ( QQ . split (             ) ) )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    DB     . Close               (                                           )
    ##########################################################################
    self   . AlbumOPTs           [ uuid ] [ "Used" ] = usage
    self   . GenerateItemToolTip ( uuid                                      )
    ##########################################################################
    return
  ############################################################################
  def OptimizeAlbumOrder                ( self                             ) :
    ##########################################################################
    TKEY = "Relation"
    MKEY = "OrganizePositions"
    ##########################################################################
    self . DoRepositionMembershipOrders ( TKEY , MKEY , self . ProgressMin   )
    ##########################################################################
    MSG  = self . getMenuItem           ( "OptimizeAlbumCompleted"           )
    self . emitLog . emit               ( MSG                                )
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
    self . ShowWebPages . emit ( text , 76 , xsid , Related , icon           )
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
  def OpenAlbumIdentifier          ( self                                  ) :
    ##########################################################################
    atItem = self . currentItem    (                                         )
    ##########################################################################
    if                             ( atItem == None                        ) :
      return
    ##########################################################################
    uuid   = atItem . data         ( Qt . UserRole                           )
    uuid   = int                   ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return
    ##########################################################################
    self   . AssignAlbumIdentifier ( uuid                                    )
    ##########################################################################
    return
  ############################################################################
  def OpenAlbumSources             ( self , website , item                 ) :
    ##########################################################################
    uuid = item . data             ( Qt . UserRole                           )
    uuid = int                     ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return
    ##########################################################################
    text = item . text             (                                         )
    icon = item . icon             (                                         )
    xsid = str                     ( uuid                                    )
    ##########################################################################
    self . ShowAlbumSources . emit ( website , text , xsid , icon            )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGallery                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return False
    ##########################################################################
    text = item . text                (                                      )
    icon = item . icon                (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , self . GType , xsid , icon    )
    ##########################################################################
    return True
  ############################################################################
  def OpenItemIcons                 ( self , item                          ) :
    ##########################################################################
    uuid = item . data              ( Qt . UserRole                          )
    uuid = int                      ( uuid                                   )
    ##########################################################################
    if                              ( uuid <= 0                            ) :
      return False
    ##########################################################################
    text = item . text              (                                        )
    icon = item . icon              (                                        )
    xsid = str                      ( uuid                                   )
    ##########################################################################
    relz = "Using"
    ##########################################################################
    self . ShowPersonalIcons . emit ( text                                 , \
                                      self . GType                         , \
                                      relz                                 , \
                                      xsid                                 , \
                                      icon                                   )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentGallery          ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( atItem == None                         ) :
      return False
    ##########################################################################
    return self . OpenItemGallery ( atItem                                   )
  ############################################################################
  def OpenItemGalleries               ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return False
    ##########################################################################
    text = item . text                (                                      )
    icon = item . icon                (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . GalleryGroup . emit        ( text , self . GType , xsid           )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentGalleries          ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    ##########################################################################
    if                              ( atItem == None                       ) :
      return False
    ##########################################################################
    return self . OpenItemGalleries ( atItem                                 )
  ############################################################################
  def OpenCurrentCrowds           ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( atItem == None                         ) :
      return False
    ##########################################################################
    return self . OpenOwnedCrowds ( atItem                                   )
  ############################################################################
  def OpenOwnedCrowds              ( self , item                           ) :
    ##########################################################################
    uuid = item . data             ( Qt . UserRole                           )
    uuid = int                     ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return False
    ##########################################################################
    text = item . text             (                                         )
    xsid = str                     ( uuid                                    )
    ##########################################################################
    self . OwnedPeopleGroup . emit ( text , self . GType , xsid              )
    ##########################################################################
    return
  ############################################################################
  def OpenEpisodesSubgroup         ( self                                  ) :
    ##########################################################################
    atItem = self . currentItem    (                                         )
    ##########################################################################
    if                             ( atItem == None                        ) :
      return False
    ##########################################################################
    return self . OpenSubgroupItem ( atItem                                  )
  ############################################################################
  def OpenSubgroupItem                  ( self , item                      ) :
    ##########################################################################
    uuid = item . data                  ( Qt . UserRole                      )
    uuid = int                          ( uuid                               )
    ##########################################################################
    if                                  ( uuid <= 0                        ) :
      return False
    ##########################################################################
    text = item . text                  (                                    )
    xsid = str                          ( uuid                               )
    ##########################################################################
    self . OwnedEpisodesSubgroup . emit ( text , self . GType , xsid         )
    ##########################################################################
    return
  ############################################################################
  def OpenFragmentItem               ( self , item                         ) :
    ##########################################################################
    uuid = item . data               ( Qt . UserRole                         )
    uuid = int                       ( uuid                                  )
    ##########################################################################
    if                               ( uuid <= 0                           ) :
      return False
    ##########################################################################
    text = item . text               (                                       )
    icon = item . icon               (                                       )
    xsid = str                       ( uuid                                  )
    relz = "Subordination"
    ##########################################################################
    self . emitFragmentEditor . emit ( text                                , \
                                       xsid                                , \
                                       self . GType                        , \
                                       xsid                                , \
                                       relz                                , \
                                       icon                                  )
    ##########################################################################
    return True
  ############################################################################
  def OpenVFragments               ( self                                  ) :
    ##########################################################################
    atItem = self . currentItem    (                                         )
    ##########################################################################
    if                             ( atItem == None                        ) :
      return False
    ##########################################################################
    return self . OpenFragmentItem ( atItem                                  )
  ############################################################################
  ############################################################################
  def OpenDateEventsItem              ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    text = item . text                (                                      )
    icon = item . icon                (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowAlbumDateEvents . emit ( text , xsid , icon                   )
    ##########################################################################
    return
  ############################################################################
  def OpenAlbumDateEvents       ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenDateEventsItem ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Albums" , "NamesEditing"     )
    ##########################################################################
    return
  ############################################################################
  def ConnectDirectoryToAlbumUuid  ( self , uuid                           ) :
    ##########################################################################
    self . emitConnectAlbum . emit ( str  ( uuid )                           )
    ##########################################################################
    return
  ############################################################################
  def ConnectDirectoryToAlbum            ( self                            ) :
    ##########################################################################
    atItem = self   . currentItem        (                                   )
    ##########################################################################
    if                                   ( self . NotOkay ( atItem )       ) :
      return
    ##########################################################################
    uuid   = atItem . data               ( Qt . UserRole                     )
    uuid   = int                         ( uuid                              )
    ##########################################################################
    if                                   ( uuid <= 0                       ) :
      return
    ##########################################################################
    self   . ConnectDirectoryToAlbumUuid ( uuid                              )
    ##########################################################################
    return
  ############################################################################
  def CopyGroupUuidToClipboard     ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping      (        ) ) :
      return
    ##########################################################################
    if                             (     self . isSubordination (        ) ) :
      ########################################################################
      uuid = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                           (     self . isReverse       (        ) ) :
      ########################################################################
      uuid = self . Relation . get ( "second"                                )
    ##########################################################################
    qApp . clipboard ( ) . setText ( f"{uuid}"                               )
    ##########################################################################
    return
  ############################################################################
  def CopyAlbumUuidToClipboard     ( self , uuid                           ) :
    ##########################################################################
    qApp . clipboard ( ) . setText ( f"{uuid}"                               )
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
  def FunctionsMenu              ( self , mm , uuid , item                 ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Functions"                               )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isGrouping (                   ) ) :
      ########################################################################
      msg = self . getMenuItem   ( "CopyGroupUuidToClipboard"                )
      mm  . addActionFromMenu    ( LOM , 34621301 , msg                      )
      mm  . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      mm  . addActionFromMenu    ( LOM , 34621302 , msg                      )
      ########################################################################
      msg = self . getMenuItem   ( "GroupsToCLI"                             )
      mm  . addActionFromMenu    ( LOM , 34621303 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "DoReposition"                            )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   34621304                                , \
                                   msg                                     , \
                                   True                                    , \
                                   self . DoReposition                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "Watermarking"                            )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   34621305                                , \
                                   msg                                     , \
                                   True                                    , \
                                   self . Watermarking                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ShowIdentifier"                          )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   34621101                                , \
                                   MSG                                     , \
                                   True                                    , \
                                   self . ShowIdentifier                     )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "Search"                                  )
    mm    . addActionFromMenu    ( LOM , 34621391 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "SearchIdentifier"                        )
    mm    . addActionFromMenu    ( LOM , 34621392 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "WebPages"                                )
    mm    . addActionFromMenu    ( LOM , 34621321 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "IdentWebPage"                            )
    ICO   = QIcon                ( ":/images/webfind.png"                    )
    mm    . addActionFromMenuWithIcon ( LOM , 34621322 , ICO , MSG           )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "OptimizeAlbumOrder"                      )
    mm    . addActionFromMenu    ( LOM , 8836001 , MSG                       )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 34621101                    ) :
      ########################################################################
      if                               ( self . ShowIdentifier             ) :
        self . ShowIdentifier = False
      else                                                                   :
        self . ShowIdentifier = True
      ########################################################################
      self   . clear                   (                                     )
      self   . startup                 (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621301                    ) :
      ########################################################################
      self . CopyGroupUuidToClipboard  (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621302                    ) :
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
    if                                 ( at == 34621303                    ) :
      ########################################################################
      self . EmitRelateParameters      (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621304                    ) :
      ########################################################################
      self . DoReposition = not self . DoReposition
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621305                    ) :
      ########################################################################
      self . Watermarking = not self . Watermarking
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621321                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Subordination"                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621322                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Equivalent"                        )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621391                    ) :
      ########################################################################
      self . Search                    (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621392                    ) :
      ########################################################################
      self . SearchIdentifier          (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 8836001                     ) :
      ########################################################################
      self . Go                        ( self . OptimizeAlbumOrder           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                      ( self , mm , uuid , item            ) :
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return mm
    ##########################################################################
    TRX   = self . Translations
    NAME  = item . text               (                                      )
    MSG   = self . getMenuItem        ( "Belongs"                            )
    LOM   = mm   . addMenu            ( MSG                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "CopyAlbumUuidToClipboard"           )
    mm    . addActionFromMenu         ( LOM , 34611101 ,        MSG          )
    ##########################################################################
    mm    . addSeparatorFromMenu      ( LOM                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "CreateAlbum"                        )
    mm    . addActionFromMenu         ( LOM , 34635101 ,        MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "UpdateAlbum"                        )
    mm    . addActionFromMenu         ( LOM , 34635102 ,        MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "ConnectAlbum"                       )
    ICON  = QIcon                     ( ":/images/sqltable.png"              )
    mm    . addActionFromMenuWithIcon ( LOM , 34635103 , ICON , MSG          )
    ##########################################################################
    mm    . addSeparatorFromMenu      ( LOM                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "AssignIdentifier"                   )
    ICON  = QIcon                     ( ":/images/jointag.png"               )
    mm    . addActionFromMenuWithIcon ( LOM , 34635201 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "Vendors"                            )
    mm    . addActionFromMenu         ( LOM , 34635202 ,        MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "Crowds"                             )
    ICON  = QIcon                     ( ":/images/peoplegroups.png"          )
    mm    . addActionFromMenuWithIcon ( LOM , 34635203 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "PossibleCrowds"                     )
    mm    . addActionFromMenu         ( LOM , 34635204 ,        MSG          )
    ##########################################################################
    mm    . addSeparatorFromMenu      ( LOM                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "IconGroups"                         )
    mm    . addActionFromMenu         ( LOM , 34231201 ,        MSG          )
    ##########################################################################
    MSG   = TRX                       [ "UI::PersonalGallery"                ]
    ICON  = QIcon                     ( ":/images/pictures.png"              )
    mm    . addActionFromMenuWithIcon ( LOM , 34231202 , ICON , MSG          )
    ##########################################################################
    MSG   = TRX                       [ "UI::Galleries"                      ]
    ICON  = QIcon                     ( ":/images/galleries.png"             )
    mm    . addActionFromMenuWithIcon ( LOM , 34231203 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "VideoFragments"                     )
    ICON  = QIcon                     ( ":/images/vfragments.png"            )
    mm    . addActionFromMenuWithIcon ( LOM , 34231204 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "AlbumSubgroups"                     )
    ICON  = QIcon                     ( ":/images/modifyproject.png"         )
    mm    . addActionFromMenuWithIcon ( LOM , 34231205 , ICON , MSG          )
    ##########################################################################
    mm    . addSeparatorFromMenu      ( LOM                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "DateEvents"                         )
    ICO   = QIcon                     ( ":/images/calendars.png"             )
    mm    . addActionFromMenuWithIcon ( LOM , 34231501 , ICO , MSG           )
    ##########################################################################
    MSG   = self . getMenuItem        ( "LogHistory"                         )
    ICO   = QIcon                     ( ":/images/documents.png"             )
    mm    . addActionFromMenuWithIcon ( LOM , 34231401 , ICO , MSG           )
    ##########################################################################
    mm    . addSeparatorFromMenu      ( LOM                                  )
    ##########################################################################
    MSG   = self . getMenuItem        ( "WebPages"                           )
    mm    . addActionFromMenu         ( LOM , 34631321 ,        MSG          )
    ##########################################################################
    MSG   = self . getMenuItem        ( "IdentWebPage"                       )
    ICO   = QIcon                     ( ":/images/webfind.png"               )
    mm    . addActionFromMenuWithIcon ( LOM , 34631322 , ICO , MSG           )
    ##########################################################################
    MSG   = self . getMenuItem        ( "OpenIdentWebPage"                   )
    ICO   = QIcon                     ( ":/images/bookmarks.png"             )
    mm    . addActionFromMenuWithIcon ( LOM , 34631323 , ICO , MSG           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , uuid , item               ) :
    ##########################################################################
    if                             ( at == 34611101                        ) :
      ########################################################################
      self . CopyAlbumUuidToClipboard ( uuid                                 )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635101                        ) :
      ########################################################################
      self . CreateAlbum           ( uuid , item . text ( )                  )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635102                        ) :
      ########################################################################
      self . UpdateAlbum           ( uuid , item . text ( )                  )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635103                        ) :
      ########################################################################
      self . ConnectDirectoryToAlbumUuid ( uuid                              )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635201                        ) :
      ########################################################################
      self . AssignAlbumIdentifier ( uuid                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635202                        ) :
      ########################################################################
      text = item . text           (                                         )
      icon = item . icon           (                                         )
      xsid = str                   ( uuid                                    )
      ########################################################################
      self . OwnedOrganizationGroup . emit                                 ( \
                                     text                                  , \
                                     76                                    , \
                                     xsid                                  , \
                                     "Subordination"                       , \
                                     icon                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635203                        ) :
      ########################################################################
      self . OpenOwnedCrowds       ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635204                        ) :
      ########################################################################
      text = item . text           (                                         )
      xsid = str                   ( uuid                                    )
      rele = "Candidate"
      ########################################################################
      self . OwnedPeopleGroupRelate . emit ( text , 76 , xsid , rele         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231201                        ) :
      ########################################################################
      text = item . text           (                                         )
      icon = item . icon           (                                         )
      xsid = str                   ( uuid                                    )
      relz = "Using"
      ########################################################################
      self . ShowPersonalIcons . emit ( text , 76 , relz , xsid , icon       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231202                        ) :
      ########################################################################
      self . OpenItemGallery       ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231203                        ) :
      ########################################################################
      self . OpenItemGalleries     ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231204                        ) :
      ########################################################################
      self . OpenFragmentItem      ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231205                        ) :
      ########################################################################
      self . OpenSubgroupItem      ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34631321                        ) :
      ########################################################################
      self . OpenWebPageBelongings ( uuid , item , "Subordination"           )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34631322                        ) :
      ########################################################################
      self . OpenWebPageBelongings ( uuid , item , "Equivalent"              )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34631323                        ) :
      ########################################################################
      self . OpenIdentWebPageURLs  (        item , "Equivalent"              )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231401                        ) :
      ########################################################################
      self . OpenLogHistoryItem    ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34231501                        ) :
      ########################################################################
      self . OpenDateEventsItem    ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def VideosMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX   = self . Translations
    TRM   = TRX                [ "VideoAlbumsView" ] [ "ContainsVideos"      ]
    NAME  = item . text        (                                             )
    MSG   = self . getMenuItem ( "VideoGroups"                               )
    LOM   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    KEYs  = TRM . keys         (                                             )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      KXD = int                ( K                                           )
      MSG = TRM                [ K                                           ]
      mm  . addActionFromMenu  ( LOM , int ( 34670000 + KXD ) , MSG          )
    ##########################################################################
    return mm
  ############################################################################
  def RunVideosMenu                    ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at <  34670001                    ) :
      return False
    ##########################################################################
    if                                 ( at >= 34680000                    ) :
      return False
    ##########################################################################
    KXD    = int                       ( at -  34670000                      )
    text   = item . text               (                                     )
    icon   = item . icon               (                                     )
    xsid   = str                       ( uuid                                )
    REL    = Relation                  (                                     )
    relate = REL . GetRelationName     ( KXD                                 )
    ##########################################################################
    self   . emitOpenVideoGroup . emit ( text , 76 , xsid , relate , icon    )
    ##########################################################################
    return   True
  ############################################################################
  def AlbumSourcesMenu        ( self , mm , item                           ) :
    ##########################################################################
    if                        ( self . NotOkay ( item                    ) ) :
      return mm
    ##########################################################################
    uuid = item  . data       ( Qt . UserRole                                )
    uuid = int                ( uuid                                         )
    ##########################################################################
    if                        ( uuid not in self . AlbumOPTs               ) :
      return mm
    ##########################################################################
    MSG  = self . getMenuItem ( "AlbumSources"                               )
    COL  = mm   . addMenu     ( MSG                                          )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchAllSources"                           )
    mm   . addActionFromMenu  ( COL , 29436050 , MSG                         )
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
    MSG  = self . getMenuItem ( "SearchJavBus"                               )
    mm   . addActionFromMenu  ( COL , 29436055 , MSG                         )
    ##########################################################################
    MSG  = self . getMenuItem ( "SearchJavFree"                              )
    mm   . addActionFromMenu  ( COL , 29436056 , MSG                         )
    ##########################################################################
    return mm
  ############################################################################
  def RunAlbumSourcesMenu       ( self , at , item                         ) :
    ##########################################################################
    if                          ( 29436050 == at                           ) :
      ########################################################################
      LISTs  =                  [ "ADE"                                    , \
                                  "IAFD"                                   , \
                                  "Private"                                , \
                                  "BANG"                                   , \
                                  "JavBus"                                 , \
                                  "JavFree"                                  ]
      for N in LISTs                                                         :
        self . OpenAlbumSources ( N         , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436051 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "ADE"     , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436052 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "IAFD"    , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436053 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "Private" , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436054 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "BANG"    , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436055 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "JavBus"  , item                           )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 29436056 == at                           ) :
      ########################################################################
      self   . OpenAlbumSources ( "JavFree" , item                           )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def WebSearchMenu            ( self , mm , item                          ) :
    ##########################################################################
    if                         ( self . NotOkay ( item                   ) ) :
      return mm
    ##########################################################################
    uuid = item  . data        ( Qt . UserRole                               )
    uuid = int                 ( uuid                                        )
    ##########################################################################
    if                         ( uuid not in self . AlbumOPTs              ) :
      return mm
    ##########################################################################
    MSG  = self  . getMenuItem ( "WebSearchAlbum"                            )
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
    if                           ( uuid not in self . AlbumOPTs            ) :
      return
    ##########################################################################
    VAKEY = "VideoAlbumsView"
    MSG   = self  . getMenuItem  ( "AlbumUsage"                              )
    COL   = mm    . addMenu      ( MSG                                       )
    USAGE = self  . Translations [ VAKEY ] [ "Usage"                         ]
    KEYs  = USAGE . keys         (                                           )
    USED  = self  . AlbumOPTs    [ uuid  ] [ "Used"                          ]
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
    if                           ( uuid not in self . AlbumOPTs            ) :
      return
    ##########################################################################
    VID   = int                  ( at - 29431000                             )
    VSD   = f"{VID}"
    VAKEY = "VideoAlbumsView"
    USAGE = self  . Translations [ VAKEY ] [ "Usage"                         ]
    ##########################################################################
    if                           ( VSD not in USAGE                        ) :
      return False
    ##########################################################################
    VP    =                      ( uuid , VID ,                              )
    self  . Go                   ( self . UpdateAlbumUsage , VP              )
    ##########################################################################
    return True
  ############################################################################
  def DisplayMenu                ( self , mm                               ) :
    ##########################################################################
    MSG   = self  . getMenuItem  ( "DisplayUsage"                            )
    COL   = mm    . addMenu      ( MSG                                       )
    VAKEY = "VideoAlbumsView"
    USAGE = self  . Translations [ VAKEY ] [ "Usage"                         ]
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
    VAKEY  = "VideoAlbumsView"
    USAGE  = self  . Translations [ VAKEY ] [ "Usage"                        ]
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
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self . Notify                  ( 0                                       )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( self . isSearching ( )                ) :
      ########################################################################
      msg  = self . getMenuItem    ( "NotSearch"                             )
      mm   . addAction             ( 7401 , msg                              )
    ##########################################################################
    self   . StopIconMenu          ( mm                                      )
    self   . AmountIndexMenu       ( mm , True                               )
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    if                             ( uuid > 0                              ) :
      self . AppendRenameAction    ( mm , 1102                               )
      self . AssureEditNamesAction ( mm , 1601 , atItem                      )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . FunctionsMenu         ( mm , uuid , atItem                      )
    ##########################################################################
    if                             ( atItem not in self . EmptySet         ) :
      ########################################################################
      self . GroupsMenu            ( mm , uuid , atItem                      )
      self . VideosMenu            ( mm , uuid , atItem                      )
      mm   . addSeparator          (                                         )
      self . AlbumSourcesMenu      ( mm ,        atItem                      )
      self . WebSearchMenu         ( mm ,        atItem                      )
    ##########################################################################
    mm     . addSeparator          (                                         )
    self   . UsageMenu             ( mm ,        atItem                      )
    self   . DisplayMenu           ( mm                                      )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . ScrollBarMenu         ( mm                                      )
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
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking     ( mm , aa                                 )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu  ( at , uuid , atItem                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunVideosMenu  ( at , uuid , atItem                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunAlbumSourcesMenu ( at , atItem                        )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunWebSearchMenu ( at , atItem                           )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunUsageMenu   ( at , atItem                             )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunDisplayMenu ( at                                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu ( at , uuid , atItem                    )
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
    OKAY   = self . HandleLocalityMenu ( at                                  )
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
    OKAY    = self . RunStopIconMenu   ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      ########################################################################
      self . RenameVideo           (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor ( at , 1601 , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                              ( at == 7401                           ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

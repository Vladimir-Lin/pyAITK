# -*- coding: utf-8 -*-
##############################################################################
## GalleriesView
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
from   AITK    . Documents  . Variables     import Variables as VariableItem
from   AITK    . Pictures   . Gallery       import Gallery   as GalleryItem
from   AITK    . Pictures   . Picture6      import Picture   as PictureItem
##############################################################################
from   AITK    . UUIDs      . UuidListings6 import appendUuid
from   AITK    . UUIDs      . UuidListings6 import appendUuids
from   AITK    . UUIDs      . UuidListings6 import assignUuids
from   AITK    . UUIDs      . UuidListings6 import getUuids
##############################################################################
class GalleriesView            ( IconDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  ShowPeopleGroup     = Signal ( str , int  , str                            )
  OwnedPeopleGroup    = Signal ( str , int  , str                            )
  OwnedVideoAlbums    = Signal ( str , int  , str ,       QIcon              )
  ShowPersonalGallery = Signal ( str , int  , str       , QIcon              )
  ShowPersonalIcons   = Signal ( str , int  , str , str , QIcon              )
  ShowFoundPictures   = Signal ( str , list ,             QIcon              )
  ViewFullGallery     = Signal ( str , int  , str , int , QIcon              )
  ShowWebPages        = Signal ( str , int  , str , str , QIcon              )
  OpenVariantTables   = Signal ( str , str  , int , str , dict               )
  emitOpenSmartNote   = Signal ( str                                         )
  OpenLogHistory      = Signal ( str , str  , str , str , str                )
  emitLog             = Signal ( str                                         )
  emitStartDetecting  = Signal (                                             )
  emitStopDetecting   = Signal (                                             )
  emitSelectFound     = Signal ( list , list                                 )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . ClassTag           = "GalleriesView"
    self . FetchTableKey      = self . ClassTag
    ##########################################################################
    self . Total              =  0
    self . StartId            =  0
    self . Amount             = 60
    self . GType              = 64
    self . SortOrder          = "asc"
    self . SortByName         = False
    self . ExtraINFOs         = True
    self . RefreshOpts        = True
    self . Watermarking       = True
    self . UsedOptions        = [ 1 , 2 , 3 , 4 , 5 , 6 , 7                  ]
    self . GalleryOPTs        = {                                            }
    ##########################################################################
    self . KeepDetecting      = False
    self . DetectingTotal     = 0
    self . DetectingCount     = 0
    self . DetectingWT        = None
    self . DetectingSB        = None
    self . DetectingBT        = None
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
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( "Gallery"                               )
    self . Relation . setT2        ( "Gallery"                               )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . emitStartDetecting . connect ( self . DoStartDetectingBT          )
    self . emitStopDetecting  . connect ( self . DoStopDetectingBT           )
    self . emitSelectFound    . connect ( self . ToggleSelectFound           )
    ##########################################################################
    self . setFunction             ( self . HavingMenu , True                )
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
    self . PrepareFetchTableKey     (                                        )
    self . AppendToolNamingAction   (                                        )
    ##########################################################################
    self . AppendSideActionWithIcon ( "PersonalGallery"                    , \
                                      ":/images/pictures.png"              , \
                                      self . OpenCurrentGallery              )
    self . AppendSideActionWithIcon ( "ViewFullPictures"                   , \
                                      ":/images/searchimages.png"          , \
                                      self . ViewCurrentGallery              )
    self . AppendSideActionWithIcon ( "BelongsCrowd"                       , \
                                      ":/images/peoplegroups.png"          , \
                                      self . OpenCurrentCrowds               )
    self . AppendSideActionWithIcon ( "BelongsAlbums"                      , \
                                      ":/images/videos.png"                , \
                                      self . OpenCurrentAlbums               )
    self . AppendSideActionWithIcon ( "PossibleContains"                   , \
                                      ":/images/possible-contains.png"     , \
                                      self . RunPossibleGroupInGalleries     )
    self . AppendSideActionWithIcon ( "DetectFaces"                        , \
                                      ":/images/detect-faces.png"          , \
                                      self . RunDetectFacesInGalleries       )
    ##########################################################################
    return
  ############################################################################
  def TellStory               ( self , Enabled                             ) :
    ##########################################################################
    GG   = self . Grouping
    TT   = self . windowTitle (                                              )
    MM   = self . getMenuItem ( "GalleriesViewParameter"                     )
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
    self . LinkAction ( "Insert"     , self . InsertItem        , Enabled    )
    self . LinkAction ( "Delete"     , self . DeleteItems       , Enabled    )
    self . LinkAction ( "Cut"        , self . DeleteItems       , Enabled    )
    self . LinkAction ( "Copy"       , self . DoCopyItemText    , Enabled    )
    self . LinkAction ( "Rename"     , self . RenameItem        , Enabled    )
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
    if                       ( self . AnythingRunning (                  ) ) :
      return False
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
    self . clear             (                                               )
    self . UuidItemMaps  =   {                                               }
    self . UuidItemNames =   {                                               }
    self . GalleryOPTs   =   {                                               }
    self . UUIDs         =   [                                               ]
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
    return self . defaultGetUuidIcon ( DB , RELTAB , "Gallery" , UUID        )
  ############################################################################
  def FetchBaseINFO                  ( self , DB , UUID , PUID             ) :
    ##########################################################################
    ICZ    = self . FetchEntityImage (        DB , PUID                      )
    ##########################################################################
    if                               ( ICZ in self . EmptySet              ) :
      return
    ##########################################################################
    if                               ( UUID in self . GalleryOPTs          ) :
      ########################################################################
      self . GalleryOPTs [ UUID ] [ "Image" ] = ICZ
      self . GalleryOPTs [ UUID ] [ "PUID"  ] = PUID
      ########################################################################
    else                                                                     :
      ########################################################################
      self . GalleryOPTs [ UUID ] =  { "Image" : ICZ                       , \
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
    if                                ( UUID not in self . GalleryOPTs     ) :
      return
    ##########################################################################
    GOPTs     = self . GalleryOPTs    [ UUID                                 ]
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
    PICs      = -1
    ALMs      = -1
    DINFO     = False
    ##########################################################################
    if                                ( "Used"     in GOPTs                ) :
      ########################################################################
      USED    = GOPTs                 [ "Used"                               ]
      ########################################################################
      if                              ( USED in [ 2 , 3 , 4 , 5 , 6 , 7 ]  ) :
        DINFO = True
    ##########################################################################
    if                                ( "Pictures" in GOPTs                ) :
      ########################################################################
      PICs    = GOPTs                 [ "Pictures"                           ]
      ########################################################################
      if                              ( PICs > 0                           ) :
        DINFO = True
    ##########################################################################
    if                                ( "Albums"   in GOPTs                ) :
      ########################################################################
      ALMs    = GOPTs                 [ "Albums"                             ]
      ########################################################################
      if                              ( ALMs > 0                           ) :
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
      if                              ( ALMs > 0                           ) :
        ######################################################################
        WIMG  = QImage                ( ":/images/videos.png"                )
        WIMG  = WIMG . scaled         ( TIW , TIH                            )
        ######################################################################
        PTS   = QPoint                ( ISIZE . width  ( ) - TIW , 0         )
        p     . drawImage             ( PTS , WIMG                           )
      ########################################################################
      if                              ( PICs > 0                           ) :
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
        p     . drawText              ( RTS , f"{PICs}"                      )
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
  def doubleClicked        ( self , item                                   ) :
    ##########################################################################
    self . OpenItemGallery (        item                                     )
    ##########################################################################
    return True
  ############################################################################
  def FetchRegularDepotCount        ( self , DB                            ) :
    ##########################################################################
    GALTAB = self . Tables          [ "Galleries"                            ]
    UOPTS  = " , " . join           ( str(x) for x in self . UsedOptions     )
    QQ     = f"""select count(*) from {GALTAB}
                 where ( `used` in ( {UOPTS} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def FetchGroupMembersCount ( self , DB                                   ) :
    ##########################################################################
    GALTAB = self . Tables   [ "Galleries"                                   ]
    RELTAB = self . Tables   [ "Relation"                                    ]
    UOPTS  = " , " . join    ( str(x) for x in self . UsedOptions            )
    RQ     = self . Relation . GetSecondUuidsSqlSyntax ( RELTAB              )
    ##########################################################################
    QQ     = f"""select count(*) from {GALTAB}
                 where ( `used` in ( {UOPTS} ) )
                   and ( `uuid` in ( {RQ} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def FetchGroupOwnersCount ( self , DB                                    ) :
    ##########################################################################
    GALTAB = self . Tables  [ "Galleries"                                    ]
    RELTAB = self . Tables  [ "Relation"                                     ]
    UOPTS  = " , " . join   ( str(x) for x in self . UsedOptions             )
    RQ     = self . Relation . GetFirstUuidsSqlSyntax ( RELTAB               )
    ##########################################################################
    QQ     = f"""select count(*) from {GALTAB}
                 where ( `used` in ( {UOPTS} ) )
                   and ( `uuid` in ( {RQ} ) ) ;"""
    ##########################################################################
    return self . DbCountDepotTotal ( DB , QQ                                )
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    GALTAB = self . Tables [ "Galleries"                                     ]
    UOPTS  = " , " . join  ( str(x) for x in self . UsedOptions              )
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"""select `uuid` from {GALTAB}
                 where ( `used` in ( {UOPTS} ) )
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def ObtainSubgroupUuids           ( self , DB                            ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ASC    =                        ( ORDER . lower in [ "asc"             ] )
    LMTS   = f"limit {SID} , {AMOUNT}"
    GALTAB = self . Tables          [ "Galleries"                            ]
    RELTAB = self . Tables          [ "Relation"                             ]
    NAMTAB = self . Tables          [ "Names"                                ]
    UOPTS  = " , " . join           ( str(x) for x in self . UsedOptions     )
    ##########################################################################
    if                              ( self . isSubordination (           ) ) :
      ########################################################################
      RQ   = self . Relation . GetSecondUuidsSqlSyntax ( RELTAB              )
      EQ   = f"""select `uuid` from {GALTAB}
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
      EQ   = f"""select `uuid` from {GALTAB}
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
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . GalleryOPTs =                  {                                  }
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
    if                                ( UUID not in self . GalleryOPTs     ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem       ( "GalleryToolTip"                     )
    USAGE  = self . Translations      [ self . ClassTag ] [ "Usage"          ]
    STATEs = self . Translations      [ self . ClassTag ] [ "States"         ]
    ##########################################################################
    USD    = self . GalleryOPTs       [ UUID ] [ "Used"                      ]
    SSS    = self . GalleryOPTs       [ UUID ] [ "States"                    ]
    PICs   = self . GalleryOPTs       [ UUID ] [ "Pictures"                  ]
    SGPs   = self . GalleryOPTs       [ UUID ] [ "Subgroups"                 ]
    PEOs   = self . GalleryOPTs       [ UUID ] [ "People"                    ]
    VIDs   = self . GalleryOPTs       [ UUID ] [ "Albums"                    ]
    ##########################################################################
    UMSG   = ""
    ##########################################################################
    if                                ( f"{USD}" in USAGE                  ) :
      ########################################################################
      UMSG = USAGE                    [ f"{USD}"                             ]
    ##########################################################################
    text   = FMT . format             ( UUID                               , \
                                        PICs                               , \
                                        SGPs                               , \
                                        PEOs                               , \
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
    GALTAB       = self . Tables       [ "Galleries"                         ]
    PICTAB       = self . Tables       [ "RelationPictures"                  ]
    RELTAB       = self . Tables       [ "Relation"                          ]
    SGPTAB       = self . Tables       [ "Relation"                          ]
    PEOTAB       = self . Tables       [ "Relation"                          ]
    ## PEOTAB       = self . Tables       [ "RelationPeople"                    ]
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
                                         "States"    : 0                   , \
                                         "Pictures"  : 0                   , \
                                         "Subgroups" : 0                   , \
                                         "People"    : 0                   , \
                                         "Albums"    : 0                     }
      ########################################################################
      if                               ( U in self . GalleryOPTs           ) :
        ######################################################################
        GOPTs    = self . GalleryOPTs  [ U                                   ]
        ######################################################################
        if                             ( "Image" in GOPTs                  ) :
          ####################################################################
          GJSON [ "Image" ] = GOPTs    [ "Image"                             ]
      ########################################################################
      self       . GalleryOPTs [ U ] = GJSON
      ########################################################################
      QQ         = f"""select `used` , `states` from {GALTAB}
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
          self   . GalleryOPTs [ U ] [ "Used"   ] = USD
          self   . GalleryOPTs [ U ] [ "States" ] = SSS
      ########################################################################
      REL        . set                 ( "first" , U                         )
      REL        . setT1               ( "Gallery"                           )
      REL        . setT2               ( "Picture"                           )
      REL        . setRelation         ( "Subordination"                     )
      PICs       = REL . CountSecond   ( DB , PICTAB                         )
      ########################################################################
      self       . GalleryOPTs [ U ] [ "Pictures" ] = PICs
      ########################################################################
      REL        . set                 ( "second" , U                        )
      REL        . setT2               ( "Gallery"                           )
      ########################################################################
      REL        . setT1               ( "Subgroup"                          )
      SGPs       = REL . CountFirst    ( DB , SGPTAB                         )
      ########################################################################
      self       . GalleryOPTs [ U ] [ "Subgroups" ] = SGPs
      ########################################################################
      REL        . setT1               ( "People"                            )
      PEOs       = REL . CountFirst    ( DB , PEOTAB                         )
      ########################################################################
      self       . GalleryOPTs [ U ] [ "People" ] = PEOs
      ########################################################################
      REL        . setT1               ( "Album"                             )
      VIDs       = REL . CountFirst    ( DB , ALMTAB                         )
      ########################################################################
      self       . GalleryOPTs [ U ] [ "Albums" ] = VIDs
      ########################################################################
      self       . GenerateItemToolTip ( U                                   )
    ##########################################################################
    DB           . Close               (                                     )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "gallery/uuids"
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
    FMTs    =              [ "people/uuids"                                , \
                             "gallery/uuids"                               , \
                             "picture/uuids"                                 ]
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
    if                                   ( mtype in [ "people/uuids" ]     ) :
      ########################################################################
      if                                 ( atItem in self . EmptySet       ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus    ( "JoinPeople"   , title , CNT      )
    ##########################################################################
    elif                                 ( mtype in [ "picture/uuids" ]    ) :
      ########################################################################
      if                                 ( atItem in self . EmptySet       ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus    ( "JoinPictures" , title , CNT      )
    ##########################################################################
    elif                                 ( mtype in [ "gallery/uuids" ]    ) :
      ########################################################################
      ## if                                 ( atItem in self . EmptySet       ) :
      ##   ######################################################################
      ##   print ( "GalleriesView empty drop" )
      ##   ######################################################################
      ## else                                                                   :
      ##   ######################################################################
      ##   uxid = atItem . data             ( Qt . UserRole                     )
      ##   print ( f"GalleriesView {uxid}" )
      ########################################################################
      if                                 ( self == sourceWidget            ) :
        self . ShowMenuItemCountStatus   ( "MoveGalleries" ,         CNT     )
      else                                                                   :
        self . ShowMenuItemTitleStatus   ( "JoinGalleries" , title , CNT     )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def acceptGalleriesDrop    ( self                                        ) :
    return self . isGrouping (                                               )
  ############################################################################
  def dropPeople                        ( self , source , pos , JSON       ) :
    FUNC = self . PeopleAppending
    return self . defaultDropInFunction ( self , source , pos , JSON , FUNC  )
  ############################################################################
  def dropPictures                      ( self , source , pos , JSON       ) :
    FUNC = self . PicturesAppending
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def dropGalleries                 ( self , source , pos , JSON           ) :
    ##########################################################################
    MF   = self . GalleriesMoving
    AF   = self . GalleriesAppending
    ##########################################################################
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationPeople" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationPeople" , LAST , UUIDs   )
  ############################################################################
  def GalleriesMoving  ( self , atUuid , NAME , JSON                       ) :
    ##########################################################################
    TK   = "Relation"
    ## TK   = "RelationPeople"
    MK   = "OrganizePositions"
    ##########################################################################
    self . MajorMoving (        atUuid ,        JSON , TK , MK               )
    ##########################################################################
    return
  ############################################################################
  def GalleriesAppending  ( self , atUuid , NAME , JSON                    ) :
    ##########################################################################
    TK   = "RelationPeople"
    MK   = "OrganizePositions"
    ##########################################################################
    self . MajorAppending (        atUuid ,        JSON , TK , MK            )
    ##########################################################################
    return
  ############################################################################
  def PeopleAppending                    ( self , atUuid , NAME , JSON     ) :
    ##########################################################################
    T2      = "Gallery"
    TABLE   = "RelationPeople"
    RELATED = "Subordination"
    ##########################################################################
    OK      = self . AppendingIntoPeople ( atUuid                          , \
                                           NAME                            , \
                                           JSON                            , \
                                           TABLE                           , \
                                           T2                              , \
                                           RELATED                           )
    if                                   ( not OK                          ) :
      return
    ##########################################################################
    self    . loading                    (                                   )
    ##########################################################################
    return
  ############################################################################
  def PicturesAppending            ( self , atUuid , NAME , JSON           ) :
    ##########################################################################
    T1  = "Gallery"
    TAB = "RelationPictures"
    ##########################################################################
    OK  = self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1  )
    if                             ( not OK                                ) :
      return
    ##########################################################################
    self   . loading               (                                         )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                           ( self , UUIDs                 ) :
    ##########################################################################
    if                                      ( len ( UUIDs ) <= 0           ) :
      return
    ##########################################################################
    if                                      ( not self . isGrouping ( )    ) :
      return
    ##########################################################################
    TITLE  = "RemoveGalleryItems"
    RELTAB = self . Tables                  [ "Relation"                     ]
    RV     = self . isReverse               (                                )
    SQLs   = self . GenerateGroupRemoveSQLs ( UUIDs                        , \
                                              self . Relation              , \
                                              RELTAB                       , \
                                              RV                             )
    self   . QuickExecuteSQLs               ( TITLE , 100 , RELTAB , SQLs    )
    self   . Notify                         ( 5                              )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemName             ( self           , item , uuid , name     ) :
    ##########################################################################
    self . UpdateItemNameByTable ( "NamesEditing" , item , uuid , name       )
    ##########################################################################
    return
  ############################################################################
  def AppendGalleryItem      ( self , DB                                   ) :
    ##########################################################################
    GALTAB = self . Tables   [ "Galleries"                                   ]
    uuid   = DB   . LastUuid ( GALTAB , "uuid" , 2800001000000000000         )
    DB     . AppendUuid      ( GALTAB ,  uuid                                )
    ##########################################################################
    return uuid
  ############################################################################
  def AppendItemName                   ( self , item , name                ) :
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    GALTAB  = self . Tables            [ "Galleries"                         ]
    NAMTAB  = self . Tables            [ "Names"                             ]
    RELTAB  = self . Tables            [ "Relation"                          ]
    TABLES  =                          [ GALTAB , NAMTAB , RELTAB            ]
    ##########################################################################
    FRID    = self . Relation . get    ( "first"                             )
    SEID    = self . Relation . get    ( "second"                            )
    T1      = self . Relation . get    ( "t1"                                )
    T2      = self . Relation . get    ( "t2"                                )
    RR      = self . Relation . get    ( "relation"                          )
    ##########################################################################
    DB      . LockWrites               ( TABLES                              )
    ##########################################################################
    uuid    = self . AppendGalleryItem ( DB                                  )
    self    . AssureUuidNameByLocality ( DB                                , \
                                         NAMTAB                            , \
                                         uuid                              , \
                                         name                              , \
                                         self . getLocality ( )              )
    ##########################################################################
    if                                 ( self . isGrouping ( )             ) :
      ########################################################################
      REL   = Relation                 (                                     )
      REL   . set                      ( "t1"       , T1                     )
      REL   . set                      ( "t2"       , T2                     )
      REL   . set                      ( "relation" , RR                     )
      ########################################################################
      if                               ( self . isSubordination ( )        ) :
        ######################################################################
        REL . set                      ( "first"    , FRID                   )
        REL . set                      ( "second"   , uuid                   )
        REL . Join                     ( DB , RELTAB                         )
        ######################################################################
      elif                             ( self . isReverse       ( )        ) :
        ######################################################################
        REL . set                      ( "first"    , uuid                   )
        REL . set                      ( "second"   , SEID                   )
        REL . Join                     ( DB , RELTAB                         )
    ##########################################################################
    DB      . UnlockTables             (                                     )
    DB      . Close                    (                                     )
    ##########################################################################
    self    . PrepareItemContent       ( item , uuid , name                  )
    self    . assignToolTip            ( item , str ( uuid )                 )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems (                                              )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage                     ( self                       ) :
    return self . subgroupUpdateLocalityUsage (                              )
  ############################################################################
  def ReloadLocality                     ( self , DB                       ) :
    return self . subgroupReloadLocality (        DB                         )
  ############################################################################
  def ForceStopDetectingBT ( self                                          ) :
    ##########################################################################
    self . KeepDetecting = False
    ##########################################################################
    return
  ############################################################################
  def DoStartDetectingBT   ( self                                          ) :
    ##########################################################################
    TOTAL = int            ( self . DetectingTotal - self . DetectingCount   )
    ##########################################################################
    if                     ( TOTAL < 10                                    ) :
      return
    ##########################################################################
    WPLAN = self . GetPlan (                                                 )
    ##########################################################################
    if                     ( WPLAN in [ False , None ]                     ) :
      return
    ##########################################################################
    if                     ( self . DetectingWT not in self . EmptySet     ) :
      return
    ##########################################################################
    if                     ( self . DetectingSB not in self . EmptySet     ) :
      return
    ##########################################################################
    self  . DetectingWT = QTimer             ( self                          )
    self  . DetectingWT . timeout . connect  ( self . DoRefreshDetectingBT   )
    self  . DetectingWT . setInterval        ( 250                           )
    ##########################################################################
    self  . DetectingSB = QProgressBar       (                               )
    ##########################################################################
    self  . DetectingSB . setFormat          ( "%v / %m"                     )
    self  . DetectingSB . setMinimumWidth    ( 320                           )
    self  . DetectingSB . setMaximumWidth    ( 320                           )
    ##########################################################################
    self  . DetectingBT = QToolButton        (                               )
    self  . DetectingBT . setAutoRaise       ( True                          )
    self  . DetectingBT . setText            ( "Stop"                        )
    self  . DetectingBT . setToolButtonStyle ( Qt . ToolButtonIconOnly       )
    PIX   = QPixmap                          ( ":/images/stoprecord.png"     )
    ICON  = QIcon                            ( PIX                           )
    self  . DetectingBT . setIcon            ( ICON                          )
    self  . DetectingBT . clicked . connect  ( self . ForceStopDetectingBT   )
    ##########################################################################
    WPLAN . statusBar . addPermanentWidget   ( self . DetectingBT            )
    WPLAN . statusBar . addPermanentWidget   ( self . DetectingSB            )
    ##########################################################################
    self  . DetectingSB . setRange           ( 0 , self . DetectingTotal     )
    self  . DetectingSB . setValue           (     self . DetectingCount     )
    self  . DetectingWT . start              (                               )
    ##########################################################################
    return
  ############################################################################
  def DoStopDetectingBT ( self                                             ) :
    ##########################################################################
    if                  ( self . DetectingWT not in self . EmptySet        ) :
      ########################################################################
      self . DetectingWT . stop        (                                     )
      self . DetectingWT . deleteLater (                                     )
    ##########################################################################
    if                  ( self . DetectingSB not in self . EmptySet        ) :
      ########################################################################
      self . DetectingSB . deleteLater (                                     )
    ##########################################################################
    if                  ( self . DetectingBT not in self . EmptySet        ) :
      ########################################################################
      self . DetectingBT . deleteLater (                                     )
    ##########################################################################
    self   . KeepDetecting  = False
    self   . DetectingTotal = 0
    self   . DetectingCount = 0
    self   . DetectingWT    = None
    self   . DetectingSB    = None
    self   . DetectingBT    = None
    ##########################################################################
    return
  ############################################################################
  def DoRefreshDetectingBT        ( self                                   ) :
    ##########################################################################
    if                            ( self . DetectingSB in self . EmptySet  ) :
      return
    ##########################################################################
    self . DetectingSB . setRange ( 0 , self . DetectingTotal                )
    self . DetectingSB . setValue (     self . DetectingCount                )
    ##########################################################################
    return
  ############################################################################
  def DetectFacesFromPicture           ( self , DB , PCID                  ) :
    ##########################################################################
    RECG   = self . GetRecognizer      (                                     )
    ##########################################################################
    if                                 ( RECG in self . EmptySet           ) :
      return
    ##########################################################################
    PICTAB = self . Tables             [ "Information"                       ]
    DOPTAB = self . Tables             [ "Depot"                             ]
    VARTAB = self . Tables             [ "DescribeVariables"                 ]
    ##########################################################################
    PIC    = PictureItem               (                                     )
    PV     = VariableItem              (                                     )
    ##########################################################################
    PV     . Type = 9
    PV     . Name = "Description"
    PV     . Uuid  = PCID
    ##########################################################################
    RECJ   = PV  . GetValue            ( DB , VARTAB                         )
    ##########################################################################
    if                                 ( RECJ not in self . EmptySet       ) :
      ########################################################################
      if                               ( len ( RECJ ) > 0                  ) :
        ######################################################################
        try                                                                  :
          ####################################################################
          BODY = RECJ . decode         ( "utf-8"                             )
          ####################################################################
          if                           ( len ( BODY ) > 0                  ) :
            ##################################################################
            JJ = json . loads          ( BODY                                )
            OK = RECG . hasFaces       ( JJ                                  )
            ##################################################################
            if                         ( OK                                ) :
              return True
          ####################################################################
        except                                                               :
          pass
    ##########################################################################
    INFO   = PIC . GetInformation      ( DB , PICTAB , PCID                  )
    ##########################################################################
    if                                 ( INFO in self . EmptySet           ) :
      return False
    ##########################################################################
    QQ     = f"select `file` from {DOPTAB} where ( `uuid` = {PCID} ) ;"
    OKAY   = PIC . FromDB              ( DB , QQ                             )
    ##########################################################################
    if                                 ( not OKAY                          ) :
      return False
    ##########################################################################
    OPTs   =                           {                                     }
    ##########################################################################
    J      = RECG . DoBasicDescription ( PIC , INFO , OPTs                   )
    OK     = RECG . hasFaces           ( J                                   )
    ##########################################################################
    PV     . Value = json . dumps      ( J                                   )
    PV     . AssureValue               ( DB , VARTAB                         )
    ##########################################################################
    return OK
  ############################################################################
  def DetectFacesFromPictures              ( self , DB , PCIDs             ) :
    ##########################################################################
    FCIDs  =                               [                                 ]
    self   . DetectingTotal = len          ( PCIDs                           )
    self   . DetectingCount = 0
    ##########################################################################
    self   . emitStartDetecting . emit     (                                 )
    ##########################################################################
    for PCID in PCIDs                                                        :
      ########################################################################
      if                                   ( not self . KeepDetecting      ) :
        continue
      ########################################################################
      if                                   ( not self . StayAlive          ) :
        continue
      ########################################################################
      OKAY = self . DetectFacesFromPicture ( DB , PCID                       )
      ########################################################################
      if                                   ( OKAY                          ) :
        ######################################################################
        FCIDs . append                     ( PCID                            )
        ######################################################################
        MSG   = f"{PCID}"
        self  . emitLog . emit             ( MSG                             )
      ########################################################################
      self . DetectingCount = int          ( self . DetectingCount + 1       )
    ##########################################################################
    self   . emitStopDetecting . emit      (                                 )
    ##########################################################################
    return FCIDs
  ############################################################################
  def GetPicturesFromGalleries       ( self , DB , GUIDs                   ) :
    ##########################################################################
    RELTAB      = self . Tables      [ "Relation"                            ]
    GALT        = GalleryItem        (                                       )
    PCIDs       =                    [                                       ]
    ##########################################################################
    for GUID in GUIDs                                                        :
      ########################################################################
      if                             ( not self . KeepDetecting            ) :
        continue
      ########################################################################
      if                             ( not self . StayAlive                ) :
        continue
      ########################################################################
      UUIDs     = GALT . GetPictures ( DB , RELTAB , GUID , self . GType , 1 )
      ########################################################################
      for PCID in UUIDs                                                      :
        ######################################################################
        if                           ( PCID not in PCIDs                   ) :
          PCIDs . append             ( PCID                                  )
    ##########################################################################
    return PCIDs
  ############################################################################
  def DoDetectFacesInGalleries                ( self                       ) :
    ##########################################################################
    RECG    = self . GetRecognizer            (                              )
    ##########################################################################
    if                                        ( RECG in self . EmptySet    ) :
      return
    ##########################################################################
    UUIDs   = self . getSelectedUuids         (                              )
    ##########################################################################
    if                                        ( len ( UUIDs ) <= 0         ) :
      return
    ##########################################################################
    DB      = self . ConnectDB                (                              )
    ##########################################################################
    if                                        ( self . NotOkay ( DB )      ) :
      ########################################################################
      self  . Notify                          ( 1                            )
      ########################################################################
      return
    ##########################################################################
    self    . KeepDetecting = True
    ##########################################################################
    self    . PushRunnings                    (                              )
    self    . Notify                          ( 3                            )
    ##########################################################################
    msg     = self . getMenuItem              ( "StartDetectFaces"           )
    self    . ShowStatus                      ( msg                          )
    self    . OnBusy  . emit                  (                              )
    ##########################################################################
    PCIDs   = self . GetPicturesFromGalleries ( DB , UUIDs                   )
    FCIDs   =                                 [                              ]
    ##########################################################################
    if                                        ( len ( PCIDs ) > 0          ) :
      ########################################################################
      FCIDs = self . DetectFacesFromPictures  ( DB , PCIDs                   )
    ##########################################################################
    self    . GoRelax . emit                  (                              )
    self    . ShowStatus                      ( ""                           )
    DB      . Close                           (                              )
    self    . Notify                          ( 5                            )
    self    . PopRunnings                     (                              )
    ##########################################################################
    self    . KeepDetecting = False
    ##########################################################################
    if                                        ( len ( FCIDs ) > 0          ) :
      ########################################################################
      TITLE = self . windowTitle              (                              )
      ICON  = self . windowIcon               (                              )
      MSG   = self . getMenuItem              ( "FacesInGalleries"           )
      MSG   = MSG  . replace                  ( "$(TITLE)" , TITLE           )
      self  . ShowFoundPictures . emit        ( MSG , FCIDs , ICON           )
    ##########################################################################
    return
  ############################################################################
  def RunDetectFacesInGalleries   ( self                                   ) :
    ##########################################################################
    if ( self . DetectingSB not in self . EmptySet                         ) :
      ########################################################################
      self . ForceStopDetectingBT (                                          )
      ########################################################################
      return
    ##########################################################################
    self . Go                     ( self . DoDetectFacesInGalleries          )
    ##########################################################################
    return
  ############################################################################
  def DoPossibleGroupInGalleries       ( self                              ) :
    ##########################################################################
    UUIDs  = self . getSelectedUuids   (                                     )
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return
    ##########################################################################
    DB     = self . ConnectDB          (                                     )
    ##########################################################################
    if                                 ( self . NotOkay ( DB )             ) :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    self   . PushRunnings              (                                     )
    self   . Notify                    ( 3                                   )
    ##########################################################################
    msg    = self . getMenuItem        ( "StartPossibleContains"             )
    self   . ShowStatus                ( msg                                 )
    self   . OnBusy  . emit            (                                     )
    ##########################################################################
    RELTAB = self . Tables             [ "Relation"                          ]
    GALT   = GalleryItem               (                                     )
    FUIDs  = GALT . LookingForContains ( DB                                , \
                                         RELTAB                            , \
                                         UUIDs                             , \
                                         self . GType                      , \
                                         1                                   )
    ##########################################################################
    self   . GoRelax . emit            (                                     )
    self   . ShowStatus                ( ""                                  )
    DB     . Close                     (                                     )
    self   . Notify                    ( 5                                   )
    self   . PopRunnings               (                                     )
    ##########################################################################
    self   . emitSelectFound . emit    ( UUIDs , FUIDs                       )
    ##########################################################################
    return
  ############################################################################
  def RunPossibleGroupInGalleries ( self                                   ) :
    ##########################################################################
    self . Go                     ( self . DoPossibleGroupInGalleries        )
    ##########################################################################
    return
  ############################################################################
  def ExportUUIDs              ( self                                      ) :
    ##########################################################################
    if                         ( not self . isSubordination ( )            ) :
      return
    ##########################################################################
    DB      = self . ConnectDB (                                             )
    if                         ( DB == None                                ) :
      return False
    ##########################################################################
    RELTAB  = self . Tables    [ "Relation"                                  ]
    ##########################################################################
    UUIDs   = self . Relation . Subordination ( DB , RELTAB                  )
    ##########################################################################
    DB      . UnlockTables     (                                             )
    DB      . Close            (                                             )
    ##########################################################################
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    UXIDs   =                  [                                             ]
    for UUID in UUIDs                                                        :
      UXIDs . append           ( f"{UUID}"                                   )
    ##########################################################################
    self . emitOpenSmartNote . emit ( "\n" . join ( UXIDs )                  )
    ##########################################################################
    return
  ############################################################################
  def UpdateGalleryUsage             ( self , uuid , usage                 ) :
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
    GALTAB = self . Tables           [ "Galleries"                           ]
    ##########################################################################
    DB     . LockWrites              ( [ GALTAB                            ] )
    ##########################################################################
    QQ     = f"""update {GALTAB}
                 set `used` = {usage}
                 where ( `uuid` in ( {UUIDw} ) ) ; """
    DB     . Query                   ( " " . join ( QQ . split (         ) ) )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    DB     . Close                   (                                       )
    ##########################################################################
    for u in UUIDs                                                           :
      ########################################################################
      self . GalleryOPTs             [ u ] [ "Used" ] = usage
      self . GenerateItemToolTip     ( u                                     )
    ##########################################################################
    return
  ############################################################################
  def OptimizeGalleryOrder              ( self                             ) :
    ##########################################################################
    TKEY = "RelationPeople"
    MKEY = "OrganizePositions"
    ##########################################################################
    self . DoRepositionMembershipOrders ( TKEY , MKEY , self . ProgressMin   )
    ##########################################################################
    MSG  = self . getMenuItem           ( "OptimizeGalleryCompleted"         )
    self . emitLog . emit               ( MSG                                )
    self . Notify                       ( 5                                  )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageListings      ( self , item , Related                     ) :
    ##########################################################################
    text = item . text         (                                             )
    uuid = item . data         ( Qt . UserRole                               )
    uuid = int                 ( uuid                                        )
    icon = item . icon         (                                             )
    xsid = str                 ( uuid                                        )
    ##########################################################################
    self . ShowWebPages . emit ( text , 64 , xsid , Related , icon           )
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
  def ViewItemGallery             ( self , item                            ) :
    ##########################################################################
    uuid = item . data            ( Qt . UserRole                            )
    uuid = int                    ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return False
    ##########################################################################
    text = item . text            (                                          )
    icon = item . icon            (                                          )
    xsid = str                    ( uuid                                     )
    ##########################################################################
    self . ViewFullGallery . emit ( text , self . GType , xsid , 1 , icon    )
    ##########################################################################
    return True
  ############################################################################
  def ViewCurrentGallery          ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( atItem == None                         ) :
      return False
    ##########################################################################
    return self . ViewItemGallery ( atItem                                   )
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
  def OpenCurrentAlbums           ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( atItem == None                         ) :
      return False
    ##########################################################################
    return self . OpenOwnedAlbums ( atItem                                   )
  ############################################################################
  def OpenOwnedAlbums              ( self , item                           ) :
    ##########################################################################
    uuid = item . data             ( Qt . UserRole                           )
    uuid = int                     ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return False
    ##########################################################################
    text = item . text             (                                         )
    icon = item . icon             (                                         )
    xsid = str                     ( uuid                                    )
    ##########################################################################
    self . OwnedVideoAlbums . emit ( text , self . GType , xsid , icon       )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Gallery" , "NamesEditing"    )
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
  def BlocMenu                   ( self , mm , item , uuid                 ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Bloc"                                    )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      mm  . addActionFromMenu    ( LOM , 1301 , msg                          )
      ########################################################################
      msg = self . getMenuItem   ( "GroupsToCLI"                             )
      mm  . addActionFromMenu    ( LOM , 1302 , msg                          )
    ##########################################################################
    msg   = self . getMenuItem   ( "DoReposition"                            )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   1303                                    , \
                                   msg                                     , \
                                   True                                    , \
                                   self . DoReposition                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "Watermarking"                            )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   1304                                    , \
                                   msg                                     , \
                                   True                                    , \
                                   self . Watermarking                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "ReportTables"                            )
    mm    . addActionFromMenu    ( LOM , 1305 , msg                          )
    ##########################################################################
    msg   = self . getMenuItem   ( "SortByName"                              )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   1306                                    , \
                                   msg                                     , \
                                   True                                    , \
                                   self . SortByName                         )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "DetectFaces"                             )
    ICON  = QIcon                ( ":/images/detect-faces.png"               )
    mm    . addActionFromMenuWithIcon ( LOM , 8821001 , ICON , MSG           )
    ##########################################################################
    MSG   = self . getMenuItem   ( "PossibleContains"                        )
    ICON  = QIcon                ( ":/images/possible-contains.png"          )
    mm    . addActionFromMenuWithIcon ( LOM , 8821002 , ICON , MSG           )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ExportUUIDs"                             )
    mm    . addActionFromMenu    ( LOM , 8831001 , MSG                       )
    ##########################################################################
    if                           ( uuid > 0                                ) :
      ########################################################################
      MSG = self . getMenuItem   ( "CopyGalleryUuid"                         )
      mm  . addActionFromMenu    ( LOM , 8831101 , MSG                       )
      ########################################################################
      MSG = self . getMenuItem   ( "CopyGalleryName"                         )
      mm  . addActionFromMenu    ( LOM , 8831102 , MSG                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "AppendUuidsToLister"                     )
    mm    . addActionFromMenu    ( LOM , 8831103 , MSG                       )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "OptimizeGalleryOrder"                    )
    mm    . addActionFromMenu    ( LOM , 8836001 , MSG                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "OptimizeGalleryOrder"                    )
    mm    . addActionFromMenu    ( LOM , 8836001 , MSG                       )
    ##########################################################################
    return mm
  ############################################################################
  def RunBlocMenu ( self , at , item , uuid                                ) :
    ##########################################################################
    if                                 ( at == 1301                        ) :
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
    if                                 ( at == 1302                        ) :
      ########################################################################
      self . EmitRelateParameters      (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1303                        ) :
      ########################################################################
      self . DoReposition = not self . DoReposition
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1304                        ) :
      ########################################################################
      self . Watermarking = not self . Watermarking
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1305                        ) :
      ########################################################################
      self . emitLog . emit            ( json . dumps ( self . Tables      ) )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 1306                                             ) :
      ########################################################################
      if          ( self . SortByName                                      ) :
        self . SortByName = False
      else                                                                   :
        self . SortByName = True
      ########################################################################
      self   . restart             (                                         )
      ########################################################################
      return True
    ##########################################################################
    if            ( 8821001 == at                                          ) :
      ########################################################################
      self . RunDetectFacesInGalleries (                                     )
      ########################################################################
      return True
    ##########################################################################
    if            ( 8821002 == at                                          ) :
      ########################################################################
      self . RunPossibleGroupInGalleries (                                   )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 8831001                                          ) :
      ########################################################################
      self . Go   ( self . ExportUUIDs                                       )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 8831101                                          ) :
      ########################################################################
      qApp . clipboard ( ) . setText ( f"{uuid}"                             )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 8831102                                          ) :
      ########################################################################
      qApp . clipboard ( ) . setText ( item . text ( )                       )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 8831103                                          ) :
      ########################################################################
      UUIDs = self . getSelectedUuids (                                      )
      if                              ( len ( UUIDs ) > 0                  ) :
        appendUuids                   (       UUIDs                          )
      ########################################################################
      return True
    ##########################################################################
    if            ( at == 8836001                                          ) :
      ########################################################################
      self . Go   ( self . OptimizeGalleryOrder                              )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PropertiesMenu             ( self , mm , item                        ) :
    ##########################################################################
    if                           ( item in self . EmptySet                 ) :
      ########################################################################
      return mm
    ##########################################################################
    MSG   = self . getMenuItem   ( "Properties"                              )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "BelongsCrowd"                            )
    ICON  = QIcon                ( ":/images/peoplegroups.png"               )
    mm    . addActionFromMenuWithIcon ( COL , 62231231 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem   ( "BelongsAlbums"                           )
    ICON  = QIcon                ( ":/images/videos.png"                     )
    mm    . addActionFromMenuWithIcon ( COL , 62231232 , ICON , MSG          )
    ##########################################################################
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "WebPages"                                )
    mm    . addActionFromMenu    ( COL , 62231321 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "IdentWebPage"                            )
    mm    . addActionFromMenu    ( COL , 62231322 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "Icons"                                   )
    mm    . addActionFromMenu    ( COL , 62231331 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "GalleryDescription"                      )
    mm    . addActionFromMenu    ( COL , 62231341 , MSG                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunPropertiesMenu            ( self , at , item                      ) :
    ##########################################################################
    if                             ( at == 62231231                        ) :
      ########################################################################
      self . OpenOwnedCrowds       ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 62231232                        ) :
      ########################################################################
      self . OpenOwnedAlbums       ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 62231321                        ) :
      ########################################################################
      self . OpenWebPageListings   ( item , "Subordination"                  )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 62231322                        ) :
      ########################################################################
      self . OpenWebPageListings   ( item , "Equivalent"                     )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 62231331                        ) :
      ########################################################################
      self . OpenItemIcons         ( item                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 62231341                        ) :
      ########################################################################
      name = item . text           (                                         )
      uuid = item . data           ( Qt . UserRole                           )
      uuid = int                   ( uuid                                    )
      LOC  = self . getLocality    (                                         )
      nx   = ""
      ########################################################################
      if                           ( "Notes" in self . Tables              ) :
        nx = self . Tables         [ "Notes"                                 ]
      ########################################################################
      self . OpenLogHistory . emit ( name                                    ,
                                     str ( uuid )                            ,
                                     "Description"                           ,
                                     nx                                      ,
                                     str ( LOC  )                            )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def UsageMenu                  ( self , mm , item                        ) :
    ##########################################################################
    if                           ( self . NotOkay ( item                 ) ) :
      return
    ##########################################################################
    uuid  = item  . data         ( Qt . UserRole                             )
    uuid  = int                  ( uuid                                      )
    ##########################################################################
    if                           ( uuid not in self . GalleryOPTs          ) :
      return
    ##########################################################################
    MSG   = self  . getMenuItem  ( "GalleryUsage"                            )
    COL   = mm    . addMenu      ( MSG                                       )
    USAGE = self  . Translations [ self . ClassTag ] [ "Usage"               ]
    KEYs  = USAGE . keys         (                                           )
    USED  = self  . GalleryOPTs  [ uuid ] [ "Used"                           ]
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
    if                           ( uuid not in self . GalleryOPTs          ) :
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
    self  . Go                   ( self . UpdateGalleryUsage , VP            )
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
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared (         ) ) :
      return False
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
    if                                 ( self . isSearching (            ) ) :
      ########################################################################
      msg  = self . getMenuItem        ( "NotSearch"                         )
      mm   . addAction                 ( 7401 , msg                          )
    ##########################################################################
    self   . StopIconMenu              ( mm                                  )
    self   . AmountIndexMenu           ( mm , True                           )
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1101                           )
    ##########################################################################
    if                                 ( uuid > 0                          ) :
      ########################################################################
      mm   . addSeparator              (                                     )
      ########################################################################
      self . AppendRenameAction        ( mm , 1102                           )
      self . AssureEditNamesAction     ( mm , 1601 , atItem                  )
      ########################################################################
      mm   . addSeparator              (                                     )
      ########################################################################
      msg  = self . getMenuItem        ( "PersonalGallery"                   )
      icon = QIcon                     ( ":/images/pictures.png"             )
      mm   . addActionWithIcon         ( 1201 , icon , msg                   )
      ########################################################################
      msg  = self . getMenuItem        ( "ViewFullPictures"                  )
      icon = QIcon                     ( ":/images/searchimages.png"         )
      mm   . addActionWithIcon         ( 1202 , icon , msg                   )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . BlocMenu                  ( mm , atItem , uuid                  )
    self   . PropertiesMenu            ( mm , atItem                         )
    self   . UsageMenu                 ( mm , atItem                         )
    self   . DisplayMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . ScrollBarMenu             ( mm                                  )
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
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunBlocMenu        ( at , atItem , uuid                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunPropertiesMenu  ( at , atItem                         )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunUsageMenu       ( at , atItem                         )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunDisplayMenu     ( at                                  )
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
      self . InsertItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      self . RenameItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1201                        ) :
      ########################################################################
      self . OpenItemGallery           ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1202                        ) :
      ########################################################################
      self . ViewItemGallery           ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 7401                        ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

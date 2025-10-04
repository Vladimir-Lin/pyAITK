# -*- coding: utf-8 -*-
##############################################################################
## IconDock
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
import PySide6
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
##############################################################################
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
##############################################################################
from           . MenuManager           import MenuManager as MenuManager
from           . LineEdit              import LineEdit    as LineEdit
from           . ComboBox              import ComboBox    as ComboBox
from           . SpinBox               import SpinBox     as SpinBox
from           . ListDock              import ListDock    as ListDock
##############################################################################
from   AITK    . Essentials . Relation import Relation    as Relation
from   AITK    . Calendars  . StarDate import StarDate    as StarDate
from   AITK    . Calendars  . Periode  import Periode     as Periode
from   AITK    . Pictures   . Gallery  import Gallery     as GalleryItem
from   AITK    . Videos     . Album    import Album       as AlbumItem
from   AITK    . People     . People   import People      as PeopleItem
##############################################################################
class IconDock                    ( ListDock                               ) :
  ############################################################################
  emitIconsShow          = Signal (                                          )
  emitAllIcons           = Signal ( dict                                     )
  emitAssignIcon         = Signal ( QListWidgetItem , QIcon                  )
  emitAssignToolTip      = Signal ( QListWidgetItem , str                    )
  emitEmptySelections    = Signal (                                          )
  emitTryOpenURL         = Signal ( str                                      )
  emitRelationParameters = Signal ( str , int , int                          )
  emitDoSearch           = Signal (                                          )
  emitRestart            = Signal (                                          )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          ( parent , plan                            )
    ##########################################################################
    self . EditAllNames    = None
    self . IconFont        = None
    self . UsingName       = True
    self . SortOrder       = "asc"
    self . Total           = 0
    self . StartId         = 0
    self . Amount          = 60
    self . AssignedAmount  = 0
    self . ProgressMin     = 100
    self . scrollKeeper    = 0
    self . FetchTableKey   = "Tables"
    self . PrivateIcon     = False
    self . PrivateGroup    = False
    self . ExtraINFOs      = False
    self . DoReposition    = False
    self . LoopRunning     = True
    self . SpinStartId     = None
    self . SpinAmount      = None
    self . UuidItemMaps    =        {                                        }
    self . UuidItemNames   =        {                                        }
    self . FetchingIcons   = False
    self . DoParallelIcons =        {                                        }
    ##########################################################################
    self . Method          = "Original"
    ##########################################################################
    self . Grouping        = "Original"
    self . OldGrouping     = "Original"
    ## self . Grouping        = "Subordination"
    ## self . Grouping        = "Reverse"
    ##########################################################################
    self . defaultSelectionMode = "ContiguousSelection"
    ##########################################################################
    self . setViewMode              ( QListView . IconMode                   )
    self . setIconSize              ( QSize ( 128 , 128 )                    )
    self . setGridSize              ( QSize ( 156 , 192 )                    )
    self . setSpacing               ( 4                                      )
    self . setDragDropMode          ( QAbstractItemView . DropOnly           )
    self . setResizeMode            ( QListView . Adjust                     )
    self . setWordWrap              ( True                                   )
    self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAsNeeded             )
    self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAsNeeded             )
    self . setMinimumSize           ( QSize ( 144 , 200 )                    )
    ##########################################################################
    self . emitIconsShow       . connect ( self . ShowIconDock               )
    self . emitAllIcons        . connect ( self . refresh                    )
    self . emitAssignIcon      . connect ( self . AssignIcon                 )
    self . emitAssignToolTip   . connect ( self . AssignToolTip              )
    self . emitDoSearch        . connect ( self . DoActualSearch             )
    self . emitRestart         . connect ( self . restart                    )
    self . emitEmptySelections . connect ( self . doEmptySelections          )
    self . emitTryOpenURL      . connect ( self . doOpenURL                  )
    ##########################################################################
    return
  ############################################################################
  def setGrouping ( self , group                                           ) :
    self . Grouping    = group
    self . OldGrouping = group
    return self . Grouping
  ############################################################################
  def getGrouping ( self                                                   ) :
    return self . Grouping
  ############################################################################
  def isGrouping ( self                                                    ) :
    ##########################################################################
    ALLOWED =    [ "Subordination" , "Reverse"                               ]
    ##########################################################################
    if           ( self . Grouping not in ALLOWED                          ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def isCatalogue ( self                                                   ) :
    ##########################################################################
    ALLOWED =     [ "Subgroup" , "Reverse"                                   ]
    ##########################################################################
    if            ( self . Grouping not in ALLOWED                         ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def isOriginal      ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Original"                    ] )
  ############################################################################
  def isReverse       ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Reverse"                     ] )
  ############################################################################
  def isSubordination ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Subordination"               ] )
  ############################################################################
  def isSearching     ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Searching"                   ] )
  ############################################################################
  def isTagging       ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Tag"                         ] )
  ############################################################################
  def isCatalog       ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Catalog"                     ] )
  ############################################################################
  def isSubgroup      ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Subgroup"                    ] )
  ############################################################################
  def isPrivateListings ( self                                             ) :
    ##########################################################################
    return              ( self . Grouping in [ "PrivateListings"           ] )
  ############################################################################
  def catalogFetchTableKey         ( self                                  ) :
    ##########################################################################
    S      = self . ClassTag
    ##########################################################################
    if                             ( self . isTagging  (                 ) ) :
      ########################################################################
      T    = self . Relation . get ( "t1"                                    )
      R    = self . Relation . get ( "relation"                              )
      ########################################################################
    elif                           ( self . isSubgroup (                 ) ) :
      ########################################################################
      T    = self . Relation . get ( "t1"                                    )
      R    = self . Relation . get ( "relation"                              )
      ########################################################################
    elif                           ( self . isReverse  (                 ) ) :
      ########################################################################
      T    = self . Relation . get ( "t2"                                    )
      R    = self . Relation . get ( "relation"                              )
    ##########################################################################
    else                                                                     :
      ########################################################################
      self . FetchTableKey = S
      ########################################################################
      return
    ##########################################################################
    G      = self . Grouping
    E      = f"{S}-{G}-{T}-{R}"
    ##########################################################################
    self   . FetchTableKey = E
    ##########################################################################
    return
  ############################################################################
  def subgroupFetchTableKey        ( self                                  ) :
    ##########################################################################
    S      = self . ClassTag
    ##########################################################################
    if                             ( self . isSubordination (           ) ) :
      ########################################################################
      T    = self . Relation . get ( "t1"                                    )
      R    = self . Relation . get ( "relation"                              )
      ########################################################################
    elif                            ( self . isReverse       (           ) ) :
      ########################################################################
      T    = self . Relation . get ( "t2"                                    )
      R    = self . Relation . get ( "relation"                              )
    ##########################################################################
    else                                                                     :
      ########################################################################
      self . FetchTableKey = S
      ########################################################################
      return
    ##########################################################################
    G      = self . Grouping
    E      = f"{S}-{G}-{T}-{R}"
    ##########################################################################
    self   . FetchTableKey = E
    ##########################################################################
    return
  ############################################################################
  def PrepareFetchTableKey ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def getSelectedUuids               ( self                                ) :
    ##########################################################################
    UUIDs     =                      [                                       ]
    items     = self . selectedItems (                                       )
    ##########################################################################
    for item in items                                                        :
      ########################################################################
      UUID    = item . data          ( Qt . UserRole                         )
      UUID    = int                  ( UUID                                  )
      if                             ( UUID not in UUIDs                   ) :
        UUIDs . append               ( UUID                                  )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ShowIconDock       ( self                                            ) :
    ##########################################################################
    self . show          (                                                   )
    qApp . processEvents (                                                   )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . setActionLabel        ( "Label"   , self . windowTitle ( )        )
    self . LinkAction            ( "Insert"  , self . InsertItem             )
    self . LinkAction            ( "Delete"  , self . DeleteItems            )
    self . LinkAction            ( "Refresh" , self . startup                )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( self . defaultSelectionMode                 )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def GetUuidIcon                     ( self , DB , Uuid                   ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def defaultGetUuidIcon       ( self , DB , RELTAB , T1 , UUID            ) :
    ##########################################################################
    REL  = Relation            (                                             )
    REL  . set                 ( "first" , UUID                              )
    REL  . setT1               ( T1                                          )
    REL  . setT2               ( "Picture"                                   )
    REL  . setRelation         ( "Using"                                     )
    ##########################################################################
    PICS = REL . Subordination ( DB , RELTAB                                 )
    ##########################################################################
    if                         ( len ( PICS ) > 0                          ) :
      return PICS              [ 0                                           ]
    ##########################################################################
    return 0
  ############################################################################
  def setIconFont                     ( self , fnt                         ) :
    self . IconFont = fnt
    return self . IconFont
  ############################################################################
  def iconFont           ( self                                            ) :
    ##########################################################################
    if                   ( self . IconFont not in self . EmptySet          ) :
      return self . IconFont
    ##########################################################################
    return   self . font (                                                   )
  ############################################################################
  def AssignIcon   ( self , item , icon                                    ) :
    ##########################################################################
    if             ( item in self . EmptySet                               ) :
      return
    ##########################################################################
    if             ( icon in self . EmptySet                               ) :
      return
    ##########################################################################
    item . setIcon (               icon                                      )
    ##########################################################################
    return
  ############################################################################
  def AssignToolTip   ( self , item , text                                 ) :
    ##########################################################################
    if                ( item in self . EmptySet                            ) :
      return
    ##########################################################################
    item . setToolTip (               text                                   )
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent              ( self , item , UUID , NAME          ) :
    ##########################################################################
    FT     = self . iconFont          (                                      )
    if                                ( self . UsingName                   ) :
      item . setText                  ( NAME                                 )
    item   . setToolTip               ( str ( UUID )                         )
    item   . setTextAlignment         ( Qt   . AlignCenter                   )
    item   . setData                  ( Qt   . UserRole , str ( UUID )       )
    item   . setIcon                  ( self . defaultIcon ( )               )
    item   . setFont                  ( FT                                   )
    ##########################################################################
    JSOX   = self . itemJson          ( item                                 )
    ##########################################################################
    JSOX [ "Uuid" ] = UUID
    JSOX [ "Name" ] = NAME
    ##########################################################################
    self . setItemJson                ( item , JSOX                          )
    ##########################################################################
    return item
  ############################################################################
  def PrepareItem                     ( self ,        UUID , NAME          ) :
    ##########################################################################
    item = QListWidgetItem            (                                      )
    self . setItemJson                ( item , { }                           )
    ##########################################################################
    return self . PrepareItemContent  ( item , UUID , NAME                   )
  ############################################################################
  def PrepareEmptyItem                ( self                               ) :
    ##########################################################################
    FT   = self . iconFont            (                                      )
    IT   = QListWidgetItem            (                                      )
    if                                ( self . UsingName                   ) :
      IT . setText                    ( ""                                   )
    IT   . setTextAlignment           ( Qt   . AlignCenter                   )
    IT   . setData                    ( Qt   . UserRole , str ( 0 )          )
    IT   . setIcon                    ( self . defaultIcon ( )               )
    IT   . setFont                    ( FT                                   )
    ##########################################################################
    JSOX =                            { "Uuid" : 0 , "Name" : ""             }
    self . setItemJson                ( IT , JSOX                            )
    ##########################################################################
    return IT
  ############################################################################
  def setLineEdit                ( self , item , signal , method           ) :
    ##########################################################################
    rt   = self . visualItemRect ( item                                      )
    text = item . text           (                                           )
    fnt  = self . iconFont       (                                           )
    LE   = LineEdit              ( self , self . PlanFunc                    )
    LE   . setFont               ( fnt                                       )
    LE   . setText               ( text                                      )
    ##########################################################################
    self . EditItem   = item
    self . EditWidget = LE
    ##########################################################################
    try                                                                      :
      S  = getattr               ( LE, signal                                )
      S  . connect               ( method                                    )
    except AttributeError                                                    :
      pass
    ##########################################################################
    self . setItemWidget         ( item , LE                                 )
    ##########################################################################
    qApp . processEvents         (                                           )
    ##########################################################################
    FM   = QFontMetrics          ( fnt                                       )
    IC   = self . iconSize       (                                           )
    W    = IC   . width          (                                           )
    dW   = int                   ( int ( rt . width ( ) - W ) / 2            )
    S    = QSize                 ( W , FM . height ( ) + 4                   )
    L    = dW + rt . left        (                                           )
    T    = rt . top ( ) + IC . height (                                      )
    LE   . move                  ( L , T                                     )
    LE   . resize                ( S                                         )
    ##########################################################################
    LE   . setFocus              ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  def CreateColorIcon      ( self , R , G , B , W , H                      ) :
    ##########################################################################
    IMG = QImage           ( W , H , QImage . Format_RGB32                   )
    IMG . fill             ( QColor ( R , G , B )                            )
    ##########################################################################
    PIX = QPixmap          (                                                 )
    PIX . convertFromImage ( IMG                                             )
    ##########################################################################
    return QIcon           ( PIX                                             )
  ############################################################################
  def FetchEntityImage                ( self , DB , PUID                   ) :
    ##########################################################################
    if                                ( PUID <= 0                          ) :
      return None
    ##########################################################################
    TUBTAB     = self . Tables        [ "Thumb"                              ]
    WH         = f"where ( `usage` = 'ICON' ) and ( `uuid` = {PUID} )"
    OPTS       = "order by `id` desc limit 0 , 1"
    QQ         = f"select `thumb` from {TUBTAB} {WH} {OPTS} ;"
    DB         . Query                ( QQ                                   )
    THUMB      = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( THUMB == None                      ) :
      return None
    ##########################################################################
    if                                ( len ( THUMB ) <= 0                 ) :
      return None
    ##########################################################################
    BLOB       = THUMB                [ 0                                    ]
    if                                ( isinstance ( BLOB , bytearray )    ) :
      BLOB = bytes                    ( BLOB                                 )
    ##########################################################################
    if                                ( len ( BLOB ) <= 0                  ) :
      return None
    ##########################################################################
    IMG        = QImage               (                                      )
    IMG        . loadFromData         ( QByteArray ( BLOB ) , "PNG"          )
    TSIZE      = IMG . size           (                                      )
    ##########################################################################
    ISIZE      = self . iconSize      (                                      )
    ICZ        = QImage               ( ISIZE , QImage . Format_ARGB32       )
    ICZ        . fill                 ( QColor ( 255 , 255 , 255 )           )
    ##########################################################################
    W          = int       ( ( ISIZE . width  ( ) - TSIZE . width  ( ) ) / 2 )
    H          = int       ( ( ISIZE . height ( ) - TSIZE . height ( ) ) / 2 )
    PTS        = QPoint               ( W , H                                )
    ##########################################################################
    p          = QPainter             (                                      )
    p          . begin                ( ICZ                                  )
    p          . drawImage            ( PTS , IMG                            )
    p          . end                  (                                      )
    ##########################################################################
    return ICZ
  ############################################################################
  def FetchIcon                   ( self , DB , PUID                       ) :
    ##########################################################################
    IMG = self . FetchEntityImage (        DB , PUID                         )
    ##########################################################################
    if                            ( IMG in self . EmptySet                 ) :
      return None
    ##########################################################################
    return self . ImageToIcon     ( IMG                                      )
  ############################################################################
  def FetchBaseINFO ( self , DB , UUID , PUID                              ) :
    return
  ############################################################################
  def ParallelFetchINFOs               ( self , ID , UUIDs                 ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      ########################################################################
      self     . DoParallelIcons [ ID ] = True
      ########################################################################
      return
    ##########################################################################
    if                                 ( self . PrivateIcon                ) :
      DB       = self . ConnectHost    ( self . IconDB , True                )
    else                                                                     :
      DB       = self . ConnectDB      ( True                                )
    ##########################################################################
    if                                 ( self . NotOkay ( DB )             ) :
      ########################################################################
      self     . DoParallelIcons [ ID ] = True
      ########################################################################
      return
    ##########################################################################
    FMT        = self . Translations   [ "UI::LoadIcon"                      ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . LoopRunning            ) :
        continue
      ########################################################################
      if                               ( not self . FetchingIcons          ) :
        continue
      ########################################################################
      if                               ( U not in self . UuidItemMaps      ) :
        continue
      ########################################################################
      item     = self . UuidItemMaps   [ U                                   ]
      PUID     = self . GetUuidIcon    ( DB , U                              )
      ########################################################################
      if                               ( PUID <= 0                         ) :
        continue
      ########################################################################
      JSOX     = self . itemJson       ( item                                )
      if                               ( "Name" in JSOX                    ) :
        ######################################################################
        title  = JSOX                  [ "Name"                              ]
        ######################################################################
        if                             ( len ( title ) > 0                 ) :
          ####################################################################
          MSG  = FMT . format          ( title                               )
          self . ShowStatus            ( MSG                                 )
      ########################################################################
      if                               ( not self . LoopRunning            ) :
        continue
      ########################################################################
      self     . FetchBaseINFO         ( DB , U , PUID                       )
    ##########################################################################
    DB         . Close                 (                                     )
    ##########################################################################
    time       . sleep                 ( 0.1                                 )
    self       . DoParallelIcons [ ID ] = True
    ##########################################################################
    return
  ############################################################################
  def ParallelFetchIcons               ( self , ID , UUIDs                 ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      ########################################################################
      self     . DoParallelIcons [ ID ] = True
      ########################################################################
      return
    ##########################################################################
    if                                 ( self . PrivateIcon                ) :
      DB       = self . ConnectHost    ( self . IconDB , True                )
    else                                                                     :
      DB       = self . ConnectDB      ( True                                )
    ##########################################################################
    if                                 ( self . NotOkay ( DB )             ) :
      ########################################################################
      self     . DoParallelIcons [ ID ] = True
      ########################################################################
      return
    ##########################################################################
    FMT        = self . Translations   [ "UI::LoadIcon"                      ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . LoopRunning            ) :
        continue
      ########################################################################
      if                               ( not self . FetchingIcons          ) :
        continue
      ########################################################################
      if                               ( U not in self . UuidItemMaps      ) :
        continue
      ########################################################################
      item     = self . UuidItemMaps   [ U                                   ]
      PUID     = self . GetUuidIcon    ( DB , U                              )
      ########################################################################
      if                               ( PUID <= 0                         ) :
        continue
      ########################################################################
      JSOX     = self . itemJson       ( item                                )
      if                               ( "Name" in JSOX                    ) :
        ######################################################################
        title  = JSOX                  [ "Name"                              ]
        ######################################################################
        if                             ( len ( title ) > 0                 ) :
          ####################################################################
          MSG  = FMT . format          ( title                               )
          self . ShowStatus            ( MSG                                 )
      ########################################################################
      if                               ( not self . LoopRunning            ) :
        continue
      ########################################################################
      icon     = self . FetchIcon      ( DB , PUID                           )
      ########################################################################
      if                               ( icon not in [ False , None ]      ) :
        if                             ( self . LoopRunning                ) :
          if                           ( self . FetchingIcons              ) :
            ##################################################################
            self . emitAssignIcon . emit ( item , icon                       )
    ##########################################################################
    DB         . Close                 (                                     )
    ##########################################################################
    time       . sleep                 ( 0.1                                 )
    self       . DoParallelIcons [ ID ] = True
    ##########################################################################
    return
  ############################################################################
  def FetchIcons                       ( self , UUIDs                      ) :
    ##########################################################################
    TOTAL      = len                   ( UUIDs                               )
    ##########################################################################
    if                                 ( TOTAL  <= 0                       ) :
      return
    ##########################################################################
    self       . PushRunnings          (                                     )
    self       . OnBusy  . emit        (                                     )
    self       . setBustle             (                                     )
    self       . FetchingIcons = True
    ##########################################################################
    SLOTS      = 1
    if                                 ( TOTAL > 200                       ) :
      SLOTS    = 8
    elif                               ( TOTAL > 100                       ) :
      SLOTS    = 4
    elif                               ( TOTAL >  50                       ) :
      SLOTS    = 2
    ##########################################################################
    PART       = int                   ( TOTAL / SLOTS                       )
    ##########################################################################
    ZUIDs      =                       {                                     }
    for ID in range                    ( 0 , SLOTS                         ) :
      self     . DoParallelIcons [ ID ] = False
      ZUIDs [ ID ] =                   [                                     ]
    ##########################################################################
    if                                 ( SLOTS == 1                        ) :
      ########################################################################
      VAL      =                       ( ID , UUIDs ,                        )
      self     . Go                    ( self . ParallelFetchIcons , VAL     )
      ########################################################################
    else                                                                     :
      ########################################################################
      REMAINS  = TOTAL - int           ( PART * ( SLOTS - 1 )                )
      ########################################################################
      for i in range                   ( 0 , REMAINS                       ) :
        ZUIDs [ 0 ] . append           ( UUIDs [ i ]                         )
      ########################################################################
      for ID in range                  ( 1 , SLOTS                         ) :
        ######################################################################
        AT     = REMAINS +             ( ( ID - 1 ) * PART                   )
        ######################################################################
        for i in range                 ( 0 , PART                          ) :
           ZUIDs [ ID ] . append       ( UUIDs [ AT + i ]                    )
      ########################################################################
      for ID in range                  ( 0 , SLOTS                         ) :
        VAL    =                       ( ID , ZUIDs [ ID ] ,                 )
        self   . Go                    ( self . ParallelFetchIcons , VAL     )
    ##########################################################################
    DONE       = False
    while                              ( not DONE                          ) :
      ########################################################################
      time     . sleep                 ( 0.05                                )
      ########################################################################
      if                               ( not self . LoopRunning            ) :
        DONE   = True
        continue
      ########################################################################
      DONE     = True
      for i in range                   ( 0 , SLOTS                         ) :
        ######################################################################
        if                             ( not self . DoParallelIcons [ i ]  ) :
          ####################################################################
          DONE = False
    ##########################################################################
    self       . LoopRunning   = False
    self       . FetchingIcons = False
    ##########################################################################
    self       . setVacancy            (                                     )
    ##########################################################################
    try                                                                      :
      self     . GoRelax . emit        (                                     )
    except                                                                   :
      pass
    ##########################################################################
    self       . Notify                ( 2                                   )
    self       . ShowStatus            ( ""                                  )
    self       . PopRunnings           (                                     )
    ##########################################################################
    return
  ############################################################################
  def FetchExtraInformations          ( self , UUIDs                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def KeepScrollBar                  ( self                                ) :
    ##########################################################################
    self . scrollKeeper = 0
    ##########################################################################
    SB   = self . verticalScrollBar  (                                       )
    ##########################################################################
    if                               ( SB in self . EmptySet               ) :
      return
    ##########################################################################
    self . scrollKeeper = SB . value (                                       )
    ##########################################################################
    return
  ############################################################################
  def RestoreScrollBar              ( self                                 ) :
    ##########################################################################
    SB   = self . verticalScrollBar (                                        )
    ##########################################################################
    if                              ( SB in self . EmptySet                ) :
      return
    ##########################################################################
    MAXV = SB . maximum             (                                        )
    ##########################################################################
    if                              ( self . scrollKeeper > MAXV           ) :
      return
    ##########################################################################
    SB   . setValue                 ( self . scrollKeeper                    )
    ##########################################################################
    self . scrollKeeper = 0
    ##########################################################################
    return
  ############################################################################
  def setSortingOrder              ( self , order                          ) :
    ##########################################################################
    self . SortOrder = order
    ##########################################################################
    return
  ############################################################################
  def getSortingOrder              ( self                                  ) :
    return self . SortOrder
  ############################################################################
  def isAscendingOrder  ( self                                             ) :
    return              ( self . SortOrder in [ "asc"                      ] )
  ############################################################################
  def isDescendingOrder ( self                                             ) :
    return              ( self . SortOrder in [ "desc"                     ] )
  ############################################################################
  def SortingMenu                 ( self , mm                              ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu          ( TRX [ "UI::Sorting" ]                    )
    ##########################################################################
    msg = TRX                     [ "UI::NamesAsc"                           ]
    mm  . addActionFromMenu       ( LOM , 20000001 , msg                     )
    ##########################################################################
    msg = TRX                     [ "UI::NamesDesc"                          ]
    mm  . addActionFromMenu       ( LOM , 20000002 , msg                     )
    ##########################################################################
    hid =                         ( self . SortOrder == "asc"                )
    msg = TRX                     [ "UI::SortAsc"                            ]
    mm  . addActionFromMenu       ( LOM , 20000003 , msg , True , hid        )
    ##########################################################################
    hid =                         ( self . SortOrder == "desc"               )
    msg = TRX                     [ "UI::SortDesc"                           ]
    mm  . addActionFromMenu       ( LOM , 20000004 , msg , True , hid        )
    ##########################################################################
    return mm
  ############################################################################
  def RunSortingMenu               ( self , atId                           ) :
    ##########################################################################
    if                             ( atId == 20000001                      ) :
      self . sortItems             ( Qt . AscendingOrder                     )
      return False
    ##########################################################################
    if                             ( atId == 20000002                      ) :
      self . sortItems             ( Qt . DescendingOrder                    )
      return False
    ##########################################################################
    if                             ( atId == 20000003                      ) :
      self . SortOrder = "asc"
      return True
    ##########################################################################
    if                             ( atId == 20000004                      ) :
      self . SortOrder = "desc"
      return True
    ##########################################################################
    return   False
  ############################################################################
  def ScrollBarMenu         ( self , mm                                    ) :
    ##########################################################################
    VSB = self . verticalScrollBarPolicy (                                   )
    VSK =                                ( Qt . ScrollBarAlwaysOff == VSB    )
    HSK = not self . isWrapping          (                                   )
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu    ( TRX [ "UI::ScrollBar" ]                        )
    ##########################################################################
    msg = TRX               [ "UI::VerticalScrollBar"                        ]
    mm  . addActionFromMenu ( LOM , 21300001 , msg , True , not VSK          )
    ##########################################################################
    msg = TRX               [ "UI::HorizontalScrollBar"                      ]
    mm  . addActionFromMenu ( LOM , 21300002 , msg , True ,     HSK          )
    ##########################################################################
    return mm
  ############################################################################
  def RunScrollBarMenu ( self , atId                                       ) :
    ##########################################################################
    if                 ( 21300001 == atId                                  ) :
      ########################################################################
      VSB = self . verticalScrollBarPolicy (                                 )
      VSK =            ( Qt . ScrollBarAlwaysOff == VSB                      )
      ########################################################################
      if               ( VSK                                               ) :
        ######################################################################
        self . setVerticalScrollBarPolicy  ( Qt . ScrollBarAsNeeded          )
        ######################################################################
      else                                                                   :
        ######################################################################
        self . setVerticalScrollBarPolicy  ( Qt . ScrollBarAlwaysOff         )
      ########################################################################
      return True
    ##########################################################################
    if                 ( atId == 21300002                                  ) :
      ########################################################################
      if               ( self . isWrapping (                             ) ) :
        ######################################################################
        self . setWrapping                 ( False                           )
        self . setFlow                     ( QListView . LeftToRight         )
        ######################################################################
      else                                                                   :
        ######################################################################
        self . setWrapping                 ( True                            )
        self . setFlow                     ( QListView . TopToBottom         )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def AppendRefreshAction             ( self , mm , Id                     ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX                        [ "UI::Refresh"                        ]
    icon = QIcon                      ( ":/images/reload.png"                )
    mm   . addActionWithIcon          ( Id , icon , msg                      )
    ##########################################################################
    return mm
  ############################################################################
  def AppendInsertAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Insert"                                  ]
    icon = QIcon             ( ":/images/plus.png"                           )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendDeleteAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Delete"                                  ]
    icon = QIcon             ( ":/images/delete.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendRenameAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Rename"                                  ]
    icon = QIcon             ( ":/images/rename.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendSearchAction      ( self , mm , Id                             ) :
    ##########################################################################
    msg  = self . getMenuItem ( "Search"                                     )
    icon = QIcon              ( ":/images/search.png"                        )
    mm   . addActionWithIcon  ( Id , icon , msg                              )
    ##########################################################################
    return mm
  ############################################################################
  def AppendEditNamesAction  ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::EditNames"                               ]
    ICON = QIcon             ( ":/images/names.png"                          )
    mm   . addActionWithIcon ( Id , ICON , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AssureEditNamesAction      ( self , mm , Id , item                   ) :
    ##########################################################################
    if                           ( self . NotOkay ( item                 ) ) :
      return mm
    ##########################################################################
    if                           ( self . NotOkay ( self . EditAllNames  ) ) :
      return mm
    ##########################################################################
    self . AppendEditNamesAction ( mm , Id                                   )
    ##########################################################################
    return mm
  ############################################################################
  def AmountIndexMenu                   ( self , mm , HasFull = False      ) :
    ##########################################################################
    T      = int                        ( self . Total                       )
    AMT    = int                        ( self . Amount                      )
    if                                  ( T <= 0                           ) :
      return mm
    if                                  ( AMT > T                          ) :
      AMT  = T
    if                                  ( self . StartId > T               ) :
      self . StartId = 0
    ##########################################################################
    self   . AssignedAmount = AMT
    ##########################################################################
    MSG    = self . getMenuItem         ( "Total"                            )
    SSI    = self . getMenuItem         ( "SpinStartId"                      )
    SSA    = self . getMenuItem         ( "SpinAmount"                       )
    MSG    = MSG . format               ( T                                  )
    ##########################################################################
    mm     . addAction                  ( 9999991 , MSG                      )
    ##########################################################################
    self   . SpinStartId = SpinBox      ( None , self . PlanFunc             )
    self   . SpinStartId . setPrefix    ( SSI                                )
    self   . SpinStartId . setRange     ( 0 , self . Total                   )
    self   . SpinStartId . setValue     ( self . StartId                     )
    self   . SpinStartId . setAlignment ( Qt . AlignRight                    )
    mm     . addWidget                  ( 9999992 , self . SpinStartId       )
    ##########################################################################
    self   . SpinAmount  = SpinBox      ( None , self . PlanFunc             )
    self   . SpinAmount  . setPrefix    ( SSA                                )
    self   . SpinAmount  . setRange     ( 0 , self . Total                   )
    self   . SpinAmount  . setValue     ( AMT                                )
    self   . SpinAmount  . setAlignment ( Qt . AlignRight                    )
    mm     . addWidget                  ( 9999993 , self . SpinAmount        )
    ##########################################################################
    if                                  ( HasFull                          ) :
      ########################################################################
      MSG  = self . getMenuItem         ( "ShowEverything"                   )
      mm   . addAction                  ( 9999994 , MSG                      )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    return mm
  ############################################################################
  def RunAmountIndexMenu                ( self , ATID = -1                 ) :
    ##########################################################################
    if                                  ( 9999994 == ATID                  ) :
      ########################################################################
      self . StartId = 0
      self . Amount  = self . Total
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . SpinStartId == None       ) :
      return False
    ##########################################################################
    if                                  ( self . SpinAmount  == None       ) :
      return False
    ##########################################################################
    SID    = self . SpinStartId . value (                                    )
    AMT    = self . SpinAmount  . value (                                    )
    ##########################################################################
    self . SpinStartId = None
    self . SpinAmount  = None
    ##########################################################################
    if ( ( SID != self . StartId ) or ( AMT != self . AssignedAmount ) )     :
      ########################################################################
      self . StartId = SID
      self . Amount  = AMT
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  ## 選單當中抓取項目資訊
  ############################################################################
  def GetMenuDetails              ( self , pos                             ) :
    ##########################################################################
    items  = self . selectedItems (                                          )
    atItem = self . itemAt        ( pos                                      )
    uuid   = 0
    ##########################################################################
    if                            ( atItem not in [ False , None ]         ) :
      uuid = atItem . data        ( Qt . UserRole                            )
      uuid = int                  ( uuid                                     )
    ##########################################################################
    return items , atItem , uuid
  ############################################################################
  def PageHome     ( self                                                  ) :
    ##########################################################################
    self . StartId = 0
    self . restart (                                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd      ( self                                                  ) :
    ##########################################################################
    self . StartId   = self . Total - self . Amount
    if             ( self . StartId <= 0                                   ) :
      self . StartId = 0
    ##########################################################################
    self . restart (                                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp       ( self                                                  ) :
    ##########################################################################
    self . StartId   = self . StartId - self . Amount
    if             ( self . StartId <= 0                                   ) :
      self . StartId = 0
    ##########################################################################
    self . restart (                                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown     ( self                                                  ) :
    ##########################################################################
    self . StartId   = self . StartId + self . Amount
    if             ( self . StartId > self . Total                         ) :
      self . StartId = self . Total
    ##########################################################################
    self . restart (                                                         )
    ##########################################################################
    return
  ############################################################################
  def doEditAllNames ( self                                                ) :
    return           ( self . EditAllNames not in [ False , None ]           )
  ############################################################################
  def Shutdown          ( self                                             ) :
    ##########################################################################
    self . StayAlive     = False
    self . LoopRunning   = False
    self . FetchingIcons = False
    ##########################################################################
    if                  ( self . isThreadRunning ( )                       ) :
      return False
    ##########################################################################
    self . Leave . emit ( self                                               )
    ##########################################################################
    return True
  ############################################################################
  def defaultCloseEvent      ( self , event                                ) :
    ##########################################################################
    if                       ( self . Shutdown ( )                         ) :
      super ( ) . closeEvent ( event                                         )
    else                                                                     :
      event     . ignore     (                                               )
    ##########################################################################
    return
  ############################################################################
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . KeepScrollBar           (                                      )
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    ##########################################################################
    if                                ( self . UsingName                   ) :
      ########################################################################
      NAMEs = JSON                    [ "NAMEs"                              ]
      self . UuidItemNames = NAMEs
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                              ( self . UsingName                   ) :
        IT  = self . PrepareItem      ( U , NAMEs [ U ]                      )
      else                                                                   :
        IT  = self . PrepareItem      ( U , ""                               )
      self  . addItem                 ( IT                                   )
      self  . UuidItemMaps [ U ] = IT
    ##########################################################################
    qApp    . processEvents           (                                      )
    self    . RestoreScrollBar        (                                      )
    self    . emitIconsShow . emit    (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      ########################################################################
      self  . Go                      ( self . FetchIcons , ( UUIDs , )      )
      ########################################################################
      if                              ( self . ExtraINFOs                  ) :
        ######################################################################
        self . Go                     ( self . FetchExtraInformations      , \
                                        ( UUIDs , )                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def DefaultObtainsItemUuids         ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    UUIDs   =                         [                                      ]
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    return self . DefaultObtainsItemUuids ( DB                               )
  ############################################################################
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      ########################################################################
      TABLE = self . Tables   [ "Names"                                      ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    self    . LoopRunning = False
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    ##########################################################################
    if                                ( self . NotOkay ( DB )              ) :
      ########################################################################
      self  . emitIconsShow . emit    (                                      )
      self  . Notify                  ( 1                                    )
      self  . LoopRunning = True
      ########################################################################
      return
    ##########################################################################
    self    . PushRunnings            (                                      )
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
    if                                ( self . UsingName                   ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    ##########################################################################
    try                                                                      :
      self  . GoRelax . emit          (                                      )
    except                                                                   :
      pass
    ##########################################################################
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
    self    . PopRunnings             (                                      )
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
  def restart        ( self                                                ) :
    ##########################################################################
    self . clear     (                                                       )
    self . startup   (                                                       )
    ##########################################################################
    return
  ############################################################################
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
    self . Go          ( self . looking , ( T , )                            )
    ##########################################################################
    return
  ############################################################################
  def DoActualSearch                   ( self                              ) :
    ##########################################################################
    qApp   . processEvents             (                                     )
    time   . sleep                     ( 0.2                                 )
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
  def Search                   ( self                                      ) :
    ##########################################################################
    self . emitDoSearch . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def SearchingForT1                  ( self , name , Main , NameTable     ) :
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
    OCPTAB  = self . Tables           [ Main                                 ]
    NAMTAB  = self . Tables           [ NameTable                            ]
    LIC     = self . getLocality      (                                      )
    LNAME   = name
    LNAME   = LNAME . lower           (                                      )
    LIKE    = f"%{LNAME}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    RQ      = f"select `uuid` from {OCPTAB} where ( `used` > 0 )"
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    try                                                                      :
      self  . GoRelax . emit          (                                      )
    except                                                                   :
      pass
    ##########################################################################
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
    self . Method    = "Searching"
    ##########################################################################
    self . loading                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def SearchingForT2                  ( self , name , Main , NameTable     ) :
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
    OCPTAB  = self . Tables           [ Main                                 ]
    NAMTAB  = self . Tables           [ NameTable                            ]
    LIC     = self . getLocality      (                                      )
    LNAME   = name
    LNAME   = LNAME . lower           (                                      )
    LIKE    = f"%{LNAME}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    RQ      = f"select `uuid` from {OCPTAB} where ( `used` > 0 )"
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    try                                                                      :
      self  . GoRelax . emit          (                                      )
    except                                                                   :
      pass
    ##########################################################################
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
  def UpdateItemNameByTable           ( self , table , item , uuid , name  ) :
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    NAMTAB = self . Tables            [ table                                ]
    DB     . LockWrites               ( [ NAMTAB ]                           )
    ##########################################################################
    self   . AssureUuidNameByLocality ( DB                                 , \
                                         NAMTAB                            , \
                                         uuid                              , \
                                         name                              , \
                                         self . getLocality ( )              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def defaultLineEditorFinished         ( self                             ) :
    ##########################################################################
    if                                  ( self . EditItem   == None        ) :
      return
    ##########################################################################
    if                                  ( self . EditWidget == None        ) :
      return
    ##########################################################################
    IT                = self . EditItem
    LE                = self . EditWidget
    self . EditItem   = None
    self . EditWidget = None
    CORRECT           = True
    ##########################################################################
    JSON              = self . itemJson ( IT                                 )
    TEXT              = LE   . text     (                                    )
    NAME              = ""
    UUID              = 0
    self              . setItemWidget   ( IT , None                          )
    ##########################################################################
    if ( ( CORRECT ) and ( "Uuid" not in JSON ) )                            :
      CORRECT         = False
    else                                                                     :
      UUID            = JSON            [ "Uuid"                             ]
    ##########################################################################
    if ( ( CORRECT ) and ( "Name" in JSON ) )                                :
      NAME            = JSON            [ "Name"                             ]
    ##########################################################################
    if ( ( CORRECT ) and ( UUID == 0 ) and ( len ( TEXT ) <= 0 ) )           :
      CORRECT         = False
    ##########################################################################
    if ( ( CORRECT ) and ( UUID >  0 ) and ( NAME == TEXT ) )                :
      CORRECT         = False
    ##########################################################################
    if                                  ( not CORRECT                      ) :
      if                                ( UUID <= 0                        ) :
        self . takeItem                 ( self . row ( IT )                  )
      return
    ##########################################################################
    if                                  ( UUID > 0                         ) :
      ########################################################################
      if                                ( self . UsingName                 ) :
        ######################################################################
        IT   . setText                  ( TEXT                               )
        self . PrepareItemContent       ( IT , UUID , TEXT                   )
        self . Go                       ( self . UpdateItemName            , \
                                          ( IT , UUID , TEXT , )             )
      ########################################################################
      return
    ##########################################################################
    IT   . setText                      ( TEXT                               )
    ##########################################################################
    self . Go                           ( self . AppendItemName            , \
                                          ( IT , TEXT , )                    )
    ##########################################################################
    return
  ############################################################################
  def LineEditorFinished             ( self                                ) :
    ##########################################################################
    self . defaultLineEditorFinished (                                       )
    ##########################################################################
    return
  ############################################################################
  def doEmptySelections          ( self                                    ) :
    ##########################################################################
    items = self . selectedItems (                                           )
    ##########################################################################
    for item in items                                                        :
      row = self . row           ( item                                      )
      if                         ( row >= 0                                ) :
        self . takeItem          ( row                                       )
    ##########################################################################
    return
  ############################################################################
  def EmptySelections                 ( self                               ) :
    ##########################################################################
    self . emitEmptySelections . emit (                                      )
    ##########################################################################
    return
  ############################################################################
  def defaultRenameItem       ( self , name  , func                        ) :
    ##########################################################################
    IT   = self . currentItem (                                              )
    ##########################################################################
    if                        ( IT in [ False , None ]                     ) :
      return
    ##########################################################################
    self . setLineEdit        ( IT , name , func                             )
    ##########################################################################
    return
  ############################################################################
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( "editingFinished" , self . LineEditorFinished )
    ##########################################################################
    return
  ############################################################################
  def defaultDeleteItems            ( self                                 ) :
    ##########################################################################
    UUIDs = self . getSelectedUuids (                                        )
    ##########################################################################
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    self  . EmptySelections         (                                        )
    self  . Go                      ( self . RemoveItems , ( UUIDs , )       )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    self . defaultDeleteItems (                                              )
    ##########################################################################
    return
  ############################################################################
  def defaultInsertItem              ( self , name , func                  ) :
    ##########################################################################
    IT     = self . PrepareEmptyItem (                                       )
    if                               ( self . SortOrder == "asc"           ) :
      self . addItem                 (     IT                                )
    else                                                                     :
      self . insertItem              ( 0 , IT                                )
    ##########################################################################
    self   . setLineEdit             ( IT , name , func                      )
    ##########################################################################
    return
  ############################################################################
  def InsertItem             ( self                                        ) :
    ##########################################################################
    self . defaultInsertItem ( "editingFinished" , self . LineEditorFinished )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemTitleStatus ( self , menuItem , title , CNT              ) :
    ##########################################################################
    FMT  = self . getMenuItem ( menuItem                                     )
    MSG  = FMT  . format      ( title , CNT                                  )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemCountStatus ( self , menuItem , CNT                      ) :
    ##########################################################################
    FMT  = self . getMenuItem ( menuItem                                     )
    MSG  = FMT  . format      ( CNT                                          )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemMessage     ( self , menuItem                            ) :
    ##########################################################################
    MSG  = self . getMenuItem ( menuItem                                     )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def defaultDropInFunction        ( self , source , pos , JSON , func     ) :
    ##########################################################################
    PUID , NAME = self . itemAtPos ( pos                                     )
    PUID        = int              ( PUID                                    )
    if                             ( PUID <= 0                             ) :
      return True
    ##########################################################################
    self        . Go               ( func , ( PUID , NAME , JSON , )         )
    ##########################################################################
    return True
  ############################################################################
  def defaultDropInside            ( self , source , pos , JSON , M , A    ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ATID        = int              ( ATID                                    )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                             ( self == source                        ) :
      ########################################################################
      self      . Go               ( M , ( ATID , NAME , JSON , )            )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    self        . Go               ( A , ( ATID , NAME , JSON , )            )
    ##########################################################################
    return True
  ############################################################################
  def GenerateRemoveSQLs  ( self , UUIDs , REL , TABLE , item = "second"   ) :
    ##########################################################################
    SQLs   =              [                                                  ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  . set          ( item , UUID                                      )
      QQ   = REL . Delete ( TABLE                                            )
      SQLs . append       ( QQ                                               )
    ##########################################################################
    return SQLs
  ############################################################################
  def GenerateGroupRemoveSQLs ( self , UUIDs , REL , TAB , reverse = False ) :
    ##########################################################################
    SQLs     =                [                                              ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                      ( reverse                                    ) :
        self . Relation . set ( "first"  , UUID                              )
      else                                                                   :
        self . Relation . set ( "second" , UUID                              )
      ########################################################################
      QQ     = REL . Delete   ( TAB                                          )
      SQLs   . append         ( QQ                                           )
    ##########################################################################
    return SQLs
  ############################################################################
  def QuickExecuteSQLs        ( self , TITLE , Threshold , RELTAB , SQLs   ) :
    ##########################################################################
    DB   = self . ConnectDB   (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    self . OnBusy  . emit     (                                              )
    self . setBustle          (                                              )
    DB   . LockWrites         ( [ RELTAB                                   ] )
    ##########################################################################
    self . ExecuteSqlCommands ( TITLE , DB , SQLs , Threshold                )
    ##########################################################################
    DB   . UnlockTables       (                                              )
    self . setVacancy         (                                              )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit   (                                              )
    except                                                                   :
      pass
    ##########################################################################
    DB   . Close              (                                              )
    ##########################################################################
    return
  ############################################################################
  def AppendingPictures        ( self , atUuid , NAME , JSON , table , T1  ) :
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
    RELTAB = self . Tables     [ table                                       ]
    GALM   = GalleryItem       (                                             )
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    GALM   . ConnectToPictures ( DB , RELTAB , atUuid , T1 , UUIDs           )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit    (                                             )
    except                                                                   :
      pass
    ##########################################################################
    DB     . Close             (                                             )
    ##########################################################################
    self   . Notify            ( 5                                           )
    ##########################################################################
    return True
  ############################################################################
  def AppendingIntoPeople     ( self                                       , \
                                atUuid                                     , \
                                NAME                                       , \
                                JSON                                       , \
                                table                                      , \
                                T2                                         , \
                                RELATED                                    ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ table                                        ]
    PEOM   = PeopleItem       (                                              )
    ##########################################################################
    DB     . LockWrites       ( [ RELTAB                                   ] )
    PEOM   . RelateWithPeople ( DB , RELTAB , RELATED , atUuid , T2 , UUIDs  )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    self   . setVacancy       (                                              )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit   (                                              )
    except                                                                   :
      pass
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify            ( 5                                           )
    ##########################################################################
    return True
  ############################################################################
  def AppendingPeopleIntoT1     ( self , atUuid , NAME , JSON , table , T1 ) :
    ##########################################################################
    UUIDs  = JSON               [ "UUIDs"                                    ]
    if                          ( len ( UUIDs ) <= 0                       ) :
      return False
    ##########################################################################
    if                          ( self . PrivateGroup                      ) :
      DB   = self . ConnectHost ( self . GroupDB                             )
    else                                                                     :
      DB   = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    RELTAB = self . Tables      [ table                                      ]
    PEOM   = PeopleItem         (                                            )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    PEOM   . ConnectToPeople    ( DB , RELTAB , atUuid , T1 , UUIDs          )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    self   . setVacancy         (                                            )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit     (                                            )
    except                                                                   :
      pass
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . Notify              ( 5                                         )
    ##########################################################################
    return True
  ############################################################################
  def AppendingOrganizationIntoT1 ( self                                   , \
                                    atUuid                                 , \
                                    NAME                                   , \
                                    JSON                                   , \
                                    table                                  , \
                                    T1                                     ) :
    ##########################################################################
    UUIDs  = JSON               [ "UUIDs"                                    ]
    if                          ( len ( UUIDs ) <= 0                       ) :
      return False
    ##########################################################################
    if                          ( self . PrivateGroup                      ) :
      DB   = self . ConnectHost ( self . GroupDB                             )
    else                                                                     :
      DB   = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    RELTAB = self . Tables      [ table                                      ]
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    REL    = Relation           (                                            )
    REL    . set                ( "first" , atUuid                           )
    REL    . setT1              ( T1                                         )
    REL    . setT2              ( "Organization"                             )
    REL    . setRelation        ( "Subordination"                            )
    REL    . Joins              ( DB , RELTAB , UUIDs                        )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    self   . setVacancy         (                                            )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit     (                                            )
    except                                                                   :
      pass
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . Notify              ( 5                                         )
    ##########################################################################
    return True
  ############################################################################
  def AppendingAlbumIntoT1      ( self , atUuid , NAME , JSON , table , T1 ) :
    ##########################################################################
    UUIDs  = JSON               [ "UUIDs"                                    ]
    if                          ( len ( UUIDs ) <= 0                       ) :
      return False
    ##########################################################################
    if                          ( self . PrivateGroup                      ) :
      DB   = self . ConnectHost ( self . GroupDB                             )
    else                                                                     :
      DB   = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    RELTAB = self . Tables      [ table                                      ]
    ABUM   = AlbumItem          (                                            )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ABUM   . ConnectToAlbums    ( DB , RELTAB , atUuid , T1 , UUIDs          )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    self   . setVacancy         (                                            )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit     (                                            )
    except                                                                   :
      pass
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . Notify             ( 5                                          )
    ##########################################################################
    return True
  ############################################################################
  def GenerateRepositionSQL ( self , TABLE , REL , UUID , LUID , Reverse   ) :
    ##########################################################################
    if                      ( Reverse                                      ) :
      ########################################################################
      REL . set             ( "first" , UUID                                 )
      WS  = REL . ExactItem (                                                )
      QQ  = f"update {TABLE} set `reverse` = {LUID} {WS} ;"
      ########################################################################
    else                                                                     :
      ########################################################################
      REL . set             ( "second" , UUID                                )
      WS  = REL . ExactItem (                                                )
      QQ  = f"update {TABLE} set `position` = {LUID} {WS} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def GenerateRepositionSQLs               ( self                          , \
                                             SQLs                          , \
                                             TABLE                         , \
                                             REL                           , \
                                             UUIDs                         , \
                                             START                         , \
                                             Reverse                       ) :
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = self . GenerateRepositionSQL ( TABLE                         , \
                                             REL                           , \
                                             UUID                          , \
                                             START                         , \
                                             Reverse                         )
      SQLs  . append           ( QQ                                          )
      ########################################################################
      START = START + 1
    ##########################################################################
    return SQLs
  ############################################################################
  def GetNormalLastestPosition  ( self , DB , TABLE , LUID                 ) :
    ##########################################################################
    RELTAB = self . Tables      [ TABLE                                      ]
    ITEM   = "`position`"
    OPTS   = ""
    LMTS   = "limit 0 , 1"
    ##########################################################################
    self   . Relation . set     ( "second" , LUID                            )
    QQ     = self . Relation . ExactColumn ( RELTAB , ITEM , OPTS , LMTS     )
    DB     . Query              ( QQ                                         )
    RR     = DB . FetchOne      (                                            )
    ##########################################################################
    if                          ( RR in [ False , None ]                   ) :
      return 0
    ##########################################################################
    if                          ( len ( RR ) != 1                          ) :
      return 0
    ##########################################################################
    return int                  ( RR [ 0 ]                                   )
  ############################################################################
  def GetReverseLastestPosition ( self , DB , TABLE , LUID                 ) :
    ##########################################################################
    RELTAB = self . Tables      [ TABLE                                      ]
    ITEM   = "`reverse`"
    OPTS   = ""
    LMTS   = "limit 0 , 1"
    ##########################################################################
    self   . Relation . set     ( "first" , LUID                             )
    QQ     = self . Relation . ExactColumn ( RELTAB , ITEM , OPTS , LMTS     )
    DB     . Query              ( QQ                                         )
    RR     = DB . FetchOne      (                                            )
    ##########################################################################
    if                          ( RR in [ False , None ]                   ) :
      return 0
    ##########################################################################
    if                          ( len ( RR ) != 1                          ) :
      return 0
    ##########################################################################
    return int                  ( RR [ 0 ]                                   )
  ############################################################################
  def GetGroupLastestPosition                 ( self , DB , TABLE , LUID   ) :
    ##########################################################################
    if                                        ( self . isSubordination ( ) ) :
      return self . GetNormalLastestPosition  ( DB , TABLE , LUID            )
    return   self . GetReverseLastestPosition ( DB , TABLE , LUID            )
  ############################################################################
  def GenerateNormalMovingSQL               ( self                         , \
                                              TABLE                        , \
                                              LAST                         , \
                                              UUIDs                        , \
                                              Reverse                      ) :
    ##########################################################################
    RELTAB = self . Tables                 [ TABLE                           ]
    SQLs   =                               [                                 ]
    ##########################################################################
    SQLs   = self . GenerateRepositionSQLs ( SQLs                          , \
                                             RELTAB                        , \
                                             self . Relation               , \
                                             UUIDs                         , \
                                             LAST + 1000000                , \
                                             Reverse                         )
    SQLs   = self . GenerateRepositionSQLs ( SQLs                          , \
                                             RELTAB                        , \
                                             self . Relation               , \
                                             UUIDs                         , \
                                             0                             , \
                                             Reverse                         )
    ##########################################################################
    return SQLs
  ############################################################################
  def GenerateGroupMovingSQL              ( self , TABLE , LAST , UUIDs    ) :
    ##########################################################################
    R = self . isReverse                  (                                  )
    return self . GenerateNormalMovingSQL ( TABLE , LAST , UUIDs , R         )
  ############################################################################
  def RepositionMembershipOrders ( self , DB , TABKEY , MSGKEY , M = 100   ) :
    ##########################################################################
    RELTAB  = self . Tables      [ TABKEY                                    ]
    ##########################################################################
    if                           ( self . isSubordination (              ) ) :
      ########################################################################
      UUIDs = self . Relation . Subordination ( DB , RELTAB                  )
      ########################################################################
    elif                         ( self . isReverse       (              ) ) :
      ########################################################################
      UUIDs = self . Relation . GetOwners     ( DB , RELTAB                  )
    ##########################################################################
    if                           ( len ( UUIDs ) <= 0                      ) :
      return
    ##########################################################################
    LUID    = UUIDs              [ -1                                        ]
    LAST    = self . GetGroupLastestPosition ( DB     , TABKEY , LUID        )
    SQLs    = self . GenerateGroupMovingSQL  ( TABKEY , LAST   , UUIDs       )
    self    . ExecuteSqlCommands             ( MSGKEY , DB     , SQLs , M    )
    ##########################################################################
    return
  ############################################################################
  def DoRepositionMembershipOrders    ( self , TABKEY , MSGKEY , M = 100   ) :
    ##########################################################################
    if                                ( not self . isGrouping (          ) ) :
      return
    ##########################################################################
    DB   = self . ConnectDB           (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    RTAB = self . Tables              [ TABKEY                               ]
    ##########################################################################
    DB   . LockWrites                 ( [ RTAB                             ] )
    self . RepositionMembershipOrders ( DB , TABKEY , MSGKEY , M             )
    DB   . UnlockTables               (                                      )
    DB   . Close                      (                                      )
    ##########################################################################
    return
  ############################################################################
  def JoinMajorEntities                       ( self                       , \
                                                DB                         , \
                                                atUuid                     , \
                                                UUIDs                      , \
                                                TABKEY                     , \
                                                MSGKEY                     , \
                                                M = 100                    ) :
    ##########################################################################
    RELTAB  = self . Tables                   [ TABKEY                       ]
    ##########################################################################
    if                                        ( self . isSubordination ( ) ) :
      ########################################################################
      self  . Relation  . Joins               ( DB , RELTAB , UUIDs          )
      ########################################################################
      if                                      ( not self . DoReposition    ) :
        return
      ########################################################################
      OPTS  = f"order by `position` asc , `reverse` asc"
      PUIDs = self . Relation . Subordination ( DB , RELTAB , OPTS           )
      ########################################################################
    elif                                      ( self . isReverse       ( ) ) :
      ########################################################################
      self  . Relation  . JoinsFirst          ( DB , RELTAB , UUIDs          )
      ########################################################################
      if                                      ( not self . DoReposition    ) :
        return
      ########################################################################
      OPTS  = f"order by `reverse` asc , `position` asc"
      PUIDs = self . Relation . GetOwners     ( DB , RELTAB , OPTS           )
      ########################################################################
    else                                                                     :
      ########################################################################
      PUIDs =                                 [                              ]
    ##########################################################################
    if                                        ( len ( PUIDs ) <= 0         ) :
      return
    ##########################################################################
    LUID    = PUIDs                           [ -1                           ]
    LAST    = self . GetGroupLastestPosition  ( DB     , TABKEY , LUID       )
    PUIDs   = self . OrderingPUIDs            ( atUuid , UUIDs  , PUIDs      )
    SQLs    = self . GenerateGroupMovingSQL   ( TABKEY , LAST   , UUIDs      )
    self    . ExecuteSqlCommands              ( MSGKEY , DB     , SQLs , M   )
    ##########################################################################
    return
  ############################################################################
  def AppendingMajorEntities   ( self                                      , \
                                 atUuid                                    , \
                                 UUIDs                                     , \
                                 TABKEY                                    , \
                                 MSGKEY                                    , \
                                 M = 100                                   ) :
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ TABKEY                                      ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . JoinMajorEntities ( DB , atUuid , UUIDs , TABKEY , MSGKEY , M   )
    DB     . UnlockTables      (                                             )
    ##########################################################################
    DB     . Close             (                                             )
    ##########################################################################
    self   . setVacancy        (                                             )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit    (                                             )
    except                                                                   :
      pass
    ##########################################################################
    return
  ############################################################################
  def MajorAppending                 ( self                                , \
                                       atUuid                              , \
                                       JSON                                , \
                                       TABKEY                              , \
                                       MSGKEY                              ) :
    ##########################################################################
    UUIDs   = JSON                   [ "UUIDs"                               ]
    if                               ( len ( UUIDs ) <= 0                  ) :
      return
    ##########################################################################
    if                               ( self . isDescendingOrder (        ) ) :
      UUIDs = list                   ( reversed ( UUIDs                    ) )
    ##########################################################################
    self    . AppendingMajorEntities ( atUuid                              , \
                                       UUIDs                               , \
                                       TABKEY                              , \
                                       MSGKEY                              , \
                                       self . ProgressMin                    )
    self    . loading                (                                       )
    ##########################################################################
    return
  ############################################################################
  def MoveMajorEntities                       ( self                       , \
                                                DB                         , \
                                                atUuid                     , \
                                                UUIDs                      , \
                                                TABKEY                     , \
                                                MSGKEY                     , \
                                                M = 100                    ) :
    ##########################################################################
    RELTAB  = self . Tables                   [   TABKEY                     ]
    ##########################################################################
    if                                        ( self . isSubordination ( ) ) :
      ########################################################################
      OPTS  = f"order by `position` asc , `reverse` asc"
      PUIDs = self . Relation . Subordination ( DB , RELTAB , OPTS           )
      ########################################################################
    elif                                      ( self . isReverse       ( ) ) :
      ########################################################################
      OPTS  = f"order by `reverse` asc , `position` asc"
      PUIDs = self . Relation . GetOwners     ( DB , RELTAB , OPTS           )
      ########################################################################
    else                                                                     :
      ########################################################################
      return
    ##########################################################################
    if                                        ( len ( PUIDs ) < 2          ) :
      return
    ##########################################################################
    LUID    = PUIDs                           [ -1                           ]
    LAST    = self . GetGroupLastestPosition  ( DB     , TABKEY , LUID       )
    PUIDs   = self . OrderingPUIDs            ( atUuid , UUIDs  , PUIDs      )
    SQLs    = self . GenerateGroupMovingSQL   ( TABKEY , LAST   , PUIDs      )
    self    . ExecuteSqlCommands              ( MSGKEY , DB , SQLs , M       )
    ##########################################################################
    return
  ############################################################################
  def MovingMajorEntities      ( self                                      , \
                                 atUuid                                    , \
                                 UUIDs                                     , \
                                 TABKEY                                    , \
                                 MSGKEY                                    , \
                                 M = 100                                   ) :
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ TABKEY                                      ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . MoveMajorEntities ( DB , atUuid , UUIDs , TABKEY , MSGKEY , M   )
    DB     . UnlockTables      (                                             )
    ##########################################################################
    DB     . Close             (                                             )
    ##########################################################################
    self   . setVacancy        (                                             )
    ##########################################################################
    try                                                                      :
      self . GoRelax . emit    (                                             )
    except                                                                   :
      pass
    ##########################################################################
    return
  ############################################################################
  def MajorMoving                 ( self                                   , \
                                    atUuid                                 , \
                                    JSON                                   , \
                                    TABKEY                                 , \
                                    MSGKEY                                 ) :
    ##########################################################################
    UUIDs   = JSON                [ "UUIDs"                                  ]
    if                            ( len ( UUIDs ) <= 0                     ) :
      return
    ##########################################################################
    if                            ( self . isDescendingOrder (           ) ) :
      UUIDs = list                ( reversed ( UUIDs                       ) )
    ##########################################################################
    self    . MovingMajorEntities ( atUuid                                 , \
                                    UUIDs                                  , \
                                    TABKEY                                 , \
                                    MSGKEY                                 , \
                                    self . ProgressMin                       )
    self    . loading             (                                          )
    ##########################################################################
    return
  ############################################################################
  def defaultDropMoving    ( self , sourceWidget , mimeData , mousePos     ) :
    ##########################################################################
    if                     ( self . droppingAction                         ) :
      return False
    ##########################################################################
    if                     ( sourceWidget != self                          ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( mousePos                                        )
    ##########################################################################
    if                     ( atItem in [ False , None ]                    ) :
      return True
    ##########################################################################
    if                     ( atItem . isSelected ( )                       ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def subgroupUpdateLocalityUsage  ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping (             ) ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( self . NotOkay ( DB                 ) ) :
      return False
    ##########################################################################
    if                             ( self . isSubordination (            ) ) :
      ########################################################################
      UUID = self . Relation . get ( "first"                                 )
      TYPE = self . Relation . get ( "t1"                                    )
      ########################################################################
    elif                           ( self . isReverse       (            ) ) :
      ########################################################################
      UUID = self . Relation . get ( "second"                                )
      TYPE = self . Relation . get ( "t2"                                    )
      ########################################################################
    else                                                                     :
      return False
    ##########################################################################
    SCOPE  = self . FetchTableKey
    PAMTAB = self . Tables         [ "Parameters"                            ]
    DB     . LockWrites            ( [ PAMTAB                              ] )
    self   . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    ##########################################################################
    return True
  ############################################################################
  def subgroupReloadLocality       ( self , DB                             ) :
    ##########################################################################
    if                             ( not self . isGrouping (             ) ) :
      return False
    ##########################################################################
    if                             ( self . isSubordination (            ) ) :
      ########################################################################
      UUID = self . Relation . get ( "first"                                 )
      TYPE = self . Relation . get ( "t1"                                    )
      ########################################################################
    elif                           ( self . isReverse       (            ) ) :
      ########################################################################
      UUID = self . Relation . get ( "second"                                )
      TYPE = self . Relation . get ( "t2"                                    )
      ########################################################################
    else                                                                     :
      return False
    ##########################################################################
    SCOPE  = self . FetchTableKey
    PAMTAB = self . Tables         [ "Parameters"                            ]
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    return
  ############################################################################
  def catalogReloadLocality         ( self , DB                            ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subgroup" , "Reverse"                 ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    ##########################################################################
    if                              ( self . isSubgroup ( )                ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( self . isReverse  ( )                ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    self    . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    return
  ############################################################################
  def catalogUpdateLocalityUsage    ( self                                 ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subgroup" , "Reverse"                 ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return False
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return False
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    DB      . LockWrites            ( [ PAMTAB ]                             )
    ##########################################################################
    if                              ( self . isSubgroup ( )                ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( self . isReverse  ( )                ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    self    . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    DB      . UnlockTables          (                                        )
    DB      . Close                 (                                        )
    ##########################################################################
    return True
  ############################################################################
  def catalogRemoveItems                    ( self , UUIDs                 ) :
    ##########################################################################
    if                                      ( len ( UUIDs ) <= 0           ) :
      return
    ##########################################################################
    if ( ( not self . isSubgroup ( ) ) and ( not self . isReverse ( ) ) )    :
      return
    ##########################################################################
    TITLE  = "RemoveGroupItems"
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
  def defaultAssignIcon            ( self                                  , \
                                     atUuid                                , \
                                     NAME                                  , \
                                     JSON                                  , \
                                     TABLE                                 , \
                                     T1                                    ) :
    ##########################################################################
    UUIDs  = JSON                  [ "UUIDs"                                 ]
    if                             ( len ( UUIDs ) <= 0                    ) :
      return
    ##########################################################################
    PUID   = int                   ( UUIDs [ 0                             ] )
    ##########################################################################
    DB     = self . ConnectHost    ( self . IconDB , True                    )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    RELTAB = self . Tables         [ TABLE                                   ]
    icon   = self . FetchIcon      ( DB , PUID                               )
    DB     . LockWrites            ( [ RELTAB                              ] )
    ##########################################################################
    REL    = Relation              (                                         )
    REL    . set                   ( "first"  , atUuid                       )
    REL    . set                   ( "second" , PUID                         )
    REL    . set                   ( "t1"     , T1                           )
    REL    . setT2                 ( "Picture"                               )
    REL    . setRelation           ( "Using"                                 )
    REL    . Assure                ( DB , RELTAB                             )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    self   . Notify                ( 5                                       )
    ##########################################################################
    if                             ( icon in [ False , None ]              ) :
      return
    ##########################################################################
    if                             ( atUuid not in self . UuidItemMaps     ) :
      return
    ##########################################################################
    item   = self . UuidItemMaps   [ atUuid                                  ]
    self   . emitAssignIcon . emit ( item , icon                             )
    ##########################################################################
    return
  ############################################################################
  def catalogAssignTaggingIcon   ( self , atUuid , NAME , JSON , TABLE     ) :
    ##########################################################################
    T2   = self . Relation . get ( "t2"                                      )
    self . defaultAssignIcon     ( atUuid , NAME , JSON , TABLE , T2         )
    ##########################################################################
    return
  ############################################################################
  def catalogGetUuidIcon         ( self , DB , Uuid , TABLE                ) :
    ##########################################################################
    RELTAB = self . Tables       [ TABLE                                     ]
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , Uuid                            )
    REL    . setT2               ( "Picture"                                 )
    REL    . setRelation         ( "Using"                                   )
    ##########################################################################
    if                           ( self . isTagging ( )                    ) :
      REL  . setT1               ( "Tag"                                     )
    else                                                                     :
      REL  . setT1               ( "Subgroup"                                )
    ##########################################################################
    PICS   = REL . Subordination ( DB , RELTAB                               )
    ##########################################################################
    if                           ( len ( PICS ) > 0                        ) :
      return PICS                [ 0                                         ]
    ##########################################################################
    return 0
  ############################################################################
  def catalogObtainUuidsQuery       ( self                                 ) :
    ##########################################################################
    GID    = self . GTYPE
    TAGTAB = self . Tables          [ "Tags"                                 ]
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"""select `uuid` from {TAGTAB}
                 where ( `used` = 1 )
                   and ( `type` = {GID} )
                 order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def defaultFetchSessionInformation ( self , DB                           ) :
    ##########################################################################
    self   . UuidItemMaps =          {                                       }
    self   . ReloadLocality          ( DB                                    )
    ##########################################################################
    if                               ( self . isOriginal      ( )          ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                               ( self . isSubordination ( )          ) :
      ########################################################################
      UUID   = self . Relation . get ( "first"                               )
      TYPE   = self . Relation . get ( "t1"                                  )
      self   . Tables = self . ObtainsOwnerVariantTables                   ( \
                                       DB                                  , \
                                       str ( UUID )                        , \
                                       int ( TYPE )                        , \
                                       self . FetchTableKey                , \
                                       self . Tables                         )
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                               ( self . isReverse       ( )          ) :
      ########################################################################
      UUID   = self . Relation . get ( "second"                              )
      TYPE   = self . Relation . get ( "t2"                                  )
      self   . Tables = self . ObtainsOwnerVariantTables                   ( \
                                       DB                                  , \
                                       str ( UUID )                        , \
                                       int ( TYPE )                        , \
                                       self . FetchTableKey                , \
                                       self . Tables                         )
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                               ( self . isTagging       ( )          ) :
      ########################################################################
      UUID   = self . Relation . get ( "first"                               )
      TYPE   = self . Relation . get ( "t1"                                  )
      self   . Tables = self . ObtainsOwnerVariantTables                   ( \
                                       DB                                  , \
                                       str ( UUID )                        , \
                                       int ( TYPE )                        , \
                                       self . FetchTableKey                , \
                                       self . Tables                         )
      ########################################################################
      return
    ##########################################################################
    if                               ( self . isSubgroup      ( )          ) :
      ########################################################################
      UUID   = self . Relation . get ( "first"                               )
      TYPE   = self . Relation . get ( "t1"                                  )
      self   . Tables = self . ObtainsOwnerVariantTables                   ( \
                                       DB                                  , \
                                       str ( UUID )                        , \
                                       int ( TYPE )                        , \
                                       self . FetchTableKey                , \
                                       self . Tables                         )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def StopIconMenu  ( self , mm                                            ) :
    ##########################################################################
    if              ( not self . FetchingIcons                             ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    msg = TRX       [ "UI::StopLoadingIcons"                                 ]
    mm  . addAction ( 98643416 , msg                                         )
    ##########################################################################
    return mm
  ############################################################################
  def RunStopIconMenu ( self , at                                          ) :
    ##########################################################################
    if                ( at == 98643416                                     ) :
      ########################################################################
      self . FetchingIcons = False
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def AppendToolNamingAction      ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names-editor.png" )    )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . GotoItemNamesEditor               )
    A    . setEnabled             ( False                                    )
    ##########################################################################
    self . WindowActions . append ( A                                        )
    self . HandleActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def GotoItemNamesEditor        ( self                                    ) :
    ##########################################################################
    atItem = self . currentItem  (                                           )
    if                           ( self . NotOkay ( atItem )               ) :
      return
    ##########################################################################
    self   . OpenItemNamesEditor ( atItem                                    )
    ##########################################################################
    return
  ############################################################################
  def defaultOpenItemNamesEditor ( self , item , scope , name              ) :
    ##########################################################################
    uuid   = item . data         ( Qt . UserRole                             )
    uuid   = int                 ( uuid                                      )
    NAMTAB = self . Tables       [ name                                      ]
    self   . EditAllNames        ( self , scope , uuid , NAMTAB              )
    ##########################################################################
    return
  ############################################################################
  def AtItemNamesEditor          ( self , at , Id , item                   ) :
    ##########################################################################
    if                           ( at == Id                                ) :
      ########################################################################
      self . OpenItemNamesEditor ( item                                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def OpenItemNamesEditor ( self , item                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AssignAccessibleName          ( self                                 ) :
    ##########################################################################
    NAME = self . getSearchLineText (                                        )
    self        . detachSearchTool  (                                        )
    self        . setAccessibleName ( NAME                                   )
    self        . Notify            ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def ConfigureAccessibleName      ( self                                  ) :
    ##########################################################################
    NAME = self . accessibleName   (                                         )
    self . attachSearchToolMessage ( self . AssignAccessibleName           , \
                                     "AccessibleName"                      , \
                                     NAME                                    )
    ##########################################################################
    return
  ############################################################################
  def EmitRelateParameters               ( self                            ) :
    ##########################################################################
    if                                   ( not self . isSubordination (  ) ) :
      return
    ##########################################################################
    UUID = self . Relation  . get        ( "first"                           )
    UUID = str                           ( UUID                              )
    TYPE = self . Relation  . get        ( "t1"                              )
    TYPE = int                           ( TYPE                              )
    RR   = self . Relation  . get        ( "relation"                        )
    RR   = int                           ( RR                                )
    ##########################################################################
    self . emitRelationParameters . emit ( UUID , RR , TYPE                  )
    ##########################################################################
    return
  ############################################################################
  def FontChanged           ( self                                         ) :
    ##########################################################################
    fnt   = self . iconFont (                                                )
    CNT   = 0
    ##########################################################################
    while                   ( CNT < self . count (                       ) ) :
      ########################################################################
      it  = self . item     ( CNT                                            )
      it  . setFont         ( fnt                                            )
      ########################################################################
      CNT = CNT + 1
    ##########################################################################
    return
  ############################################################################
  def ChangeItemFont                   ( self                              ) :
    ##########################################################################
    title        = self . getMenuItem  ( "ChangeItemFont"                    )
    ( ok , fnt ) = QFontDialog.getFont ( self . iconFont ( ) , self , title  )
    if                                 ( not ok                            ) :
      return
    ##########################################################################
    self . setIconFont                 ( fnt                                 )
    self . FontChanged                 (                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenLogHistoryItem         ( self , item                             ) :
    ##########################################################################
    uuid = item . data           ( Qt . UserRole                             )
    uuid = int                   ( uuid                                      )
    ##########################################################################
    if                           ( uuid <= 0                               ) :
      return
    ##########################################################################
    t    = item . text           (                                           )
    nx   = ""
    ##########################################################################
    if                           ( "Notes" in self . Tables                ) :
      nx = self . Tables         [ "Notes"                                   ]
    ##########################################################################
    self . OpenLogHistory . emit ( t                                         ,
                                   str ( uuid )                              ,
                                   "Description"                             ,
                                   nx                                        ,
                                   ""                                        )
    ##########################################################################
    return
  ############################################################################
  def OpenCurrentLogHistory     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenLogHistoryItem ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def doOpenURL                ( self , URL                                ) :
    ##########################################################################
    QDesktopServices . openUrl ( QUrl ( URL                                ) )
    ##########################################################################
    return
  ############################################################################
  def GoOpenURL                  ( self , url                              ) :
    ##########################################################################
    self . emitTryOpenURL . emit (        url                                )
    ##########################################################################
    return
  ############################################################################
  def OpenUrlsByUuids      ( self , DB , TABLE , UUIDs                     ) :
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"select `name` from {TABLE} where ( `uuid` = {UUID} ) ;"
      DB   . Query         ( QQ                                              )
      RR   = DB . FetchOne (                                                 )
      ########################################################################
      if                   ( RR in self . EmptySet                         ) :
        continue
      ########################################################################
      if                   ( 1 != len ( RR )                               ) :
        continue
      ########################################################################
      SS   = RR            [ 0                                               ]
      ########################################################################
      try                                                                    :
        ######################################################################
        SS = SS . decode   ( "utf-8"                                         )
        ######################################################################
        if                 ( len ( SS ) > 0                                ) :
          ####################################################################
          self . GoOpenURL ( SS                                              )
        ######################################################################
      except                                                                 :
        pass
    ##########################################################################
    return
  ############################################################################
  def ToggleSelectFound        ( self , UUIDs , FUIDs                      ) :
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                       ( UUID not in self . UuidItemMaps           ) :
        continue
      ########################################################################
      IT = self . UuidItemMaps [ UUID                                        ]
      IT . setSelected         ( UUID in FUIDs                               )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

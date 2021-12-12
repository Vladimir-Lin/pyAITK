# -*- coding: utf-8 -*-
##############################################################################
## GalleryGroupView
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . IconDock          import IconDock    as IconDock
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
##############################################################################
class GalleryGroupView             ( IconDock                              ) :
  ############################################################################
  HavingMenu      = 1371434312
  ############################################################################
  GallerySubgroup = pyqtSignal     ( str , int , str                         )
  GalleryGroup    = pyqtSignal     ( str , int , str                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . GTYPE        = 64
    self . SortOrder    = "asc"
    self . PrivateIcon  = True
    self . PrivateGroup = True
    self . ExtraINFOs   = True
    self . dockingPlace = Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation     = Relation (                                         )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . Grouping     = "Tag"
    self . OldGrouping  = "Tag"
    ## self . Grouping     = "Catalog"
    ## self . Grouping     = "Subgroup"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . setFunction             ( self . HavingMenu , True                )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def setGrouping ( self , group                                           ) :
    self . Grouping = group
    return self . Grouping
  ############################################################################
  def getGrouping ( self                                                   ) :
    return self . Grouping
  ############################################################################
  def isGrouping              ( self , tag                                 ) :
    return                    ( self . Grouping == tag                       )
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
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup      , False      )
    self . LinkAction      ( "Insert"     , self . InsertItem   , False      )
    self . LinkAction      ( "Delete"     , self . DeleteItems  , False      )
    self . LinkAction      ( "Rename"     , self . RenameItem   , False      )
    self . LinkAction      ( "SelectAll"  , self . SelectAll    , False      )
    self . LinkAction      ( "SelectNone" , self . SelectNone   , False      )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked ( self , item                                          ) :
    ##########################################################################
    self . Notify   ( 0                                                      )
    ##########################################################################
    return True
  ############################################################################
  def doubleClicked                ( self , item                           ) :
    ##########################################################################
    uuid  = item . data            ( Qt . UserRole                           )
    uuid  = int                    ( uuid                                    )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      return False
    ##########################################################################
    title = item . text            (                                         )
    tid   = self . Relation . get  ( "t2"                                    )
    self  . GallerySubgroup . emit ( title , tid , str ( uuid )              )
    ##########################################################################
    return True
  ############################################################################
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
    RELTAB = self . Tables       [ "RelationPictures"                        ]
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
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    GID    = self . GTYPE
    TAGTAB = self . Tables [ "Tags"                                          ]
    ORDER  = self . getSortingOrder        (                                 )
    QQ     = f"""select `uuid` from {TAGTAB}
                 where ( `used` = 1 )
                   and ( `type` = {GID} )
                 order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def ObtainSubgroupUuids                  ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `position` {ORDER}"
    RELTAB = self . Tables                 [ "Relation"                      ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isTagging ( )         ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "gallerygroup/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , mtype , message                    )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    if                  ( self . isTagging ( )                             ) :
      return
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    if                        ( self . isTagging ( )                       ) :
      ########################################################################
      formats = "picture/uuids;gallerygroup/uuids;"
      ########################################################################
    else                                                                     :
      ########################################################################
      formats = "picture/uuids;gallery/uuids;gallerygroup/uuids;"
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
    elif                            ( mtype in [ "gallery/uuids"         ] ) :
      ########################################################################
      if                            ( self . isTagging ( )                 ) :
        return False
      ########################################################################
      if                            ( atItem in [ False , None ]           ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus  ( "JoinGalleries"  , title , CNT      )
    ##########################################################################
    elif                            ( mtype in [ "gallerygroup/uuids"    ] ) :
      ########################################################################
      if                            ( self == sourceWidget                 ) :
        self . ShowMenuItemCountStatus ( "MoveCatalogues" , CNT              )
      else                                                                   :
        self . ShowMenuItemCountStatus ( "JoinCatalogues" , CNT              )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptGalleryGroupsDrop  ( self                                      ) :
    return True
  ############################################################################
  def acceptGalleriesDrop      ( self                                      ) :
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropGalleryGroups             ( self , source , pos , JSON           ) :
    MF   = self . GalleryGroupsMoving
    AF   = self . GalleryGroupsAppending
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def dropGalleries                     ( self , source , pos , JSON       ) :
    FUNC = self . GalleriesAppending
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def dropPictures                      ( self , source , pos , JSON       ) :
    FUNC = self . AssignTaggingIcon
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def GetLastestPosition                      ( self , DB , LUID           ) :
    ##########################################################################
    RELTAB = "RelationPeople"
    ##########################################################################
    if                                        ( self . isReverse ( )       ) :
      return self . GetReverseLastestPosition ( DB , RELTAB , LUID           )
    return   self . GetNormalLastestPosition  ( DB , RELTAB , LUID           )
  ############################################################################
  def GenerateMovingSQL                   ( self   , LAST , UUIDs          ) :
    ##########################################################################
    RELTAB = "RelationPeople"
    R      = self . isReverse             (                                  )
    ##########################################################################
    return self . GenerateNormalMovingSQL ( RELTAB , LAST , UUIDs , R        )
  ############################################################################
  def GalleryGroupsMoving     ( self , atUuid , NAME , JSON                ) :
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
    RELTAB = self . Tables    [ "RelationPeople"                             ]
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
  def GalleryGroupsAppending   ( self , atUuid , NAME , JSON               ) :
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
    RELTAB = self . Tables     [ "RelationPeople"                            ]
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
  def GalleriesAppending        ( self , atUuid , NAME , JSON              ) :
    ##########################################################################
    UUIDs  = JSON               [ "UUIDs"                                    ]
    if                          ( len ( UUIDs ) <= 0                       ) :
      return False
    ##########################################################################
    DB     = self . ConnectHost ( self . GroupDB , True                      )
    if                          ( DB == None                               ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationPeople"                           ]
    GALM   = GalleryItem        (                                            )
    T1     = "Subgroup"
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    GALM   . ConnectToGalleries ( DB , RELTAB , atUuid , T1 , UUIDs          )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    ##########################################################################
    self   . Notify             ( 5                                          )
    ##########################################################################
    return True
  ############################################################################
  def AssignTaggingIcon            ( self , atUuid , NAME , JSON           ) :
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
    RELTAB = self . Tables         [ "RelationPictures"                      ]
    icon   = self . FetchIcon      ( DB , PUID                               )
    DB     . LockWrites            ( [ RELTAB                              ] )
    ##########################################################################
    T2     = self . Relation . get ( "t2"                                    )
    REL    = Relation              (                                         )
    REL    . set                   ( "first"  , atUuid                       )
    REL    . set                   ( "second" , PUID                         )
    REL    . set                   ( "t1"     , T2                           )
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
  def RemoveItems                           ( self , UUIDs                 ) :
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
  def UpdateItemName             ( self           , item , uuid , name     ) :
    ##########################################################################
    self . UpdateItemNameByTable ( "NamesEditing" , item , uuid , name       )
    ##########################################################################
    return
  ############################################################################
  def AppendTagItem                 ( self , DB                            ) :
    ##########################################################################
    TAGTAB = self . Tables          [ "Tags"                                 ]
    uuid   = DB   . LastUuid        ( TAGTAB , "uuid" , 2800000000000000000  )
    DB     . AddUuid                ( TAGTAB ,  uuid  , self . GTYPE         )
    ##########################################################################
    return uuid
  ############################################################################
  def AppendSubgroupItem            ( self , DB                            ) :
    ##########################################################################
    SUBTAB = self . Tables          [ "Subgroups"                            ]
    uuid   = DB   . LastUuid        ( SUBTAB , "uuid" , 2800004000000000000  )
    DB     . AddUuid                ( SUBTAB ,  uuid  , self . GTYPE         )
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
    NAMTAB   = self . Tables             [ "Names"                           ]
    RELTAB   = self . Tables             [ "RelationPeople"                  ]
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
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isTagging ( )                   ) :
      return
    ##########################################################################
    self . defaultDeleteItems (                                              )
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
    GFMT       = self . getMenuItem    ( "GalleriesCount"                    )
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
      if                               ( not self . LoopRunning            ) :
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
      REL      . setT2                 ( "Gallery"                           )
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
  def Menu                           ( self , pos                          ) :
    ##########################################################################
    if                               ( not self . isPrepared ( )           ) :
      return False
    ##########################################################################
    doMenu  = self . isFunction      ( self . HavingMenu                     )
    if                               ( not doMenu                          ) :
      return False
    ##########################################################################
    self   . Notify                  ( 0                                     )
    ##########################################################################
    items   = self . selectedItems   (                                       )
    atItem  = self . itemAt          ( pos                                   )
    uuid    = 0
    ##########################################################################
    if                               ( atItem != None                      ) :
      uuid  = atItem . data          ( Qt . UserRole                         )
      uuid  = int                    ( uuid                                  )
    ##########################################################################
    mm      = MenuManager            ( self                                  )
    ##########################################################################
    TRX     = self . Translations
    ##########################################################################
    if                               ( uuid > 0                            ) :
      ########################################################################
      msg   = self . getMenuItem     ( "Subgroup"                            )
      mm    . addAction              ( 2001 , msg                            )
      ########################################################################
      if                             ( self . Grouping == "Subgroup"       ) :
        ######################################################################
        msg = self . getMenuItem     ( "Galleries"                           )
        mm  . addAction              ( 2002 , msg                            )
        ######################################################################
      mm    . addSeparator           (                                       )
    ##########################################################################
    mm      = self . AppendRefreshAction ( mm , 1001                         )
    mm      = self . AppendInsertAction  ( mm , 1101                         )
    ##########################################################################
    if                               ( atItem not in [ False , None ]      ) :
      mm    = self . AppendRenameAction  ( mm , 1102                         )
    ##########################################################################
    mm      . addSeparator           (                                       )
    ##########################################################################
    if                               ( atItem not in [ False , None ]      ) :
      if                             ( self . EditAllNames != None         ) :
        mm  . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]       )
        mm  . addSeparator           (                                       )
    ##########################################################################
    mm      = self . SortingMenu     ( mm                                    )
    mm      = self . LocalityMenu    ( mm                                    )
    self    . DockingMenu            ( mm                                    )
    ##########################################################################
    mm      . setFont                ( self    . menuFont ( )                )
    aa      = mm . exec_             ( QCursor . pos      ( )                )
    at      = mm . at                ( aa                                    )
    ##########################################################################
    if                               ( self . RunDocking   ( mm , aa )     ) :
      return True
    ##########################################################################
    if                               ( self . HandleLocalityMenu ( at )    ) :
      ########################################################################
      self  . clear                  (                                       )
      self  . startup                (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( self . RunSortingMenu     ( at )    ) :
      ########################################################################
      self  . clear                  (                                       )
      self  . startup                (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 1001                          ) :
      ########################################################################
      self  . clear                  (                                       )
      self  . startup                (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 1101                          ) :
      self  . InsertItem             (                                       )
      return True
    ##########################################################################
    if                               ( at == 1102                          ) :
      self . RenameItem              (                                       )
      return True
    ##########################################################################
    if                               ( at == 1601                          ) :
      ########################################################################
      NAM   = self . Tables          [ "Names"                               ]
      self  . EditAllNames           ( self , "Gallery" , uuid , NAM         )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 2001                          ) :
      ########################################################################
      title = atItem . text          (                                       )
      tid   = self . Relation . get  ( "t2"                                  )
      self  . GallerySubgroup . emit ( title , tid , str ( uuid )            )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 2002                          ) :
      ########################################################################
      title = atItem . text          (                                       )
      tid   = self . Relation . get  ( "t2"                                  )
      self  . GalleryGroup    . emit ( title , tid , str ( uuid )            )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

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
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QMouseEvent
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
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
from   AITK  . Essentials . Relation  import Relation    as Relation
from   AITK  . Calendars  . StarDate  import StarDate    as StarDate
from   AITK  . Calendars  . Periode   import Periode     as Periode
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
from   AITK  . People     . People    import People      as PeopleItem
##############################################################################
class PeopleView                   ( IconDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  ShowPersonalGallery = pyqtSignal ( str , int , str ,       QIcon           )
  ShowGalleries       = pyqtSignal ( str , int , str ,       QIcon           )
  ShowWebPages        = pyqtSignal ( str , int , str , str , QIcon           )
  OwnedOccupation     = pyqtSignal ( str , int , str , str , QIcon           )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  emitOpenSmartNote   = pyqtSignal ( str                                     )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
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
    self . dockingPlace       = Qt . BottomDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "People"                                )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
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
  def GetUuidIcon                    ( self , DB , UUID                    ) :
    ##########################################################################
    RELTAB = self . Tables           [ "Relation"                            ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "People" , UUID         )
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
    if                         ( self . Grouping == "Subordination"        ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                         ( self . Grouping == "Reverse"              ) :
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
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label"      , self . windowTitle ( )         )
    self . LinkAction        ( "Refresh"    , self . startup                 )
    ##########################################################################
    self . LinkAction        ( "Insert"     , self . InsertItem              )
    self . LinkAction        ( "Rename"     , self . RenamePeople            )
    self . LinkAction        ( "Delete"     , self . DeleteItems             )
    self . LinkAction        ( "Cut"        , self . DeleteItems             )
    self . LinkAction        ( "Copy"       , self . CopyItems               )
    self . LinkAction        ( "Paste"      , self . PasteItems              )
    self . LinkAction        ( "Search"     , self . Search                  )
    self . LinkAction        ( "Home"       , self . PageHome                )
    self . LinkAction        ( "End"        , self . PageEnd                 )
    self . LinkAction        ( "PageUp"     , self . PageUp                  )
    self . LinkAction        ( "PageDown"   , self . PageDown                )
    ##########################################################################
    self . LinkAction        ( "SelectAll"  , self . SelectAll               )
    self . LinkAction        ( "SelectNone" , self . SelectNone              )
    ##########################################################################
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . LinkAction        ( "Refresh"    , self . startup      , False    )
    self . LinkAction        ( "Insert"     , self . InsertItem   , False    )
    self . LinkAction        ( "Rename"     , self . RenamePeople , False    )
    self . LinkAction        ( "Delete"     , self . DeleteItems  , False    )
    self . LinkAction        ( "Cut"        , self . DeleteItems  , False    )
    self . LinkAction        ( "Copy"       , self . CopyItems    , False    )
    self . LinkAction        ( "Paste"      , self . PasteItems   , False    )
    self . LinkAction        ( "Search"     , self . Search       , False    )
    self . LinkAction        ( "Home"       , self . PageHome     , False    )
    self . LinkAction        ( "End"        , self . PageEnd      , False    )
    self . LinkAction        ( "PageUp"     , self . PageUp       , False    )
    self . LinkAction        ( "PageDown"   , self . PageDown     , False    )
    self . LinkAction        ( "SelectAll"  , self . SelectAll    , False    )
    self . LinkAction        ( "SelectNone" , self . SelectNone   , False    )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . defaultCloseEvent ( event                                         )
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
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    formats = "people/uuids;picture/uuids"
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
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
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
    return RDN
  ############################################################################
  def dropMoving           ( self , sourceWidget , mimeData , mousePos     ) :
    ##########################################################################
    if                     ( self . droppingAction                         ) :
      return False
    ##########################################################################
    if                     ( sourceWidget != self                          ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( mousePos                                        )
    if                     ( atItem in [ False , None ]                    ) :
      return False
    if                     ( atItem . isSelected ( )                       ) :
      return False
    ##########################################################################
    return True
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
    if                             ( PUID <= 0                             ) :
      return True
    ##########################################################################
    self . Go ( self . PicturesAppending , ( PUID , NAME , JSON , )          )
    ##########################################################################
    return True
  ############################################################################
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationPeople" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationPeople" , LAST , UUIDs   )
  ############################################################################
  def PeopleMoving            ( self , atUuid , NAME , JSON                ) :
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
    self   . ExecuteSqlCommands ( "OrganizePeople" , DB , SQLs , 100         )
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
    self   . ExecuteSqlCommands ( "OrganizePeople" , DB , SQLs , 100         )
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
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "People" , "Names"                        )
    ##########################################################################
    return
  ############################################################################
  def CopyItems                    ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
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
    if                                   ( DB == None                      ) :
      return
    ##########################################################################
    uuid     = item . data               ( Qt . UserRole                     )
    uuid     = int                       ( uuid                              )
    ##########################################################################
    PHID     = 1400000000000000000
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
                 order by `name` asc ;"""
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
      if                           ( N == NAME                             ) :
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
  def UpdateLocalityUsage          ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
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
    SCOPE  = f"PeopleView-{SCOPE}"
    self   . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
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
    SCOPE  = f"PeopleView-{SCOPE}"
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
  def GroupsMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( item . text ( )                             )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "Occupations"                               )
    mm  . addActionFromMenu    ( LOM , 1201 , MSG                            )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "PersonalGallery"                           )
    mm  . addActionFromMenu    ( LOM , 1211 , MSG                            )
    ##########################################################################
    MSG = self . getMenuItem   ( "Galleries"                                 )
    mm  . addActionFromMenu    ( LOM , 1212 , MSG                            )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "WebPages"                                  )
    mm  . addActionFromMenu    ( LOM , 1221 , MSG                            )
    ##########################################################################
    MSG = self . getMenuItem   ( "IdentWebPage"                              )
    mm  . addActionFromMenu    ( LOM , 1222 , MSG                            )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                     ( self , at , uuid , item          ) :
    ##########################################################################
    if                                  ( at == 1201                       ) :
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
    if                                  ( at == 1211                       ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowPersonalGallery . emit ( text , 7 , xsid , icon             )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1212                       ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowGalleries       . emit ( text , 7 , xsid , icon             )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1221                       ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      rela = "Subordination"
      ########################################################################
      self . ShowWebPages        . emit ( text , 7 , xsid , rela , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1222                       ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      rela = "Equivalent"
      ########################################################################
      self . ShowWebPages        . emit ( text , 7 , xsid , rela , icon      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items  = self . selectedItems  (                                         )
    atItem = self . itemAt         ( pos                                     )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( Qt . UserRole                           )
      uuid = int                   ( uuid                                    )
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
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    msg    = self . getMenuItem    ( "Search"                                )
    mm     . addAction             ( 1103 , msg                              )
    ##########################################################################
    mm     = self . AppendRenameAction  ( mm , 1102                          )
    ##########################################################################
    msg    = self . getMenuItem    ( "AllNames"                              )
    mm     . addAction             ( 1401 , msg                              )
    ##########################################################################
    mm     . addAction             ( 1451 , "搜尋同名人物" )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      ########################################################################
      msg  = self . getMenuItem    ( "AssignTables"                          )
      mm   . addAction             ( 1301 , msg                              )
    ##########################################################################
    if                             ( atItem != None                        ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    if                             ( uuid > 0                              ) :
      self . GroupsMenu            ( mm , uuid , atItem                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunAmountIndexMenu ( )         ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if ( self . RunGroupsMenu ( at , uuid , atItem ) )                       :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      ########################################################################
      self . InsertItem            (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      ########################################################################
      self . RenamePeople          (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . Search                (                                         )
      return True
    ##########################################################################
    if                             ( at == 1301                            ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      UUID  = self . Relation  . get   ( "first"                             )
      TYPE  = self . Relation  . get   ( "t1"                                )
      TYPE  = int                      ( TYPE                                )
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         str ( UUID  )                     , \
                                         TYPE                              , \
                                         "Tables"                          , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1401                            ) :
      self . ListAllNames          (                                         )
      return True
    ##########################################################################
    if                             ( at == 1451                            ) :
      self . Go ( self . SearchForSameNames )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "People" , uuid , NAM            )
      return True
    ##########################################################################
    if                             ( at == 7401                            ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

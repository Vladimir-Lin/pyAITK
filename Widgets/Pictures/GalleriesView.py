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
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
##############################################################################
class GalleriesView                ( IconDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  ShowPersonalGallery = pyqtSignal ( str , int , str , QIcon                 )
  ViewFullGallery     = pyqtSignal ( str , int , str , int , QIcon           )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total        =  0
    self . StartId      =  0
    self . Amount       = 60
    self . SortOrder    = "asc"
    self . SortByName   = False
    ##########################################################################
    self . Grouping     = "Original"
    self . OldGrouping  = "Original"
    ## self . Grouping     = "Subordination"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Gallery"                               )
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
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
    RELTAB = self . Tables       [ "Relation"                                ]
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , Uuid                            )
    REL    . setT1               ( "Gallery"                                 )
    REL    . setT2               ( "Picture"                                 )
    REL    . setRelation         ( "Using"                                   )
    ##########################################################################
    PICS   = REL . Subordination ( DB , RELTAB                               )
    ##########################################################################
    if                           ( len ( PICS ) > 0                        ) :
      return PICS                [ 0                                         ]
    ##########################################################################
    return 0
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    GALTAB = self . Tables   [ "Galleries"                                   ]
    QQ     = f"select count(*) from {GALTAB} where ( `used` = 1 ) ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                             ]
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
    GALTAB = self . Tables          [ "Galleries"                            ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"""select `uuid` from {GALTAB}
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
    NAMTAB = self . Tables     [ "Names"                                     ]
    ##########################################################################
    if                         ( self . isSubordination ( )                ) :
      ########################################################################
      if                       ( self . SortByName                         ) :
        ######################################################################
        LC = self . getLocality          (                                   )
        WS = self . Relation . FirstItem (                                   )
        QS = f"select `second` from {RELTAB} {WS}"
        QQ = f"""select distinct(`uuid`) from {NAMTAB}
                 where ( `uuid` in ( {QS} ) )
                   and ( `locality` = {LC} )
                 order by `name` {ORDER} {LMTS} ;"""
        QQ = " " . join         ( QQ . split ( )                             )
        ######################################################################
        return DB . ObtainUuids ( QQ                                         )
        ######################################################################
      else                                                                   :
        ######################################################################
        OPTS = f"order by `position` {ORDER}"
        return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS   )
      ########################################################################
    if                         ( self . isReverse       ( )                ) :
      ########################################################################
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      UUID   = self . Relation . get  ( "first"                              )
      TYPE   = self . Relation . get  ( "t1"                                 )
      self   . Tables = self . ObtainsOwnerVariantTables                   ( \
                                          DB                               , \
                                          str ( UUID )                     , \
                                          int ( TYPE )                     , \
                                          "Tables"                         , \
                                          self . Tables                      )
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
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
    self . LinkAction     ( "Home"       , self . PageHome                   )
    self . LinkAction     ( "End"        , self . PageEnd                    )
    self . LinkAction     ( "PageUp"     , self . PageUp                     )
    self . LinkAction     ( "PageDown"   , self . PageDown                   )
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
    self . LinkAction      ( "Home"       , self . PageHome     , False      )
    self . LinkAction      ( "End"        , self . PageEnd      , False      )
    self . LinkAction      ( "PageUp"     , self . PageUp       , False      )
    self . LinkAction      ( "PageDown"   , self . PageDown     , False      )
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
    self . ShowPersonalGallery . emit ( text , 64 , xsid , icon              )
    ##########################################################################
    return True
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
    FMTs    =              [ "people/uuids"                                , \
                             "gallery/uuids"                               , \
                             "picture/uuids"                                 ]
    formats = ";" . join   ( FMTs                                            )
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
    CNT     = len                   ( UUIDs                                  )
    title   = sourceWidget . windowTitle (                                   )
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      if                            ( atItem in [ False , None ]           ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus ( "JoinPeople"   , title , CNT         )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      if                            ( atItem in [ False , None ]           ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus ( "JoinPictures" , title , CNT         )
    ##########################################################################
    elif                            ( mtype in [ "gallery/uuids" ]         ) :
      ########################################################################
      if                            ( self == sourceWidget                 ) :
        self . ShowMenuItemCountStatus ( "MoveGalleries" , CNT               )
      else                                                                   :
        self . ShowMenuItemCountStatus ( "JoinGalleries" , CNT               )
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
    MF   = self . GalleriesMoving
    AF   = self . GalleriesAppending
    return self . defaultDropInside (        source , pos , JSON , MF , AF   )
  ############################################################################
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationPeople" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationPeople" , LAST , UUIDs   )
  ############################################################################
  def GalleriesMoving         ( self , atUuid , NAME , JSON                ) :
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
  def GalleriesAppending       ( self , atUuid , NAME , JSON               ) :
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
  def PropertiesMenu           ( self , mm                                 ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "Properties"                                )
    COL   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    if                         ( self . isSubordination ( )                ) :
      ########################################################################
      msg = self . getMenuItem ( "AssignTables"                              )
      mm  . addActionFromMenu  ( COL , 1301 , msg                            )
    ##########################################################################
    msg   = self . getMenuItem ( "SortByName"                                )
    mm    . addActionFromMenu  ( COL , 1302 , msg , True , self . SortByName )
    ##########################################################################
    return mm
  ############################################################################
  def RunPropertiesMenu ( self , at                                        ) :
    ##########################################################################
    if                  ( at == 1301                                       ) :
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
    if                  ( at == 1302                                       ) :
      ########################################################################
      if                ( self . SortByName                                ) :
        self . SortByName = False
      else                                                                   :
        self . SortByName = True
      ########################################################################
      self   . clear    (                                                    )
      self   . startup  (                                                    )
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    if                              ( not self . isPrepared ( )            ) :
      return False
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . itemAt          ( pos                                    )
    uuid   = 0
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      uuid = atItem . data          ( Qt . UserRole                          )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      mm   = self . AppendRenameAction  ( mm , 1102                          )
    ##########################################################################
    if                              ( uuid > 0                             ) :
      ########################################################################
      mm   . addSeparator           (                                        )
      ########################################################################
      mm   . addAction              ( 1201 , TRX [ "UI::PersonalGallery"   ] )
      ########################################################################
      msg  = self . getMenuItem     ( "ViewFullPictures"                     )
      mm   . addAction              ( 1202 , msg                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    if                              ( atItem not in [ False , None ]       ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
        mm . addSeparator           (                                        )
    ##########################################################################
    mm     = self . PropertiesMenu  ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunAmountIndexMenu ( )        ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunDocking    ( mm , aa )     ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunPropertiesMenu  ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      self . RenameItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1201                           ) :
      ########################################################################
      text = atItem . text          (                                        )
      icon = atItem . icon          (                                        )
      xsid = str                    ( uuid                                   )
      ########################################################################
      self . ShowPersonalGallery . emit ( text , 64 , xsid , icon            )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1202                           ) :
      ########################################################################
      text = atItem . text          (                                        )
      icon = atItem . icon          (                                        )
      xsid = str                    ( uuid                                   )
      ########################################################################
      self . ViewFullGallery . emit ( text , 64 , xsid , 1 , icon            )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "Gallery" , uuid , NAM          )
      return True
    ##########################################################################
    return True
##############################################################################

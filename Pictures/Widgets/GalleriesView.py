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
from   PyQt5 . QtWidgets              import QFileDialog
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
  ShowWebPages        = pyqtSignal ( str , int , str , str , QIcon           )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  emitOpenSmartNote   = pyqtSignal ( str                                     )
  OpenLogHistory      = pyqtSignal ( str , str , str , str , str             )
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
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::PersonalGallery"                    ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/pictures.png" )        )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenCurrentGallery                )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ##########################################################################
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
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
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent (        event                                  )
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
  def UpdateLocalityUsage           ( self                                 ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subordination" , "Reverse"            ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return False
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return False
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    DB      . LockWrites            ( [ PAMTAB ]                             )
    ##########################################################################
    if                              ( SCOPE == "Subordination"             ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( SCOPE == "Reverse"                   ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    SCOPE   = f"GalleriesView-{SCOPE}"
    self    . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    DB      . UnlockTables          (                                        )
    DB      . Close                 (                                        )
    ##########################################################################
    return True
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
  def ReloadLocality                ( self , DB                            ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subordination" , "Reverse"            ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    ##########################################################################
    if                              ( SCOPE == "Subordination"             ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( SCOPE == "Reverse"                   ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    SCOPE   = f"GalleriesView-{SCOPE}"
    self    . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
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
    self . ShowPersonalGallery . emit ( text , 64 , xsid , icon              )
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
  def BlocMenu               ( self , mm , item                            ) :
    ##########################################################################
    MSG = self . getMenuItem ( "Bloc"                                        )
    LOM = mm   . addMenu     ( MSG                                           )
    ##########################################################################
    MSG = self . getMenuItem ( "ExportUUIDs"                                 )
    mm  . addActionFromMenu  ( LOM , 8831001 , MSG                           )
    ##########################################################################
    return mm
  ############################################################################
  def RunBlocMenu ( self , at , item                                       ) :
    ##########################################################################
    if            ( at == 8831001                                          ) :
      ########################################################################
      self . Go   ( self . ExportUUIDs                                       )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PropertiesMenu             ( self , mm , item                        ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Properties"                              )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      mm  . addActionFromMenu    ( COL , 1301 , msg                          )
    ##########################################################################
    msg   = self . getMenuItem   ( "SortByName"                              )
    mm    . addActionFromMenu    ( COL                                     , \
                                   1302                                    , \
                                   msg                                     , \
                                   True                                    , \
                                   self . SortByName                         )
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
    MSG   = self . getMenuItem   ( "GalleryDescription"                      )
    mm    . addActionFromMenu    ( COL , 62231331 , MSG                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunPropertiesMenu            ( self , at , item                      ) :
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
                                         self . FetchTableKey              , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1302                            ) :
      ########################################################################
      if                           ( self . SortByName                     ) :
        self . SortByName = False
      else                                                                   :
        self . SortByName = True
      ########################################################################
      self   . clear               (                                         )
      self   . startup             (                                         )
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
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu           ( mm                                     )
    self   . AmountIndexMenu        ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    self   . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( uuid > 0                             ) :
      ########################################################################
      mm   . addSeparator           (                                        )
      ########################################################################
      self . AppendRenameAction     ( mm , 1102                              )
      self . AssureEditNamesAction  ( mm , 1601 , atItem                     )
      ########################################################################
      mm   . addSeparator           (                                        )
      ########################################################################
      msg  = TRX                    [ "UI::PersonalGallery"                  ]
      icon = QIcon                  ( ":/images/pictures.png"                )
      mm   . addActionWithIcon      ( 1201 , icon , msg                      )
      ########################################################################
      msg  = self . getMenuItem     ( "ViewFullPictures"                     )
      mm   . addAction              ( 1202 , msg                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . BlocMenu               ( mm , atItem                            )
    self   . PropertiesMenu         ( mm , atItem                            )
    self   . SortingMenu            ( mm                                     )
    self   . LocalityMenu           ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking      ( mm , aa                                )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunBlocMenu     ( at , atItem                            )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunPropertiesMenu ( at , atItem                          )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . restart                (                                        )
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
      self . OpenItemGallery        ( atItem                                 )
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

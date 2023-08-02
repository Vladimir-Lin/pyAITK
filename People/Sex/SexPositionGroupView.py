# -*- coding: utf-8 -*-
##############################################################################
## SexPositionGroupView
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
from   AITK  . People     . People    import People
##############################################################################
class SexPositionGroupView         ( IconDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  SexPositionSubgroup = pyqtSignal ( str , int , str                         )
  SexPositionGroup    = pyqtSignal ( str , int , str , str , QIcon           )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  OpenLogHistory      = pyqtSignal ( str , str , str , str , str             )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . GTYPE        = 210
    self . SortOrder    = "asc"
    self . PrivateIcon  = True
    self . PrivateGroup = True
    self . ExtraINFOs   = True
    self . dockingPlace = Qt . RightDockWidgetArea
    ##########################################################################
    self . Grouping     = "Tag"
    self . OldGrouping  = "Tag"
    ## self . Grouping = "Catalog"
    ## self . Grouping = "Subgroup"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . FetchTableKey = "SexPositionGroupView"
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . set         ( "first" , 0                              )
    self . Relation . set         ( "t1"    , 75                             )
    self . Relation . set         ( "t2"    , 158                            )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . MountClicked           ( 1                                        )
    self . MountClicked           ( 2                                        )
    ##########################################################################
    self . setFunction            ( self . HavingMenu      , True            )
    ##########################################################################
    self . setDragEnabled         ( False                                    )
    self . setAcceptDrops         ( True                                     )
    self . setDragDropMode        ( QAbstractItemView . DropOnly             )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    if ( self . isSubgroup ( ) or self . isReverse ( )                     ) :
      ########################################################################
      msg  = self . getMenuItem     ( "SIG"                                  )
      A    = QAction                (                                        )
      A    . setIcon                ( QIcon ( ":/images/lists.png" )         )
      A    . setToolTip             ( msg                                    )
      A    . triggered . connect    ( self . OpenSexPositionGroup            )
      self . WindowActions . append ( A                                      )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ##########################################################################
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
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
  def GetUuidIcon                    ( self , DB , Uuid                    ) :
    TABLE = "RelationPictures"
    return self . catalogGetUuidIcon (        DB , Uuid , TABLE              )
  ############################################################################
  def singleClicked ( self , item                                          ) :
    ##########################################################################
    self . Notify   ( 0                                                      )
    ##########################################################################
    return True
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
    RELTAB = self . Tables                 [ "RelationEditing"               ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainReverseUuids                   ( self , DB                     ) :
    ##########################################################################
    ORDER  = self . getSortingOrder        (                                 )
    OPTS   = f"order by `reverse` {ORDER}"
    RELTAB = self . Tables                 [ "RelationEditing"               ]
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
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    if                        ( self . isTagging ( )                       ) :
      return False
    else                                                                     :
      ########################################################################
      formats = "sexposition/uuids"
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
    if                              ( mtype in [ "sexposition/uuids" ]     ) :
      ########################################################################
      if                            ( self . isTagging ( )                 ) :
        return False
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
    if                                ( mtype in [ "sexposition/uuids"   ] ) :
      ########################################################################
      if                              ( self . isTagging ( )               ) :
        return False
      ########################################################################
      if                              ( self . NotOkay ( atItem )          ) :
        return False
      ########################################################################
      self  . ShowMenuItemTitleStatus ( "JoinSexPosition" , title , CNT      )
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
  def acceptSexPositionsDrop ( self                                        ) :
    return True
  ############################################################################
  def dropSexPositions                  ( self , source , pos , JSON       ) :
    FUNC = self . SexPositionAppending
    return self . defaultDropInFunction (        source , pos , JSON , FUNC  )
  ############################################################################
  def SexPositionAppending ( self , atUuid , NAME , JSON                   ) :
    ##########################################################################
    T1   = "Subgroup"
    TAB  = "RelationEditing"
    ##########################################################################
    OK   = self . AppendingSexPositionIntoT1 ( atUuid                      , \
                                               NAME                        , \
                                               JSON                        , \
                                               TAB                         , \
                                               T1                            )
    if                      ( not OK                                       ) :
      return
    ##########################################################################
    self . loading          (                                                )
    ##########################################################################
    return
  ############################################################################
  def AppendingSexPositionIntoT1 ( self                                    , \
                                   atUuid                                  , \
                                   NAME                                    , \
                                   JSON                                    , \
                                   table                                   , \
                                   T1                                      ) :
    ##########################################################################
    UUIDs  = JSON                [ "UUIDs"                                   ]
    if                           ( len ( UUIDs ) <= 0                      ) :
      return False
    ##########################################################################
    if                           ( self . PrivateGroup                     ) :
      DB   = self . ConnectHost  ( self . GroupDB                            )
    else                                                                     :
      DB   = self . ConnectDB    (                                           )
    if                           ( DB == None                              ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit      (                                           )
    self   . setBustle           (                                           )
    ##########################################################################
    RELTAB = self . Tables       [ table                                     ]
    ##########################################################################
    DB     . LockWrites          ( [ RELTAB                                ] )
    ##########################################################################
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , atUuid                          )
    REL    . setT1               ( T1                                        )
    REL    . setT2               ( "SexPosition"                             )
    REL    . setRelation         ( "Subordination"                           )
    REL    . Joins               ( DB , RELTAB , UUIDs                       )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    self   . setVacancy          (                                           )
    self   . GoRelax . emit      (                                           )
    DB     . Close               (                                           )
    ##########################################################################
    self   . Notify              ( 5                                         )
    ##########################################################################
    return True
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
  @pyqtSlot                        (                                         )
  def PasteItems                   ( self                                  ) :
    ##########################################################################
    print("PasteItems")
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
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
    RELTAB   = self . Tables             [ "RelationEditing"                 ]
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
    GFMT       = self . getMenuItem    ( "SexPositionCount"                  )
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
    RELTAB     = self . Tables         [ "RelationEditing"                   ]
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
      REL      . setT2                 ( "SexPosition"                       )
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
  def FetchSessionInformation    ( self , DB                               ) :
    ##########################################################################
    self . catalogReloadLocality (        DB                                 )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage             ( self                               ) :
    return catalogUpdateLocalityUsage (                                      )
  ############################################################################
  def FunctionsMenu          ( self , mm , uuid , item                     ) :
    ##########################################################################
    msg = self . getMenuItem ( "Functions"                                   )
    LOM = mm   . addMenu     ( msg                                           )
    ##########################################################################
    msg = self . getMenuItem ( "AssignTables"                                )
    mm  . addActionFromMenu  ( LOM , 25351301 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "Description"                                 )
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
      uuid = int                       ( uuid                                )
      head = item . text               (                                     )
      nx   = ""
      ########################################################################
      if                               ( "Notes" in self . Tables          ) :
        nx = self . Tables             [ "Notes"                             ]
      ########################################################################
      self . OpenLogHistory . emit     ( head                                ,
                                         str ( uuid )                        ,
                                         "Description"                       ,
                                         nx                                  ,
                                         str ( self . getLocality ( ) )      )
    ##########################################################################
    return False
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    if                                ( not self . isPrepared ( )          ) :
      return False
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                    )
    if                                ( not doMenu                         ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu             ( mm                                   )
    ##########################################################################
    if                                ( uuid > 0                           ) :
      ########################################################################
      mg   = self . getMenuItem       ( "Subgroup"                           )
      mm   . addAction                ( 2001 , mg                            )
      ########################################################################
      if                              ( self . isSubgroup ( )              ) :
        mg = self . getMenuItem       ( "SIG"                                )
        mm . addAction                ( 2002 , mg                            )
      mm   . addSeparator             (                                      )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    ##########################################################################
    if                                ( uuid > 0                           ) :
      self . AppendRenameAction       ( mm , 1102                            )
      self . AssureEditNamesAction    ( mm , 1601 , atItem                   )
    ##########################################################################
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . FunctionsMenu            ( mm , uuid , atItem                   )
    self   . SortingMenu              ( mm                                   )
    self   . LocalityMenu             ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    OKAY   = self . RunDocking        ( mm , aa                              )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu  ( at , uuid , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu    ( at                                   )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu   ( at                                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1101                         ) :
      self . InsertItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1102                         ) :
      self . RenameItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1601                         ) :
      ########################################################################
      NAM  = self . Tables            [ "NamesEditing"                       ]
      self . EditAllNames             ( self , "SexPosition" , uuid , NAM    )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 2001                         ) :
      ########################################################################
      self . OpenItemSubgroup         ( atItem                               )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 2002                         ) :
      ########################################################################
      self . OpenItemSexPositionGroup ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    return True
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
    self  . SexPositionSubgroup . emit  ( title , tid , str ( uuid )         )
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
  def OpenSexPositionGroup          ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    self . OpenItemSexPositionGroup ( atItem                                 )
    ##########################################################################
    return
  ############################################################################
  def OpenItemSexPositionGroup ( self , item                               ) :
    ##########################################################################
    uuid  = item . data        ( Qt . UserRole                               )
    uuid  = int                ( uuid                                        )
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return False
    ##########################################################################
    icon    = item . icon      (                                             )
    title   = item . text      (                                             )
    tid     = self . Relation  . get ( "t2"                                  )
    related = "Subordination"
    self    . SexPositionGroup . emit ( title                              , \
                                        tid                                , \
                                        str ( uuid )                       , \
                                        related                            , \
                                        icon                                 )
    ##########################################################################
    return True
  ############################################################################
  def OpenCurrentSexPositionGroup          ( self                          ) :
    ##########################################################################
    atItem = self . currentItem            (                                 )
    ##########################################################################
    if                                     ( atItem == None                ) :
      return False
    ##########################################################################
    return self . OpenItemSexPositionGroup ( atItem                          )
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
##############################################################################

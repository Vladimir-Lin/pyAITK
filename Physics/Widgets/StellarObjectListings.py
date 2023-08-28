# -*- coding: utf-8 -*-
##############################################################################
## StellarObjectListings
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
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class StellarObjectListings        ( TreeDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = pyqtSignal (                                         )
  emitAllNames        = pyqtSignal ( list                                    )
  StellarObjectGroup  = pyqtSignal ( str , int , str                         )
  ShowPersonalGallery = pyqtSignal ( str , int , str       , QIcon           )
  ShowPersonalIcons   = pyqtSignal ( str , int , str , str , QIcon           )
  OpenLogHistory      = pyqtSignal ( str , str , str , str , str             )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . CKEY               = "StellarObjectListings"
    self . BaseUuid           = 4310000000000000000
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . GType              = 22
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "asc"
    self . Method             = "Original"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Star"                                  )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 600 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenStellarNames                  )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
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
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 ]                      ) :
      return
    ##########################################################################
    if                          ( column     in [ 0 ]                      ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem          ( self , JSON                                   ) :
    ##########################################################################
    UUID = JSON            [ "Uuid"                                          ]
    NAME = JSON            [ "Name"                                          ]
    UXID = str             ( UUID                                            )
    ##########################################################################
    IT   = QTreeWidgetItem (                                                 )
    ##########################################################################
    IT   . setText         ( 0 , NAME                                        )
    IT   . setToolTip      ( 0 , UXID                                        )
    IT   . setData         ( 0 , Qt . UserRole , UXID                        )
    ##########################################################################
    IT   . setData         ( 1 , Qt . UserRole , JSON                        )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0                                         ] )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def nameChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    line   = self . CurrentItem  [ "Widget"                                  ]
    text   = self . CurrentItem  [ "Text"                                    ]
    msg    = line . text         (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( len ( msg ) <= 0                        ) :
      self . removeTopLevelItem  ( item                                      )
      return
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids                    ( self , DB                   ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder          (                               )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables                   [ "RelationStars"               ]
    ##########################################################################
    if                                       ( self . isSubordination ( )  ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                                       ( self . isReverse       ( )  ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                                   [                               ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for JSON in LISTS                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( LISTS )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    if                            ( self . Method in [ "Searching" ]       ) :
      ########################################################################
      T    = self . Translations  [ self . CKEY ] [ "Title"                  ]
      K    = self . SearchKey
      T    = f"{T}:{K}"
      ########################################################################
      self . setWindowTitle       ( T                                        )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
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
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    LISTs   =                         [                                      ]
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    NAMEs   =                         [                                      ]
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      J            =                  {                                      }
      J [ "Uuid" ] = int              ( UUID                                 )
      J [ "Name" ] = NAMEs            [ UUID                                 ]
      LISTs        . append           ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( LISTs                                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot          (                                                       )
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids        ( self , DB                                    ) :
    ##########################################################################
    STOTAB = self . Tables  [ "StellarObjects"                               ]
    ##########################################################################
    QQ     = f"""select `uuid` from {STOTAB}
                 where ( `used` = 1 )
                 order by `id` asc ;"""
    ##########################################################################
    QQ     = " " . join     ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    TABLE = self . Tables       [ "NamesEditing"                             ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    STOTAB = self . Tables   [ "StellarObjects"                              ]
    QQ     = f"select count(*) from {STOTAB} where ( `used` > 0 ) ;"
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
    RELTAB = self . Tables               [ "RelationStars"                   ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "RelationStars"                   ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    STOTAB = self . Tables          [ "StellarObjects"                       ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {STOTAB}
                 where ( `used` = 1 )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "first"                              )
      TYPE = self . Relation . get    ( "t1"                                 )
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "second"                             )
      TYPE = self . Relation . get    ( "t2"                                 )
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "stellar/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , 0 , mtype , message                )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "stellar/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( atItem in [ False , None ]          ) :
      return False
    ##########################################################################
    if                               ( mtype in [ "stellar/uuids"        ] ) :
      self . ShowMenuItemTitleStatus ( "StarsFrom" , title , CNT             )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , source , mimeData , mousePos       ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    ##########################################################################
    if                         ( atItem in [ False , None ]                ) :
      return False
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    mtype  = self . DropInJSON [ "Mime"                                      ]
    UUIDs  = self . DropInJSON [ "UUIDs"                                     ]
    ##########################################################################
    return True
  ############################################################################
  def acceptStellarsDrop   ( self                                          ) :
    return True
  ############################################################################
  def dropStellars         ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    self   . Go            ( self . JoinStellars , ( UUIDs , )               )
    ##########################################################################
    return True
  ############################################################################
  def JoinStellars                   ( self , UUIDs                        ) :
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    self   . OnBusy  . emit          (                                       )
    self   . setBustle               (                                       )
    FMT    = self . getMenuItem      ( "JoinStars"                           )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    RELTAB = self . Tables           [ "RelationStars"                       ]
    DB     . LockWrites              ( [ RELTAB                            ] )
    ##########################################################################
    if                               ( self . isSubordination ( )          ) :
      ########################################################################
      self . Relation . Joins        ( DB , RELTAB , UUIDs                   )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    self   . setVacancy              (                                       )
    self   . GoRelax . emit          (                                       )
    DB     . Close                   (                                       )
    ##########################################################################
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . CKEY , 1                                  )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    STOTAB = self . Tables    [ "StellarObjects"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ STOTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      uuid = DB . LastUuid    ( STOTAB , "uuid" , self . BaseUuid            )
      DB   . AppendUuid       ( STOTAB ,  uuid                               )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def AppendingStellars       ( self , NAMEs                               ) :
    ##########################################################################
    if                        ( len ( NAMEs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    STOTAB = self . Tables    [ "StellarObjects"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    RELTAB = self . Tables    [ "RelationStars"                              ]
    ##########################################################################
    UUIDs  =                  [                                              ]
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    DB     . LockWrites       ( [ STOTAB , NAMTAB , RELTAB                 ] )
    ##########################################################################
    for N in NAMEs                                                           :
      ########################################################################
      uuid = DB . LastUuid    ( STOTAB , "uuid" , self . BaseUuid            )
      DB   . AppendUuid       ( STOTAB ,  uuid                               )
      self . AssureUuidName   ( DB     , NAMTAB , uuid , N                   )
      ########################################################################
      UUIDs . append          ( uuid                                         )
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      self . Relation . Joins ( DB , RELTAB , UUIDs                          )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    self   . ShowStatus       ( ""                                           )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def AppendingStellarsFromText             ( self , NAMEs                 ) :
    ##########################################################################
    if                                      ( len ( NAMEs ) <= 0           ) :
      return
    ##########################################################################
    LISTs     = NAMEs . split               ( "\n"                           )
    if                                      ( len ( LISTs ) <= 0           ) :
      return
    ##########################################################################
    NAMEs     =                             [                                ]
    ##########################################################################
    for N in LISTs                                                           :
      ########################################################################
      K       = N
      K       = K . replace                 ( "\r" , ""                      )
      K       = K . replace                 ( "\n" , ""                      )
      K       = K .  strip                  (                                )
      K       = K . rstrip                  (                                )
      ########################################################################
      if                                    ( len ( K ) > 0                ) :
        ######################################################################
        NAMEs . append                      ( K                              )
    ##########################################################################
    if                                      ( len ( NAMEs ) <= 0           ) :
      return
    ##########################################################################
    VAL       =                             ( NAMEs ,                        )
    self      . Go                          ( self . AppendingStellars , VAL )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                  (                                               )
  def InsertItem             ( self                                        ) :
    ##########################################################################
    self . defaultInsertItem ( 0 , "editingFinished" , self . nameChanged    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                              (                                   )
  def PasteItems                         ( self                            ) :
    ##########################################################################
    NAMEs = qApp  . clipboard ( ) . text (                                   )
    self  . AppendingStellarsFromText    ( NAMEs                             )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def OpenStellarNames          ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    NAM    = self . Tables      [ "NamesEditing"                             ]
    self   . EditAllNames       ( self , "Star" , uuid , NAM                 )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGallery                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( 0 , Qt . UserRole                    )
    uuid = int                        ( uuid                                 )
    text = item . text                ( 0                                    )
    icon = self . windowIcon          (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , self . GType , xsid , icon    )
    ##########################################################################
    return
  ############################################################################
  def OpenItemStars                   ( self , item                        ) :
    ##########################################################################
    uuid  = item . data               ( 0 , Qt . UserRole                    )
    uuid  = int                       ( uuid                                 )
    ##########################################################################
    if                                ( uuid <= 0                          ) :
      return False
    ##########################################################################
    title = item . text               ( 0                                    )
    self  . StellarObjectGroup . emit ( title , self . GType , str ( uuid )  )
    ##########################################################################
    return True
  ############################################################################
  def GroupsMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( item . text ( 0 )                           )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "CopyStellarUuid"                           )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AppendStellarUuid"                         )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "Subgroup"                                  )
    mm  . addActionFromMenu    ( LOM , 24231201 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "Icon"                                      )
    mm  . addActionFromMenu    ( LOM , 24231202 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "Gallery"                                   )
    mm  . addActionFromMenu    ( LOM , 24231203 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "Description"                               )
    mm  . addActionFromMenu    ( LOM , 24231204 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , uuid , item              ) :
    ##########################################################################
    if                              ( at == 24231101                       ) :
      ########################################################################
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231102                       ) :
      ########################################################################
      appendUuid                    ( uuid                                   )
      self . Notify                 ( 5                                      )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231201                       ) :
      ########################################################################
      self . OpenItemStars          ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 24231202                       ) :
      ########################################################################
      icon = self . windowIcon      (                                        )
      head = item . text            ( 0                                      )
      xsid = str                    ( uuid                                   )
      relz = "Using"
      ########################################################################
      self . ShowPersonalIcons . emit ( head , 22 , relz , xsid , icon       )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 24231203                       ) :
      ########################################################################
      self . OpenItemGallery        ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 24231204                       ) :
      ########################################################################
      head = item . text            ( 0                                      )
      nx   = ""
      ########################################################################
      if                            ( "Notes" in self . Tables             ) :
        nx = self . Tables          [ "Notes"                                ]
      ########################################################################
      self . OpenLogHistory . emit  ( head                                   ,
                                      str ( uuid )                           ,
                                      "Description"                          ,
                                      nx                                     ,
                                      str ( self . getLocality ( ) )         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9001 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
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
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    uuid   = 0
    ##########################################################################
    if                              ( atItem != None                       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    if                              ( self . Method not in [ "Original" ]  ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Original"                             )
      mm   . addAction              ( 1002 , msg                             )
    ##########################################################################
    self   . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      self . AppendRenameAction     ( mm , 1102                              )
      ########################################################################
      if                            ( self . EditAllNames != None          ) :
        ######################################################################
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . GroupsMenu             ( mm , uuid , atItem                     )
    self   . ColumnsMenu            ( mm                                     )
    self   . SortingMenu            ( mm                                     )
    self   . LocalityMenu           ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunAmountIndexMenu ( )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu   ( at , uuid , atItem                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . Method = "Original"
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      ########################################################################
      self . InsertItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      ########################################################################
      self . RenameItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "NamesEditing"                         ]
      self . EditAllNames           ( self , "Stars" , uuid , NAM            )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################

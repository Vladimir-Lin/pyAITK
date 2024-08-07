# -*- coding: utf-8 -*-
##############################################################################
## DocumentListings
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import pathlib
##############################################################################
from   PyQt5                             import QtCore
from   PyQt5                             import QtGui
from   PyQt5                             import QtWidgets
##############################################################################
from   PyQt5 . QtCore                    import QObject
from   PyQt5 . QtCore                    import pyqtSignal
from   PyQt5 . QtCore                    import pyqtSlot
from   PyQt5 . QtCore                    import Qt
from   PyQt5 . QtCore                    import QPoint
from   PyQt5 . QtCore                    import QPointF
from   PyQt5 . QtCore                    import QSize
##############################################################################
from   PyQt5 . QtGui                     import QIcon
from   PyQt5 . QtGui                     import QCursor
from   PyQt5 . QtGui                     import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                 import QApplication
from   PyQt5 . QtWidgets                 import QWidget
from   PyQt5 . QtWidgets                 import qApp
from   PyQt5 . QtWidgets                 import QAction
from   PyQt5 . QtWidgets                 import QShortcut
from   PyQt5 . QtWidgets                 import QMenu
from   PyQt5 . QtWidgets                 import QAbstractItemView
from   PyQt5 . QtWidgets                 import QFileDialog
from   PyQt5 . QtWidgets                 import QTreeWidget
from   PyQt5 . QtWidgets                 import QTreeWidgetItem
from   PyQt5 . QtWidgets                 import QLineEdit
from   PyQt5 . QtWidgets                 import QComboBox
from   PyQt5 . QtWidgets                 import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager          import MenuManager as MenuManager
from   AITK  . Qt . TreeDock             import TreeDock    as TreeDock
from   AITK  . Qt . LineEdit             import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox             import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox              import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation     import Relation
from   AITK  . Calendars  . StarDate     import StarDate
from   AITK  . Calendars  . Periode      import Periode
##############################################################################
from   AITK  . UUIDs      . UuidListings import appendUuid
from   AITK  . UUIDs      . UuidListings import appendUuids
from   AITK  . UUIDs      . UuidListings import getUuids
##############################################################################
class DocumentListings             ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . CKEY               = "DocumentListings"
    self . GType              = 48
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "desc"
    self . Method             = "Original"
    self . BaseUuid           = 6300000000000000000
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Document"                              )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 7                                       )
    self . setColumnHidden         ( 6 , True                                )
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
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 800 , 400                               )
  ############################################################################
  def setGrouping                ( self , group                            ) :
    ##########################################################################
    self . Grouping = group
    ##########################################################################
    return self . Grouping
  ############################################################################
  def getGrouping                ( self                                    ) :
    return self . Grouping
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    TABLE = self . Tables    [ "Documents"                                   ]
    QQ    = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
    DB    . Query            ( QQ                                            )
    ONE   = DB . FetchOne    (                                               )
    ##########################################################################
    if                       ( ONE in [ False , None ]                     ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                           ]
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
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Insert"     , self . InsertItem        )
    self . LinkAction              ( "Delete"     , self . DeleteItems       )
    self . LinkAction              ( "Import"     , self . ImportCurrentFile )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                     ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                column                                     , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem              ( self , JSOX                               ) :
    ##########################################################################
    UUID    = JSOX             [ "Uuid"                                      ]
    UUID    = int              ( UUID                                        )
    UXID    = str              ( UUID                                        )
    ##########################################################################
    NAME    = JSOX             [ "Name"                                      ]
    USED    = JSOX             [ "Used"                                      ]
    DTYPE   = JSOX             [ "Type"                                      ]
    SIZE    = JSOX             [ "Size"                                      ]
    FORMAT  = JSOX             [ "Format"                                    ]
    HANDLER = JSOX             [ "Handler"                                   ]
    ##########################################################################
    IT      = QTreeWidgetItem  (                                             )
    ##########################################################################
    IT      . setText          ( 0 , NAME                                    )
    IT      . setToolTip       ( 0 , UXID                                    )
    IT      . setData          ( 0 , Qt . UserRole , UUID                    )
    ##########################################################################
    IT      . setText          ( 1 , str ( USED  )                           )
    ##########################################################################
    IT      . setText          ( 2 , str ( DTYPE )                           )
    ##########################################################################
    IT      . setText          ( 3 , str ( SIZE  )                           )
    IT      . setTextAlignment ( 3 , Qt.AlignRight                           )
    ##########################################################################
    IT      . setText          ( 4 , FORMAT                                  )
    ##########################################################################
    IT      . setText          ( 5 , HANDLER                                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    item = QTreeWidgetItem       (                                           )
    item . setData               ( 0 , Qt . UserRole , 0                     )
    self . addTopLevelItem       ( item                                      )
    line = self . setLineEdit    ( item                                    , \
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
    line . setFocus              ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                          (                                       )
  def DeleteItems                    ( self                                ) :
    ##########################################################################
    UUIDs  = self . getSelectedUuids ( 0                                     )
    if                               ( len ( UUIDs ) <= 0                  ) :
      return
    ##########################################################################
    items  = self . selectedItems    (                                       )
    for item in items                                                        :
      self . pendingRemoveItem       ( item                                  )
    ##########################################################################
    self   . Go                      ( self . RemoveItems , ( UUIDs , )      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot             (                                                    )
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
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
  def Paste                      ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , ITEMs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for J in ITEMs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( J                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( ITEMs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    ##########################################################################
    if                                ( self . Grouping == "Original"      ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  def loading                          ( self                              ) :
    ##########################################################################
    DB       = self . ConnectDB        (                                     )
    ##########################################################################
    if                                 ( DB == None                        ) :
      self   . emitNamesShow . emit    (                                     )
      return
    ##########################################################################
    self     . OnBusy  . emit          (                                     )
    self     . setBustle               (                                     )
    ##########################################################################
    FMT      = self . Translations     [ "UI::StartLoading"                  ]
    MSG      = FMT . format            ( self . windowTitle ( )              )
    self     . ShowStatus              ( MSG                                 )
    ##########################################################################
    self     . ObtainsInformation      ( DB                                  )
    ##########################################################################
    ITEMs    =                         [                                     ]
    UUIDs    = self . ObtainsItemUuids ( DB                                  )
    ##########################################################################
    if                                 ( len ( UUIDs ) > 0                 ) :
      ########################################################################
      NAMEs  = self . ObtainsUuidNames ( DB , UUIDs                          )
      ########################################################################
      DOCTAB = self . Tables           [ "Documents"                         ]
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        QQ   = f"""select `used` , `type` , `size` , `format` , `handler`
                   from {DOCTAB}
                   where ( `uuid` = {UUID} )
                   order by `id` desc
                   limit 0 , 1 ;"""
        ######################################################################
        QQ   = " " . join              ( QQ . split ( )                      )
        DB   . Query                   ( QQ                                  )
        RR   = DB . FetchOne           (                                     )
        ######################################################################
        if                             ( RR in [ False , None ]            ) :
          continue
        ######################################################################
        if                             ( len ( RR ) != 5                   ) :
          continue
        ######################################################################
        NAME = NAMEs                   [ UUID                                ]
        USED = int                     ( RR [ 0                            ] )
        DTYP = int                     ( RR [ 1                            ] )
        SIZE = int                     ( RR [ 2                            ] )
        FMT  = self . assureString     ( RR [ 3                            ] )
        DEAL = self . assureString     ( RR [ 4                            ] )
        ######################################################################
        ITEMs . append                 ( { "Uuid"    : UUID                , \
                                           "Name"    : NAME                , \
                                           "Used"    : USED                , \
                                           "Type"    : DTYP                , \
                                           "Size"    : SIZE                , \
                                           "Format"  : FMT                 , \
                                           "Handler" : DEAL                } )
    ##########################################################################
    self     . setVacancy              (                                     )
    self     . GoRelax . emit          (                                     )
    self     . ShowStatus              ( ""                                  )
    DB       . Close                   (                                     )
    ##########################################################################
    if                                 ( len ( ITEMs ) <= 0                ) :
      self   . emitNamesShow . emit    (                                     )
      return
    ##########################################################################
    self     . emitAllNames . emit     ( ITEMs                               )
    self     . Notify                  ( 5                                   )
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
    DOCTAB = self . Tables  [ "Documents"                                    ]
    ##########################################################################
    QQ     = f"""select `uuid` from {DOCTAB}
                 where ( `used` > 0 )
                 order by `id` asc ;"""
    ##########################################################################
    QQ     = " " . join     ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self  . Total = 0
    ##########################################################################
    TABLE = self . Tables [ "Documents"                                      ]
    ##########################################################################
    QQ    = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
    DB    . Query         ( QQ                                               )
    RR    = DB . FetchOne (                                                  )
    ##########################################################################
    if                    ( RR in [ False , None ]                         ) :
      return
    ##########################################################################
    if                    ( len ( RR ) <= 0                                ) :
      return
    ##########################################################################
    self  . Total = int   ( RR [ 0                                         ] )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TABLE  = self . Tables          [ "Documents"                            ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` > 0 )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "document/uuids"
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
    formats = "document/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                            ( self                            , \
                                           sourceWidget                    , \
                                           mimeData                        , \
                                           mousePos                        ) :
    ##########################################################################
    if                                   ( self == sourceWidget            ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew      ( mimeData                          )
    if                                   ( not RDN                         ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON          [ "Mime"                            ]
    UUIDs   = self . DropInJSON          [ "UUIDs"                           ]
    ##########################################################################
    if                                   ( mtype in [ "document/uuids" ]   ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      ########################################################################
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "Copying"                         )
      MSG   = FMT  . format              ( title , CNT                       )
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptDocumentsDrop ( self                                           ) :
    return True
  ############################################################################
  def dropDocuments                 ( self , source , pos , JSON           ) :
    ##########################################################################
    return self . defaultDropInside ( source                               , \
                                      JSON                                 , \
                                      self . DocumentJoinFolder              )
  ############################################################################
  def DocumentJoinFolder           ( self , UUIDs                          ) :
    ##########################################################################
    COUNT  = len                   ( UUIDs                                   )
    ##########################################################################
    if                             ( COUNT <= 0                            ) :
      return
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    self   . setDroppingAction     ( True                                    )
    self   . OnBusy  . emit        (                                         )
    self   . setBustle             (                                         )
    ##########################################################################
    FMT    = self . getMenuItem    ( "Joining"                               )
    MSG    = FMT  . format         ( COUNT                                   )
    self   . ShowStatus            ( MSG                                     )
    self   . TtsTalk               ( MSG , 1002                              )
    ##########################################################################
    RELTAB = self . Tables         [ "RelationDocuments"                     ]
    ##########################################################################
    DB     . LockWrites            ( [ RELTAB                              ] )
    ##########################################################################
    if                             ( self . isSubordination (            ) ) :
      ########################################################################
      self . Relation . Joins      ( DB , RELTAB , UUIDs                     )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    ##########################################################################
    self   . setVacancy            (                                         )
    self   . GoRelax . emit        (                                         )
    self   . setDroppingAction     ( False                                   )
    self   . ShowStatus            ( ""                                      )
    DB     . Close                 (                                         )
    ##########################################################################
    self   . restart               (                                         )
    ##########################################################################
    return
  ############################################################################
  def ImportCurrentFile       ( self                                       ) :
    ##########################################################################
    item = self . currentItem (                                              )
    ##########################################################################
    if                        ( item in [ False , None ]                   ) :
      return
    ##########################################################################
    uuid = atItem . data      ( 0 , Qt . UserRole                            )
    uuid = int                ( uuid                                         )
    ##########################################################################
    self . ImportFile         ( uuid                                         )
    ##########################################################################
    return
  ############################################################################
  def ImportFile                   ( self , UUID                           ) :
    ##########################################################################
    MSG       = self . getMenuItem ( "ImportDocument"                        )
    FILTERS   = self . getMenuItem ( "OpenDocumentFilters"                   )
    ##########################################################################
    FNAME , _ = QFileDialog . getOpenFileName                                (
                                     self                                    ,
                                     MSG                                     ,
                                     ""                                      ,
                                     FILTERS                                 )
    ##########################################################################
    if                             ( len ( FNAME ) <= 0                    ) :
      return
    ##########################################################################
    self      . Go                 ( self . GoImporting , ( UUID , FNAME , ) )
    ##########################################################################
    return
  ############################################################################
  def GoImporting                ( self , UUID , FILENAME                ) :
    ##########################################################################
    FSIZE  = os . path . getsize ( FILENAME                                )
    FG2    = int                 ( 2 * 1024 * 1024 * 1024                  )
    ##########################################################################
    if                           ( FSIZE > FG2                           ) :
      ########################################################################
      self . Notify              ( 1                                       )
      ########################################################################
      return
    ##########################################################################
    BODY   = None
    ##########################################################################
    with open                    ( FILENAME , "rb" ) as F                    :
      BODY = F . read            (                                           )
    ##########################################################################
    if                           ( BODY in [ False , None ]                ) :
      ########################################################################
      self . Notify              ( 1                                         )
      ########################################################################
      return
    ##########################################################################
    CNT    = len                 ( BODY                                      )
    if                           ( CNT != FSIZE                            ) :
      ########################################################################
      self . Notify              ( 1                                         )
      ########################################################################
      return
    ##########################################################################
    SUFFIX = pathlib . Path      ( FILENAME ) . suffix
    EXT    = SUFFIX  . lower     (                                           )
    EXT    = EXT     . replace   ( "." , ""                                  )
    DEAL   = ""
    ##########################################################################
    if                           ( "txt" == EXT                            ) :
      DEAL = "plaintext"
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB in [ False , None ]                  ) :
      ########################################################################
      self . Notify              ( 1                                         )
      ########################################################################
      return
    ##########################################################################
    DOCTAB = self . Tables       [ "Documents"                               ]
    ##########################################################################
    DB     . LockWrites          ( [ DOCTAB                                ] )
    ##########################################################################
    QQ     = f"""update {DOCTAB}
                 set `size` = {FSIZE} ,
                     `format` = %s ,
                     `handler` = %s ,
                     `body` = %s
                 where ( `uuid` = {UUID} ) ;"""
    ##########################################################################
    QQ     = " " . join          ( QQ . split ( )                            )
    DB     . QueryValues         ( QQ , ( EXT , DEAL , BODY , )              )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    ##########################################################################
    DB     . Close               (                                           )
    ##########################################################################
    self   . Notify              ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . CKEY , 6                                  )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    DOCTAB = self . Tables    [ "Documents"                                  ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    RELTAB = self . Tables    [ "RelationDocuments"                          ]
    ##########################################################################
    DB     . LockWrites       ( [ DOCTAB , NAMTAB , RELTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( DOCTAB , "uuid" , self . BaseUuid            )
      DB   . AddUuid          ( DOCTAB , uuid , 1                            )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    if                        ( self . isSubordination (                 ) ) :
      ########################################################################
      self . Relation . set   ( "second" , uuid                              )
      self . Relation . Join  ( DB , RELTAB                                  )
      ########################################################################
    elif                      ( self . isReverse       (                 ) ) :
      ########################################################################
      self . Relation . set   ( "first"  , uuid                              )
      self . Relation . Join  ( DB , RELTAB                                  )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    item    . setData         ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def RemoveSubordination             ( self , DB , UUIDs                  ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for UUID in UUIDs                                                        :
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
      DB   . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def RemoveReverse                   ( self , DB , UUIDs                  ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for UUID in UUIDs                                                        :
      self . Relation . set           ( "first" , UUID                       )
      QQ   = self . Relation . Delete ( RELTAB                               )
      DB   . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                ( self , UUIDs                            ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB == None                              ) :
      return
    ##########################################################################
    if                           ( self . Grouping in [ "Subordination" ]  ) :
      self . RemoveSubordination ( DB , UUIDs                                )
    elif                         ( self . Grouping in [ "Reverse" ]        ) :
      self . RemoveReverse       ( DB , UUIDs                                )
    ##########################################################################
    DB     . Close               (                                           )
    self   . Notify              ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
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
    msg = self . getMenuItem   ( "CopyDocumentUuid"                          )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AppendDocumentUuid"                        )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "Import"                                    )
    mm  . addActionFromMenu    ( LOM , 24231201 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , uuid , item              ) :
    ##########################################################################
    if                              ( at == 24231101                       ) :
      ########################################################################
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 24231102                       ) :
      ########################################################################
      appendUuid                    ( uuid                                   )
      self . Notify                 ( 5                                      )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 24231201                       ) :
      ########################################################################
      self . ImportFile             ( uuid                                   )
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
    if                             ( at >= 9001 ) and ( at <= 9006 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9001 ) and ( hid )            ) :
        ######################################################################
        self . startup             (                                         )
        ######################################################################
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
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    self   . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( len ( items ) > 0                    ) :
      ########################################################################
      GRP  =                        [ "Subordination" , "Reverse"            ]
      ########################################################################
      if                            ( self . Grouping in GRP               ) :
        ######################################################################
        self . AppendDeleteAction   ( mm , 1102                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      self . AppendRenameAction     ( mm , 1103                              )
      ########################################################################
      if                            ( self . EditAllNames != None          ) :
        ######################################################################
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . GroupsMenu             ( mm , uuid , atItem                     )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . ColumnsMenu            ( mm                                     )
    self   . SortingMenu            ( mm                                     )
    self   . LocalityMenu           ( mm                                     )
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
    OKAY   = self . RunGroupsMenu   ( at , uuid , atItem                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . restart                (                                        )
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
      self . DeleteItems            (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1103                           ) :
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
    return True
##############################################################################

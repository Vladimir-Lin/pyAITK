# -*- coding: utf-8 -*-
##############################################################################
## MimeTypeListings
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
##############################################################################
from   AITK  . Calendars . StarDate   import StarDate
from   AITK  . Calendars . Periode    import Periode
from   AITK  . Documents . MIME       import MIME        as MimeItem
##############################################################################
class MimeTypeListings             ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( dict                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "MimeTypeListings"
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
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
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return self . SizeSuggestion   ( QSize ( 1024 , 640 )                    )
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ## self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
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
    self . setActionLabel    ( "Label"      , self . windowTitle ( )         )
    self . AttachActions     ( True                                          )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut               ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent ( event                                         )
    ##########################################################################
    return
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
  def PrepareItemContent     ( self , IT , UUID , JSON                     ) :
    ##########################################################################
    ID    = str              ( JSON [ "Id" ]                                 )
    UXID  = str              ( UUID                                          )
    MIME  = JSON             [ "MIME"                                        ]
    TYPE  = JSON             [ "Type"                                        ]
    STYPE = JSON             [ "SubType"                                     ]
    COMM  = JSON             [ "Comment"                                     ]
    WIKI  = JSON             [ "Wiki"                                        ]
    ##########################################################################
    IT    . setText          ( 0 , ID                                        )
    IT    . setToolTip       ( 0 , UXID                                      )
    IT    . setData          ( 0 , Qt . UserRole , UUID                      )
    IT    . setTextAlignment ( 0 , Qt.AlignRight                             )
    ##########################################################################
    IT    . setText          ( 1 , MIME                                      )
    IT    . setText          ( 2 , TYPE                                      )
    IT    . setText          ( 3 , STYPE                                     )
    IT    . setText          ( 4 , COMM                                      )
    IT    . setText          ( 5 , WIKI                                      )
    ##########################################################################
    IT   . setData           ( 6 , Qt . UserRole , JSON                      )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , UUID , JSON                      ) :
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    self . PrepareItemContent    ( IT , UUID , JSON                          )
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
  @pyqtSlot                       (        dict                              )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    JSONs  = JSON                 [ "JSONs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , JSONs [ U ]                          )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( UUIDs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
    return self . DefaultObtainsItemUuids (        DB                        )
  ############################################################################
  def ObtainsUuidJsons            ( self , DB , UUIDs                      ) :
    ##########################################################################
    JSONs   =                     {                                          }
    if                            ( len ( UUIDs ) <= 0                     ) :
      return JSONs
    ##########################################################################
    TABLE   = self . Tables       [ "MIME"                                   ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      COLS  = f"`id` , `mime` , `type` , `subtype` , `comment` , `wiki`"
      QQ    = f"""select {COLS} from {TABLE} where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join          ( QQ . split ( )                           )
      DB    . Query               ( QQ                                       )
      RR    = DB . FetchOne       (                                          )
      ########################################################################
      if                          ( RR in [ False , None ]                 ) :
        continue
      ########################################################################
      if                          ( len ( RR ) <= 0                        ) :
        continue
      ########################################################################
      ID    = int                 ( RR [ 0 ]                                 )
      MIME  = self . assureString ( RR [ 1 ]                                 )
      TYPE  = self . assureString ( RR [ 2 ]                                 )
      STYPE = self . assureString ( RR [ 3 ]                                 )
      COMM  = self . assureString ( RR [ 4 ]                                 )
      WIKI  = self . assureString ( RR [ 5 ]                                 )
      J     =                     { "Id"      : ID                         , \
                                    "Uuid"    : UUID                       , \
                                    "MIME"    : MIME                       , \
                                    "Type"    : TYPE                       , \
                                    "SubType" : STYPE                      , \
                                    "Comment" : COMM                       , \
                                    "Wiki"    : WIKI                         }
      ########################################################################
      JSONs [ UUID ] = J
    ##########################################################################
    return JSONs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    JSONs   =                         {                                      }
    if                                ( len ( UUIDs ) > 0                  ) :
      ########################################################################
      JSONs = self . ObtainsUuidJsons ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "JSONs" ] = JSONs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
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
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self  . Total = 0
    ##########################################################################
    TABLE = self . Tables [ "MIME"                                           ]
    ##########################################################################
    QQ    = f"select count(*) from {TABLE} ;"
    DB    . Query         ( QQ                                               )
    RR    = DB . FetchOne (                                                  )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self  . Total = int   ( RR [ 0 ]                                         )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TABLE  = self . Tables          [ "MIME"                                 ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 ,  80                                          )
    self . setColumnWidth ( 1 , 320                                          )
    self . setColumnWidth ( 2 , 160                                          )
    self . setColumnWidth ( 5 , 240                                          )
    self . defaultPrepare ( self . ClassTag , 6                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    PLSTAB  = self . Tables        [ "Places"                                ]
    NAMTAB  = self . Tables        [ "NamesPlaces"                           ]
    ##########################################################################
    DB      . LockWrites           ( [ PLSTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . UnusedUuid      ( PLSTAB                                  )
      DB    . UseUuid              ( PLSTAB , uuid                           )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . UnlockTables         (                                         )
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                ( self , UUIDs                            ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB == None                              ) :
      return
    ##########################################################################
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9006 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AmountIndexMenu       ( mm                                      )
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    ##########################################################################
    if                             ( len ( items ) > 0                     ) :
      self . AppendDeleteAction    ( mm , 1102                               )
    ##########################################################################
    mm     . addSeparator          (                                         )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
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
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    return True
##############################################################################

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
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
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
    self . StartId            = 0
    self . Amount             = 35
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
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
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
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . AttachActions  ( True                                             )
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
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    STOTAB = self . Tables [ "StellarObjects"                                ]
    ##########################################################################
    QQ     = f"select count(*) from {STOTAB} where ( `used` = 1 ) ;"
    DB     . Query                   ( QQ                                    )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
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
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . CKEY , 1                                  )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
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
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
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
  @pyqtSlot                  (                                               )
  def PasteItems             ( self                                        ) :
    ##########################################################################
    NAMEs = qApp  . clipboard ( ) . text (                                   )
    LISTs = NAMEs . split                (                                   )
    ##########################################################################
    print(LISTs)
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
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
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
      self . EditAllNames           ( self , "Stellars" , uuid , NAM         )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################

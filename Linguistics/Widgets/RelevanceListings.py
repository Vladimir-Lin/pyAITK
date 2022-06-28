# -*- coding: utf-8 -*-
##############################################################################
## RelevanceListings
## 語言關聯性
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
class RelevanceListings            ( TreeDock                              ) :
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
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 6                                       )
    self . setColumnHidden         ( 5 , True                                )
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
    return self . SizeSuggestion   ( QSize ( 1024 , 400 )                    )
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
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
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
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    self . Notify             ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 1 , 2 , 3 , 4 ]            ) :
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
  def PrepareItem              ( self , JSON                               ) :
    ##########################################################################
    UXID    = str              ( JSON [ "Uuid" ]                             )
    UUID    = int              ( UXID                                        )
    Id      = int              ( JSON [ "Id"   ]                             )
    Used    = int              ( JSON [ "Used" ]                             )
    ENGLISH = JSON             [ "English"                                   ]
    NAME    = JSON             [ "Name"                                      ]
    COMMENT = JSON             [ "Comment"                                   ]
    WIKI    = JSON             [ "Wiki"                                      ]
    ##########################################################################
    IT      = QTreeWidgetItem  (                                             )
    ##########################################################################
    IT      . setText          ( 0 , str ( Id )                              )
    IT      . setToolTip       ( 0 , UXID                                    )
    IT      . setData          ( 0 , Qt . UserRole , UUID                    )
    IT      . setTextAlignment ( 0 , Qt.AlignRight                           )
    ##########################################################################
    IT      . setText          ( 1 , ENGLISH                                 )
    IT      . setText          ( 2 , NAME                                    )
    IT      . setText          ( 3 , COMMENT                                 )
    IT      . setText          ( 4 , WIKI                                    )
    ##########################################################################
    IT      . setData          ( 5 , Qt . UserRole , JSON                    )
    ##########################################################################
    return IT
  ############################################################################
  def AppendRelevanceItem        ( self                                    ) :
    ##########################################################################
    DB      = self . ConnectDB   (                                           )
    if                           ( DB == None                              ) :
      return
    ##########################################################################
    REVTAB  = self . Tables      [ "Relevance"                               ]
    ##########################################################################
    UUID    = DB   . UnusedUuid  ( REVTAB                                    )
    if                           ( int ( UUID ) > 0                        ) :
      DB    . UseUuid            ( REVTAB , UUID                             )
    ##########################################################################
    DB      . Close              (                                           )
    self    . loading            (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    self . Go                    ( self . AppendRelevanceItem                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (                                          )
  def RenameItem                  ( self                                   ) :
    ##########################################################################
    IT     = self . currentItem   (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    column = self . currentColumn (                                          )
    ##########################################################################
    if                            ( column not in [ 1 , 2 , 3 , 4 ]        ) :
      return
    ##########################################################################
    self   . doubleClicked        ( IT , column                              )
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
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , column , msg , )          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for R in LISTS                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( R                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    UUIDs   =                         [                                      ]
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    return UUIDs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    REVTAB  = self . Tables           [ "Relevance"                          ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    ##########################################################################
    LISTS   =                         [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      J     =                         { "Uuid"    : UUID                   , \
                                        "Id"      : -1                     , \
                                        "Used"    : 0                      , \
                                        "English" : ""                     , \
                                        "Name"    : ""                     , \
                                        "Comment" : ""                     , \
                                        "Wiki"    : ""                       }
      QQ    = f"""select `id`,`used`,`name`,`comment`,`wiki` from {REVTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if                              ( RR in [ False , None ]             ) :
        continue
      ########################################################################
      if                              ( len ( RR ) != 5                    ) :
        continue
      ########################################################################
      Name  = self . GetName          ( DB , NAMTAB , UUID                   )
      ########################################################################
      J  [ "Id"      ] = int                 ( RR [ 0 ]                      )
      J  [ "Used"    ] = int                 ( RR [ 1 ]                      )
      J  [ "English" ] = self . assureString ( RR [ 2 ]                      )
      J  [ "Name"    ] = Name
      J  [ "Comment" ] = self . assureString ( RR [ 3 ]                      )
      J  [ "Wiki"    ] = self . assureString ( RR [ 4 ]                      )
      ########################################################################
      LISTS . append                  ( J                                    )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . emitAllNames  . emit    ( LISTS                                )
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
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None"                      ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock"                      ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"                       ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    REVTAB = self . Tables [ "Relevance"                                     ]
    ##########################################################################
    QQ     = f"select count(*) from {REVTAB} where ( `used` > 0 ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( RR in [ False , None ] ) or ( len ( RR ) <= 0 )                     :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    REVTAB = self . Tables [ "Relevance"                                     ]
    ORDER  = self . SortOrder
    ##########################################################################
    QQ     = f"""select `uuid` from {REVTAB}
                 where ( `used` > 0 )
                 order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 0 ,  80                                      )
    self   . setColumnWidth   ( 1 , 200                                      )
    self   . setColumnWidth   ( 2 , 120                                      )
    self   . setColumnWidth   ( 3 , 320                                      )
    self   . setColumnWidth   ( 4 , 200                                      )
    self   . setColumnWidth   ( 5 ,   3                                      )
    ##########################################################################
    TRX    = self . Translations
    LABELs = TRX              [ "RelevanceListings" ] [ "Labels"             ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , column , name    ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    REVTAB  = self . Tables        [ "Relevance"                             ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    ##########################################################################
    DB      . LockWrites           ( [ REVTAB , NAMTAB                     ] )
    ##########################################################################
    if                             ( column == 2                           ) :
      self  . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    elif                           ( column in [ 1 , 3 , 4 ]               ) :
      ########################################################################
      col   = ""
      ########################################################################
      if                           ( column == 1                           ) :
        col   = "`name`"
      elif                         ( column == 3                           ) :
        col   = "`comment`"
      elif                         ( column == 4                           ) :
        col   = "`wiki`"
      ########################################################################
      if                           ( len ( col ) > 0                       ) :
        ######################################################################
        QQ    = f"""update {REVTAB}
                    set {col} = %s
                    where ( `uuid` = {uuid} ) ;"""
        QQ    = " " . join         ( QQ . split ( )                          )
        DB    . QueryValues        ( QQ , ( name , )                         )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    self    . Notify               ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard               ( self                                 ) :
    ##########################################################################
    IT     = self . currentItem     (                                        )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    column = self . currentColumn   (                                        )
    MSG    = IT   . text            ( column                                 )
    LID    = self . getLocality     (                                        )
    qApp   . clipboard ( ). setText ( MSG                                    )
    ##########################################################################
    self   . Go                     ( self . Talk , ( MSG , LID , )          )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    HEAD   = self . headerItem     (                                         )
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    for i in range                 ( 1 , 5                                 ) :
      ########################################################################
      msg  = HEAD . text           ( i                                       )
      hid  = self . isColumnHidden ( i                                       )
      mm   . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid   )
    ##########################################################################
    msg    = TRX                   [ "UI::Whitespace"                        ]
    hid    = self . isColumnHidden ( 5                                       )
    mm     . addActionFromMenu     ( COL , 9005     , msg , True , not hid   )
    ##########################################################################
    return mm
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9005 )         :
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
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items  = self . selectedItems  (                                         )
    atItem = self . currentItem    (                                         )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunColumnsMenu     ( at )      ) :
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
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( atItem , 0                              )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Relevance" , uuid , NAM         )
      return True
    ##########################################################################
    return True
##############################################################################

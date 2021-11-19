# -*- coding: utf-8 -*-
##############################################################################
## CountryCodeWidget
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
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QUrl
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDesktopServices
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
class CountryCodeWidget            ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
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
    self . MountClicked            ( 9                                       )
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
    return QSize                   ( 1024 , 640                              )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
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
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 , 1 , 2 , 3 ]          ) :
      return
    ##########################################################################
    if                          ( column in [ 0 , 1 , 2 , 3 ]              ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  def getItemJson                ( self , item                             ) :
    return item . data           ( 5 , Qt . UserRole                         )
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    UUID    = int                 ( JSON [ "Uuid"     ]                      )
    UXID    = str                 ( UUID                                     )
    USED    = int                 ( JSON [ "Used"     ]                      )
    NATION  = int                 ( JSON [ "Nation"   ]                      )
    ITU     = int                 ( JSON [ "ITU"      ]                      )
    PLACE   = int                 ( JSON [ "Place"    ]                      )
    ##########################################################################
    CODE    = self . assureString ( JSON [ "Code"     ]                      )
    NAME    = self . assureString ( JSON [ "Name"     ]                      )
    COMMENT = self . assureString ( JSON [ "Comment"  ]                      )
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    IT      . setText             ( 0 , NAME                                 )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    ##########################################################################
    IT      . setText             ( 1 , CODE                                 )
    ##########################################################################
    ## IT      . setText             ( 2 , AREA                                 )
    ## IT      . setToolTip          ( 2 , UXID                                 )
    ##########################################################################
    ## IT      . setText             ( 3 , NUMBER                               )
    ## IT      . setToolTip          ( 3 , UXID                                 )
    ##########################################################################
    IT      . setText             ( 4 , ""                                   )
    ##########################################################################
    IT      . setData             ( 5 , Qt . UserRole , JSON                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def RenameItem                 ( self                                    ) :
    ##########################################################################
    IT = self . currentItem      (                                           )
    if                           ( IT is None                              ) :
      return
    ##########################################################################
    self . doubleClicked         ( IT , 1                                    )
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
  def refresh                     ( self , TASKS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in TASKS                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
    ##########################################################################
    return self . DefaultObtainsItemUuids (        DB                        )
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
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    PCCTAB  = self . Tables           [ "CountryCode"                        ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"    : U                      , \
                                        "Used"    : 0                      , \
                                        "Code"    : ""                     , \
                                        "Nation"  : 0                      , \
                                        "ITU"     : 0                      , \
                                        "Place"   : 0                      , \
                                        "Name"    : ""                     , \
                                        "Comment" : ""                       }
      ########################################################################
      QQ    = f"""select
                  `used`,`code`,`nation`,`itu`,`place`,`name`,`comment`
                  from {PCCTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( RR not in [ False , None ] ) and ( len ( RR ) == 7 )              :
        ######################################################################
        J [ "Used"    ] = int         ( RR [ 0 ]                             )
        J [ "Code"    ] = RR          [ 1                                    ]
        J [ "Nation"  ] = int         ( RR [ 2 ]                             )
        J [ "ITU"     ] = int         ( RR [ 3 ]                             )
        J [ "Place"   ] = int         ( RR [ 4 ]                             )
        J [ "Name"    ] = RR          [ 5                                    ]
        J [ "Comment" ] = RR          [ 6                                    ]
      ########################################################################
      IMACT . append                  ( J                                    )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( IMACT ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( IMACT                                )
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
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    PCCTAB  = self . Tables      [ "CountryCode"                             ]
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"select `uuid` from {PCCTAB} order by `id` {ORDER} ;"
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    PCCTAB  = self . Tables           [ "CountryCode"                        ]
    ##########################################################################
    QQ      = f"select count(*) from {PCCTAB} ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    PCCTAB = self . Tables     [ "CountryCode"                               ]
    QQ     = f"select count(*) from {PCCTAB} ;"
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
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    PCCTAB  = self . Tables   [ "CountryCode"                                ]
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"select `uuid` from {PCCTAB} order by `id` {ORDER} ;"
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def FetchSessionInformation                    ( self , DB               ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount (        DB                 )
    ##########################################################################
    return
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    ## self   . setColumnWidth      ( 0 , 200                                   )
    ## self   . setColumnWidth      ( 1 ,  80                                   )
    ## self   . setColumnWidth      ( 2 ,  80                                   )
    ## self   . setColumnWidth      ( 3 , 160                                   )
    ## self   . setColumnWidth      ( 4 , 100                                   )
    self   . setColumnWidth      ( 5 ,   3                                   )
    LABELs = self . Translations [ "CountryCodeWidget" ] [ "Labels"          ]
    self   . setCentralLabels    ( LABELs                                    )
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( 0                                        )
    LID  = self . getLocality     (                                          )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    self . TtsTalk                ( MSG , LID                                )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    msg    = TRX [ "UI::PeopleAmount" ]
    hid    = self . isColumnHidden ( 1                                       )
    mm     . addActionFromMenu     ( COL , 9001 , msg , True , not hid       )
    ##########################################################################
    msg    = TRX                   [ "UI::Whitespace"                        ]
    hid    = self . isColumnHidden ( 2                                       )
    mm     . addActionFromMenu     ( COL , 9002 , msg , True , not hid       )
    ##########################################################################
    return mm
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    items  = self . selectedItems  (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     . addSeparator          (                                         )
    mm     = self . SortingMenu    ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
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
    return True
##############################################################################

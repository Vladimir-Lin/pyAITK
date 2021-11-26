# -*- coding: utf-8 -*-
##############################################################################
## TldsWidget
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
class TldsWidget                   ( TreeDock                              ) :
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
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 10                                      )
    self . setColumnHidden         ( 9 , True                                )
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
    self . LinkAction              ( "Search"     , self . Search            )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkVoice               ( self . CommandParser                    )
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
  def singleClicked            ( self , item , column                      ) :
    ##########################################################################
    if                         ( self . isItemPicked ( )                   ) :
      if                       ( column != self . CurrentItem [ "Column" ] ) :
        self . removeParked    (                                             )
    ##########################################################################
    self     . Notify          ( 0                                           )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 ]                      ) :
      return
    ##########################################################################
    """
    if                          ( column in [ 0 ]                          ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    """
    ##########################################################################
    return
  ############################################################################
  def getItemJson                  ( self , item                           ) :
    return item . data             ( 7 , Qt . UserRole                       )
  ############################################################################
  def PrepareItem                  ( self , JSON                           ) :
    ##########################################################################
    UUID     = int                 ( JSON [ "Uuid"                         ] )
    UXID     = str                 ( UUID                                    )
    ID       = JSON                [ "Id"                                    ]
    USED     = JSON                [ "Used"                                  ]
    TYPE     = JSON                [ "Type"                                  ]
    OWNER    = JSON                [ "Owner"                                 ]
    ##########################################################################
    NAME     = JSON                [ "Name"                                  ]
    REVERSE  = JSON                [ "Reverse"                               ]
    IANA     = JSON                [ "IANA"                                  ]
    EXPLAIN  = JSON                [ "Explain"                               ]
    ##########################################################################
    SLD      = JSON                [ "SLD"                                   ]
    DOMAINS  = JSON                [ "Domains"                               ]
    HOSTS    = JSON                [ "Hosts"                                 ]
    PAGES    = JSON                [ "Pages"                                 ]
    ##########################################################################
    IT       = QTreeWidgetItem     (                                         )
    IT       . setText             ( 0 , NAME                                )
    IT       . setToolTip          ( 0 , UXID                                )
    IT       . setData             ( 0 , Qt . UserRole , UXID                )
    ##########################################################################
    IT       . setText             ( 1 , str ( TYPE    )                     )
    IT       . setToolTip          ( 1 , UXID                                )
    ##########################################################################
    IT       . setText             ( 2 , IANA                                )
    IT       . setToolTip          ( 2 , UXID                                )
    ##########################################################################
    IT       . setText             ( 3 , EXPLAIN                             )
    ##########################################################################
    IT       . setText             ( 4 , str ( OWNER   )                     )
    IT       . setTextAlignment    ( 4 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 5 , str ( SLD     )                     )
    IT       . setTextAlignment    ( 5 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 6 , str ( DOMAINS )                     )
    IT       . setTextAlignment    ( 6 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 7 , str ( HOSTS   )                     )
    IT       . setTextAlignment    ( 7 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 8 , str ( PAGES   )                     )
    IT       . setTextAlignment    ( 8 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setData             ( 9 , Qt . UserRole , JSON                )
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
    self . doubleClicked         ( IT , 0                                    )
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
  def Search                      ( self                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in LISTS                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
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
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    TLDTAB  = self . Tables           [ "TLD"                                ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"     : U                     , \
                                        "Id"       : 0                     , \
                                        "Used"     : 0                     , \
                                        "Type"     : 0                     , \
                                        "Owner"    : 0                     , \
                                        "Name"     : ""                    , \
                                        "Reverse"  : ""                    , \
                                        "IANA"     : ""                    , \
                                        "Explain"  : ""                    , \
                                        "SLD"      : 0                     , \
                                        "Domains"  : 0                     , \
                                        "Hosts"    : 0                     , \
                                        "Pages"    : 0                       }
      ########################################################################
      QQ    = f"""select
                  `id`,`used`,`type`,
                  `owner`,`name`,`reverse`,
                  `iana`,`explain`,`sld`,
                  `domains`,`hosts`,`pages`
                  from {TLDTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 12 ) )         :
        ######################################################################
        J [ "Id"      ] = int         ( RR [  0 ]                            )
        J [ "Used"    ] = int         ( RR [  1 ]                            )
        J [ "Type"    ] = int         ( RR [  2 ]                            )
        J [ "Owner"   ] = int         ( RR [  3 ]                            )
        J [ "Name"    ] = self . assureString ( RR [ 4 ]                     )
        J [ "Reverse" ] = self . assureString ( RR [ 5 ]                     )
        J [ "IANA"    ] = self . assureString ( RR [ 6 ]                     )
        J [ "Explain" ] = self . assureString ( RR [ 7 ]                     )
        J [ "SLD"     ] = int         ( RR [  8 ]                            )
        J [ "Domains" ] = int         ( RR [  9 ]                            )
        J [ "Hosts"   ] = int         ( RR [ 10 ]                            )
        J [ "Pages"   ] = int         ( RR [ 11 ]                            )
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkVoice       ( None                                            )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount ( DB                        )
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TLDTAB = self . Tables     [ "TLD"                                       ]
    QQ     = f"select count(*) from {TLDTAB} ;"
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
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TLDTAB = self . Tables          [ "TLD"                                  ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TLDTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 0 , 120                                   )
    self   . setColumnWidth      ( 1 , 100                                   )
    self   . setColumnWidth      ( 2 , 160                                   )
    self   . setColumnWidth      ( 3 , 320                                   )
    self   . setColumnWidth      ( 9 ,   3                                   )
    LABELs = self . Translations [ "TldsWidget" ] [ "Labels"                 ]
    self   . setCentralLabels    ( LABELs                                    )
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def PageHome                     ( self                                  ) :
    ##########################################################################
    self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd                      ( self                                  ) :
    ##########################################################################
    self . StartId    = self . Total - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp                       ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown                     ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId + self . Amount
    if                             ( self . StartId > self . Total         ) :
      self . StartId  = self . Total
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    """
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TSKTAB  = self . Tables        [ "Tasks"                                 ]
    PRDTAB  = self . Tables        [ "Periods"                               ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    HEAD    = 5702000000000000000
    ##########################################################################
    DB      . LockWrites           ( [ PRJTAB , PRDTAB , NAMTAB ]            )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . LastUuid        ( PRJTAB , "uuid" , HEAD                  )
      DB    . AddUuid              ( PRJTAB , uuid   , 1                     )
      ########################################################################
      NOW   = StarDate             (                                         )
      NOW   . Now                  (                                         )
      CDT   = NOW . Stardate
      ########################################################################
      PRD   = Periode              (                                         )
      PRID  = PRD  . GetUuid       ( DB , PRDTAB                             )
      ########################################################################
      PRD   . Realm    = uuid
      PRD   . Role     = 71
      PRD   . Item     = 1
      PRD   . States   = 0
      PRD   . Creation = CDT
      PRD   . Modified = CDT
      Items =                      [ "realm"                               , \
                                     "role"                                , \
                                     "item"                                , \
                                     "states"                              , \
                                     "creation"                            , \
                                     "modified"                              ]
      PRD   . UpdateItems          ( DB , PRDTAB , Items                     )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    """
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9009 )         :
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
    mm     = self . AmountIndexMenu     ( mm                                 )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendRenameAction  ( mm , 1103                          )
    mm     . addSeparator          (                                         )
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . SortingMenu    ( mm                                      )
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
    if                             ( at == 1103                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    return True
##############################################################################

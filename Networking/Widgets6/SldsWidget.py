# -*- coding: utf-8 -*-
##############################################################################
## SldsWidget
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
class SldsWidget                   ( TreeDock                              ) :
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
    self . TldTypes           =    {                                         }
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
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
    if                          ( column     in [ 0 ]                      ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  def getItemJson                  ( self , item                           ) :
    return item . data             ( 6 , Qt . UserRole                       )
  ############################################################################
  def PrepareItem                  ( self , JSON                           ) :
    ##########################################################################
    UUID     = int                 ( JSON [ "Uuid"                         ] )
    UXID     = str                 ( UUID                                    )
    ID       = JSON                [ "Id"                                    ]
    USED     = JSON                [ "Used"                                  ]
    OWNER    = JSON                [ "Owner"                                 ]
    ##########################################################################
    NAME     = JSON                [ "Name"                                  ]
    REVERSE  = JSON                [ "Reverse"                               ]
    ##########################################################################
    TLD      = JSON                [ "TLD"                                   ]
    DOMAINS  = JSON                [ "Domains"                               ]
    HOSTS    = JSON                [ "Hosts"                                 ]
    PAGES    = JSON                [ "Pages"                                 ]
    ##########################################################################
    TNAME    = f"{TLD}"
    TUID     = f"8300000000001{TLD}"
    if                             ( TUID in self . TldTypes               ) :
      TNAME  = self . TldTypes     [ TUID                                    ]
    ##########################################################################
    IT       = QTreeWidgetItem     (                                         )
    IT       . setText             ( 0 , NAME                                )
    IT       . setToolTip          ( 0 , UXID                                )
    IT       . setData             ( 0 , Qt . UserRole , UXID                )
    IT       . setTextAlignment    ( 0 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 1 , str ( TNAME   )                     )
    IT       . setTextAlignment    ( 1 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 2 , str ( OWNER   )                     )
    IT       . setTextAlignment    ( 2 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 3 , str ( DOMAINS )                     )
    IT       . setTextAlignment    ( 3 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 4 , str ( HOSTS   )                     )
    IT       . setTextAlignment    ( 4 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 5 , str ( PAGES   )                     )
    IT       . setTextAlignment    ( 5 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setData             ( 6 , Qt . UserRole , JSON                )
    ##########################################################################
    return IT
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
    if                            ( column not in [ 0 ]                    ) :
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
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , column , msg , )          )
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
    SLDTAB  = self . Tables           [ "SLD"                                ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"     : U                     , \
                                        "Id"       : 0                     , \
                                        "Used"     : 0                     , \
                                        "Owner"    : 0                     , \
                                        "Name"     : ""                    , \
                                        "Reverse"  : ""                    , \
                                        "TLD"      : 0                     , \
                                        "Domains"  : 0                     , \
                                        "Hosts"    : 0                     , \
                                        "Pages"    : 0                       }
      ########################################################################
      QQ    = f"""select
                  `id`,`used`,`owner`,`name`,`reverse`,
                  `tld`,`domains`,`hosts`,`pages`
                  from {SLDTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 9 ) )          :
        ######################################################################
        J [ "Id"      ] = int         ( RR [ 0 ]                             )
        J [ "Used"    ] = int         ( RR [ 1 ]                             )
        J [ "Owner"   ] = int         ( RR [ 2 ]                             )
        J [ "Name"    ] = self . assureString ( RR [ 3 ]                     )
        J [ "Reverse" ] = self . assureString ( RR [ 4 ]                     )
        J [ "TLD"     ] = int         ( RR [ 5 ]                             )
        J [ "Domains" ] = int         ( RR [ 6 ]                             )
        J [ "Hosts"   ] = int         ( RR [ 7 ]                             )
        J [ "Pages"   ] = int         ( RR [ 8 ]                             )
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
  def ObtainsInformation               ( self , DB                         ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount ( DB                        )
    ##########################################################################
    ## 抓取頂層網域名稱
    ##########################################################################
    self         . TldTypes =          {                                     }
    TLDTAB       = self . Tables       [ "TLD"                               ]
    QQ           = f"select `uuid`,`name` from {TLDTAB} order by `id` asc ;"
    DB           . Query               ( QQ                                  )
    ALL          = DB . FetchAll       (                                     )
    for J in ALL                                                             :
      ########################################################################
      UUID       = str                 ( J [ 0 ]                             )
      NAME       = self . assureString ( J [ 1 ]                             )
      self       . TldTypes [ UUID ] = NAME
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    SLDTAB = self . Tables     [ "SLD"                                       ]
    QQ     = f"select count(*) from {SLDTAB} ;"
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
    SLDTAB = self . Tables          [ "SLD"                                  ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {SLDTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 0 , 240                                   )
    self   . setColumnWidth      ( 6 ,   3                                   )
    LABELs = self . Translations [ "SldsWidget" ] [ "Labels"                 ]
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
  def AssureUuidItem               ( self , item , uuid , column , name    ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TLDTAB  = self . Tables        [ "SLD"                                   ]
    ##########################################################################
    DB      . LockWrites           ( [ TLDTAB ]                              )
    ##########################################################################
    ## if                             ( column == 0                           ) :
    ##   ########################################################################
    ##   QQ    = f"""update {TLDTAB}
    ##               set `name` = %s , `reverse` = %s
    ##               where ( `uuid` = {uuid} ) ;"""
    ##   reve  = name                 [ ::-1                                    ]
    ##   VAL   =                      ( name , reve ,                           )
    ##   ########################################################################
    ## elif                           ( column == 2                           ) :
    ##   ########################################################################
    ##   QQ    = f"""update {TLDTAB}
    ##               set `iana` = %s
    ##               where ( `uuid` = {uuid} ) ;"""
    ##   VAL   =                      ( name ,                                  )
    ##   ########################################################################
    ## elif                           ( column == 3                           ) :
    ##   ########################################################################
    ##   QQ    = f"""update {TLDTAB}
    ##               set `explain` = %s
    ##               where ( `uuid` = {uuid} ) ;"""
    ##   VAL   =                      ( name ,                                  )
    ##########################################################################
    ## try                                                                      :
    ##   if                           ( len ( QQ ) > 0                        ) :
    ##     DB  . QueryValues          ( QQ , VAL                                )
    ## except                                                                   :
    ##   pass
    ##########################################################################
    DB      . UnlockTables         (                                         )
    DB      . Close                (                                         )
    ##########################################################################
    self    . emitAssignColumn . emit ( item , column , name                 )
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
    MSG    = IT . text              ( column                                 )
    LID    = self . getLocality     (                                        )
    qApp   . clipboard ( ). setText ( MSG                                    )
    ##########################################################################
    self   . TtsTalk                ( MSG , LID                              )
    ##########################################################################
    return
  ############################################################################
  def SldBelongings              ( self , DB , Uuid                        ) :
    ##########################################################################
    TLDTAB     = self . Tables   [ "TLD"                                     ]
    SLDTAB     = self . Tables   [ "SLD"                                     ]
    ##########################################################################
    ## SldTotal   = 0
    ## TLDID      = int             ( Uuid % 1000000                            )
    ##########################################################################
    ## QQ         = f"""select count(*) from {SLDTAB}
    ##                  where ( `tld` = {TLDID} ) ;"""
    ## QQ         = " " . join      ( QQ . split ( )                            )
    ## DB         . Query           ( QQ                                        )
    ## RR         = DB . FetchOne   (                                           )
    ##########################################################################
    ## if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )            :
    ##   SldTotal = RR              [ 0                                         ]
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    DB         . LockWrites    ( [ TLDTAB ]                                  )
    ##########################################################################
    ## QQ         = f"""update {TLDTAB}
    ##                  set `sld` = {SldTotal}
    ##                  where ( `uuid` = {Uuid} ) ;"""
    ## QQ         = " " . join    ( QQ . split ( )                              )
    DB         . Query         ( QQ                                          )
    ##########################################################################
    DB         . UnlockTables  (                                             )
    ##########################################################################
    return
  ############################################################################
  def CountBelongings       ( self , UUID                                  ) :
    ##########################################################################
    DB   = self . ConnectDB (                                                )
    if                      ( DB in [ False , None ]                       ) :
      return
    ##########################################################################
    self . SldBelongings    ( DB , UUID                                      )
    DB   . Close            (                                                )
    self . Notify           ( 5                                              )
    ##########################################################################
    return
  ############################################################################
  def CountAllBelongings          ( self                                   ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    plan     = None
    if                            ( self . hasPlan ( )                     ) :
      plan   = self . GetPlan     (                                          )
    ##########################################################################
    self     . OnBusy  . emit     (                                          )
    SLDTAB   = self . Tables      [ "SLD"                                    ]
    ##########################################################################
    QQ       = f"select `uuid` from {SLDTAB} order by `id` asc ;"
    QQ       = " " . join         ( QQ . split ( )                           )
    UUIDs    = DB  . ObtainUuids  ( QQ                                       )
    ##########################################################################
    if ( ( UUIDs not in [ False , None ] ) and ( len ( UUIDs ) > 0 ) )       :
      ########################################################################
      if                          ( plan not in [ False , None ]           ) :
        ######################################################################
        NAME = self . getMenuItem ( "CountAll"                               )
        cFmt = self . getMenuItem ( "SecsCounting"                           )
        rFmt = self . getMenuItem ( "ItemCounting"                           )
        FMT  = self . getMenuItem ( "Percentage"                             )
        PID  = plan . Progress    ( NAME , FMT                               )
        plan . setFrequency       ( PID  , cFmt , rFmt                       )
      ########################################################################
      plan   . setRange           ( PID , 0 , len ( UUIDs )                  )
      plan   . Start              ( PID , 0 , True                           )
      plan   . ProgressReady      ( PID , 300                                )
      ########################################################################
      K      = 0
      while ( K < len ( UUIDs ) ) and ( plan . isProgressRunning ( PID ) )   :
        ######################################################################
        UUID = UUIDs              [ K                                        ]
        plan . setProgressValue   ( PID , K                                  )
        plan . ProgressText       ( PID , str ( UUID )                       )
        ######################################################################
        self . SldBelongings      ( DB , UUID                                )
        ######################################################################
        K    = K + 1
      ########################################################################
      plan   . Finish             ( PID                                      )
    ##########################################################################
    self     . GoRelax . emit     (                                          )
    DB       . Close              (                                          )
    self     . Notify             ( 5                                        )
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
    if                             ( atItem not in [ False , None ]        ) :
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
    ##########################################################################
    mm     . addSeparator          (                                         )
    msg    = self . getMenuItem    ( "CountAll"                              )
    mm     . addAction             ( 4251 , msg                              )
    if                             ( uuid > 0                              ) :
      msg  = self . getMenuItem    ( "Counting"                              )
      mm   . addAction             ( 4252 , msg                              )
    ##########################################################################
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
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 4251                            ) :
      self . Go                    ( self . CountAllBelongings               )
      return True
    ##########################################################################
    if                             ( at == 4252                            ) :
      self . Go                    ( self . CountBelongings , ( uuid , )     )
      return True
    ##########################################################################
    return True
##############################################################################

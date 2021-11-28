# -*- coding: utf-8 -*-
##############################################################################
## TimeZoneListings
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
from   googletrans                    import Translator
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
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class TimeZoneListings             ( TreeDock                              ) :
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
    self . Total    = 0
    self . StartId  = 0
    self . Amount   = 28
    self . Order    = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 5                                       )
    self . setColumnHidden         ( 4 , True                                )
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
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
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
    self     . Notify         ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 , 1 , 2 , 3 ]            ) :
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
  def PrepareItem                ( self , JSON                             ) :
    ##########################################################################
    UUID    = JSON               [ "Uuid"                                    ]
    UXID    = str                ( UUID                                      )
    ZONE    = JSON               [ "Zone"                                    ]
    NAME    = JSON               [ "Name"                                    ]
    COMMENT = JSON               [ "Comment"                                 ]
    WIKI    = JSON               [ "Wiki"                                    ]
    ##########################################################################
    IT      = QTreeWidgetItem    (                                           )
    ##########################################################################
    IT      . setText            ( 0 , ZONE                                  )
    IT      . setToolTip         ( 0 , UXID                                  )
    IT      . setData            ( 0 , Qt . UserRole , UUID                  )
    ##########################################################################
    IT      . setText            ( 1 , NAME                                  )
    IT      . setToolTip         ( 1 , UXID                                  )
    ##########################################################################
    IT      . setText            ( 2 , COMMENT                               )
    ##########################################################################
    IT      . setText            ( 3 , WIKI                                  )
    ##########################################################################
    IT      . setData            ( 4 , Qt . UserRole , JSON                  )
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
    self   . doubleClicked        ( IT , column                              )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item   , 0                                 )
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , column , msg ,               )
    self   . Go                 ( self . UpdateItem , VAL                    )
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
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      TABLE = self . Tables   [ "Names"                                      ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . OnBusy        . emit    (                                      )
    TZLTAB  = self . Tables           [ "TimeZones"                          ]
    LISTS   =                         [                                      ]
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      N     = NAMEs                   [ UUID                                 ]
      J     =                         { "Uuid"    : int ( UUID )           , \
                                        "Zone"    : ""                     , \
                                        "Name"    : N                      , \
                                        "Comment" : ""                     , \
                                        "Wiki"    : ""                       }
      ########################################################################
      QQ    = f"""select `zonename`,`comment`,`wiki`
                  from {TZLTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 3 ) )          :
        ######################################################################
        J [ "Zone"    ] = self . assureString ( RR [ 0 ]                     )
        J [ "Comment" ] = self . assureString ( RR [ 1 ]                     )
        J [ "Wiki"    ] = self . assureString ( RR [ 2 ]                     )
        ######################################################################
        LISTS . append                ( J                                    )
    ##########################################################################
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames  . emit     ( LISTS                                )
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
    TZLTAB = self . Tables  [ "TimeZones"                                    ]
    ##########################################################################
    QQ     = f"""select `uuid` from {TZLTAB}
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
    TABLE = self . Tables       [ "Names"                                    ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    ##########################################################################
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
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
    TZLTAB  = self . Tables           [ "TimeZones"                          ]
    ##########################################################################
    QQ      = f"select count(*) from {TZLTAB} ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery      ( self                                         ) :
    ##########################################################################
    TZLTAB  = self . Tables [ "TimeZones"                                    ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . Order
    ##########################################################################
    QQ      = f"""select `uuid` from {TZLTAB}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join       ( QQ . split ( )                                 )
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 4 , 3                                     )
    ##########################################################################
    LABELs = self . Translations [ "TimeZoneListings" ] [ "Labels"           ]
    self   . setCentralLabels    ( LABELs                                    )
    ##########################################################################
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
  def UpdateItem                   ( self , item , uuid , column , name    ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TZLTAB  = self . Tables        [ "TimeZones"                             ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    ##########################################################################
    DB      . LockWrites           ( [ TZLTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    ##########################################################################
    if                             ( column in [ 0 , 2 , 3 ]               ) :
      ########################################################################
      if                           ( column == 0                           ) :
        ######################################################################
        QQ  = f"""update {TZLTAB}
                  set `zonename` = %s
                  where ( `uuid` = {uuid} ) ;"""
        ######################################################################
      elif                         ( column == 2                           ) :
        ######################################################################
        QQ  = f"""update {TZLTAB}
                  set `comment` = %s
                  where ( `uuid` = {uuid} ) ;"""
        ######################################################################
      elif                         ( column == 3                           ) :
        ######################################################################
        QQ  = f"""update {TZLTAB}
                  set `wiki` = %s
                  where ( `uuid` = {uuid} ) ;"""
      ########################################################################
      QQ    = " " . join           ( QQ . split ( )                          )
      DB    . QueryValues          ( QQ , ( name , )                         )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                           ( column == 1                           ) :
        ######################################################################
        self . AssureUuidName      ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    self    . Notify               ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def NamingAll                   ( self                                   ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB in [ False , None ]                 ) :
      return
    ##########################################################################
    plan     = None
    if                            ( self . hasPlan ( )                     ) :
      plan   = self . GetPlan     (                                          )
    ##########################################################################
    GURL     = "translate.googleapis.com"
    gt       = Translator         ( service_urls = [ GURL ]                  )
    enUS     = self . LocalityToGoogleLC ( 1001                              )
    zhTW     = self . LocalityToGoogleLC ( 1002                              )
    ##########################################################################
    self     . OnBusy  . emit     (                                          )
    TZLTAB   = self . Tables      [ "TimeZones"                              ]
    ##########################################################################
    QQ       = f"""select `uuid` from {TZLTAB}
                  where ( length(`wiki`) <= 0 )
                  and ( ( `zonename` like "Africa/%" )
                     or ( `zonename` like "America/%" )
                     or ( `zonename` like "Antarctica/%" )
                     or ( `zonename` like "Arctic/%" )
                     or ( `zonename` like "Asia/%" )
                     or ( `zonename` like "Atlantic/%" )
                     or ( `zonename` like "Australia/%" )
                     or ( `zonename` like "Europe/%" )
                     or ( `zonename` like "Indian/%" )
                     or ( `zonename` like "Pacific/%" ) )
                  order by `id` asc ;"""
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
        QQ   = f"""select `zonename` from {TZLTAB}
                   where ( `uuid` = {UUID} ) ;"""
        QQ   = " " . join         ( QQ . split ( )                           )
        DB   . Query              ( QQ                                       )
        RR   = DB . FetchOne      (                                          )
        ######################################################################
        if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )        :
          ####################################################################
          NN = self . assureString ( RR [ 0 ]                                )
          LL = NN . split         ( "/"                                      )
          ####################################################################
          if                      ( len ( LL ) == 2                        ) :
            ##################################################################
            KK    = LL            [ 1                                        ]
            KK    = KK . replace  ( "_" , " "                                )
            ##################################################################
            plan  . ProgressText  ( PID , f"<{KK}>({UUID})"                  )
            ##################################################################
            target   = ""
            ##################################################################
            try                                                              :
              target = gt . translate ( KK , src = enUS , dest = zhTW ) . text
            except                                                           :
              pass
            ##################################################################
            if                    ( len ( target ) > 0                     ) :
              ################################################################
              QQ     = f"""update {TZLTAB}
                           set `wiki` = %s
                           where ( `uuid` = {UUID} ) ;"""
              QQ     = " " . join ( QQ . split ( )                           )
              DB     . QueryValues ( QQ , ( target , )                       )
        ######################################################################
        time . sleep              ( 15.0                                     )
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
    self   . Go                     ( self . Talk , ( MSG , LID , )          )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9004 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
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
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    if                              ( atItem not in [ False , None ]       ) :
      self . AppendRenameAction     ( mm , 1101                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    mm     . addSeparator           (                                        )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunAmountIndexMenu ( )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( self . RunColumnsMenu    ( at )      ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu    ( at )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . startup                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . RenameItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "TimeZones" , uuid , NAM        )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################

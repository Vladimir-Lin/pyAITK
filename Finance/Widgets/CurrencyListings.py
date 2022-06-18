# -*- coding: utf-8 -*-
##############################################################################
## CurrencyListings
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
from   AITK  . Essentials . Relation  import Relation    as Relation
##############################################################################
from   AITK  . Calendars . StarDate   import StarDate    as StarDate
from   AITK  . Calendars . Periode    import Periode     as Periode
from   AITK  . Documents . Identifier import Identifier  as IdentifierItem
##############################################################################
class CurrencyListings             ( TreeDock                              ) :
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
    self . EditAllNames       = None
    self . GType              = 45
    self . ClassTag           = "CurrencyListings"
    self . SortOrder          = "asc"
    self . Countries          =    {                                         }
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 12                                      )
    self . setColumnHidden         (  3 , True                               )
    self . setColumnHidden         (  5 , True                               )
    self . setColumnHidden         (  8 , True                               )
    self . setColumnHidden         (  9 , True                               )
    self . setColumnHidden         ( 10 , True                               )
    self . setColumnHidden         ( 11 , True                               )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setAcceptDrops          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 1024 , 640                              )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    """
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationNames             )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Search"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/search.png" )          )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . Search                            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Crowds"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/viewpeople.png" )      )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationCrowds            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Films"                                  )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/video.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationVideos            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Identifiers"                            )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/tag.png" )             )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationIdentifiers       )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "IdentWebPage"                           )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/webfind.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenIdentifierWebPages            )
    self . WindowActions . append ( A                                        )
    """
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
    ## self . attachActionsTool (                                               )
    ## self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                  ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    ## self . LinkVoice         ( None                                          )
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
    if                          ( column in [ 0 ]                          ) :
      return
    ##########################################################################
    if                          ( column in [ 1 , 2 , 6 , 7 ]              ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [  3 ]                         ) :
      ########################################################################
      LL  = self . Translations [ self . ClassTag ] [ "Usage"                ]
      val = item . data         ( column , Qt . UserRole                     )
      val = int                 ( val                                        )
      cb  = self . setComboBox  ( item                                       ,
                                  column                                     ,
                                  "activated"                                ,
                                  self . usageChanged                        )
      cb  . addJson             ( LL , val                                   )
      cb  . setMaxVisibleItems  ( 20                                         )
      cb  . showPopup           (                                            )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [  4 ]                         ) :
      ########################################################################
      LL  = self . Translations [ self . ClassTag ] [ "Types"                ]
      val = item . data         ( column , Qt . UserRole                     )
      val = int                 ( val                                        )
      cb  = self . setComboBox  ( item                                       ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . typesChanged                       )
      cb  . addJson             ( LL , val                                   )
      cb  . setMaxVisibleItems  ( 20                                         )
      cb  . showPopup           (                                            )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [  5 ]                         ) :
      ########################################################################
      sb  = self . setSpinBox   ( item                                       ,
                                  column                                     ,
                                  0                                          ,
                                  999999999                                  ,
                                  "editingFinished"                          ,
                                  self . preferChanged                       )
      sb  . setAlignment        ( Qt . AlignRight                            )
      sb  . setFocus            ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    ## 國家
    ##########################################################################
    if                          ( column in [  8 ]                         ) :
      ########################################################################
      val = item . data         ( column , Qt . UserRole                     )
      val = int                 ( val                                        )
      cb  = self . setComboBox  ( item                                       ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . countryChanged                     )
      cb  . addJson             ( self . Countries , val                     )
      cb  . setMaxVisibleItems  ( 30                                         )
      cb  . showPopup           (                                            )
      ########################################################################
      return
    ##########################################################################
    ## 開始
    ##########################################################################
    if                          ( column in [  9 ]                         ) :
      ########################################################################
      ########################################################################
      return
    ##########################################################################
    ## 消亡
    ##########################################################################
    if                          ( column in [ 10 ]                         ) :
      ########################################################################
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent          ( self , IT , ITEM                       ) :
    ##########################################################################
    TRX     = self . Translations [ self . ClassTag                          ]
    ##########################################################################
    ID      = ITEM                [ "Id"                                     ]
    UUID    = ITEM                [ "Uuid"                                   ]
    USED    = ITEM                [ "Used"                                   ]
    TYPE    = ITEM                [ "Type"                                   ]
    PREFER  = ITEM                [ "Prefer"                                 ]
    NAME    = ITEM                [ "Name"                                   ]
    NUMBER  = ITEM                [ "Number"                                 ]
    START   = ITEM                [ "Start"                                  ]
    VANISH  = ITEM                [ "Vanish"                                 ]
    COUNTRY = ITEM                [ "Country"                                ]
    ENGLISH = ITEM                [ "English"                                ]
    NATIVE  = ITEM                [ "Native"                                 ]
    UXID    = str                 ( UUID                                     )
    ##########################################################################
    NOW     = StarDate            (                                          )
    TZ      = self . Settings     [ "TimeZone"                               ]
    ##########################################################################
    SDT     = ""
    if                            ( START  > 0                             ) :
      ########################################################################
      NOW   . Stardate = START
      SDT   = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"    )
    ##########################################################################
    VDT     = ""
    if                            ( VANISH > 0                             ) :
      ########################################################################
      NOW   . Stardate = VANISH
      VDT   = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"    )
    ##########################################################################
    UNAME   = TRX                 [ "Usage" ] [ str ( USED )                 ]
    TNAME   = TRX                 [ "Types" ] [ str ( TYPE )                 ]
    ##########################################################################
    CNAME   = ""
    if                            ( COUNTRY in self . Countries            ) :
      CNAME = self . Countries    [ COUNTRY                                  ]
    ##########################################################################
    IT      . setText             (  0 , str ( ID      )                     )
    IT      . setToolTip          (  0 , UXID                                )
    IT      . setData             (  0 , Qt . UserRole , UXID                )
    IT      . setTextAlignment    (  0 , Qt . AlignRight                     )
    ##########################################################################
    IT      . setText             (  1 , NAME                                )
    ##########################################################################
    IT      . setText             (  2 , NUMBER                              )
    ##########################################################################
    IT      . setText             (  3 , UNAME                               )
    IT      . setData             (  3 , Qt . UserRole , USED                )
    ##########################################################################
    IT      . setText             (  4 , TNAME                               )
    IT      . setData             (  4 , Qt . UserRole , TYPE                )
    ##########################################################################
    IT      . setText             (  5 , str ( PREFER  )                     )
    IT      . setData             (  5 , Qt . UserRole , UXID                )
    IT      . setTextAlignment    (  5 , Qt . AlignRight                     )
    ##########################################################################
    IT      . setText             (  6 , ENGLISH                             )
    ##########################################################################
    IT      . setText             (  7 , NATIVE                              )
    ##########################################################################
    IT      . setText             (  8 , CNAME                               )
    IT      . setData             (  8 , Qt . UserRole , str ( COUNTRY )     )
    ##########################################################################
    IT      . setText             (  9 , str ( SDT     )                     )
    ##########################################################################
    IT      . setText             ( 10 , str ( VDT     )                     )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , ITEM                                ) :
    ##########################################################################
    IT   = QTreeWidgetItem    (                                              )
    self . PrepareItemContent ( IT   , ITEM                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    self . Go                    ( self . AppendCurrency                     )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def RenameItem              ( self                                       ) :
    ##########################################################################
    IT   = self . currentItem (                                              )
    if                        ( IT is None                                 ) :
      return
    ##########################################################################
    self . doubleClicked      ( IT , self . currentColumn ( )                )
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
    VAL    =                     ( item , column , uuid , msg ,              )
    self   . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    return
  ############################################################################
  def usageChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      uuid = int                 ( item . data ( 0 , Qt . UserRole )         )
      LL   = self . Translations [ self . ClassTag ] [ "Usage"               ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      VAL  =                     ( item , column , uuid , value ,            )
      self . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def typesChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      uuid = int                 ( item . data ( 0 , Qt . UserRole )         )
      LL   = self . Translations [ self . ClassTag ] [ "Types"               ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      VAL  =                     ( item , column , uuid , value ,            )
      self . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def countryChanged             ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      uuid = int                 ( item . data ( 0 , Qt . UserRole )         )
      msg  = self . Countries    [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      VAL  =                     ( item , column , uuid , value ,            )
      self . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def preferChanged             ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    sb     = self . CurrentItem [ "Widget"                                   ]
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      uuid = int                ( item . data ( 0 , Qt . UserRole )          )
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      VAL  =                    ( item , column , uuid , nv ,                )
      self . Go                 ( self . AssureUuidItem , VAL                )
    ##########################################################################
    self . removeParked         (                                            )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  def LoadCountries              ( self , DB                               ) :
    ##########################################################################
    if                           ( 0 in self . Countries                   ) :
      return
    ##########################################################################
    MSG    = self . getMenuItem  ( "NoCountry"                               )
    self   . Countries [ 0 ] = MSG
    ##########################################################################
    NAMTAB = self . Tables       [ "Names"                                   ]
    CTYTAB = self . Tables       [ "ISO-4217"                                ]
    QQ     = f"""select `uuid` from {CTYTAB} where ( `used` > 0 ) ;"""
    UUIDs  = DB . ObtainUuids    ( QQ                                        )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME = self . GetName      ( DB , NAMTAB , UUID                        )
      self . Countries [ int ( UUID ) ] = NAME
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for ITEM in LISTS                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( ITEM                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def loading                          ( self                              ) :
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      self . emitNamesShow . emit      (                                     )
      return
    ##########################################################################
    self    . Notify                   ( 3                                   )
    ##########################################################################
    FMT     = self . Translations      [ "UI::StartLoading"                  ]
    MSG     = FMT . format             ( self . windowTitle ( )              )
    self    . ShowStatus               ( MSG                                 )
    self    . OnBusy  . emit           (                                     )
    self    . setBustle                (                                     )
    ##########################################################################
    self    . LoadCountries            ( DB                                  )
    ##########################################################################
    ISOTAB  = self . Tables            [ "ISO-4217"                          ]
    ORDER   = self . SortOrder
    COLS    = "`id`,`uuid`,`used`,`type`,`prefer`,`name`,`number`,`start`,`vanish`,`country`,`english`,`native`"
    QQ      = f"select {COLS} from {ISOTAB} order by `id` {ORDER} ;"
    DB      . Query                    ( QQ                                  )
    ALL     = DB . FetchAll            (                                     )
    ##########################################################################
    LISTS   =                          [                                     ]
    for C in ALL                                                             :
      ########################################################################
      J     = { "Id"      : int                 ( C [  0 ]                 ) ,
                "Uuid"    : int                 ( C [  1 ]                 ) ,
                "Used"    : int                 ( C [  2 ]                 ) ,
                "Type"    : int                 ( C [  3 ]                 ) ,
                "Prefer"  : int                 ( C [  4 ]                 ) ,
                "Name"    : self . assureString ( C [  5 ]                 ) ,
                "Number"  : self . assureString ( C [  6 ]                 ) ,
                "Start"   : int                 ( C [  7 ]                 ) ,
                "Vanish"  : int                 ( C [  8 ]                 ) ,
                "Country" : int                 ( C [  9 ]                 ) ,
                "English" : self . assureString ( C [ 10 ]                 ) ,
                "Native"  : self . assureString ( C [ 11 ]                 ) }
      LISTS . append                   ( J                                   )
    ##########################################################################
    self    . setVacancy               (                                     )
    self    . GoRelax . emit           (                                     )
    self    . ShowStatus               ( ""                                  )
    DB      . Close                    (                                     )
    ##########################################################################
    if                                 ( len ( LISTS ) <= 0                ) :
      self . emitNamesShow . emit      (                                     )
      return
    ##########################################################################
    self   . emitAllNames  . emit      ( LISTS                               )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 11                             )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , column , uuid , name         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( None )                    ) :
      return
    ##########################################################################
    ISOTAB = self . Tables    [ "ISO-4217"                                   ]
    ##########################################################################
    DB     . LockWrites       ( [ ISOTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    VAL    =                  ( name ,                                       )
    COL    = ""
    ##########################################################################
    if                        ( column ==  1                               ) :
      COL  = "name"
    elif                      ( column ==  2                               ) :
      COL  = "number"
    elif                      ( column ==  3                               ) :
      COL  = "used"
    elif                      ( column ==  4                               ) :
      COL  = "type"
    elif                      ( column ==  5                               ) :
      COL  = "name"
    elif                      ( column ==  6                               ) :
      COL  = "prefer"
    elif                      ( column ==  7                               ) :
      COL  = "native"
    elif                      ( column ==  8                               ) :
      COL  = "country"
    elif                      ( column ==  9                               ) :
      COL  = "start"
    elif                      ( column == 10                               ) :
      COL  = "vanish"
    ##########################################################################
    if                        ( len ( COL ) > 0                            ) :
      ########################################################################
      QQ   = f"""update {ISOTAB}
                     set `{COL}` = %s
                     where ( `uuid` = {uuid} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . QueryValues      ( QQ , VAL                                     )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AppendCurrency          ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    ISOTAB = self . Tables    [ "ISO-4217"                                   ]
    ##########################################################################
    CUID   = DB . LastUuid    ( ISOTAB , "uuid" , 4110000000100000000        )
    ID     = int              ( int ( CUID ) % 10000000                      )
    DB     . LockWrites       ( [ ISOTAB                                   ] )
    ##########################################################################
    QQ     = f"""insert into {ISOTAB} ( `id` , `uuid` , `used` , `type`  )
                 values ( {ID} , {CUID} , 3 , 7 ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def BuildTable ( self ) :
    ##########################################################################
    BASE  = 4110000000100000000
    LISTS = [ [ ""    , ""    ] ,
              [ "AED" , "784" ] ,
              [ "AFN" , "971" ] ,
              [ "ALL" , "008" ] ,
              [ "AMD" , "051" ] ,
              [ "ANG" , "532" ] ,
              [ "AOA" , "973" ] ,
              [ "ARS" , "032" ] ,
              [ "AUD" , "036" ] ,
              [ "AWG" , "533" ] ,
              [ "AZN" , "944" ] ,
              [ "BAM" , "977" ] ,
              [ "BBD" , "052" ] ,
              [ "BDT" , "050" ] ,
              [ "BGN" , "975" ] ,
              [ "BHD" , "048" ] ,
              [ "BIF" , "108" ] ,
              [ "BMD" , "060" ] ,
              [ "BND" , "096" ] ,
              [ "BOB" , "068" ] ,
              [ "BOV" , "984" ] ,
              [ "BRL" , "986" ] ,
              [ "BSD" , "044" ] ,
              [ "BTN" , "064" ] ,
              [ "BWP" , "072" ] ,
              [ "BYN" , "933" ] ,
              [ "BZD" , "084" ] ,
              [ "CAD" , "124" ] ,
              [ "CDF" , "976" ] ,
              [ "CHE" , "947" ] ,
              [ "CHF" , "756" ] ,
              [ "CHW" , "948" ] ,
              [ "CLF" , "990" ] ,
              [ "CLP" , "152" ] ,
              [ "COP" , "170" ] ,
              [ "COU" , "970" ] ,
              [ "CRC" , "188" ] ,
              [ "CUC" , "931" ] ,
              [ "CUP" , "192" ] ,
              [ "CVE" , "132" ] ,
              [ "CZK" , "203" ] ,
              [ "DJF" , "262" ] ,
              [ "DKK" , "208" ] ,
              [ "DOP" , "214" ] ,
              [ "DZD" , "012" ] ,
              [ "EGP" , "818" ] ,
              [ "ERN" , "232" ] ,
              [ "ETB" , "230" ] ,
              [ "EUR" , "978" ] ,
              [ "FJD" , "242" ] ,
              [ "FKP" , "238" ] ,
              [ "GEL" , "981" ] ,
              [ "GHS" , "936" ] ,
              [ "GIP" , "292" ] ,
              [ "GMD" , "270" ] ,
              [ "GNF" , "324" ] ,
              [ "GTQ" , "320" ] ,
              [ "GYD" , "328" ] ,
              [ "HKD" , "344" ] ,
              [ "HNL" , "340" ] ,
              [ "HRK" , "191" ] ,
              [ "HTG" , "332" ] ,
              [ "HUF" , "348" ] ,
              [ "IDR" , "360" ] ,
              [ "ILS" , "376" ] ,
              [ "INR" , "356" ] ,
              [ "IQD" , "368" ] ,
              [ "IRR" , "364" ] ,
              [ "ISK" , "352" ] ,
              [ "JMD" , "388" ] ,
              [ "JOD" , "400" ] ,
              [ "JPY" , "392" ] ,
              [ "KES" , "404" ] ,
              [ "KGS" , "417" ] ,
              [ "KHR" , "116" ] ,
              [ "KMF" , "174" ] ,
              [ "KPW" , "408" ] ,
              [ "KRW" , "410" ] ,
              [ "KWD" , "414" ] ,
              [ "KYD" , "136" ] ,
              [ "KZT" , "398" ] ,
              [ "LAK" , "418" ] ,
              [ "LBP" , "422" ] ,
              [ "LKR" , "144" ] ,
              [ "LRD" , "430" ] ,
              [ "LSL" , "426" ] ,
              [ "LYD" , "434" ] ,
              [ "MAD" , "504" ] ,
              [ "MDL" , "498" ] ,
              [ "MGA" , "969" ] ,
              [ "MKD" , "807" ] ,
              [ "MMK" , "104" ] ,
              [ "MNT" , "496" ] ,
              [ "MOP" , "446" ] ,
              [ "MRU" , "929" ] ,
              [ "MUR" , "480" ] ,
              [ "MVR" , "462" ] ,
              [ "MWK" , "454" ] ,
              [ "MXN" , "484" ] ,
              [ "MXV" , "979" ] ,
              [ "MYR" , "458" ] ,
              [ "MZN" , "943" ] ,
              [ "NAD" , "516" ] ,
              [ "NGN" , "566" ] ,
              [ "NIO" , "558" ] ,
              [ "NOK" , "578" ] ,
              [ "NPR" , "524" ] ,
              [ "NZD" , "554" ] ,
              [ "OMR" , "512" ] ,
              [ "PAB" , "590" ] ,
              [ "PEN" , "604" ] ,
              [ "PGK" , "598" ] ,
              [ "PHP" , "608" ] ,
              [ "PKR" , "586" ] ,
              [ "PLN" , "985" ] ,
              [ "PYG" , "600" ] ,
              [ "QAR" , "634" ] ,
              [ "RON" , "946" ] ,
              [ "RSD" , "941" ] ,
              [ "CNY" , "156" ] ,
              [ "RUB" , "643" ] ,
              [ "RWF" , "646" ] ,
              [ "SAR" , "682" ] ,
              [ "SBD" , "090" ] ,
              [ "SCR" , "690" ] ,
              [ "GBP" , "826" ] ,
              [ "SDG" , "938" ] ,
              [ "SEK" , "752" ] ,
              [ "SGD" , "702" ] ,
              [ "SHP" , "654" ] ,
              [ "SLL" , "694" ] ,
              [ "SOS" , "706" ] ,
              [ "SRD" , "968" ] ,
              [ "SSP" , "728" ] ,
              [ "STN" , "930" ] ,
              [ "SVC" , "222" ] ,
              [ "SYP" , "760" ] ,
              [ "SZL" , "748" ] ,
              [ "THB" , "764" ] ,
              [ "TJS" , "972" ] ,
              [ "TMT" , "934" ] ,
              [ "TND" , "788" ] ,
              [ "TOP" , "776" ] ,
              [ "TRY" , "949" ] ,
              [ "TTD" , "780" ] ,
              [ "TWD" , "901" ] ,
              [ "TZS" , "834" ] ,
              [ "UAH" , "980" ] ,
              [ "UGX" , "800" ] ,
              [ "USD" , "840" ] ,
              [ "USN" , "997" ] ,
              [ "UYI" , "940" ] ,
              [ "UYU" , "858" ] ,
              [ "UYW" , "927" ] ,
              [ "UZS" , "860" ] ,
              [ "VED" , "926" ] ,
              [ "VES" , "928" ] ,
              [ "VND" , "704" ] ,
              [ "VUV" , "548" ] ,
              [ "WST" , "882" ] ,
              [ "XAF" , "950" ] ,
              [ "XAG" , "961" ] ,
              [ "XAU" , "959" ] ,
              [ "XBA" , "955" ] ,
              [ "XBB" , "956" ] ,
              [ "XBC" , "957" ] ,
              [ "XBD" , "958" ] ,
              [ "XCD" , "951" ] ,
              [ "XDR" , "960" ] ,
              [ "XOF" , "952" ] ,
              [ "XPD" , "964" ] ,
              [ "XPF" , "953" ] ,
              [ "XPT" , "962" ] ,
              [ "XSU" , "994" ] ,
              [ "XTS" , "963" ] ,
              [ "XUA" , "965" ] ,
              [ "XXX" , "999" ] ,
              [ "YER" , "886" ] ,
              [ "ZAR" , "710" ] ,
              [ "ZMW" , "967" ] ,
              [ "ZWL" , "932" ]                                              ]
    ##########################################################################
    DB         = self . ConnectDB (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    ID     = 0
    for C in LISTS                                                           :
      ########################################################################
      N    = C                    [ 0                                        ]
      D    = C                    [ 1                                        ]
      QQ   = f"""insert into `iso_4217`
                 ( `id` , `uuid` , `used` , `type` , `prefer` , `name` , `number` )
                 values
                 ( {ID} , {BASE} , 1 , 1 , {ID} , '{N}' , '{D}' ) ;"""
      QQ   = " " . join           ( QQ . split ( )                           )
      DB   . Query                ( QQ                                       )
      ########################################################################
      ID   = ID   + 1
      BASE = BASE + 1
    ##########################################################################
    DB         . Close            (                                          )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9012 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                          ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                     )
    if                              ( not doMenu                          ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager            ( self                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    self   . AppendInsertAction     ( mm , 1101                              )
    self   . AppendRenameAction     ( mm , 1102                              )
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
    OKAY   = self   . RunAmountIndexMenu (                                   )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking      ( mm , aa                                )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . Countries =            {                                        }
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      self . RenameItem             (                                        )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      ########################################################################
      uuid = self . itemUuid       ( atItem , 0                              )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Currency" , uuid , NAM          )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

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
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QFileDialog
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
    self . LinkAction ( "Import"     , self . ImportItems     , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
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
    if                          ( column in [ 3 ]                          ) :
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
    if                          ( column in [ 4 ]                          ) :
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
    if                          ( column in [ 5 ]                          ) :
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
    if                          ( column in [ 8 ]                          ) :
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
    ## 開始及消亡
    ##########################################################################
    if                          ( column in [ 9 , 10 ]                     ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . dateChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
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
      print("Start:",NOW.Timestamp())
      SDT   = NOW . toDateString  ( TZ , "%Y/%m/%d"                          )
    ##########################################################################
    VDT     = ""
    if                            ( VANISH > 0                             ) :
      ########################################################################
      NOW   . Stardate = VANISH
      print("Vanish:",NOW.Timestamp())
      VDT   = NOW . toDateString  ( TZ , "%Y/%m/%d"                          )
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
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    VAL    =                     ( item , column , uuid , msg ,              )
    self   . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
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
  @pyqtSlot                      (                                           )
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
  @pyqtSlot                      (                                           )
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
      msg  = self . Countries    [ int ( value )                             ]
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
  @pyqtSlot                     (                                            )
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
  @pyqtSlot                      (                                           )
  def dateChanged                ( self                                    ) :
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
    value  = 0
    ##########################################################################
    if                           ( len ( msg ) > 0                         ) :
      ########################################################################
      NOW   = StarDate           (                                           )
      TZ    = self . Settings    [ "TimeZone"                                ]
      ########################################################################
      try                                                                    :
        ######################################################################
        NOW   . fromInput        ( f"{msg}T00:00:00" , TZ                    )
        value = NOW . Stardate
        msg   = NOW . toDateString ( TZ , "%Y/%m/%d"                         )
        ######################################################################
      except                                                                 :
        msg   = ""
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    VAL    =                     ( item , column , uuid , value ,            )
    self   . Go                  ( self . AssureUuidItem , VAL               )
    ##########################################################################
    return
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
    CTYTAB = self . Tables       [ "Countries"                               ]
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
    self . setColumnWidth ( 0 ,  60                                          )
    self . setColumnWidth ( 1 ,  60                                          )
    self . setColumnWidth ( 2 ,  60                                          )
    self . setColumnWidth ( 3 ,  60                                          )
    self . setColumnWidth ( 4 , 100                                          )
    self . setColumnWidth ( 5 , 100                                          )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , column , uuid , name         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
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
      COL  = "prefer"
    elif                      ( column ==  6                               ) :
      COL  = "english"
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
                 values ( {ID} , {CUID} , 3 , 8 ) ;"""
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
  def AppendCurrencyItems       ( self , text                              ) :
    ##########################################################################
    LINEs    = text . split     ( "\n"                                       )
    if                          ( len ( LINEs ) <= 0                       ) :
      return
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    ISOTAB   = self . Tables    [ "ISO-4217"                                 ]
    ##########################################################################
    CUID     = DB . LastUuid    ( ISOTAB , "uuid" , 4110000000100000000      )
    DB       . LockWrites       ( [ ISOTAB                                 ] )
    ##########################################################################
    for LINE in LINEs                                                        :
      ########################################################################
      KKs    = LINE . split     (                                            )
      if                        ( len ( KKs ) <= 0                         ) :
        continue
      ########################################################################
      NAME   = ""
      NUM    = ""
      ########################################################################
      if                        ( len ( KKs ) > 0                          ) :
        NAME = self . assureString ( KKs [ 0 ]                               )
      ########################################################################
      if                        ( len ( KKs ) > 1                          ) :
        NUM  = self . assureString ( KKs [ 1 ]                               )
      ########################################################################
      ID     = int              ( int ( CUID ) % 10000000                    )
      ########################################################################
      QQ     = f"""insert into {ISOTAB}
                   ( `id` , `uuid` , `used` , `type` , `prefer` , `name` , `number`  )
                   values
                   ( {ID} , {CUID} , 3 , 8 , {ID} , '{NAME}' , '{NUM}' ) ;"""
      QQ     = " " . join       ( QQ . split ( )                             )
      DB     . Query            ( QQ                                         )
      ########################################################################
      CUID   = int ( CUID ) + 1
    ##########################################################################
    DB       . UnlockTables     (                                            )
    DB       . Close            (                                            )
    ##########################################################################
    self     . loading          (                                            )
    ##########################################################################
    return
  ############################################################################
  def ImportItems                           ( self                         ) :
    ##########################################################################
    TITLE   = self . getMenuItem            ( "ImportCurrencies"             )
    FILTERS = self . getMenuItem            ( "CurrencyFilters"              )
    F , _   = QFileDialog . getOpenFileName ( self , TITLE , "" , FILTERS    )
    ##########################################################################
    if                                      ( len ( F ) <= 0               ) :
      return
    ##########################################################################
    T       = ""
    try                                                                      :
      ########################################################################
      with open                             ( F , "rb" ) as J                :
        T   = J . read                      (                                )
    except                                                                   :
      self . Notify                         ( 2                              )
      return
    ##########################################################################
    T       = self . assureString           ( T                              )
    if                                      ( len ( T ) <= 0               ) :
      self . Notify                         ( 2                              )
      return
    ##########################################################################
    self   . Go ( self . AppendCurrencyItems , ( T , )                       )
    ##########################################################################
    return
  ############################################################################
  def PasteItems        ( self                                             ) :
    ##########################################################################
    self . defaultPaste ( self . AppendCurrencyItems                         )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
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
  def Menu                            ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                   )
    if                                ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    self   . AmountIndexMenu          ( mm                                   )
    self   . AppendRefreshAction      ( mm , 1001                            )
    self   . AppendInsertAction       ( mm , 1101                            )
    ##########################################################################
    msg    = self . getMenuItem       ( "ModifyItem"                         )
    mm     . addAction                ( 1102 , msg                           )
    ##########################################################################
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    ##########################################################################
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . ColumnsMenu              ( mm                                   )
    self   . SortingMenu              ( mm                                   )
    self   . LocalityMenu             ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    OKAY   = self   . RunAmountIndexMenu (                                   )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking        ( mm , aa                              )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                ( OKAY                               ) :
      ########################################################################
      self . Countries =              {                                      }
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu    ( at                                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu    ( at                                   )
    if                                ( OKAY                               ) :
      self . restart                  (                                      )
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      self . restart                  (                                      )
      return True
    ##########################################################################
    if                                ( at == 1101                         ) :
      self . InsertItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1102                         ) :
      self . RenameItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1601                         ) :
      ########################################################################
      uuid = self . itemUuid          ( atItem , 0                           )
      NAM  = self . Tables            [ "NamesEditing"                       ]
      self . EditAllNames             ( self , "Currency" , uuid , NAM       )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

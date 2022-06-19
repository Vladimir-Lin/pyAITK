# -*- coding: utf-8 -*-
##############################################################################
## CurrencyPairListings
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
class CurrencyPairListings         ( TreeDock                              ) :
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
    self . GType              = 46
    self . ClassTag           = "CurrencyPairListings"
    self . SortOrder          = "asc"
    self . DoReverse          = True
    self . DoDissect          = True
    self . Currencies         =    {                                         }
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 7                                       )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 6 , True                                )
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
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
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
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 1 ]                          ) :
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
    if                          ( column in [ 2 ]                          ) :
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
    if                          ( column in [ 3 ]                          ) :
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
    ## 貨幣選擇
    ##########################################################################
    if                          ( column in [ 4 , 5 ]                      ) :
      ########################################################################
      val = item . data         ( column , Qt . UserRole                     )
      val = int                 ( val                                        )
      cb  = self . setComboBox  ( item                                       ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . currencyChanged                    )
      cb  . addJson             ( self . Currencies , val                    )
      cb  . setMaxVisibleItems  ( 30                                         )
      cb  . showPopup           (                                            )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent          ( self , IT , ITEM                       ) :
    ##########################################################################
    TRX     = self . Translations [ self . ClassTag                          ]
    ##########################################################################
    UUID    = ITEM                [ "Uuid"                                   ]
    USAGE   = ITEM                [ "Usage"                                  ]
    TYPE    = ITEM                [ "Type"                                   ]
    PREFER  = ITEM                [ "Prefer"                                 ]
    SOURCE  = ITEM                [ "Source"                                 ]
    TARGET  = ITEM                [ "Target"                                 ]
    REVERSE = ITEM                [ "Reverse"                                ]
    SYMBOL  = ITEM                [ "Symbol"                                 ]
    UXID    = str                 ( UUID                                     )
    ##########################################################################
    UNAME   = TRX                 [ "Usage" ] [ str ( USAGE )                ]
    TNAME   = TRX                 [ "Types" ] [ str ( TYPE  )                ]
    SNAME   = self . Currencies   [ SOURCE                                   ]
    GNAME   = self . Currencies   [ TARGET                                   ]
    ##########################################################################
    PNAME   = ""
    if                            ( PREFER >= 0                            ) :
      PNAME = str                 ( PREFER                                   )
    ##########################################################################
    IT      . setText             ( 0 , SYMBOL                               )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    ##########################################################################
    IT      . setText             ( 1 , TNAME                                )
    IT      . setData             ( 1 , Qt . UserRole , TYPE                 )
    ##########################################################################
    IT      . setText             ( 2 , UNAME                                )
    IT      . setData             ( 2 , Qt . UserRole , USAGE                )
    ##########################################################################
    IT      . setText             (  3 , PNAME                               )
    IT      . setData             (  3 , Qt . UserRole , PREFER              )
    IT      . setTextAlignment    (  3 , Qt . AlignRight                     )
    ##########################################################################
    IT      . setText             ( 4 , SNAME                                )
    IT      . setData             ( 4 , Qt . UserRole , SOURCE               )
    ##########################################################################
    IT      . setText             ( 5 , GNAME                                )
    IT      . setData             ( 5 , Qt . UserRole , TARGET               )
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
  @pyqtSlot                   (                                              )
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
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
  @pyqtSlot                       (                                          )
  def nameChanged                 ( self                                   ) :
    ##########################################################################
    if                            ( not self . isItemPicked ( )            ) :
      return False
    ##########################################################################
    item   = self . CurrentItem   [ "Item"                                   ]
    column = self . CurrentItem   [ "Column"                                 ]
    line   = self . CurrentItem   [ "Widget"                                 ]
    text   = self . CurrentItem   [ "Text"                                   ]
    msg    = line . text          (                                          )
    uuid   = self . itemUuid      ( item , 0                                 )
    uuid   = int                  ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      ########################################################################
      if ( ( len ( msg ) <= 0 ) or ( not self . DoDissect ) )                :
        ######################################################################
        self . removeTopLevelItem ( item                                     )
        ######################################################################
        return
      ########################################################################
      if                          ( not self . isCurrencyPair ( msg )      ) :
        ######################################################################
        self . removeTopLevelItem ( item                                     )
        self . Notify             ( 2                                        )
        ######################################################################
        return
    ##########################################################################
    item   . setText              ( column ,              msg                )
    self   . removeParked         (                                          )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      ########################################################################
      VAL  =                      ( msg ,                                    )
      self . Go                   ( self . AppendEmptyPair , VAL             )
      ########################################################################
    else                                                                     :
      ########################################################################
      VAL  =                     ( item , column , uuid , msg ,              )
      self . Go                  ( self . AssureUuidItem , VAL               )
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
  def currencyChanged            ( self                                    ) :
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
  def LoadCurrencies               ( self , DB                             ) :
    ##########################################################################
    if                             ( len ( self . Currencies ) > 0         ) :
      return
    ##########################################################################
    self . Currencies [ 0 ] = self . getMenuItem ( "NoCurrency"              )
    ##########################################################################
    ISOTAB   = self . Tables       [ "ISO-4217"                              ]
    NAMTAB   = self . Tables       [ "Names"                                 ]
    UUIDs    =                     [                                         ]
    ##########################################################################
    QQ       = f"""select `uuid`,`name` from {ISOTAB}
                   where ( `used` > 0 )
                   order by `prefer` asc ;"""
    QQ       = " " . join          ( QQ . split ( )                          )
    DB       . Query               ( QQ                                      )
    ALL      = DB . FetchAll       (                                         )
    ##########################################################################
    if                             ( self . NotOkay ( ALL )                ) :
      return
    ##########################################################################
    if                             ( len            ( ALL ) <= 0           ) :
      return
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      UUID   = int                 ( R [ 0                                 ] )
      NAME   = self . assureString ( R [ 1                                 ] )
      UUIDs  . append              ( UUID                                    )
      ########################################################################
      self   . Currencies [ UUID ] = NAME
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME   = self . GetName      ( DB , NAMTAB , UUID                      )
      ########################################################################
      if                           ( len ( NAME ) > 0                      ) :
        ######################################################################
        self . Currencies [ UUID ] = NAME
    ##########################################################################
    return
  ############################################################################
  def loading                     ( self                                   ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    if                            ( self . NotOkay ( DB )                  ) :
      self . emitNamesShow . emit (                                          )
      return
    ##########################################################################
    self   . Notify               ( 3                                        )
    ##########################################################################
    FMT    = self . Translations  [ "UI::StartLoading"                       ]
    MSG    = FMT . format         ( self . windowTitle ( )                   )
    self   . ShowStatus           ( MSG                                      )
    self   . OnBusy  . emit       (                                          )
    self   . setBustle            (                                          )
    ##########################################################################
    self   . LoadCurrencies       ( DB                                       )
    ##########################################################################
    CRPTAB = self . Tables        [ "CurrencyPairs"                          ]
    LISTS  =                      [                                          ]
    ##########################################################################
    COLS   = "`uuid`,`used`,`type`,`prefer`,`source`,`target`,`reverse`,`symbol`"
    QQ     = f"select {COLS} from {CRPTAB} order by `id` asc ;"
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . Query                ( QQ                                       )
    ALL    = DB . FetchAll        (                                          )
    ##########################################################################
    if ( ( self . IsOkay ( ALL ) ) and ( len ( ALL ) > 0 ) )                 :
      ########################################################################
      for R in ALL                                                           :
        ######################################################################
        J  = { "Uuid"    : int                 ( R [ 0 ]                 ) , \
               "Usage"   : int                 ( R [ 1 ]                 ) , \
               "Type"    : int                 ( R [ 2 ]                 ) , \
               "Prefer"  : int                 ( R [ 3 ]                 ) , \
               "Source"  : int                 ( R [ 4 ]                 ) , \
               "Target"  : int                 ( R [ 5 ]                 ) , \
               "Reverse" : int                 ( R [ 6 ]                 ) , \
               "Symbol"  : self . assureString ( R [ 7 ]                 )   }
        LISTS . append            ( J                                        )
    ##########################################################################
    self   . setVacancy           (                                          )
    self   . GoRelax . emit       (                                          )
    self   . ShowStatus           ( ""                                       )
    DB     . Close                (                                          )
    ##########################################################################
    if                            ( len ( LISTS ) <= 0                     ) :
      self . emitNamesShow . emit (                                          )
      return
    ##########################################################################
    self   . emitAllNames  . emit ( LISTS                                    )
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
    self . defaultPrepare ( self . ClassTag , 6                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , column , uuid , name         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    CRYTAB = self . Tables    [ "CurrencyPairs"                              ]
    ##########################################################################
    DB     . LockWrites       ( [ CRYTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    VAL    =                  ( name ,                                       )
    COL    = ""
    ##########################################################################
    if                        ( column ==  0                               ) :
      COL  = "symbol"
    elif                      ( column ==  1                               ) :
      COL  = "type"
    elif                      ( column ==  2                               ) :
      COL  = "used"
    elif                      ( column ==  3                               ) :
      COL  = "prefer"
    elif                      ( column ==  4                               ) :
      COL  = "source"
    elif                      ( column ==  5                               ) :
      COL  = "target"
    ##########################################################################
    if                        ( len ( COL ) > 0                            ) :
      ########################################################################
      QQ   = f"""update {CRYTAB}
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
  def GetCurrencyUuid      ( self , DB , CURRENCY                          ) :
    ##########################################################################
    ISOTAB = self . Tables [ "ISO-4217"                                      ]
    QQ     = f"select `uuid` from {ISOTAB} where ( `name` = '{CURRENCY}' ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if                     ( self . NotOkay ( RR )                         ) :
      return 0
    ##########################################################################
    if                     ( len ( RR ) != 1                               ) :
      return 0
    ##########################################################################
    UUID   = 0
    ##########################################################################
    try                                                                      :
      UUID = int           ( RR [ 0                                        ] )
    except                                                                   :
      return 0
    ##########################################################################
    return UUID
  ############################################################################
  def GetCurrencyPair      ( self , DB , FromCurrency , ToCurrency         ) :
    ##########################################################################
    CRPTAB = self . Tables [ "CurrencyPairs"                                 ]
    QQ     = f"""select `uuid` from {CRPTAB}
                 where ( `source` = {FromCurrency} )
                   and ( `target` = {ToCurrency} )
                   and ( `used` > 0 ) ;"""
    QQ     = " " . join    ( QQ . split ( )                                  )
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if                     ( self . NotOkay ( RR )                         ) :
      return 0
    ##########################################################################
    if                     ( len ( RR ) != 1                               ) :
      return 0
    ##########################################################################
    UUID   = 0
    ##########################################################################
    try                                                                      :
      UUID = int           ( RR [ 0                                        ] )
    except                                                                   :
      return 0
    ##########################################################################
    return UUID
  ############################################################################
  def AppendCurrencyPair   ( self                                          , \
                             DB                                            , \
                             FromCurrency                                  , \
                             FUID                                          , \
                             ToCurrency                                    , \
                             TUID                                          ) :
    ##########################################################################
    CRPTAB = self . Tables [ "CurrencyPairs"                                 ]
    CUID   = DB . LastUuid ( CRPTAB , "uuid" , 4110000000200000000           )
    ##########################################################################
    QQ     = f"""insert into {CRPTAB}
                 ( `uuid` , `type` , `source` , `target` , `symbol` ) values
                 ( {CUID} , 9 , {FUID} , {TUID} , '{FromCurrency}/{ToCurrency}' ) ;"""
    QQ     = " " . join    ( QQ . split ( )                                  )
    ##########################################################################
    DB     . LockWrites    ( [ CRPTAB                                      ] )
    DB     . Query         ( QQ                                              )
    DB     . UnlockTables  (                                                 )
    ##########################################################################
    return CUID
  ############################################################################
  def UpdateReverseCurrencyPair ( self , DB , CUID , RUID                  ) :
    ##########################################################################
    CRPTAB = self . Tables      [ "CurrencyPairs"                            ]
    QQ     = f"""update {CRPTAB}
                 set `reverse` = {RUID}
                 where ( `uuid` = {CUID} ) ;"""
    QQ     = " " . join         ( QQ . split ( )                             )
    DB     . Query              ( QQ                                         )
    ##########################################################################
    return
  ############################################################################
  def isCurrencyPair   ( self , PAIR                                       ) :
    ##########################################################################
    P = PAIR . upper   (                                                     )
    P = P    . rstrip  (                                                     )
    P = P    .  strip  (                                                     )
    P = P    . replace ( " " , ""                                            )
    ##########################################################################
    if                 ( "/" not in P                                      ) :
      return False
    ##########################################################################
    C = P    . split   ( "/"                                                 )
    if                 ( len ( C ) != 2                                    ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def ImportCurrencyPair               ( self , DB , PAIR                  ) :
    ##########################################################################
    C      = PAIR . split              ( "/"                                 )
    if                                 ( len ( C ) != 2                    ) :
      return False
    ##########################################################################
    FCUR   = C                         [ 0                                   ]
    TCUR   = C                         [ 1                                   ]
    ##########################################################################
    FCUR   = FCUR . upper              (                                     )
    TCUR   = TCUR . upper              (                                     )
    ##########################################################################
    FUID   = self . GetCurrencyUuid    ( DB , FCUR                           )
    TUID   = self . GetCurrencyUuid    ( DB , TCUR                           )
    ##########################################################################
    if                                 ( FUID <= 0                         ) :
      return False
    ##########################################################################
    if                                 ( TUID <= 0                         ) :
      return False
    ##########################################################################
    CUID   = self . GetCurrencyPair    ( DB , FUID , TUID                    )
    if                                 ( CUID <= 0                         ) :
      ########################################################################
      CUID = self . AppendCurrencyPair ( DB , FCUR , FUID , TCUR , TUID      )
    ##########################################################################
    if                                 ( CUID <= 0                         ) :
      return False
    ##########################################################################
    if                                 ( not self . DoReverse              ) :
      return True
    ##########################################################################
    RUID   = self . GetCurrencyPair    ( DB , TUID , FUID                    )
    if                                 ( RUID <= 0                         ) :
      ########################################################################
      RUID = self . AppendCurrencyPair ( DB , TCUR , TUID , FCUR , FUID      )
    ##########################################################################
    if                                 ( RUID <= 0                         ) :
      return False
    ##########################################################################
    self   . UpdateReverseCurrencyPair ( DB , CUID , RUID                    )
    self   . UpdateReverseCurrencyPair ( DB , RUID , CUID                    )
    ##########################################################################
    return   True
  ############################################################################
  def AppendEmptyCurrencyPair ( self , DB , SYMBOL                         ) :
    ##########################################################################
    CRPTAB = self . Tables    [ "CurrencyPairs"                              ]
    CUID   = DB . LastUuid    ( CRPTAB , "uuid" , 4110000000200000000        )
    ##########################################################################
    QQ     = f"""insert into {CRPTAB}
                 ( `uuid` , `type` , `symbol` ) values
                 ( {CUID} , 9 , %s ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    ##########################################################################
    DB     . LockWrites       ( [ CRPTAB                                   ] )
    DB     . QueryValues      ( QQ , ( SYMBOL , )                            )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return CUID
  ############################################################################
  def ImportCurrencyPairs           ( self , DB , PAIRs                    ) :
    ##########################################################################
    LISTs      = PAIRs . split      ( "\n"                                   )
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      P        = L . rstrip         (                                        )
      P        = P .  strip         (                                        )
      P        = P . replace        ( " " , ""                               )
      if                            ( ( len ( P ) > 0 ) and ( "/" in P )   ) :
        C      = P . split          ( "/"                                    )
        if                          ( len ( C ) == 2                       ) :
          ####################################################################
          self . ImportCurrencyPair ( DB , P                                 )
    ##########################################################################
    return
  ############################################################################
  def AppendEmptyPair              ( self , TEXT                           ) :
    ##########################################################################
    DB   = self . ConnectDB        (                                         )
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    self . OnBusy  . emit          (                                         )
    self . setBustle               (                                         )
    ##########################################################################
    self . AppendEmptyCurrencyPair ( DB , TEXT                               )
    ##########################################################################
    self . setVacancy              (                                         )
    self . GoRelax . emit          (                                         )
    self . ShowStatus              ( ""                                      )
    DB   . Close                   (                                         )
    self . loading                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def ImportPairs              ( self , TEXT                               ) :
    ##########################################################################
    DB   = self . ConnectDB    (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self . OnBusy  . emit      (                                             )
    self . setBustle           (                                             )
    ##########################################################################
    self . ImportCurrencyPairs ( DB , TEXT                                   )
    ##########################################################################
    self . setVacancy          (                                             )
    self . GoRelax . emit      (                                             )
    self . ShowStatus          ( ""                                          )
    DB   . Close               (                                             )
    self . loading             (                                             )
    ##########################################################################
    return
  ############################################################################
  def ImportItems                           ( self                         ) :
    ##########################################################################
    TITLE   = self . getMenuItem            ( "ImportCurrencyPairs"          )
    FILTERS = self . getMenuItem            ( "CurrencyPairFilters"          )
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
    self   . Go ( self . ImportPairs , ( T , )                               )
    ##########################################################################
    return
  ############################################################################
  def PasteItems        ( self                                             ) :
    ##########################################################################
    self . defaultPaste ( self . ImportPairs                                 )
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
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                    )
    if                                ( not doMenu                         ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
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
    msg    = self . getMenuItem       ( "AutoReversal"                       )
    mm     . addAction                ( 2001 , msg , True , self . DoReverse )
    ##########################################################################
    msg    = self . getMenuItem       ( "DoDissect"                          )
    mm     . addAction                ( 2002 , msg , True , self . DoDissect )
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
    OKAY   = self . RunDocking        ( mm , aa                              )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                ( OKAY                               ) :
      self . restart                  (                                      )
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
      self . EditAllNames             ( self , "CurrencyPairs" , uuid , NAM  )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 2001                         ) :
      ########################################################################
      if                              ( self . DoReverse                   ) :
        self . DoReverse = False
      else                                                                   :
        self . DoReverse = True
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 2002                         ) :
      ########################################################################
      if                              ( self . DoDissect                   ) :
        self . DoDissect = False
      else                                                                   :
        self . DoDissect = True
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

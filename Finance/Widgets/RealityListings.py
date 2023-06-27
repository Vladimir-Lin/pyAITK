# -*- coding: utf-8 -*-
##############################################################################
## RealityListings
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
from   AITK  . People     . People    import People
##############################################################################
class RealityListings              ( TreeDock                              ) :
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
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "asc"
    self . Major              = "Reality"
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
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
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
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 640 )                       )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Insert"     , self . InsertItem                 )
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
    self . LinkAction     ( "Home"       , self . PageHome                   )
    self . LinkAction     ( "End"        , self . PageEnd                    )
    self . LinkAction     ( "PageUp"     , self . PageUp                     )
    self . LinkAction     ( "PageDown"   , self . PageDown                   )
    ##########################################################################
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
    ##########################################################################
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column in [ 0 ]                         ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 1 ]                          ) :
      ########################################################################
      LL   = self . Translations [ "RealityListings" ] [ "Types"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . rtypeChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 2 ]                         ) :
      ########################################################################
      LL   = self . Translations [ "RealityListings" ] [ "Useds"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . usedChanged                        )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 3 ]                         ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . statesChanged                      )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 4 ]                         ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . tagChanged                         )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 5 ]                         ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   0                                       , \
                                   "editingFinished"                       , \
                                   self . wikiChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , JSOX                             ) :
    ##########################################################################
    TL    = self . Translations  [ "RealityListings" ] [ "Types"             ]
    UL    = self . Translations  [ "RealityListings" ] [ "Useds"             ]
    ##########################################################################
    UUID  = JSOX                 [ "Uuid"                                    ]
    NAME  = JSOX                 [ "Name"                                    ]
    RTYPE = JSOX                 [ "Type"                                    ]
    USED  = JSOX                 [ "Used"                                    ]
    STATE = JSOX                 [ "States"                                  ]
    TAG   = JSOX                 [ "Tag"                                     ]
    WIKI  = JSOX                 [ "Wiki"                                    ]
    ##########################################################################
    STYPE = TL                   [ str ( RTYPE )                             ]
    SUSED = UL                   [ str ( USED  )                             ]
    ##########################################################################
    UXID = str                   ( UUID                                      )
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    ##########################################################################
    IT   . setText               ( 0 , NAME                                  )
    IT   . setToolTip            ( 0 , UXID                                  )
    IT   . setData               ( 0 , Qt . UserRole , UUID                  )
    ##########################################################################
    IT   . setText               ( 1 , STYPE                                 )
    IT   . setData               ( 0 , Qt . UserRole , RTYPE                 )
    ##########################################################################
    IT   . setText               ( 2 , SUSED                                 )
    IT   . setData               ( 0 , Qt . UserRole , USED                  )
    ##########################################################################
    IT   . setText               ( 3 , str ( STATE )                         )
    IT   . setData               ( 0 , Qt . UserRole , STATE                 )
    ##########################################################################
    IT   . setText               ( 4 , TAG                                   )
    IT   . setText               ( 5 , WIKI                                  )
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
  def rtypeChanged               ( self                                    ) :
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
      pid  = int                 ( item . text ( 0 )                         )
      LL   = self . Translations [ "RealityListings" ] [ "Types"             ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateUuidColumn                 , \
                                   ( "type" , pid , value , )                )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def usedChanged                ( self                                    ) :
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
      pid  = int                 ( item . text ( 0 )                         )
      LL   = self . Translations [ "RealityListings" ] [ "Useds"             ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateUuidColumn                 , \
                                   ( "used" , pid , value , )                )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def statesChanged              ( self                                    ) :
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
    STATES = 0
    try                                                                      :
      STATES = int               ( msg                                       )
    except                                                                   :
      pass
    ##########################################################################
    msg    = f"{STATES}"
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . UpdateUuidColumn                 , \
                                   ( "states" , uuid , msg , )               )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def tagChanged                 ( self                                    ) :
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
    self   . Go                  ( self . UpdateUuidColumn                 , \
                                   ( "name" , uuid , msg , )                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def wikiChanged                ( self                                    ) :
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
    self   . Go                  ( self . UpdateUuidColumn                 , \
                                   ( "wiki" , uuid , msg , )                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (        list                             )
  def refresh                      ( self , JSONs                          ) :
    ##########################################################################
    self    . clear                (                                         )
    ##########################################################################
    UUIDs   = JSON                 [ "UUIDs"                                 ]
    NAMEs   = JSON                 [ "NAMEs"                                 ]
    ##########################################################################
    for J in JSONs                                                           :
      ########################################################################
      IT    = self . PrepareItem   ( J                                       )
      self  . addTopLevelItem      ( IT                                      )
    ##########################################################################
    FMT     = self . getMenuItem   ( "DisplayTotal"                          )
    MSG     = FMT  . format        ( len ( JSONs )                           )
    self    . setToolTip           ( MSG                                     )
    ##########################################################################
    self    . emitNamesShow . emit (                                         )
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
  def ObtainsUuidNames         ( self , DB , UUIDs                         ) :
    ##########################################################################
    NAMEs    =                 {                                             }
    ##########################################################################
    if                         ( len ( UUIDs ) > 0                         ) :
      NAMTAB = self . Tables   [ "NamesEditing"                              ]
      NAMEs  = self . GetNames ( DB , NAMTAB , UUIDs                         )
    ##########################################################################
    return NAMEs
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
    JSOX    =                         [                                      ]
    RLETAB  = self . Tables           [ self . Major                         ]
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME  = NAMEs                   [ UUID                                 ]
      ########################################################################
      QQ    = f"""select `type`,`used`,`states`,`name`,`wiki` from {RLETAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      ########################################################################
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      RTYPE = 1
      USED  = 1
      STATE = 0
      TAG   = ""
      WIKI  = ""
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 5 ) )          :
        ######################################################################
        RTYPE = int                   ( RR [ 0 ]                             )
        USED  = int                   ( RR [ 1 ]                             )
        STATE = int                   ( RR [ 2 ]                             )
        TAG   = self . assureString   ( RR [ 3 ]                             )
        WIKI  = self . assureString   ( RR [ 4 ]                             )
      ########################################################################
      J     =                         { "Uuid"   : UUID                    , \
                                        "Name"   : NAME                    , \
                                        "Type"   : RTYPE                   , \
                                        "Used"   : USED                    , \
                                        "States" : STATE                   , \
                                        "Tag"    : TAG                     , \
                                        "Wiki"   : WIKI                      }
      ########################################################################
      JSOX  . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( JSOX ) <= 0                  ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSOX                                 )
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
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
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
    RLETAB = self . Tables [ self . Major                                    ]
    ##########################################################################
    QQ     = f"select count(*) from {RLETAB} where ( `used` = 1 ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    RLETAB  = self . Tables          [ self . Major                          ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {RLETAB}
                  where ( `used` = 1 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 6 , 3                                     )
    ##########################################################################
    LABELs = self . Translations [ "RealityListings" ] [ "Labels"            ]
    self   . setCentralLabels    ( LABELs                                    )
    ##########################################################################
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    RLETAB = self . Tables    [ self . Major                                 ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ RLETAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( RLETAB , "uuid" , 6710000000000000000        )
      DB   . AppendUuid       ( RLETAB , uuid                                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def UpdateUuidColumn        ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    RLETAB = self . Tables    [ self . Major                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ RLETAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"""update {RLETAB}
                 set `{item}` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    ##########################################################################
    DB     . QueryValues      ( QQ , ( name , )                              )
    ##########################################################################
    DB     . Close            (                                              )
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
  def PartitionMenu             ( self , mm                                ) :
    ##########################################################################
    TRX  = self . Translations  [ "RealityListings" ] [ "Major"              ]
    ##########################################################################
    MSG  = self . getMenuItem   ( "Partition"                                )
    COL  = mm . addMenu         ( MSG                                        )
    ##########################################################################
    CHK  =                      ( "Reality"    == self . Major               )
    msg  = TRX                  [ "Reality"                                  ]
    mm   . addActionFromMenu    ( COL , 43521001 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Commons"    == self . Major               )
    msg  = TRX                  [ "Commons"                                  ]
    mm   . addActionFromMenu    ( COL , 43521002 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Equipments" == self . Major               )
    msg  = TRX                  [ "Equipments"                               ]
    mm   . addActionFromMenu    ( COL , 43521003 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Parts"      == self . Major               )
    msg  = TRX                  [ "Parts"                                    ]
    mm   . addActionFromMenu    ( COL , 43521004 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Products"   == self . Major               )
    msg  = TRX                  [ "Products"                                 ]
    mm   . addActionFromMenu    ( COL , 43521005 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Virtuals"   == self . Major               )
    msg  = TRX                  [ "Virtuals"                                 ]
    mm   . addActionFromMenu    ( COL , 43521006 , msg , True , CHK          )
    ##########################################################################
    CHK  =                      ( "Others"     == self . Major               )
    msg  = TRX                  [ "Others"                                   ]
    mm   . addActionFromMenu    ( COL , 43521007 , msg , True , CHK          )
    ##########################################################################
    return mm
  ############################################################################
  def RunPartitionMenu             ( self , at                             ) :
    ##########################################################################
    if                             ( at == 43521001                        ) :
      ########################################################################
      self . Major = "Reality"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521002                        ) :
      ########################################################################
      self . Major = "Commons"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521003                        ) :
      ########################################################################
      self . Major = "Equipments"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521004                        ) :
      ########################################################################
      self . Major = "Parts"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521005                        ) :
      ########################################################################
      self . Major = "Products"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521006                        ) :
      ########################################################################
      self . Major = "Virtuals"
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 43521007                        ) :
      ########################################################################
      self . Major = "Others"
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
    if                              ( atItem not in [ False , None ]       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    self   . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      mm   . addSeparator           (                                        )
      ########################################################################
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . PartitionMenu          ( mm                                     )
    ##########################################################################
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
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunPartitionMenu ( at )       ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . startup                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "NamesEditing"                         ]
      self . EditAllNames           ( self , "Reality" , uuid , NAM          )
      return True
    ##########################################################################
    return True
##############################################################################

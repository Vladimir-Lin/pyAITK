# -*- coding: utf-8 -*-
##############################################################################
## RaceListings
## 種族列表
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
from   PyQt5 . QtWidgets              import QFileDialog
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
class RaceListings                 ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int                               )
  PeopleGroup       = pyqtSignal   ( str , int , str                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "asc"
    self . Method             = "Original"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 3                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
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
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 320 , 640                               )
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
    self . LinkAction              ( "Search"     , self . Search            )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Paste"      , self . Paste             )
    self . LinkAction              ( "Import"     , self . Import            )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
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
    self     . Notify         ( 0                                            )
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
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
  def PrepareItem                ( self , UUID , NAME                      ) :
    ##########################################################################
    UXID = str                   ( UUID                                      )
    IT   = QTreeWidgetItem       (                                           )
    IT   . setText               ( 0 , NAME                                  )
    IT   . setToolTip            ( 0 , UXID                                  )
    IT   . setData               ( 0 , Qt . UserRole , UUID                  )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot            (                                                     )
  def Finding          ( self                                              ) :
    ##########################################################################
    L    = self . SearchLine
    ##########################################################################
    if                 ( L in [ False , None ]                             ) :
      return
    ##########################################################################
    self . SearchLine = None
    T    = L . text    (                                                     )
    L    . deleteLater (                                                     )
    ##########################################################################
    if                 ( len ( T ) <= 0                                    ) :
      return
    ##########################################################################
    self . Go          ( self . looking , ( T , )                            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                            (                                     )
  def Search                           ( self                              ) :
    ##########################################################################
    L      = LineEdit                  ( None , self . PlanFunc              )
    OK     = self . attacheStatusBar   ( L , 1                               )
    ##########################################################################
    if                                 ( not OK                            ) :
      ########################################################################
      L    . deleteLater               (                                     )
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . Finding                      )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "Search"                            )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
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
  @pyqtSlot                           (        dict                          )
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    NAMEs   = JSON                    [ "NAMEs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem      ( U , NAMEs [ U ]                      )
      self  . addTopLevelItem         ( IT                                   )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
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
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  @pyqtSlot                           (        str  , int                    )
  def AssignAmounts                   ( self , UUID , Amounts              ) :
    ##########################################################################
    IT    = self . uuidAtItem         ( UUID , 0                             )
    if                                ( IT is None                         ) :
      return
    ##########################################################################
    IT . setText                      ( 1 , str ( Amounts )                  )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                 ( self , UUIDs                      ) :
    ##########################################################################
    time    . sleep                    ( 1.0                                 )
    ##########################################################################
    RELTAB  = self . Tables            [ "Relation"                          ]
    REL     = Relation                 (                                     )
    REL     . setT1                    ( "Race"                              )
    REL     . setT2                    ( "People"                            )
    REL     . setRelation              ( "Subordination"                     )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL   . set                      ( "first" , UUID                      )
      CNT   = REL . CountSecond        ( DB , RELTAB                         )
      ########################################################################
      self  . emitAssignAmounts . emit ( str ( UUID ) , CNT                  )
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    return
  ############################################################################
  def looking                         ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    RACTAB  = self . Tables           [ "Races"                              ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    LIC     = self . getLocality      (                                      )
    LIKE    = f"%{name}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    RQ      = f"select `uuid` from {RACTAB} where ( `used` > 0 )"
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( `name` like %s )
                  group by `uuid` asc ;"""
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( ALL in [ False , None ] ) or ( len ( ALL ) <= 0 ) )               :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    for U in ALL                                                             :
      UUIDs . append                  ( U [ 0 ]                              )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    self . SearchKey = name
    self . UUIDs     = UUIDs
    self . Method    = "Searching"
    ##########################################################################
    self . loading                    (                                      )
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
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    if                                ( self . Method in [ "Original" ]    ) :
      self  . UUIDs =                 [                                      ]
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    else                                                                     :
      UUIDs = self . UUIDs
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 1 )    ) :
      self . Go                       ( self . ReportBelongings            , \
                                        ( UUIDs , )                          )
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
    RACTAB = self . Tables  [ "Races"                                        ]
    ##########################################################################
    QQ     = f"""select `uuid` from {RACTAB}
                 where ( `used` = 1 )
                 order by `id` asc ;"""
    ##########################################################################
    QQ     = " " . join     ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Paste"      , self . Paste           , False   )
    self . LinkAction      ( "Import"     , self . Import          , False   )
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
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    RACTAB = self . Tables [ "Races"                                         ]
    ##########################################################################
    QQ     = f"select count(*) from {RACTAB} where ( `used` = 1 ) ;"
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
  def ObtainUuidsQuery      ( self                                         ) :
    ##########################################################################
    RACTAB  = self . Tables [ "Races"                                        ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `uuid` from {RACTAB}
                  where ( `used` = 1 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join       ( QQ . split ( )                                 )
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    if                              ( self == sourceWidget                 ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      FMT   = self . getMenuItem    ( "CopyFrom"                             )
      MSG   = FMT . format          ( title , CNT                            )
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget != self                      ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    if                         ( atItem is None                            ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    if                         ( "UUIDs" not in JSOX                       ) :
      return True
    ##########################################################################
    UUIDs  = JSOX              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    if                         ( atItem is None                            ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinRace                     , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinRace                ( self , UUID , UUIDs                  ) :
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    COUNT   = len                   ( UUIDs                                  )
    if                              ( COUNT <= 0                           ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden ( 1                                      )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem    ( "JoinPeople"                           )
    MSG     = FMT  . format         ( COUNT                                  )
    self    . ShowStatus            ( MSG                                    )
    self    . TtsTalk               ( MSG , 1002                             )
    ##########################################################################
    PER     = People                (                                        )
    RELTAB  = self . Tables         [ "Relation"                             ]
    DB      . LockWrites            ( [ RELTAB ]                             )
    PER     . ConnectToPeople       ( DB , RELTAB , UUID , "Race" , UUIDs    )
    DB      . UnlockTables          (                                        )
    ##########################################################################
    if                              ( not Hide                             ) :
      TOTAL = PER . CountBelongs    ( DB , RELTAB , UUID , "Race"            )
    ##########################################################################
    DB      . Close                 (                                        )
    ##########################################################################
    self    . ShowStatus            ( ""                                     )
    self    . Notify                ( 5                                      )
    ##########################################################################
    if                              ( Hide                                 ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem     ( UUID , 0                               )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    IT      . setText               ( 1 , str ( TOTAL )                      )
    self    . DoUpdate              (                                        )
    ##########################################################################
    return
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 2 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs = TRX              [ "RaceListings" ] [ "Labels"                  ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
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
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    RACTAB  = self . Tables        [ "Races"                                 ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    ##########################################################################
    DB      . LockWrites           ( [ RACTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . UnusedUuid      ( RACTAB                                  )
      DB    . UseUuid              ( RACTAB , uuid                           )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
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
  def ImportFromText          ( self , text                                ) :
    ##########################################################################
    L      = text . split     ( "\n"                                         )
    if                        ( len ( L ) <= 0                             ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    RACTAB = self . Tables    [ "Races"                                      ]
    NAMTAB = self . Tables    [ "Names"                                      ]
    ##########################################################################
    DB     . LockWrites       ( [ RACTAB , NAMTAB                          ] )
    ##########################################################################
    for N in L                                                               :
      ########################################################################
      name = N
      name = name .  strip    (                                              )
      name = name . rstrip    (                                              )
      ########################################################################
      if                      ( len ( name ) <= 0                          ) :
        continue
      ########################################################################
      uuid = DB . UnusedUuid  ( RACTAB                                       )
      DB   . UseUuid          ( RACTAB , uuid                                )
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def Paste                         ( self                                 ) :
    ##########################################################################
    T = qApp . clipboard ( ) . text (                                        )
    ##########################################################################
    if                              ( len ( T ) <= 0                       ) :
      return
    ##########################################################################
    self . Go                       ( self . ImportFromText , ( text , )     )
    ##########################################################################
    return
  ############################################################################
  def Import                             ( self                            ) :
    ##########################################################################
    FILTERS       = self . Translations  [ "UI::PlainTextFiles"              ]
    Filename , Ok = QFileDialog . getOpenFileName                          ( \
                      self                                                 , \
                      self . windowTitle (                               ) , \
                      ""                                                   , \
                      FILTERS                                                )
    ##########################################################################
    if                                   ( len ( Filename ) <= 0           ) :
      return
    ##########################################################################
    BODY          = ""
    with open                            ( Filename , "rb" ) as f            :
      BODY        = f . read             (                                   )
    ##########################################################################
    if                                   ( len ( BODY ) <= 0               ) :
      return
    ##########################################################################
    text          = ""
    try                                                                      :
      text        = BODY . decode        ( "utf-8"                           )
    except                                                                   :
      return
    ##########################################################################
    if                                   ( len ( text ) <= 0               ) :
      return
    ##########################################################################
    self          . Go                   ( self . ImportFromText           , \
                                           ( text , )                        )
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
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at == 9001 ) and ( hid )            ) :
        self . startup             (                                         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                   ( self , mm , item                      ) :
    ##########################################################################
    TRX    = self . Translations
    NAME   = item . text           ( 0                                       )
    FMT    = TRX                   [ "UI::Belongs"                           ]
    MSG    = FMT . format          ( NAME                                    )
    COL    = mm . addMenu          ( MSG                                     )
    ##########################################################################
    msg    = self . getMenuItem    ( "Crowds"                                )
    mm     . addActionFromMenu     ( COL , 1201 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , item                      ) :
    ##########################################################################
    if                             ( at == 1201                            ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . PeopleGroup   . emit  ( head , 34 , str ( uuid )                )
      ########################################################################
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
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    if                              ( self . Method not in [ "Original" ]  ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Original"                             )
      mm   . addAction              ( 1002 , msg                             )
    ##########################################################################
    self   . AppendInsertAction     ( mm , 1101                              )
    self   . AppendRenameAction     ( mm , 1102                              )
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      mm   = self . GroupsMenu      ( mm , atItem                            )
      mm   . addSeparator           (                                        )
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
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    self   . RunAmountIndexMenu     (                                        )
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunGroupsMenu ( at , atItem ) ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . startup                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      self . Method = "Original"
      self . startup                (                                        )
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
    if                              ( at == 1601                           ) :
      ########################################################################
      uuid = self . itemUuid        ( atItem , 0                             )
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "Races" , uuid , NAM            )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################

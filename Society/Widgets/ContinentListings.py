# -*- coding: utf-8 -*-
##############################################################################
## ContinentListings
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
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class ContinentListings            ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int                               )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
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
    self . setAcceptDrops          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
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
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkAction              ( "Rename"     , self . RenameItem        )
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
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
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
    ## time    . sleep                    ( 1.0                                 )
    ##########################################################################
    ## TABLE = self . Tables              [ "Continents"                        ]
    ##########################################################################
    ## DB      = self . ConnectDB         (                                     )
    ##########################################################################
    ## for UUID in UUIDs                                                        :
    ##   ########################################################################
    ##   CNT   = 0
    ##   TYPE  = int                      ( UUID % 10000                        )
    ##   QQ    = f"""select count(*) from {TABLE}
    ##               where ( `used` = 1 )
    ##               and ( `type` = {TYPE} ) ;"""
    ##   QQ    = " " . join               ( QQ . split ( )                      )
    ##   DB    . Query                    ( QQ                                  )
    ##   RR    = DB . FetchOne            (                                     )
    ##   ########################################################################
    ##   if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )          :
    ##     CNT = RR                       [ 0                                   ]
    ##   ########################################################################
    ##   self  . emitAssignAmounts . emit ( str ( UUID ) , CNT                  )
    ##########################################################################
    ## DB      . Close                    (                                     )
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
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
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
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    TABLE = self . Tables        [ "Continents"                              ]
    ##########################################################################
    QQ    = f"select `uuid` from {TABLE} order by `id` asc ;"
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
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
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery    ( self                                           ) :
    ##########################################################################
    TABLE = self . Tables [ "Continents"                                     ]
    ##########################################################################
    return f"select `uuid` from {TABLE} order by `id` asc ;"
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 2 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs =                  [ TRX [ "UI::Continents" ]                   , \
                                TRX [ "UI::Amount"     ]                   , \
                                ""                                           ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NAMTAB  = self . Tables        [ "Names"                                 ]
    ##########################################################################
    DB      . LockWrites           ( [ OCPTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    if                             ( uuid > 0                              ) :
      self  . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
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
    self . Go                     ( self . Talk , ( MSG , LID , )            )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    msg    = TRX                   [ "UI::Amount"                            ]
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
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
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
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"           ] )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    mm     . addSeparator          (                                         )
    mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
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
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9001 ) and ( hid )            ) :
        self . startup             (                                         )
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Continents" , uuid , NAM        )
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
##############################################################################

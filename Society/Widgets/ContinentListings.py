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
  emitAssignAmounts = pyqtSignal   ( str , int , int                         )
  PlaceSubgroups    = pyqtSignal   ( str , int , str , str , QIcon           )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . GType              = 65
    self . ClassTag           = "ContinentListings"
    self . EditAllNames       = None
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 6                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 4 , True                                )
    self . setColumnHidden         ( 5 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setAcceptDrops          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 320 , 640                               )
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
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
  def PrepareItem              ( self , UUID , NAME , JSON                 ) :
    ##########################################################################
    TRX  = self . Translations [ self . ClassTag                             ]
    ##########################################################################
    UXID = str                 ( UUID                                        )
    IT   = QTreeWidgetItem     (                                             )
    IT   . setText             ( 0 , NAME                                    )
    IT   . setToolTip          ( 0 , UXID                                    )
    IT   . setData             ( 0 , Qt . UserRole , UUID                    )
    ##########################################################################
    USED = JSON                [ "Usage"                                     ]
    UNAM = TRX                 [ "Usage" ] [ str ( USED )                    ]
    IT   . setText             ( 1 , UNAM                                    )
    IT   . setData             ( 1 , Qt . UserRole , USED                    )
    ##########################################################################
    ENAM = JSON                [ "Name"                                      ]
    IT   . setText             ( 2 , ENAM                                    )
    ##########################################################################
    TYPE = JSON                [ "Type"                                      ]
    TNAM = TRX                 [ "Types" ] [ str ( TYPE )                    ]
    IT   . setText             ( 3 , TNAM                                    )
    IT   . setData             ( 3 , Qt . UserRole , TYPE                    )
    ##########################################################################
    IT   . setTextAlignment    ( 4 , Qt.AlignRight                           )
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
    JSONs   = JSON                    [ "JSONs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem      ( U , NAMEs [ U ] , JSONs [ U ]        )
      self  . addTopLevelItem         ( IT                                   )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( UUIDs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
    self   . Notify               ( 5                                        )
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
  def ObtainsUuidNames      ( self , DB , UUIDs                            ) :
    ##########################################################################
    NAMEs =                 {                                                }
    if                      ( len ( UUIDs ) <= 0                           ) :
      return NAMEs
    ##########################################################################
    TABLE = self . Tables   [ "Names"                                        ]
    NAMEs = self . GetNames ( DB , TABLE , UUIDs                             )
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainsUuidJsons             ( self , DB , UUIDs                     ) :
    ##########################################################################
    JSONs    =                     {                                         }
    if                             ( len ( UUIDs ) <= 0                    ) :
      return JSONs
    ##########################################################################
    TABLE    = self . Tables       [ "Continents"                            ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ     = f"""select `type`,`usage`,`name` from {TABLE}
                  where ( `uuid` = {UUID} ) ;"""
      QQ     = " " . join          ( QQ . split ( )                          )
      DB     . Query               ( QQ                                      )
      RR     = DB  . FetchOne      (                                         )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 3 ) )          :
        ######################################################################
        TYPE = int                 ( RR [ 0                                ] )
        USED = int                 ( RR [ 1                                ] )
        NAME = self . assureString ( RR [ 2                                ] )
        ######################################################################
        JSONs [ UUID ] =           { "Type"  : TYPE                        , \
                                     "Usage" : USED                        , \
                                     "Name"  : NAME                          }
    ##########################################################################
    return   JSONs
  ############################################################################
  @pyqtSlot                           (        str  , int     , int          )
  def AssignAmounts                   ( self , UUID , Amounts , Column     ) :
    ##########################################################################
    IT    = self . uuidAtItem         ( UUID , 0                             )
    if                                ( IT is None                         ) :
      return
    ##########################################################################
    IT . setText                      ( Column , str ( Amounts )             )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "RelationPlaces"                     ]
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  = Relation                 (                                      )
      REL  . set                      ( "first" , UUID                       )
      REL  . setT1                    ( "Continent"                          )
      REL  . setT2                    ( "Place"                              )
      REL  . setRelation              ( "Contains"                           )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 4               )
    ##########################################################################
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . OnBusy        . emit    (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
      JSONs = self . ObtainsUuidJsons ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax       . emit    (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    JSON [ "JSONs" ] = JSONs
    ##########################################################################
    self    . emitAllNames . emit     ( JSON                                 )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 1 )    ) :
      ########################################################################
      VAL   =                         ( UUIDs ,                              )
      self  . Go                      ( self . ReportBelongings , VAL        )
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
    if                          ( self . NotOkay ( DB )                    ) :
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
  def ObtainUuidsQuery    ( self                                           ) :
    ##########################################################################
    TABLE = self . Tables [ "Continents"                                     ]
    ##########################################################################
    return f"select `uuid` from {TABLE} order by `id` asc ;"
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    formats = "place/uuids;position/uuids;nation/uuids"
    return self . MimeType (        mime , formats                           )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    if                               ( self == source                      ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( mtype in [ "place/uuids" ]          ) :
      ########################################################################
      if                             ( self . NotOkay ( atItem )           ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus ( "CopyFrom" , title , CNT              )
    ##########################################################################
    if                               ( mtype in [ "position/uuids" ]       ) :
      ########################################################################
      if                             ( self . NotOkay ( atItem )           ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus ( "CopySpot" , title , CNT              )
    ##########################################################################
    if                               ( mtype in [ "nation/uuids" ]         ) :
      ########################################################################
      if                             ( self . NotOkay ( atItem )           ) :
        return False
      ########################################################################
      self . ShowMenuItemTitleStatus ( "CopyNation" , title , CNT            )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , source , mimeData , mousePos       ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( source == self                            ) :
      return False
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    mtype  = self . DropInJSON [ "Mime"                                      ]
    ##########################################################################
    if                         ( mtype  in [ "place/uuids" ]               ) :
      ########################################################################
      if                       ( self . NotOkay ( atItem )                 ) :
        return False
    ##########################################################################
    return True
  ############################################################################
  def acceptPlacesDrop   ( self                                            ) :
    return True
  ############################################################################
  def acceptPositionDrop ( self                                            ) :
    return True
  ############################################################################
  def acceptNationsDrop  ( self                                            ) :
    return True
  ############################################################################
  def dropPlaces           ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( self . NotOkay ( atItem )                     ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    VAL    =               ( UUID , UUIDs ,                                  )
    self   . Go            ( self . JoinPlaces , VAL                         )
    ##########################################################################
    return True
  ############################################################################
  def dropPositions        ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( self . NotOkay ( atItem )                     ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    VAL    =               ( UUID , UUIDs ,                                  )
    self   . Go            ( self . JoinPositions , VAL                      )
    ##########################################################################
    return True
  ############################################################################
  def dropNations          ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( self . NotOkay ( atItem )                     ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    VAL    =               ( UUID , UUIDs ,                                  )
    self   . Go            ( self . JoinNations , VAL                        )
    ##########################################################################
    return True
  ############################################################################
  def JoinPlaces                    ( self , UUID , UUIDs                  ) :
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    COUNT   = len                   ( UUIDs                                  )
    if                              ( COUNT <= 0                           ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden ( 4                                      )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem    ( "JoinPlaces"                           )
    MSG     = FMT  . format         ( COUNT                                  )
    self    . ShowStatus            ( MSG                                    )
    self    . TtsTalk               ( MSG , 1002                             )
    ##########################################################################
    RELTAB  = self . Tables         [ "RelationPlaces"                       ]
    REL     = Relation              (                                        )
    REL     . set                   ( "first" , UUID                         )
    REL     . setT1                 ( "Continent"                            )
    REL     . setT2                 ( "Place"                                )
    REL     . setRelation           ( "Contains"                             )
    ##########################################################################
    DB      . LockWrites            ( [ RELTAB                             ] )
    ##########################################################################
    REL     . Joins                 ( DB , RELTAB , UUIDs                    )
    ##########################################################################
    DB      . UnlockTables          (                                        )
    ##########################################################################
    if                              ( not Hide                             ) :
      ########################################################################
      TOTAL = REL . CountSecond     ( DB , RELTAB                            )
    ##########################################################################
    DB      . Close                 (                                        )
    ##########################################################################
    self    . ShowStatus            ( ""                                     )
    ##########################################################################
    if                              ( Hide                                 ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem     ( UUID , 0                               )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    IT      . setText               ( 4 , str ( TOTAL )                      )
    self    . DoUpdate              (                                        )
    ##########################################################################
    return
  ############################################################################
  def JoinPositions             ( self , UUID , UUIDs                      ) :
    ##########################################################################
    if                          ( UUID <= 0                                ) :
      return
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem ( "JoinPositions"                            )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationPlaces"                           ]
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "Continent"                                )
    REL    . setT2              ( "EarthSpot"                                )
    REL    . setRelation        ( "Contains"                                 )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    REL    . Joins              ( DB , RELTAB , UUIDs                        )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    DB     . Close              (                                            )
    ##########################################################################
    self   . ShowStatus         ( ""                                         )
    ##########################################################################
    return
  ############################################################################
  def JoinNations               ( self , UUID , UUIDs                      ) :
    ##########################################################################
    if                          ( UUID <= 0                                ) :
      return
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem ( "JoinNations"                              )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationPlaces"                           ]
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "Continent"                                )
    REL    . setT2              ( "Nation"                                   )
    REL    . setRelation        ( "Contains"                                 )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    REL    . Joins              ( DB , RELTAB , UUIDs                        )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    DB     . Close              (                                            )
    ##########################################################################
    self   . ShowStatus         ( ""                                         )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 5                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ NAMTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid > 0                                   ) :
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9005 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9004 ) and ( hid )            ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    ##########################################################################
    if                             ( self . IsOkay ( atItem )              ) :
      ########################################################################
      msg  = self . getMenuItem    ( "ContainPlaces"                         )
      mm   . addAction             ( 2001 , msg                              )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      ########################################################################
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 , TRX [ "UI::EditNames" ]          )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ## mm     . addSeparator          (                                         )
    ## mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
    ##########################################################################
    self   . ColumnsMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
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
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 2001                            ) :
      ########################################################################
      uuid = atItem . data         ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = atItem . text         ( 0                                       )
      icon = QIcon                 ( ":/images/vectorizer.png"               )
      self . PlaceSubgroups . emit ( head                                    ,
                                     self . GType                            ,
                                     str ( uuid )                            ,
                                     "Contains"                              ,
                                     icon                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Continents" , uuid , NAM        )
      return True
    ##########################################################################
    ## if                             ( at == 3001                            ) :
    ##   self . Go                    ( self . TranslateAll                     )
    ##   return True
    ##########################################################################
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## ItuWidget
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
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class ItuWidget                    ( TreeDock                              ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitNamesShow  = pyqtSignal      (                                         )
  emitAllNames   = pyqtSignal      ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
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
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 400 , 640 )                       )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
    ##########################################################################
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
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
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def getItemJson                ( self , item                             ) :
    return item . data           ( 3 , Qt . UserRole                         )
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    UUID    = int                 ( JSON [ "Uuid"     ]                      )
    UXID    = str                 ( UUID                                     )
    DETAILS = int                 ( JSON [ "Details"  ]                      )
    PLACE   = int                 ( JSON [ "Place"    ]                      )
    PName   = str                 ( JSON [ "PName"    ]                      )
    ITU     = str                 ( JSON [ "ITU"      ]                      )
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    IT      . setText             ( 0 , ITU                                  )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    ##########################################################################
    IT      . setText             ( 1 , PName                                )
    IT      . setData             ( 1 , Qt . UserRole , PLACE                )
    ##########################################################################
    ## IT      . setText             ( 2 , AREA                                 )
    ## IT      . setData             ( 2 , Qt . UserRole , DETAILS              )
    ##########################################################################
    IT      . setData             ( 3 , Qt . UserRole , JSON                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , E164s                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in E164s                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
    ##########################################################################
    return self . DefaultObtainsItemUuids (        DB                        )
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    ITUTAB  = self . Tables           [ "ITU"                                ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"    : U                      , \
                                        "ITU"     : ""                     , \
                                        "Details" : 0                      , \
                                        "Place"   : 0                        }
      ########################################################################
      QQ    = f"""select `itu`,`details`,`place` from {ITUTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( RR not in [ False , None ] ) and ( len ( RR ) == 3 )              :
        ######################################################################
        J [ "ITU"     ] = self . assureString ( RR [ 0 ]                     )
        J [ "Details" ] = int         ( RR [ 1 ]                             )
        J [ "Place"   ] = int         ( RR [ 2 ]                             )
        ######################################################################
        PUID            = J           [ "Place"                              ]
        PNAME           = ""
        ######################################################################
        if                            ( PUID > 0                           ) :
          PNAME         = self . GetName ( DB , NAMTAB , PUID                )
        ######################################################################
        J [ "PName"   ] = PNAME
      ########################################################################
      IMACT . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
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
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    ITUTAB  = self . Tables      [ "ITU"                                     ]
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"select `uuid` from {ITUTAB} order by `id` {ORDER} ;"
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
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
    ITUTAB = self . Tables [ "ITU"                                           ]
    ##########################################################################
    QQ     = f"select count(*) from {ITUTAB} ;"
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
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    ITUTAB  = self . Tables    [ "ITU"                                       ]
    QQ     = f"select count(*) from {ITUTAB} ;"
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
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    ITUTAB  = self . Tables          [ "ITU"                                 ]
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"select `uuid` from {ITUTAB} order by `id` {ORDER} ;"
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def FetchSessionInformation                    ( self , DB               ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount (        DB                 )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "itu/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , 0 , mtype , message                )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "place/uuids"
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
    if                              ( mtype in [ "place/uuids" ]           ) :
      ########################################################################
      MSG   = self . getMenuItem    ( "AssignPlace"                          )
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPlacesDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPlaces                       ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . AssingPlaceToITU             )
  ############################################################################
  def AssingItemToITU                ( self                                , \
                                       UUID                                , \
                                       UUIDs                               , \
                                       msgId                               , \
                                       Column                              , \
                                       posId                               ) :
    ##########################################################################
    if                               ( UUID <= 0                           ) :
      return
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    PCID   = UUIDs                   [ 0                                     ]
    MSG    = self . getMenuItem      ( msgId                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    ITUTAB = self . Tables           [ "ITU"                                 ]
    NAMTAB = self . Tables           [ "Names"                               ]
    DB     . LockWrites              ( [ ITUTAB ]                            )
    QQ     = f"""update {ITUTAB}
                  set `{Column}` = {PCID}
                  where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    DB     . UnlockTables            (                                       )
    ##########################################################################
    name   = self . GetName          ( DB , NAMTAB , PCID                    )
    ##########################################################################
    DB     . Close                   (                                       )
    ##########################################################################
    self   . ShowStatus              ( ""                                    )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    IT     = self . uuidAtItem       ( UUID , 0                              )
    if                               ( IT is None                          ) :
      return
    ##########################################################################
    self   . emitAssignColumn . emit ( IT , posId , name                     )
    ##########################################################################
    return
  ############################################################################
  def AssingPlaceToITU            ( self , UUID , UUIDs                    ) :
    return self . AssingItemToITU ( UUID                                   , \
                                    UUIDs                                  , \
                                    "AssignPlace"                          , \
                                    "place"                                , \
                                    1                                        )
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "ItuWidget" , 3                                  )
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
    if                             ( at >= 9000 ) and ( at <= 9003 )         :
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
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     . addSeparator          (                                         )
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . SortingMenu    ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
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
    return True
##############################################################################

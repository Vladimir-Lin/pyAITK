# -*- coding: utf-8 -*-
##############################################################################
## AreaCodeWidget
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
class AreaCodeWidget               ( TreeDock                              ) :
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
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 10                                      )
    self . setColumnHidden         ( 7 , True                                )
    self . setColumnHidden         ( 9 , True                                )
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
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 640 )                      )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
    ##########################################################################
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
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
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 0 , 3 , 8 ]             ) :
      return
    ##########################################################################
    if                           ( column in [ 0 , 8 ]                     ) :
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      return
    ##########################################################################
    if                           ( column in [ 3 ]                         ) :
      ########################################################################
      LL   = self . Translations [ "AreaCodeWidget" ] [ "Used"               ]
      cb   = self . bindComboBox ( item                                    , \
                                   column                                  , \
                                   LL                                      , \
                                   self . usageChanged                     , \
                                   5                                         )
      cb   . showPopup           (                                           )
    ##########################################################################
    return
  ############################################################################
  def getItemJson                 ( self , item                            ) :
    return item . data            ( 9 , Qt . UserRole                        )
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    USAGE   = self . Translations [ "AreaCodeWidget" ] [ "Used"              ]
    ##########################################################################
    UUID    = int                 ( JSON [ "Uuid"     ]                      )
    UXID    = str                 ( UUID                                     )
    USED    = int                 ( JSON [ "Used"     ]                      )
    NATION  = int                 ( JSON [ "Nation"   ]                      )
    CNAME   = str                 ( JSON [ "Country"  ]                      )
    ITU     = int                 ( JSON [ "ITU"      ]                      )
    E164    = int                 ( JSON [ "E164"     ]                      )
    ADMIN   = int                 ( JSON [ "Admin"    ]                      )
    PLACE   = int                 ( JSON [ "Place"    ]                      )
    PNAME   = str                 ( JSON [ "PName"    ]                      )
    ##########################################################################
    ISD     = JSON                [ "ISD"                                    ]
    CODE    = JSON                [ "Code"                                   ]
    NAME    = JSON                [ "Name"                                   ]
    COMMENT = JSON                [ "Comment"                                ]
    ##########################################################################
    ESTR    = ""
    if                            ( E164 > 0                               ) :
      ESTR  = f"{E164}"
    ##########################################################################
    UNAME   = USAGE               [ str ( USED )                             ]
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    IT      . setText             ( 0 , NAME                                 )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    ##########################################################################
    IT      . setText             ( 1 , ISD                                  )
    IT      . setToolTip          ( 2 , UXID                                 )
    ##########################################################################
    IT      . setText             ( 2 , CODE                                 )
    IT      . setToolTip          ( 2 , UXID                                 )
    ##########################################################################
    IT      . setText             ( 3 , UNAME                                )
    IT      . setData             ( 3 , Qt . UserRole , USED                 )
    ##########################################################################
    IT      . setText             ( 4 , CNAME                                )
    IT      . setText             ( 5 , PNAME                                )
    IT      . setText             ( 6 , ESTR                                 )
    ##########################################################################
    ## IT      . setText             ( 7 , ""                                   )
    ##########################################################################
    IT      . setText             ( 8 , COMMENT                              )
    ##########################################################################
    IT      . setData             ( 9 , Qt . UserRole , JSON                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0 , 3 , 8 ]                                 )
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
    self   . Go                  ( self . UpdateItem                       , \
                                   ( item , uuid , column , msg , )          )
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
      uuid = self . itemUuid     ( item , 0                                  )
      LL   = self . Translations [ "AreaCodeWidget" ] [ "Used"               ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateUsage                      , \
                                   ( item , uuid , value , )                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (        list                                )
  def refresh                   ( self , AREAS                             ) :
    ##########################################################################
    self . defaultRefreshItems  ( AREAS , self . PrepareItem                 )
    self . emitNamesShow . emit (                                            )
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
    PACTAB  = self . Tables           [ "AreaCode"                           ]
    ITUTAB  = self . Tables           [ "ITU"                                ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J     =                         { "Uuid"    : U                      , \
                                        "Used"    : 0                      , \
                                        "ISD"     : ""                     , \
                                        "Code"    : ""                     , \
                                        "Nation"  : 0                      , \
                                        "Country" : ""                     , \
                                        "ITU"     : 0                      , \
                                        "E164"    : 0                      , \
                                        "Admin"   : 0                      , \
                                        "Place"   : 0                      , \
                                        "PName"   : ""                     , \
                                        "Name"    : ""                     , \
                                        "Comment" : ""                       }
      ########################################################################
      QQ    = f"""select
                  `used`,`isd`,`code`,`nation`,
                  `itu`,`administrative`,`place`,`name`,`comment`
                  from {PACTAB}
                  where ( `uuid` = {U} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( RR not in [ False , None ] ) and ( len ( RR ) == 9 )              :
        ######################################################################
        J [ "Used"    ] = int         ( RR [ 0 ]                             )
        J [ "ISD"     ] = self . assureString ( RR [ 1 ]                     )
        J [ "Code"    ] = self . assureString ( RR [ 2 ]                     )
        J [ "Nation"  ] = int         ( RR [ 3 ]                             )
        J [ "ITU"     ] = int         ( RR [ 4 ]                             )
        J [ "Admin"   ] = int         ( RR [ 5 ]                             )
        J [ "Place"   ] = int         ( RR [ 6 ]                             )
        J [ "Name"    ] = self . assureString ( RR [ 7 ]                     )
        J [ "Comment" ] = self . assureString ( RR [ 8 ]                     )
        ######################################################################
        TUID            = J           [ "ITU"                                ]
        E164            = 0
        ######################################################################
        if                            ( TUID > 0                           ) :
          QQ            = f"""select `itu` from {ITUTAB}
                              where ( `uuid` = {TUID} ) ;"""
          QQ            = " " . join  ( QQ . split ( )                       )
          DB            . Query       ( QQ                                   )
          RR            = DB . FetchOne (                                    )
          if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )      :
            E164        = RR          [ 0                                    ]
        ######################################################################
        J [ "E164"    ] = E164
        ######################################################################
        NUID            = J           [ "Nation"                             ]
        CNAME           = ""
        ######################################################################
        if                            ( NUID > 0                           ) :
          CNAME         = self . GetName ( DB , NAMTAB , NUID                )
        ######################################################################
        J [ "Country" ] = CNAME
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
    PACTAB  = self . Tables      [ "AreaCode"                                ]
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"select `uuid` from {PACTAB} order by `id` {ORDER} ;"
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
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
    PACTAB = self . Tables [ "AreaCode"                                      ]
    ##########################################################################
    QQ     = f"select count(*) from {PACTAB} ;"
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
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    PACTAB = self . Tables   [ "AreaCode"                                    ]
    QQ     = f"select count(*) from {PACTAB} ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    PACTAB = self . Tables [ "AreaCode"                                      ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . SortOrder
    ##########################################################################
    QQ     = f"""select `uuid` from {PACTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def FetchSessionInformation                    ( self , DB               ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount (        DB                 )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "place/uuids;nation/uuids;itu/uuids"
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
      ########################################################################
    elif                            ( mtype in [ "nation/uuids" ]          ) :
      ########################################################################
      MSG   = self . getMenuItem    ( "AssignNation"                         )
      self  . ShowStatus            ( MSG                                    )
      ########################################################################
    elif                            ( mtype in [ "itu/uuids" ]             ) :
      ########################################################################
      MSG   = self . getMenuItem    ( "AssignITU"                            )
      self  . ShowStatus            ( MSG                                    )
      ########################################################################
    elif                            ( mtype in [ "organization/uuids" ]    ) :
      ########################################################################
      MSG   = self . getMenuItem    ( "AssignOrganization"                   )
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
  def acceptNationsDrop        ( self                                      ) :
    return True
  ############################################################################
  def acceptItuDrop            ( self                                      ) :
    return True
  ############################################################################
  def acceptOrganizationsDrop  ( self                                      ) :
    return True
  ############################################################################
  def dropPlaces                       ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . AssingPlaceToAreaCode        )
  ############################################################################
  def dropNations                      ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . AssingNationToAreaCode       )
  ############################################################################
  def dropITU                          ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . AssingItuToAreaCode          )
  ############################################################################
  def dropOrganizations                ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . AssingOrganizationToAreaCode )
  ############################################################################
  def AssingItemToAreaCode           ( self                                , \
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
    FMT    = self . getMenuItem      ( msgId                                 )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    PACTAB = self . Tables           [ "AreaCode"                            ]
    NAMTAB = self . Tables           [ "Names"                               ]
    DB     . LockWrites              ( [ PACTAB ]                            )
    QQ     = f"""update {PACTAB}
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
  def AssingPlaceToAreaCode            ( self , UUID , UUIDs               ) :
    return self . AssingItemToAreaCode ( UUID                              , \
                                         UUIDs                             , \
                                         "AssignPlace"                     , \
                                         "place"                           , \
                                         5                                   )
  ############################################################################
  def AssingNationToAreaCode           ( self , UUID , UUIDs               ) :
    return self . AssingItemToAreaCode ( UUID                              , \
                                         UUIDs                             , \
                                         "AssignNation"                    , \
                                         "nation"                          , \
                                         4                                   )
  ############################################################################
  def AssingOrganizationToAreaCode     ( self , UUID , UUIDs               ) :
    return self . AssingItemToAreaCode ( UUID                              , \
                                         UUIDs                             , \
                                         "AssignOrganization"              , \
                                         "administrative"                  , \
                                         6                                   )
  ############################################################################
  def AssingItuToAreaCode            ( self , UUID , UUIDs                 ) :
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
    FMT    = self . getMenuItem      ( "AssignITU"                           )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    PACTAB = self . Tables           [ "AreaCode"                            ]
    ITUTAB = self . Tables           [ "ITU"                                 ]
    DB     . LockWrites              ( [ PACTAB ]                            )
    QQ     = f"""update {PACTAB}
                  set `itu` = {PCID}
                  where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    DB     . UnlockTables            (                                       )
    ##########################################################################
    name   = ""
    QQ     = f"select `itu` from {ITUTAB} where ( `uuid` = {PCID} ) ;"
    DB     . Query                   ( QQ                                    )
    RR     = DB . FetchOne           (                                       )
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )            :
      name = str                     ( RR [ 0 ]                              )
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
    self   . emitAssignColumn . emit ( IT , 6 , name                         )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "AreaCodeWidget" , 9                             )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def UpdateItem                     ( self , item , uuid , column , name  ) :
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    PACTAB = self . Tables           [ "AreaCode"                            ]
    ##########################################################################
    DB     . LockWrites              ( [ PACTAB ]                            )
    ##########################################################################
    col    = "name"
    if                               ( column in [ 0 ]                     ) :
      col  = "name"
    elif                             ( column in [ 8 ]                     ) :
      col  = "comment"
    ##########################################################################
    QQ     = f"""update {PACTAB}
                   set `{col}` = %s
                   where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . QueryValues             ( QQ , ( name , )                       )
    ##########################################################################
    DB     . Close                   (                                       )
    ##########################################################################
    self   . emitAssignColumn . emit ( item , column , name                  )
    ##########################################################################
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def UpdateUsage             ( self , item , uuid , usage                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    PACTAB = self . Tables    [ "AreaCode"                                   ]
    ##########################################################################
    DB     . LockWrites       ( [ PACTAB ]                                   )
    ##########################################################################
    QQ     = f"""update {PACTAB}
                 set `used` = {usage}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 0                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9009 )         :
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
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu     ( mm                                 )
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
    return True
##############################################################################

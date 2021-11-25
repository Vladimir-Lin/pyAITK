# -*- coding: utf-8 -*-
##############################################################################
## PositionListings
## 地理經緯度
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
"""
4730000000000000001
create table `positions` (
  `id` integer not null auto_increment primary key,
  `uuid` bigint not null,
  `prefer` integer default 0,
  `states` bigint default 0,
  `longitude` bigint default -1,
  `latitude` bigint default -1,
  `altitude` bigint default 0,
  `longstr` tinyblob default '' ,
  `altistr` tinyblob default '' ,
  `ltime` timestamp not null default current_timestamp() ON UPDATE current_timestamp(),
  UNIQUE KEY `position` (`uuid`,`longitude`,`latitude`,`altitude`),
  KEY `uuid` (`uuid`),
  KEY `prefer` (`prefer`),
  KEY `states` (`states`),
  KEY `longitude` (`longitude`),
  KEY `latitude` (`latitude`),
  KEY `altitude` (`altitude`),
  KEY `longstr` (`longstr`(32)),
  KEY `altistr` (`altistr`(32)),
  KEY `ltime` (`ltime`)
) Engine = Federated default charset = utf8mb4 connection = "FederatedForInsider/positions" ;
"""
##############################################################################
class PositionListings             ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( list                                    )
  emitAssignColumn  = pyqtSignal   ( QTreeWidgetItem , int , str             )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "asc"
    self . Uuid               = 0
    self . Symbol             = "°"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
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
    self . emitNamesShow    . connect ( self . show                          )
    self . emitAllNames     . connect ( self . refresh                       )
    self . emitAssignColumn . connect ( self . AssignColumnText              )
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
    return self . SizeSuggestion   ( QSize ( 640 , 640 )                     )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self   . setActionLabel        ( "Label"      , self . windowTitle ( )   )
    self   . LinkAction            ( "Refresh"    , self . startup           )
    ##########################################################################
    if                             ( int ( self . Uuid ) > 0               ) :
      self . LinkAction            ( "Insert"     , self . InsertItem        )
    ##########################################################################
    self   . LinkAction            ( "Delete"     , self . DeleteItems       )
    self   . LinkAction            ( "Rename"     , self . RenameItem        )
    self   . LinkAction            ( "Copy"       , self . CopyToClipboard   )
    self   . LinkAction            ( "Home"       , self . PageHome          )
    self   . LinkAction            ( "End"        , self . PageEnd           )
    self   . LinkAction            ( "PageUp"     , self . PageUp            )
    self   . LinkAction            ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self   . LinkAction            ( "SelectAll"  , self . SelectAll         )
    self   . LinkAction            ( "SelectNone" , self . SelectNone        )
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
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 , 1 , 2 ]              ) :
      return
    ##########################################################################
    line   = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
    line   . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    text   = item . text        ( column                                     )
    if                          ( len ( text ) > 0                         ) :
      return
    ##########################################################################
    S      = self . Symbol
    ##########################################################################
    if                          ( column == 0                              ) :
      msg  = f"00{S}00'00.000000\"E"
      line . setText            ( msg                                        )
      return
    ##########################################################################
    if                          ( column == 1                              ) :
      msg  = f"00{S}00'00.000000\"N"
      line . setText            ( msg                                        )
      return
    ##########################################################################
    if                          ( column == 2                              ) :
      msg  = "0.0"
      line . setText            ( msg                                        )
      return
    ##########################################################################
    return
  ############################################################################
  def AssignColumnText             ( self , item , ID , text ) :
    ##########################################################################
    item . setText                 ( ID , text                               )
    ##########################################################################
    return
  ############################################################################
  def toAltitudeString           ( self , altitude                         ) :
    ##########################################################################
    Z     = int                  ( altitude                                  )
    V     = int                  ( altitude                                  )
    K     =                      ( Z >= 0                                    )
    P     = ""
    if                           ( not K                                   ) :
      P   = "-"
      V   = -V
    ##########################################################################
    if                           ( V <= 0                                  ) :
      return "0"
    ##########################################################################
    if                           ( V < 10000                               ) :
      ########################################################################
      S   = f"{V}"
      L   = len                  ( S                                         )
      for i in range             ( L , 4                                   ) :
        S = f"0{S}"
      ########################################################################
      return f"{P}0.{S}"
    ##########################################################################
    S     = f"{V}"
    L     = len                  ( S                                         )
    T     = S                    [ -4 :                                      ]
    H     = S                    [    : L - 4                                ]
    ##########################################################################
    return f"{P}{H}.{T}"
  ############################################################################
  def PrepareItem                ( self , JSON                             ) :
    ##########################################################################
    ID        = JSON             [ "Id"                                      ]
    UUID      = JSON             [ "Uuid"                                    ]
    PREFER    = JSON             [ "Prefer"                                  ]
    STATES    = JSON             [ "States"                                  ]
    LONGITUDE = JSON             [ "Longitude"                               ]
    LATITUDE  = JSON             [ "Latitude"                                ]
    ALTITUDE  = JSON             [ "Altitude"                                ]
    LONGSTR   = JSON             [ "LongString"                              ]
    LATISTR   = JSON             [ "LatiString"                              ]
    ##########################################################################
    UXID      = str              ( UUID                                      )
    ALTISTR   = self . toAltitudeString ( ALTITUDE                           )
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    ##########################################################################
    IT   . setText               ( 0 , LONGSTR                               )
    IT   . setToolTip            ( 0 , UXID                                  )
    IT   . setData               ( 0 , Qt . UserRole , str ( ID )            )
    ##########################################################################
    IT   . setText               ( 1 , LATISTR                               )
    ## IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    ##########################################################################
    IT   . setText               ( 2 , ALTISTR                               )
    IT   . setTextAlignment      ( 2 , Qt.AlignRight                         )
    ##########################################################################
    IT   . setData               ( 3 , Qt . UserRole , JSON                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    if                           ( int ( self . Uuid ) <= 0                ) :
      return
    ##########################################################################
    self . Go                    ( self . AppendPosition                     )
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
    ID     = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . UpdateItem                       , \
                                   ( item , column , ID , msg , )            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def DeleteItems                ( self                                    ) :
    ##########################################################################
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
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    POSTAB  = self . Tables           [ "Positions"                          ]
    LISTS   =                         [                                      ]
    UUID    = int                     ( self . Uuid                          )
    ##########################################################################
    if                                ( UUID > 0                           ) :
      QQ    = f"select count(*) from {POSTAB} where ( `uuid` = {UUID} ) ;"
    else                                                                     :
      QQ    = f"select count(*) from {POSTAB} ;"
    ##########################################################################
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )            :
      self . Total = RR               [ 0                                    ]
    ##########################################################################
    TOTAL   = self . Total
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder  (                                      )
    ##########################################################################
    if                                ( UUID > 0                           ) :
      QQ    = f"""select
                  `id`,`uuid`,
                  `prefer`,`states`,
                  `longitude`,`latitude`,`altitude`,
                  `longstr`,`latistr`
                  from {POSTAB}
                  where ( `uuid` = {UUID} )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    else                                                                     :
      QQ    = f"""select
                  `id`,`uuid`,
                  `prefer`,`states`,
                  `longitude`,`latitude`,`altitude`,
                  `longstr`,`latistr`
                  from {POSTAB}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    if ( ( ALL not in [ False , None ] ) and ( len ( ALL ) > 0 ) )           :
      for K in ALL                                                           :
        ######################################################################
        J   =                         {                                      }
        ######################################################################
        J [ "Id"         ] = int      ( K [ 0 ]                              )
        J [ "Uuid"       ] = int      ( K [ 1 ]                              )
        J [ "Prefer"     ] = int      ( K [ 2 ]                              )
        J [ "States"     ] = int      ( K [ 3 ]                              )
        J [ "Longitude"  ] = int      ( K [ 4 ]                              )
        J [ "Latitude"   ] = int      ( K [ 5 ]                              )
        J [ "Altitude"   ] = int      ( K [ 6 ]                              )
        J [ "LongString" ] = self . assureString ( K [ 7 ]                   )
        J [ "LatiString" ] = self . assureString ( K [ 8 ]                   )
        ######################################################################
        LISTS . append                ( J                                    )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . emitAllNames  . emit    ( LISTS                                )
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
  def AppendPosition             ( self                                    ) :
    ##########################################################################
    if                           ( int ( self . Uuid ) <= 0                ) :
      return
    ##########################################################################
    DB      = self . ConnectDB   (                                           )
    if                           ( DB == None                              ) :
      return
    ##########################################################################
    POSTAB  = self . Tables      [ "Positions"                               ]
    UUID    = self . Uuid
    ##########################################################################
    DB      . LockWrites         ( [ POSTAB ]                                )
    QQ      = f"insert into {POSTAB} ( `uuid` ) values ( {UUID} ) ;"
    DB      . Query              ( QQ                                        )
    ##########################################################################
    DB      . UnlockTables       (                                           )
    DB      . Close              (                                           )
    ##########################################################################
    self    . loading            (                                           )
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
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 3 , 3                                     )
    ##########################################################################
    LABELs = self . Translations [ "PositionListings" ] [ "Labels"           ]
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
  def toDegreeString               ( self , Degree                         ) :
    ##########################################################################
    S         = self . Symbol
    ##########################################################################
    MSECS     = int                ( Degree % 1000000                        )
    R         = int                ( Degree / 1000000                        )
    SECS      = int                ( R % 100                                 )
    R         = int                ( R / 100                                 )
    MINUTE    = int                ( R % 100                                 )
    DEGREE    = int                ( R / 100                                 )
    ##########################################################################
    MM        = f"{MSECS}"
    MM        = MM . zfill         ( 6                                       )
    ##########################################################################
    SS        = f"{SECS}"
    SS        = SS . zfill         ( 2                                       )
    ##########################################################################
    MS        = f"{MINUTE}"
    MS        = MS . zfill         ( 2                                       )
    ##########################################################################
    return f"{DEGREE}{S}{MS}'{SS}.{MM}\""
  ############################################################################
  def toLongitude                   ( self , text                          ) :
    ##########################################################################
    S        = self . Symbol
    ##########################################################################
    L        = text . split         ( S                                      )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    DEGREE   = L                    [ 0                                      ]
    R        = L                    [ 1                                      ]
    ##########################################################################
    L        = R    . split         ( "'"                                    )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    MINUTE   = L                    [ 0                                      ]
    R        = L                    [ 1                                      ]
    ##########################################################################
    L        = R    . split         ( "\""                                   )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    SECS     = L                    [ 0                                      ]
    MSECS    = "0"
    RD       = L                    [ 1                                      ]
    RD       = RD . lower           (                                        )
    ##########################################################################
    if                              ( RD not in [ "e" , "w" ]              ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    if                              ( "." in SECS                          ) :
      ########################################################################
      L      = SECS . split         ( "."                                    )
      if                            ( len ( L ) != 2                       ) :
        return                      { "Okay" : False                         }
      ########################################################################
      SECS   = L                    [ 0                                      ]
      MSECS  = L                    [ 1                                      ]
    ##########################################################################
    try                                                                      :
      DEGREE = int                  ( DEGREE                                 )
      if                            ( ( DEGREE > 180 ) or ( DEGREE < 0 ) )   :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      MINUTE = int                  ( MINUTE                                 )
      if                            ( ( MINUTE >= 60 ) or ( MINUTE < 0 ) )   :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      SECS   = int                  ( SECS                                   )
      if                            ( ( SECS >= 60 ) or ( SECS < 0 ) )       :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      ########################################################################
      LEN    = len                  ( MSECS                                  )
      RV     = int                  ( MSECS                                  )
      ########################################################################
      if                            ( LEN > 6                              ) :
        for i in range              ( 6 , LEN                              ) :
          RV = int                  ( RV / 10                                )
      elif                          ( LEN < 6                              ) :
        for i in range              ( LEN , 6                              ) :
          RV = int                  ( RV * 10                                )
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    V       = int                   ( DEGREE * 10000000000                   )
    V       = V + int               ( MINUTE *   100000000                   )
    V       = V + int               ( SECS   *     1000000                   )
    V       = V + RV
    ##########################################################################
    K       = V
    if                              ( RD in [ "w" ]                        ) :
      V     = -V
    ##########################################################################
    RD      = RD   . upper          (                                        )
    TDS     = self . toDegreeString ( K                                      )
    ##########################################################################
    return                          { "Okay"   : True                      , \
                                      "Value"  : V                         , \
                                      "String" : f"{TDS}{RD}"                }
  ############################################################################
  def toLatitude                    ( self , text                          ) :
    ##########################################################################
    S        = self . Symbol
    ##########################################################################
    L        = text . split         ( S                                      )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    DEGREE   = L                    [ 0                                      ]
    R        = L                    [ 1                                      ]
    ##########################################################################
    L        = R    . split         ( "'"                                    )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    MINUTE   = L                    [ 0                                      ]
    R        = L                    [ 1                                      ]
    ##########################################################################
    L        = R    . split         ( "\""                                   )
    if                              ( len ( L ) != 2                       ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    SECS     = L                    [ 0                                      ]
    MSECS    = "0"
    RD       = L                    [ 1                                      ]
    RD       = RD . lower           (                                        )
    ##########################################################################
    if                              ( RD not in [ "n" , "s" ]              ) :
      return                        { "Okay" : False                         }
    ##########################################################################
    if                              ( "." in SECS                          ) :
      ########################################################################
      L      = SECS . split         ( "."                                    )
      if                            ( len ( L ) != 2                       ) :
        return                      { "Okay" : False                         }
      ########################################################################
      SECS   = L                    [ 0                                      ]
      MSECS  = L                    [ 1                                      ]
    ##########################################################################
    try                                                                      :
      DEGREE = int                  ( DEGREE                                 )
      if                            ( ( DEGREE > 90 ) or ( DEGREE < 0 ) )    :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      MINUTE = int                  ( MINUTE                                 )
      if                            ( ( MINUTE >= 60 ) or ( MINUTE < 0 ) )   :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      SECS   = int                  ( SECS                                   )
      if                            ( ( SECS >= 60 ) or ( SECS < 0 ) )       :
        return                      { "Okay" : False                         }
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    try                                                                      :
      ########################################################################
      LEN    = len                  ( MSECS                                  )
      RV     = int                  ( MSECS                                  )
      ########################################################################
      if                            ( LEN > 6                              ) :
        for i in range              ( 6 , LEN                              ) :
          RV = int                  ( RV / 10                                )
      elif                          ( LEN < 6                              ) :
        for i in range              ( LEN , 6                              ) :
          RV = int                  ( RV * 10                                )
    except                                                                   :
      return                        { "Okay" : False                         }
    ##########################################################################
    V       = int                   ( DEGREE * 10000000000                   )
    V       = V + int               ( MINUTE *   100000000                   )
    V       = V + int               ( SECS   *     1000000                   )
    V       = V + RV
    ##########################################################################
    K       = V
    if                              ( RD in [ "s" ]                        ) :
      V     = -V
    ##########################################################################
    RD      = RD   . upper          (                                        )
    TDS     = self . toDegreeString ( K                                      )
    ##########################################################################
    return                          { "Okay"   : True                      , \
                                      "Value"  : V                         , \
                                      "String" : f"{TDS}{RD}"                }
  ############################################################################
  def toAltitude                   ( self , text                           ) :
    ##########################################################################
    if                             ( "." in text                           ) :
      ########################################################################
      L     = text . split         ( "."                                     )
      if                           ( len ( L ) != 2                        ) :
        return                     { "Okay" : False                          }
      ########################################################################
      try                                                                    :
        ######################################################################
        V     = int                ( L [ 0 ]                                 )
        V     = V * 10000
        ######################################################################
      except                                                                 :
        return                     { "Okay" : False                          }
      ########################################################################
      try                                                                    :
        ######################################################################
        LEN   = len                ( L [ 1 ]                                 )
        R     = int                ( L [ 1 ]                                 )
        ######################################################################
        if                         ( LEN > 4                               ) :
          for i in range           ( 4 , LEN                               ) :
            R = int                ( R / 10                                  )
        elif                       ( LEN < 4                               ) :
          for i in range           ( LEN , 4                               ) :
            R = int                ( R * 10                                  )
        ######################################################################
        V     = int                ( V + R                                   )
        ######################################################################
        return                     { "Okay" : True , "Value" : V             }
      except                                                                 :
        return                     { "Okay" : False                          }
      ########################################################################
      return
    ##########################################################################
    try                                                                      :
      ########################################################################
      V     = int                  ( text                                    )
      V     = V * 10000
      ########################################################################
      return                       { "Okay" : True , "Value" : V             }
    except                                                                   :
      pass
    ##########################################################################
    return                         { "Okay" : False                          }
  ############################################################################
  def UpdateItem                   ( self , item , column , ID , name      ) :
    ##########################################################################
    JSON   = item . data           ( 3 , Qt . UserRole                       )
    ##########################################################################
    if                             ( column == 0                           ) :
      A    = self . toLongitude    ( name                                    )
    elif                           ( column == 1                           ) :
      A    = self . toLatitude     ( name                                    )
    elif                           ( column == 2                           ) :
      A    = self . toAltitude     ( name                                    )
    else                                                                     :
      self . Notify                ( 1                                       )
      return
    ##########################################################################
    if                             ( not A [ "Okay" ]                      ) :
      self . Notify                ( 1                                       )
      return
    ##########################################################################
    if                             ( column == 0                           ) :
      LONGITUDE = A                [ "Value"                                 ]
      LONGSTR   = A                [ "String"                                ]
    elif                           ( column == 1                           ) :
      LATITUDE  = A                [ "Value"                                 ]
      LATISTR   = A                [ "String"                                ]
    elif                           ( column == 2                           ) :
      ALTITUDE  = A                [ "Value"                                 ]
    ##########################################################################
    DON     = False
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      self . Notify                ( 1                                       )
      return
    ##########################################################################
    POSTAB  = self . Tables      [ "Positions"                               ]
    ##########################################################################
    if                             ( column == 0                           ) :
      ########################################################################
      QQ    = f"""update {POSTAB}
                  set `longitude` = %s , `longstr` = %s
                  where ( `id` = {ID} ) ;"""
      VAL   =                      ( LONGITUDE , LONGSTR                     )
      ########################################################################
    elif                           ( column == 1                           ) :
      ########################################################################
      QQ    = f"""update {POSTAB}
                  set `latitude` = %s , `latistr` = %s
                  where ( `id` = {ID} ) ;"""
      VAL   =                      ( LATITUDE  , LATISTR                     )
      ########################################################################
    elif                           ( column == 2                           ) :
      ########################################################################
      QQ    = f"""update {POSTAB}
                  set `altitude` = %s
                  where ( `id` = {ID} ) ;"""
      VAL   =                      ( ALTITUDE ,                              )
    ##########################################################################
    QQ      = " " . join           ( QQ . split ( )                          )
    if                             ( len ( QQ ) > 0                        ) :
      ########################################################################
      DB    . LockWrites           ( [ POSTAB ]                              )
      ########################################################################
      try                                                                    :
        ######################################################################
        DB  . QueryValues          ( QQ , VAL                                )
        DON = True
        ######################################################################
      except                                                                 :
        pass
      ########################################################################
      DB    . UnlockTables         (                                         )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    if                             ( not DON                               ) :
      self . Notify                ( 1                                       )
      return
    ##########################################################################
    if                             ( column == 0                           ) :
      ########################################################################
      JSON [ "Longitude"  ] = LONGITUDE
      JSON [ "LongString" ] = LONGSTR
      item . setData                 ( 3 , Qt . UserRole , JSON              )
      self . emitAssignColumn . emit ( item , column , LONGSTR               )
      ########################################################################
    elif                           ( column == 1                           ) :
      ########################################################################
      JSON [ "Latitude"   ] = LATITUDE
      JSON [ "LatiString" ] = LATISTR
      item . setData                 ( 3 , Qt . UserRole , JSON              )
      self . emitAssignColumn . emit ( item , column , LATISTR               )
      ########################################################################
    elif                           ( column == 2                           ) :
      ########################################################################
      JSON [ "Altitude" ] = ALTITUDE
      item . setData                 ( 3 , Qt . UserRole , JSON              )
      MSG  = self . toAltitudeString ( ALTITUDE                              )
      self . emitAssignColumn . emit ( item , column , MSG                   )
    ##########################################################################
    self   . Notify                ( 0                                       )
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 2                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9002 ) and ( at <= 9003 )         :
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
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    if                              ( int ( self . Uuid ) > 0              ) :
      self . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    self   . AppendRenameAction     ( mm , 1102                              )
    self   . AppendDeleteAction     ( mm , 1103                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
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
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
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
    if                              ( at == 1103                           ) :
      self . DeleteItems            (                                        )
      return True
    ##########################################################################
    return True
##############################################################################

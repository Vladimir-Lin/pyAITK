# -*- coding: utf-8 -*-
##############################################################################
## GeocontourListings
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
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
from   PyQt5 . QtWidgets              import QFileDialog
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
class GeocontourListings           ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int , int                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "GeocontourListings"
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "desc"
    self . EditAllNames       = None
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 7 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setAcceptDrops          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DragOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1280 , 640 )                      )
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
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
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 0 , 1 , 2 , 4 , 5 , 6 ] ) :
      return
    ##########################################################################
    if                           ( column     in [ 0 ,         4 , 5 , 6 ] ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    TRX    = self . Translations [ self . ClassTag                           ]
    ##########################################################################
    if                           ( column in [ 1                         ] ) :
      ########################################################################
      LL   = TRX                 [ "Types"                                   ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . comboChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 2                         ] ) :
      ########################################################################
      LL   = TRX                 [ "Public"                                  ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . comboChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem              ( self , UUID , NAME , TYPE                 ) :
    ##########################################################################
    TRX  = self . Translations [ self . ClassTag                             ]
    UXID = str                 ( UUID                                        )
    GTYP = str                 ( TYPE [ 0                                  ] )
    PUBL = str                 ( TYPE [ 1                                  ] )
    PTS  = str                 ( TYPE [ 2                                  ] )
    ##########################################################################
    IT   = QTreeWidgetItem     (                                             )
    IT   . setText             ( 0 , NAME                                    )
    IT   . setToolTip          ( 0 , UXID                                    )
    IT   . setData             ( 0 , Qt . UserRole , UUID                    )
    IT   . setText             ( 1 , TRX [ "Types"  ] [ GTYP ]               )
    IT   . setData             ( 1 , Qt . UserRole , GTYP                    )
    IT   . setText             ( 2 , TRX [ "Public" ] [ PUBL ]               )
    IT   . setData             ( 2 , Qt . UserRole , PUBL                    )
    IT   . setText             ( 3 , PTS                                     )
    IT   . setTextAlignment    ( 3 , Qt.AlignRight                           )
    IT   . setText             ( 4 , self . BlobToString ( TYPE [ 3      ] ) )
    IT   . setText             ( 5 , self . BlobToString ( TYPE [ 4      ] ) )
    IT   . setText             ( 6 , self . BlobToString ( TYPE [ 5      ] ) )
    ##########################################################################
    return IT
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
    ##########################################################################
    if                           ( column in [ 0                         ] ) :
      ########################################################################
      self . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    if                           ( column in [ 4 , 5 , 6                 ] ) :
      ########################################################################
      self . Go                  ( self . AssureUuidColumn                 , \
                                   ( item , uuid , msg , column )            )
    ##########################################################################
    return
  ############################################################################
  def comboChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    TRX    = self . Translations [ self . ClassTag                           ]
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    sb     = self . CurrentItem  [ "Widget"                                  ]
    v      = item . data         ( column , Qt . UserRole                    )
    v      = int                 ( v                                         )
    nv     = sb   . itemData     ( sb . currentIndex ( )                     )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    name   = ""
    na     = ""
    ##########################################################################
    if                           ( column in [ 1 ]                         ) :
      ########################################################################
      name = TRX [ "Types"  ]    [ nv                                        ]
      na   = "type"
      ########################################################################
    elif                         ( column in [ 2 ]                         ) :
      ########################################################################
      name = TRX [ "Public" ]    [ nv                                        ]
      na   = "public"
    ##########################################################################
    if                           ( v == nv                                 ) :
      ########################################################################
      item . setText             ( column , name                             )
      self . removeParked        (                                           )
      return
    ##########################################################################
    self . Go                    ( self . UpdateItemValue                  , \
                                   ( uuid , na , nv , )                      )
    ##########################################################################
    item . setText               ( column , name                             )
    item . setData               ( column , Qt . UserRole , nv               )
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        dict                              )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    TYPEs  = JSON                 [ "TYPEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , NAMEs [ U ] , TYPEs [ U ]            )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( UUIDs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
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
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    TYPEs   =                         {                                      }
    TYPTAB  = self . Tables           [ "Contours"                           ]
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select
                  `type`,`public`,`points`,`name`,`comment`,`wiki`
                  from {TYPTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR is not False ) and ( RR is not None ) )                      :
        TYPEs [ UUID ] = RR
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
    JSON [ "TYPEs" ] = TYPEs
    ##########################################################################
    self    . emitAllNames  . emit    ( JSON                                 )
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "geocontours/uuids"
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
  def ObtainAllUuids        ( self , DB                                    ) :
    ##########################################################################
    TABLE = self . Tables   [ "Contours"                                     ]
    ##########################################################################
    QQ    = f"select `uuid` from {TABLE} order by `id` asc ;"
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    CTRTAB = self . Tables          [ "Contours"                             ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                       )
    ##########################################################################
    QQ     = f"""select `uuid` from {CTRTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                        )
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 7                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    CTRTAB = self . Tables    [ "Contours"                                   ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ CTRTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( CTRTAB , "uuid" , 4840000000000000000        )
      DB   . AppendUuid       ( CTRTAB , uuid                                )
    ##########################################################################
    if                        ( uuid > 0                                   ) :
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidColumn        ( self , item , uuid , name , column         ) :
    ##########################################################################
    try                                                                      :
      blob = name . encode    ( "utf-8"                                      )
    except                                                                   :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    CTRTAB = self . Tables    [ "Contours"                                   ]
    COLN   = ""
    ##########################################################################
    if                        ( 4 == column                                ) :
      COLN = "name"
    elif                      ( 5 == column                                ) :
      COLN = "comment"
    elif                      ( 6 == column                                ) :
      COLN = "wiki"
    ##########################################################################
    DB     . LockWrites       ( [ CTRTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {CTRTAB}
                 set `{COLN}` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . QueryValues      ( QQ , ( blob , )                              )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemValue         ( self , uuid , item , value                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    CTRTAB = self . Tables    [ "Contours"                                   ]
    ##########################################################################
    DB     . LockWrites       ( [ CTRTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"""update {CTRTAB}
                 set `{item}` = {value}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . insertTopLevelItem ( 0 , item                                     )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def LoadFileContent        ( self , Filename                             ) :
    ##########################################################################
    TEXT     = ""
    BODY     = ""
    ##########################################################################
    try                                                                      :
      with open              ( Filename , "rb" ) as File                     :
        TEXT = File . read   (                                               )
    except                                                                   :
      return "" , False
    ##########################################################################
    try                                                                      :
      BODY   = TEXT . decode ( "utf-8"                                       )
    except                                                                   :
      return "" , False
    ##########################################################################
    return BODY , True
  ############################################################################
  def DecodeFromText      ( self , BODY                                    ) :
    ##########################################################################
    LINEs  = BODY . split ( " "                                              )
    KMLs   =              [                                                  ]
    ##########################################################################
    for L in LINEs                                                           :
      ########################################################################
      if                  ( len ( L ) <= 0                                 ) :
        continue
      ########################################################################
      P    = L . split    ( ","                                              )
      ########################################################################
      if                  ( 3 != len ( P )                                 ) :
        continue
      ########################################################################
      A    = float        ( P [ 0                                          ] )
      B    = float        ( P [ 1                                          ] )
      C    = float        ( P [ 2                                          ] )
      ########################################################################
      KMLs . append       ( [ A , B , C                                    ] )
    ##########################################################################
    return KMLs
  ############################################################################
  def DecodeFromKml       ( self , BODY                                    ) :
    ##########################################################################
    LINEs  = BODY . split ( " "                                              )
    KMLs   =              [                                                  ]
    ##########################################################################
    for L in LINEs                                                           :
      ########################################################################
      if                  ( len ( L ) <= 0                                 ) :
        continue
      ########################################################################
      P    = L . split    ( ","                                              )
      ########################################################################
      if                  ( 3 != len ( P )                                 ) :
        continue
      ########################################################################
      A    = float        ( P [ 0                                          ] )
      B    = float        ( P [ 1                                          ] )
      C    = float        ( P [ 2                                          ] )
      ########################################################################
      KMLs . append       ( [ A , B , C                                    ] )
    ##########################################################################
    return KMLs
  ############################################################################
  def LoadFromFilename                   ( self , uuid , Filename          ) :
    ##########################################################################
    if                                   ( len ( Filename ) <= 0           ) :
      self      . Notify                 ( 1                                 )
      return
    ##########################################################################
    BODY , OKAY = self . LoadFileContent ( Filename                          )
    ##########################################################################
    if                                   ( not OKAY                        ) :
      self      . Notify                 ( 1                                 )
      return
    ##########################################################################
    LNAME       = Filename . lower       (                                   )
    SPOTs       =                        [                                   ]
    ##########################################################################
    if                                   ( ".txt" in LNAME                 ) :
      ########################################################################
      SPOTs     = self . DecodeFromText  ( BODY                              )
      ########################################################################
    elif                                 ( ".kml" in LNAME                 ) :
      ########################################################################
      SPOTs     = self . DecodeFromKml   ( BODY                              )
    ##########################################################################
    POINTs      = len                    ( SPOTs                             )
    ##########################################################################
    try                                                                      :
      ########################################################################
      name      = json . dumps           ( SPOTs                             )
      name      = name . replace         ( " " , ""                          )
      blob      = name . encode          ( "utf-8"                           )
      ########################################################################
    except                                                                   :
      return
    ##########################################################################
    DB          = self . ConnectDB       (                                   )
    if                                   ( self . NotOkay ( DB )           ) :
      return
    ##########################################################################
    CTRTAB      = self . Tables          [ "Contours"                        ]
    ##########################################################################
    DB          . LockWrites             ( [ CTRTAB                        ] )
    ##########################################################################
    QQ          = f"""update {CTRTAB}
                      set `spots` = %s , `points` = {POINTs}
                      where ( `uuid` = {uuid} ) ;"""
    QQ          = " " . join             ( QQ . split (                    ) )
    DB          . QueryValues            ( QQ , ( blob , )                   )
    ##########################################################################
    DB          . Close                  (                                   )
    ##########################################################################
    self        . loading                (                                   )
    self        . Notify                 ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def ImportKml                   ( self , uuid                            ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "TextFilters"                            )
    Name , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    "D:/AITK/Geocontours"                  , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    self     . Go                 ( self . LoadFromFilename                , \
                                    ( uuid , Name , )                        )
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
    return self . DefaultColumnsMenu (        mm , 7                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9007 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    self   . AppendInsertAction     ( mm , 1011                              )
    ##########################################################################
    if                              ( uuid > 0                             ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Import"                               )
      mm   . addAction              ( 2001 , msg                             )
    ##########################################################################
    if                              ( len ( items ) == 1                   ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
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
    if                              ( at == 1001                           ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1011                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 2001                           ) :
      self . ImportKml              ( uuid                                   )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      ########################################################################
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "NamesEditing"                         ]
      self . EditAllNames           ( self , "Contours" , uuid , NAM         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

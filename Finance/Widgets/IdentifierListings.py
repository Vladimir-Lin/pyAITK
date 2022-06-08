# -*- coding: utf-8 -*-
##############################################################################
## IdentifierListings
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
class IdentifierListings           ( TreeDock                              ) :
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
    self . ProductType        = 0
    self . IdentifierTag      = "IdentifierListings"
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "desc"
    self . Uuid               = 0
    self . UUIDs              =    [                                         ]
    self . TypeMaps           =    {                                         }
    ##########################################################################
    self . Method             = "All"
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    ##########################################################################
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 3 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
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
  def setUuidMethod                ( self , UUID , TYPE                    ) :
    ##########################################################################
    self . Method      = "UUID"
    self . ProductType = TYPE
    self . Uuid        = UUID
    ##########################################################################
    return
  ############################################################################
  def isUuidMethod ( self                                                  ) :
    return         ( self . Method in [ "UUID" ]                             )
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 1024 , 640                              )
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
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
    self . setActionLabel ( "Label" , self . windowTitle ( )                 )
    self . AttachActions  ( True                                             )
    ## self . LinkVoice      ( self . CommandParser                             )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent           ( self , event                                  ) :
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
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 2 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                2                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent    ( self , IT , ITEM                             ) :
    ##########################################################################
    ID         = ITEM       [ "Id"                                           ]
    UUID       = ITEM       [ "Uuid"                                         ]
    TYPE       = ITEM       [ "Type"                                         ]
    NAME       = ITEM       [ "Name"                                         ]
    TNAME      = ITEM       [ "TName"                                        ]
    IDENTIFIER = ITEM       [ "Identifier"                                   ]
    UXID       = str        ( UUID                                           )
    ##########################################################################
    IT         . setText    ( 0 , NAME                                       )
    IT         . setToolTip ( 0 , UXID                                       )
    IT         . setData    ( 0 , Qt . UserRole , ID                         )
    ##########################################################################
    IT         . setText    ( 1 , TNAME                                      )
    IT         . setText    ( 2 , IDENTIFIER                                 )
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
  @pyqtSlot                     (                                            )
  def InsertItem                ( self                                     ) :
    ##########################################################################
    if                          ( not self . isUuidMethod ( )              ) :
      return
    ##########################################################################
    item   = QTreeWidgetItem    (                                            )
    item   . setData            ( 0 , Qt . UserRole , 0                      )
    ##########################################################################
    if                          ( self . SortOrder in [ "desc" ]           ) :
      self . insertTopLevelItem ( 0 , item                                   )
    else :
      self . addTopLevelItem    ( item                                       )
    ##########################################################################
    line   = self . setLineEdit ( item                                     , \
                                  2                                        , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
    line   . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
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
    self . doubleClicked         ( IT , 2                                    )
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
  def GetTypeMaps               ( self , DB                                ) :
    ##########################################################################
    CNT    = len                ( self . TypeMaps                            )
    if                          ( CNT > 0                                  ) :
      return
    ##########################################################################
    TYPTAB = self . Tables      [ "Types"                                    ]
    NAMTAB = self . Tables      [ "Names"                                    ]
    ##########################################################################
    QQ     = f"""select `uuid` from {TYPTAB}
                 where ( `used` = 1 )
                 order by `id` asc ;"""
    QQ     = " " . join         ( QQ . split ( )                             )
    UUIDs  = DB   . ObtainUuids ( QQ                                         )
    NAMEs  = self . GetNames    ( DB , NAMTAB , UUIDs                        )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      TYPE = int                ( UUID % 1000000                             )
      self . TypeMaps [ TYPE ] = NAMEs [ UUID ]
    ##########################################################################
    return
  ############################################################################
  def ObtainOriginal                      ( self , DB                      ) :
    ##########################################################################
    IDFTAB       = self . Tables          [ "Identifiers"                    ]
    ##########################################################################
    self . Total = 0
    ##########################################################################
    QQ           = f"select count(*) from {IDFTAB} ;"
    DB           . Query                  ( QQ                               )
    RR           = DB . FetchOne          (                                  )
    ##########################################################################
    if                                    ( RR not in [ False , None ]     ) :
      if                                  ( len ( RR ) > 0                 ) :
        self . Total = int                ( RR [ 0 ]                         )
    ##########################################################################
    if                                    ( self . Total <= 0              ) :
      return                              [                                  ]
    ##########################################################################
    IDs          =                        [                                  ]
    STARTID      = self . StartId
    AMOUNT       = self . Amount
    ORDER        = self . getSortingOrder (                                  )
    ##########################################################################
    QQ           = f"""select `id` from {IDFTAB}
                       order by `id` {ORDER}
                       limit {STARTID} , {AMOUNT} ;"""
    QQ           = " " . join             ( QQ . split ( )                   )
    IDs          = DB . ObtainUuids       ( QQ                               )
    ##########################################################################
    return IDs
  ############################################################################
  def ObtainSearching           ( self , DB                                ) :
    ##########################################################################
    ##########################################################################
    return                      [                                            ]
  ############################################################################
  def ObtainSubordination       ( self , DB                                ) :
    ##########################################################################
    ##########################################################################
    return                      [                                            ]
  ############################################################################
  def ObtainReverse             ( self , DB                                ) :
    ##########################################################################
    ##########################################################################
    return                      [                                            ]
  ############################################################################
  def ObtainSpecified           ( self , DB                                ) :
    ##########################################################################
    IDFTAB       = self . Tables          [ "Identifiers"                    ]
    ##########################################################################
    self . Total = 0
    UUID         = self . Uuid
    GTYPE        = self . ProductType
    ##########################################################################
    QQ           = f"""select count(*) from {IDFTAB}
                       where ( `uuid` = {UUID} )
                         and ( `type` = {GTYPE} ) ;"""
    QQ           = " " . join             ( QQ . split ( )                   )
    DB           . Query                  ( QQ                               )
    RR           = DB . FetchOne          (                                  )
    ##########################################################################
    if                                    ( RR not in [ False , None ]     ) :
      if                                  ( len ( RR ) > 0                 ) :
        self . Total = int                ( RR [ 0 ]                         )
    ##########################################################################
    if                                    ( self . Total <= 0              ) :
      return                              [                                  ]
    ##########################################################################
    IDs          =                        [                                  ]
    STARTID      = self . StartId
    AMOUNT       = self . Amount
    ORDER        = self . getSortingOrder (                                  )
    ##########################################################################
    QQ           = f"""select `id` from {IDFTAB}
                       where ( `uuid` = {UUID} )
                         and ( `type` = {GTYPE} )
                       order by `id` {ORDER}
                       limit {STARTID} , {AMOUNT} ;"""
    QQ           = " " . join             ( QQ . split ( )                   )
    IDs          = DB . ObtainUuids       ( QQ                               )
    ##########################################################################
    return IDs
  ############################################################################
  def GetIdentifierDetail             ( self , DB , ID                     ) :
    ##########################################################################
    IDFTAB       = self . Tables      [ "Identifiers"                        ]
    NAMTAB       = self . Tables      [ "Names"                              ]
    ##########################################################################
    J            =                    { "Id"         : ID                    ,
                                        "Uuid"       : 0                     ,
                                        "Type"       : 0                     ,
                                        "Name"       : ""                    ,
                                        "TName"      : ""                    ,
                                        "Identifier" : ""                    }
    ##########################################################################
    QQ           = f"""select `uuid`,`type`,`name` from {IDFTAB}
                       where ( `id` = {ID} ) ;"""
    QQ           = " " . join         ( QQ . split ( )                       )
    DB           . Query              ( QQ                                   )
    RR           = DB . FetchOne      (                                      )
    ##########################################################################
    if                                ( RR in [ False , None ]             ) :
      return J
    ##########################################################################
    if                                ( len ( RR ) != 3                    ) :
      return J
    ##########################################################################
    UUID               = int          ( RR [ 0 ]                             )
    TYPEID             = int          ( RR [ 1 ]                             )
    ##########################################################################
    J [ "Uuid"       ] = UUID
    J [ "Type"       ] = TYPEID
    J [ "Identifier" ] = self . assureString ( RR [ 2 ]                      )
    ##########################################################################
    if                                ( TYPEID in self . TypeMaps          ) :
      J [ "TName" ] = self . TypeMaps [ TYPEID                               ]
    ##########################################################################
    NAME = self . GetName             ( DB , NAMTAB , UUID                   )
    J   [ "Name"  ] = NAME
    ##########################################################################
    return J
  ############################################################################
  def ObtainIdentifierDetails            ( self , DB , IDs                 ) :
    ##########################################################################
    if                                   ( len ( IDs ) <= 0                ) :
      return                             [                                   ]
    ##########################################################################
    LISTS   =                            [                                   ]
    ##########################################################################
    for ID in IDs                                                            :
      ########################################################################
      J     = self . GetIdentifierDetail ( DB , ID                           )
      LISTS . append                     ( J                                 )
    ##########################################################################
    return LISTS
  ############################################################################
  def ObtainIdentifiers                   ( self , DB                      ) :
    ##########################################################################
    IDs   =                               [                                  ]
    ##########################################################################
    if                                    ( self . isUuidMethod    ( )     ) :
      ########################################################################
      IDs = self . ObtainSpecified        ( DB                               )
      ########################################################################
    elif                                  ( self . isOriginal      ( )     ) :
      IDs = self . ObtainOriginal         ( DB                               )
    elif                                  ( self . isSearching     ( )     ) :
      IDs = self . ObtainSearching        ( DB                               )
    elif                                  ( self . isSubordination ( )     ) :
      IDs = self . ObtainSubordination    ( DB                               )
    elif                                  ( self . isReverse       ( )     ) :
      IDs = self . ObtainReverse          ( DB                               )
    ##########################################################################
    return self . ObtainIdentifierDetails ( DB , IDs                         )
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
    self    . GetTypeMaps              ( DB                                  )
    LISTS   = self . ObtainIdentifiers ( DB                                  )
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
    self . defaultPrepare ( self . IdentifierTag , 3                         )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    IDFTAB = self . Tables            [ "Identifiers"                        ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"delete from {IDFTAB} where ( `id` = {UUID} ) ;"
      SQLs . append                   ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    TITLE  = "RemoveIdentifiers"
    self   . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    self   . loading                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem              ( self , item , uuid , name              ) :
    ##########################################################################
    DB         = self . ConnectDB (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    IDFTAB     = self . Tables    [ "Identifiers"                            ]
    Reload     = False
    ##########################################################################
    DB         . LockWrites       ( [ IDFTAB                               ] )
    ##########################################################################
    uuid       = int              ( uuid                                     )
    VAL        =                  ( name ,                                   )
    ##########################################################################
    if                            ( uuid > 0                               ) :
      ########################################################################
      QQ       = f"""update {IDFTAB}
                     set `name` = %s
                     where ( `id` = {uuid} ) ;"""
      QQ       = " " . join       ( QQ . split ( )                           )
      DB       . QueryValues      ( QQ , VAL                                 )
      ########################################################################
      self     . Notify           ( 5                                        )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                          ( self . isUuidMethod ( )                ) :
        ######################################################################
        Reload = True
        UUID   = self . Uuid
        GTYPE  = self . ProductType
        ######################################################################
        QQ     = f"""insert into {IDFTAB}
                     ( `uuid` , `type` , `name` )
                     values
                     ( {UUID} , {GTYPE} , %s ) ;"""
        QQ     = " " . join       ( QQ . split ( )                           )
        DB     . QueryValues      ( QQ , VAL                                 )
    ##########################################################################
    DB         . Close            (                                          )
    ##########################################################################
    if                            ( Reload                                 ) :
      self     . loading          (                                          )
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
    return self . DefaultColumnsMenu (        mm , 3                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9003 ) and ( at <= 9003 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                          ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                     )
    if                              ( not doMenu                          ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                     )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager            ( self                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    if                              ( self . isUuidMethod ( )              ) :
      self . AppendInsertAction     ( mm , 1101                              )
    self   . AppendRenameAction     ( mm , 1102                              )
    self   . AppendDeleteAction     ( mm , 1103                              )
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
    OKAY   = self   . RunAmountIndexMenu (                                   )
    if                              ( OKAY                                 ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking      ( mm , aa                                )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                              ( OKAY                                 ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      self . restart                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . restart                (                                        )
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

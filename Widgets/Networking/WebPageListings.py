# -*- coding: utf-8 -*-
##############################################################################
## WebPageListings
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
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
from   PyQt5 . QtCore                 import QDateTime
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
from   PyQt5 . QtWidgets              import QToolTip
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
from   AITK  . Calendars  . StarDate  import StarDate    as StarDate
from   AITK  . Calendars  . Periode   import Periode     as Periode
from   AITK  . Networking . WebPage   import WebPage     as WebPage
##############################################################################
class WebPageListings              ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames = None
    self . ClassTag     = "WebPageListings"
    ##########################################################################
    self . Total        = 0
    self . StartId      = 0
    self . Amount       = 40
    self . Order        = "asc"
    ##########################################################################
    self . Grouping     = "Original"
    self . OldGrouping  = "Original"
    ## self . Grouping     = "Subordination"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "WebPage"                               )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
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
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 1024 )                      )
  ############################################################################
  def AttachActions   ( self                                  , Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
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
  def PrepareItem           ( self , UUID , NAME                           ) :
    ##########################################################################
    UXID = str              ( UUID                                           )
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , UXID                                       )
    IT   . setData          ( 0 , Qt . UserRole , UUID                       )
    IT   . setTextAlignment ( 1 , Qt . AlignRight                            )
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
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0                                         ] )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column ,              msg                  )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , msg ,                        )
    self   . Go                 ( self . AssureUrlItem , VAL                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       ( dict                                     )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    URLs   = JSON                 [ "URLs"                                   ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , URLs [ U ]                           )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids                    ( self , DB                   ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder          (                               )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables                   [ "Relation"                    ]
    ##########################################################################
    if                                       ( self . isSubordination ( )  ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                                       ( self . isReverse       ( )  ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidURLs                 ( self , DB , UUIDs                  ) :
    ##########################################################################
    URLs    =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Webpages"                           ]
      for UUID in UUIDs                                                      :
        ######################################################################
        QQ  = f"select `name` from {TABLE} where ( `uuid` = {UUID} ) ;"
        DB  . Query                   ( QQ                                   )
        RR  = DB . FetchOne           (                                      )
        ######################################################################
        if ( ( RR not in [ None , False ] ) and ( len ( RR ) == 1 ) )        :
          ####################################################################
          SS = RR                     [ 0                                    ]
          try                                                                :
            SS = SS . decode          ( "utf-8"                              )
          except                                                             :
            pass
          ####################################################################
          URLs [ UUID ] = SS
    ##########################################################################
    return URLs
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
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    URLs    =                         {                                      }
    if                                ( len ( UUIDs ) > 0                  ) :
      URLs  = self . ObtainsUuidURLs  ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "URLs"  ] = URLs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    self   . Notify                   ( 5                                    )
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
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "Webpages"                                  ]
    QQ     = f"select count(*) from {TABLE} where ( `used` > 0 ) ;"
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
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    TABLE   = self . Tables          [ "Webpages"                            ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def dragMime                      ( self                                 ) :
    ##########################################################################
    items    = self . selectedItems (                                        )
    total    = len                  ( items                                  )
    if                              ( len ( items ) <= 0                   ) :
      return None
    ##########################################################################
    URLs     =                      [                                        ]
    for it in items                                                          :
      ########################################################################
      URL    = QUrl                 ( it . text ( 0 )                        )
      URLs   . append               ( URL                                    )
    ##########################################################################
    mime     = QMimeData            (                                        )
    mime     . setUrls              ( URLs                                   )
    ##########################################################################
    message  = self . getMenuItem   ( "TotalPicked"                          )
    tooltip  = message . format     ( total                                  )
    QToolTip . showText             ( QCursor . pos ( ) , tooltip            )
    ##########################################################################
    return mime
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  """
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  """
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                 ( self , sourceWidget , mimeData , mousePos  ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return mimeData . hasUrls (                                              )
  ############################################################################
  def dropMoving              ( self , sourceWidget , mimeData , mousePos  ) :
    ##########################################################################
    if                        ( self . droppingAction                      ) :
      return False
    ##########################################################################
    if                        ( sourceWidget == self                       ) :
      return False
    ##########################################################################
    return mimeData . hasUrls (                                              )
  ############################################################################
  def dropAppend ( self , sourceWidget , mimeData , mousePos               ) :
    ##########################################################################
    if           ( self . droppingAction                                   ) :
      return False
    ##########################################################################
    Bypass , Result = self . HandleDropInURLs                                (
                   sourceWidget                                            , \
                   mimeData                                                , \
                   mousePos                                                  )
    if           ( not Bypass                                              ) :
      return Result
    ##########################################################################
    return   False
  ############################################################################
  def acceptUrlsDrop          ( self                                       ) :
    return True
  ############################################################################
  def dropUrls ( self , source , pos , URLs                                ) :
    ##########################################################################
    if         ( len ( URLs ) <= 0                                         ) :
      return True
    ##########################################################################
    self . Go  ( self . JoinURLs ,  ( URLs , )                               )
    ##########################################################################
    return True
  ############################################################################
  def JoinURL                       ( self , DB , URL                      ) :
    ##########################################################################
    if                              ( not self . isGrouping ( )            ) :
      return
    ##########################################################################
    URI           = URL . toString  (                                        )
    print ( URI )
    ##########################################################################
    """
    RELTAB        = self . Tables   [ "Relation"                             ]
    WP            = WebPage         ( URI                                    )
    WP   . Tables = self . Tables
    uuid          = 0
    ##########################################################################
    if                              ( WP . isProtocol (                  ) ) :
      if                            ( WP . Assure     ( DB               ) ) :
        uuid    = WP . Uuid
    ##########################################################################
    if                              ( uuid <= 0                            ) :
      return
    ##########################################################################
    if                              ( self . isSubordination ( )           ) :
      ########################################################################
      self      . Relation . set    ( "second" , uuid                        )
      DB        . LockWrites        ( [ RELTAB                             ] )
      self      . Relation . Join   ( DB , RELTAB                            )
      DB        . UnlockTables      (                                        )
      ########################################################################
    elif                            ( self . isReverse       ( )           ) :
      ########################################################################
      self      . Relation . set    ( "first"  , uuid                        )
      DB        . LockWrites        ( [ RELTAB                             ] )
      self      . Relation . Join   ( DB , RELTAB                            )
      DB        . UnlockTables      (                                        )
    """
    ##########################################################################
    return
  ############################################################################
  def JoinURLs                  ( self , URLs                              ) :
    ##########################################################################
    COUNT  = len                ( URLs                                       )
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem ( "JoinURLs"                                 )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    ##########################################################################
    for URL in URLs                                                          :
      ########################################################################
      self . JoinURL            ( DB , URL                                   )
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . ShowStatus         ( ""                                         )
    self   . loading            (                                            )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "WebPageListings" , 1                            )
    self . setPrepared    ( True                                             )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
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
    TITLE  = "RemoveURLs"
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
  def AssureUrlItem                  ( self , item , uuid , URL            ) :
    ##########################################################################
    DB            = self . ConnectDB ( UsePure = True                        )
    if                               ( DB in [ False , None ]              ) :
      return
    ##########################################################################
    RELTAB        = self . Tables    [ "Relation"                            ]
    WP            = WebPage          ( URL                                   )
    WP   . Tables = self . Tables
    ##########################################################################
    if                               ( uuid > 0                            ) :
      ########################################################################
      WP . Uuid   = uuid
      if                             ( WP . isProtocol (                 ) ) :
        WP        . Update           ( DB                                    )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                             ( WP . isProtocol (                 ) ) :
        if                           ( WP . Assure     ( DB              ) ) :
          uuid    = WP . Uuid
    ##########################################################################
    if                               ( self . isSubordination ( )          ) :
      ########################################################################
      self        . Relation . set   ( "second" , uuid                       )
      DB          . LockWrites       ( [ RELTAB                            ] )
      self        . Relation . Join  ( DB , RELTAB                           )
      DB          . UnlockTables     (                                       )
      ########################################################################
    elif                             ( self . isReverse       ( )          ) :
      ########################################################################
      self        . Relation . set   ( "first"  , uuid                       )
      DB          . LockWrites       ( [ RELTAB                            ] )
      self        . Relation . Join  ( DB , RELTAB                           )
      DB          . UnlockTables     (                                       )
    ##########################################################################
    DB            . Close            (                                       )
    ##########################################################################
    item          . setData          ( 0 , Qt . UserRole , uuid              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( atItem != None                        ) :
      msg  = self . getMenuItem    ( "OpenUrl"                               )
      mm   . addAction             ( 7001 , msg                              )
    ##########################################################################
    self   . AmountIndexMenu       ( mm                                      )
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    if                             ( uuid > 0                              ) :
      ########################################################################
      self . AppendRenameAction    ( mm , 1102                               )
      self . AppendDeleteAction    ( mm , 1103                               )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    LINE   = QLineEdit             (                                         )
    LINE   . setText               ( self . Tables [ "Relation" ]            )
    mm     . addWidget             ( 91241356 , LINE                         )
    ##########################################################################
    mm     . addSeparator          (                                         )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    self . Tables [ "Relation" ] = LINE . text (                             )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 7001                            ) :
      ########################################################################
      URL  = atItem . text         ( 0                                       )
      QDesktopServices . openUrl   ( QUrl ( URL )                            )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## AlbumSources
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
import AITK
##############################################################################
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Qt6        . MenuManager import MenuManager as MenuManager
from   AITK    . Qt6        . TreeDock    import TreeDock    as TreeDock
from   AITK    . Qt6        . LineEdit    import LineEdit    as LineEdit
from   AITK    . Qt6        . ComboBox    import ComboBox    as ComboBox
from   AITK    . Qt6        . SpinBox     import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation    import Relation    as Relation
from   AITK    . Calendars  . StarDate    import StarDate    as StarDate
from   AITK    . Calendars  . Periode     import Periode     as Periode
from   AITK    . Networking . WebPage     import WebPage     as WebPage
##############################################################################
class AlbumSources       ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal ( dict                                              )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . EditAllNames = None
    self . ClassTag     = ""
    self . BType        = "Album"
    self . GType        = 76
    self . WebPath      = ""
    ##########################################################################
    self . Total        = 0
    self . StartId      = 0
    self . Amount       = 40
    self . Order        = "asc"
    self . Grouping     = "Subordination"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( self . BType                            )
    self . Relation . setT2        ( "WebPage"                               )
    self . Relation . setRelation  ( "Equivalent"                            )
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
    self . setMinimumSize          ( 180 , 32                                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 600 , 200 )                       )
  ############################################################################
  def PrepareForActions ( self , title , uuid                              ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self                                  , Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Import"     , self . ImportURLs      , Enabled      )
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
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked            ( self , item , column                       ) :
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
  def PrepareItem           ( self , UUID , JSON                           ) :
    ##########################################################################
    UXID = str              ( UUID                                           )
    NAME = JSON             [ "URL"                                          ]
    ##########################################################################
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , UXID                                       )
    IT   . setData          ( 0 , Qt . UserRole , UUID                       )
    IT   . setTextAlignment ( 1 , Qt . AlignRight                            )
    ##########################################################################
    IT   . setData          ( 2 , Qt . UserRole , JSON                       )
    ##########################################################################
    return IT
  ############################################################################
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
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0                                         ] )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def ImportText            ( self , text                                  ) :
    ##########################################################################
    if                      ( len ( text ) <= 0                            ) :
      return
    ##########################################################################
    LISTs    = text . split ( "\n"                                           )
    URLs     =              [                                                ]
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      K      = L
      K      = K . replace  ( "\n" , ""                                      )
      K      = K . replace  ( "\r" , ""                                      )
      K      = K . rstrip   (                                                )
      K      = K .  strip   (                                                )
      ########################################################################
      if                    ( len ( K ) > 0                                ) :
        ######################################################################
        U    = QUrl         ( K                                              )
        URLs . append       ( U                                              )
    ##########################################################################
    if                      ( len ( URLs ) <= 0                            ) :
      return
    ##########################################################################
    self     . Go           ( self . JoinURLs ,  ( URLs , )                  )
    ##########################################################################
    return
  ############################################################################
  def PasteItems ( self                                                    ) :
    ##########################################################################
    mime = qApp . clipboard ( ) . mimeData (                                 )
    text = qApp . clipboard ( ) . text     (                                 )
    if           ( self . NotOkay ( mime )                                 ) :
      ########################################################################
      self . ImportText ( text                                               )
      ########################################################################
      return
    ##########################################################################
    if           ( not mime . hasUrls ( )                                  ) :
      ########################################################################
      self . ImportText ( text                                               )
      ########################################################################
      return
    ##########################################################################
    self . Go    ( self . JoinURLs ,  ( mime . urls ( ) , )                  )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard                    ( self                            ) :
    ##########################################################################
    items  = self . selectedItems        (                                   )
    if                                   ( len ( items ) <= 0              ) :
      return
    ##########################################################################
    LIST   =                             [                                   ]
    URLs   =                             [                                   ]
    for item in items                                                        :
      ########################################################################
      T    = item . text                 ( 0                                 )
      U    = QUrl                        ( T                                 )
      LIST . append                      ( T                                 )
      URLs . append                      ( U                                 )
    ##########################################################################
    X      = "\n" . join                 ( LIST                              )
    M      = QMimeData                   (                                   )
    M      . setUrls                     ( URLs                              )
    qApp   . clipboard ( ) . setMimeData ( M                                 )
    qApp   . clipboard ( ) . setText     ( X                                 )
    ##########################################################################
    return
  ############################################################################
  def ImportURLs                  ( self                                   ) :
    ##########################################################################
    FILTERS = self . Translations [ "UI::PlainTextFiles"                     ]
    TITLE   = self . getMenuItem  ( "ImportURLs"                             )
    F , _   = QFileDialog . getOpenFileName ( self                           ,
                                               TITLE                         ,
                                               ""                            ,
                                               FILTERS                       )
    ##########################################################################
    if                            ( len ( F ) <= 0                         ) :
      return
    ##########################################################################
    TEXT    = ""
    with open                     ( F , "rb" ) as j                          :
      TEXT  = j . read            (                                          )
    ##########################################################################
    if                            ( len ( TEXT ) <= 0                      ) :
      return
    ##########################################################################
    try                                                                      :
      BODY  = TEXT . decode       ( "utf-8"                                  )
    except                                                                   :
      return
    ##########################################################################
    if                            ( len ( BODY ) <= 0                      ) :
      return
    ##########################################################################
    self    . ImportText          ( BODY                                     )
    ##########################################################################
    return
  ############################################################################
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
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    ORDER   = self . getSortingOrder (                                       )
    WEBTAB  = self . Tables          [ "Webpages"                            ]
    RELTAB  = self . Tables          [ "Relation"                            ]
    UUID    = self . Relation . get  ( "first"                               )
    SID     = self . StartId
    AMOUNT  = self . Amount
    GTYPE   = self . GType
    WPATH   = self . WebPath
    WLIKE   = f"{WPATH}%"
    LMTS    = f"limit {SID} , {AMOUNT}"
    ##########################################################################
    RQ      = f"""select `second` from {RELTAB}
                  where ( `first` =  {UUID} )
                    and ( `t1` = {GTYPE} )
                    and ( `t2` = 208 )
                    and ( `relation` = 10 )"""
    WQ      = f"""select `uuid` from {WEBTAB}
                  where ( `uuid` in ( {RQ} ) )
                    and ( `name` like %s )"""
    QQ      = f"""select `second` from {RELTAB}
                  where ( `first` =  {UUID} )
                    and ( `t1` = {GTYPE} )
                    and ( `t2` = 208 )
                    and ( `relation` = 10 )
                    and ( `second` in ( {WQ} ) )
                    order by `position` {ORDER} {LMTS} ;"""
    DB      . QueryValues            ( QQ , ( WLIKE ,                      ) )
    ALL     = DB . FetchAll          (                                       )
    ##########################################################################
    if                               ( ALL in self . EmptySet              ) :
      return                         [                                       ]
    ##########################################################################
    UUIDs   =                        [                                       ]
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      UUIDs . append                 ( int ( RR [ 0                      ] ) )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ObtainsUuidJson         ( self , DB , UUID , S                       ) :
    ##########################################################################
    TABLE = self . Tables     [ "Webpages"                                   ]
    ##########################################################################
    if                        ( " " in S                                   ) :
      ########################################################################
      S   = S . replace       ( " "  , ""                                    )
      S   = S . replace       ( "\t" , ""                                    )
      S   = S . replace       ( "\r" , ""                                    )
      S   = S . replace       ( "\n" , ""                                    )
      ########################################################################
      W   = WebPage           (                                              )
      W   . setPage           ( S                                            )
      W   . UpdatePageContent ( DB , TABLE , UUID                            )
    ##########################################################################
    return                    { "Uuid" : UUID                              , \
                                "URL"  : S                                   }
  ############################################################################
  def ObtainsUuidURLs                        ( self , DB , UUIDs           ) :
    ##########################################################################
    URLs  =                                  {                               }
    ##########################################################################
    if                                       ( len ( UUIDs ) <= 0          ) :
      return URLs
    ##########################################################################
    TABLE = self . Tables                    [ "Webpages"                    ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ  = f"select `name` from {TABLE} where ( `uuid` = {UUID} ) ;"
      DB  . Query                            ( QQ                            )
      RR  = DB . FetchOne                    (                               )
      ########################################################################
      if                                     ( RR in self . EmptySet       ) :
        continue
      ########################################################################
      if                                     ( 1 != len ( RR )             ) :
        continue
      ########################################################################
      S   = self . assureString              ( RR [ 0                      ] )
      ########################################################################
      URLs [ UUID ] = self . ObtainsUuidJson ( DB , UUID , S                 )
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
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation                 ( self , DB                       ) :
    ##########################################################################
    self . Total = 0
    ##########################################################################
    WEBTAB       = self . Tables         [ "Webpages"                        ]
    RELTAB       = self . Tables         [ "Relation"                        ]
    UUID         = self . Relation . get ( "first"                           )
    GTYPE        = self . GType
    WPATH        = self . WebPath
    WLIKE        = f"{WPATH}%"
    ##########################################################################
    RQ           = f"""select `second` from {RELTAB}
                       where ( `first` =  {UUID} )
                         and ( `t1` = {GTYPE} )
                         and ( `t2` = 208 )
                         and ( `relation` = 10 )"""
    WQ           = f"""select `uuid` from {WEBTAB}
                       where ( `uuid` in ( {RQ} ) )
                         and ( `name` like %s )"""
    QQ           = f"""select count(*) from {RELTAB}
                       where ( `first` =  {UUID} )
                         and ( `t1` = {GTYPE} )
                         and ( `t2` = 208 )
                         and ( `relation` = 10 )
                         and ( `second` in ( {WQ} ) ) ;"""
    DB           . QueryValues           ( QQ , ( WLIKE ,                  ) )
    RR           = DB . FetchOne         (                                   )
    ##########################################################################
    if                                   ( RR in self . EmptySet           ) :
      return
    ##########################################################################
    if                                   ( len ( RR ) != 1                 ) :
      return
    ##########################################################################
    self . Total = int                   ( RR [ 0                          ] )
    ##########################################################################
    return
  ############################################################################
  def FetchSessionInformation ( self , DB                                  ) :
    ##########################################################################
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
    ##########################################################################
    RELTAB        = self . Tables   [ "RelationEditing"                      ]
    WP            = WebPage         ( URI                                    )
    WP   . Tables = self . Tables
    uuid          = 0
    ##########################################################################
    if                              ( WP . isProtocol (                  ) ) :
      if                            ( WP . Assure     ( DB               ) ) :
        uuid      = WP . Uuid
    ##########################################################################
    if                              ( uuid <= 0                            ) :
      return
    ##########################################################################
    self          . Relation . set  ( "second" , uuid                        )
    DB            . LockWrites      ( [ RELTAB                             ] )
    self          . Relation . Join ( DB , RELTAB                            )
    DB            . UnlockTables    (                                        )
    ##########################################################################
    self          . Notify          ( 5                                      )
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
    self . defaultPrepare ( self . ClassTag , 1                              )
    self . setPrepared    ( True                                             )
    ##########################################################################
    self . LoopRunning = False
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
    if                                ( self . NotOkay ( DB )              ) :
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
    if                               ( self . NotOkay ( DB )               ) :
      return
    ##########################################################################
    RELTAB        = self . Tables    [ "RelationEditing"                     ]
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
    self          . Relation . set   ( "second" , uuid                       )
    DB            . LockWrites       ( [ RELTAB                            ] )
    self          . Relation . Join  ( DB , RELTAB                           )
    DB            . UnlockTables     (                                       )
    ##########################################################################
    DB            . Close            (                                       )
    ##########################################################################
    item          . setData          ( 0 , Qt . UserRole , uuid              )
    ##########################################################################
    return
  ############################################################################
  def StartDownload ( self , item                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                                 ( atItem != None                    ) :
      ########################################################################
      msg  = self . getMenuItem        ( "OpenUrl"                           )
      mm   . addAction                 ( 7001 , msg                          )
      ########################################################################
      msg  = self . getMenuItem        ( "Download"                          )
      mm   . addAction                 ( 7002 , msg                          )
      ########################################################################
      mm   . addSeparator              (                                     )
    ##########################################################################
    self   . AmountIndexMenu           ( mm , True                           )
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1101                           )
    ##########################################################################
    if                                 ( uuid > 0                          ) :
      ########################################################################
      self . AppendRenameAction        ( mm , 1102                           )
      self . AppendDeleteAction        ( mm , 1103                           )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    msg    = self . getMenuItem        ( "ImportURLs"                        )
    mm     . addAction                 ( 6001 , msg                          )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    mm     . addSeparator              (                                     )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    ##########################################################################
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( self . RunDocking ( mm , aa )     ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      self . restart                   (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1101                        ) :
      self . InsertItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      self . RenameItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1103                        ) :
      self . DeleteItems               (                                     )
      return True
    ##########################################################################
    if                                 ( at == 6001                        ) :
      ########################################################################
      self . ImportURLs                (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 7001                        ) :
      ########################################################################
      URL  = atItem . text             ( 0                                   )
      QDesktopServices . openUrl       ( QUrl ( URL )                        )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 7002                        ) :
      ########################################################################
      self . StartDownload             ( atItem                              )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

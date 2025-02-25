# -*- coding: utf-8 -*-
##############################################################################
## LogHistory
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
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
from   AITK    . Qt6                   import *
##############################################################################
from   AITK    . Essentials . Relation import Relation
from   AITK    . Calendars  . StarDate import StarDate
from   AITK    . Calendars  . Periode  import Periode
from   AITK    . Documents  . Notes    import Notes
##############################################################################
class LogHistory         ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal ( list                                              )
  OpenSmartNote = Signal ( str , str , str , str , int , str                 )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . ClassTag           = "LogHistory"
    self . Uuid               = 0
    self . NOXTAB             = ""
    self . Key                = ""
    self . Extra              = ""
    self . SortOrder          = "desc"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 4 , True                                )
    self . setColumnHidden         ( 5 , True                                )
    self . setColumnHidden         ( 7 , True                                )
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
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    self . setMinimumSize          ( 120 , 80                                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 480 , 320 )                       )
  ############################################################################
  def PrepareForActions ( self                                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
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
    if                          ( self . isItemPicked ( )                  ) :
      if                        ( column != self . CurrentItem ["Column"]  ) :
        self . removeParked     (                                            )
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked                ( self , item , column                   ) :
    ##########################################################################
    if                            ( column not in [ 0 , 3 , 4 , 5        ] ) :
      return
    ##########################################################################
    if                            ( column     in [ 0                    ] ) :
      ########################################################################
      sb   = self . setSpinBox    ( item                                     ,
                                    column                                   ,
                                    column                                   ,
                                    999999999                                ,
                                    "editingFinished"                        ,
                                    self . spinChanged                       )
      sb   . setAlignment         ( Qt . AlignRight                          )
      sb   . setFocus             ( Qt . TabFocusReason                      )
    ##########################################################################
    if                            ( column     in [     3 , 4 , 5        ] ) :
      ########################################################################
      line = self . setLineEdit   ( item                                   , \
                                    column                                 , \
                                    "editingFinished"                      , \
                                    self . nameChanged                       )
      line . setFocus             ( Qt . TabFocusReason                      )
    ##########################################################################
    self   . defaultSingleClicked (        item , column                     )
    ##########################################################################
    return
  ############################################################################
  def setOwner                   ( self , UUID , KEY                       ) :
    ##########################################################################
    self . Uuid = UUID
    self . Key  = KEY
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent         ( self , IT , JSON                        ) :
    ##########################################################################
    TRX = self . Translations    [ self . ClassTag                           ]
    TZ  = self . Settings        [ "TimeZone"                                ]
    ##########################################################################
    NOW = StarDate               (                                           )
    ID  = int                    ( JSON [ "Prefer"                         ] )
    ID  = int                    ( ID                                        )
    LEN = int                    ( JSON [ "Length"                         ] )
    LEN = int                    ( LEN                                       )
    NID = int                    ( JSON [ "Id"                             ] )
    NID = int                    ( NID                                       )
    ##########################################################################
    NOW . Stardate = int         ( JSON [ "Lastest"                        ] )
    DT  = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"        )
    ##########################################################################
    IT  . setText                ( 0 , str ( ID )                            )
    IT  . setToolTip             ( 0 , str ( ID )                            )
    IT  . setData                ( 0 , Qt . UserRole , ID                    )
    IT  . setTextAlignment       ( 0 , Qt.AlignRight                         )
    ##########################################################################
    IT  . setText                ( 1 , str ( LEN )                           )
    IT  . setTextAlignment       ( 1 , Qt.AlignRight                         )
    ##########################################################################
    IT  . setText                ( 2 , JSON [ "Name"                       ] )
    IT  . setText                ( 3 , JSON [ "Title"                      ] )
    IT  . setText                ( 4 , JSON [ "Comment"                    ] )
    IT  . setText                ( 5 , JSON [ "Extra"                      ] )
    ##########################################################################
    IT  . setText                ( 6 , DT                                    )
    ##########################################################################
    IT  . setData                ( 7 , Qt . UserRole , str ( NID )           )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , JSON                                ) :
    ##########################################################################
    IT   = QTreeWidgetItem    (                                              )
    self . PrepareItemContent ( IT   , JSON                                  )
    ##########################################################################
    return IT
  ############################################################################
  def InsertItem ( self                                                    ) :
    ##########################################################################
    self . Go    ( self . AppendPrefer                                       )
    ##########################################################################
    return
  ############################################################################
  def CopyNote ( self , Prefer                                             ) :
    ##########################################################################
    self . Go  ( self . AppendAndCopyPrefer , ( Prefer , )                   )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveNotes                       )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , NOTEs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for N in NOTEs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( N                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB in [ False , None ]             ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    NOW     = StarDate                (                                      )
    NOXTAB  = self . Tables           [ "Notes"                              ]
    ##########################################################################
    if                                ( len ( self . NOXTAB ) > 0          ) :
      NOXTAB = self . NOXTAB
    ##########################################################################
    KEY     = self . Key
    UUID    = self . Uuid
    ORDER   = self . SortOrder
    ITEMs   =                         [                                      ]
    ##########################################################################
    QQ      = f"""select `id`,`prefer`,length(`note`),`title`,`comment`,`extra`,`ltime` from {NOXTAB}
                  where ( `uuid` = '{UUID}' )
                    and ( `name` = '{KEY}' )
                  order by `prefer` {ORDER} ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    ##########################################################################
    ALL     = DB . FetchAll           (                                      )
    if ( ( ALL not in [ False , None ] ) and ( len ( ALL ) > 0 ) )           :
      ########################################################################
      for ITEM in ALL                                                        :
        ######################################################################
        NXID   = int                  ( ITEM [ 0 ]                           )
        PREFER = int                  ( ITEM [ 1 ]                           )
        LENGTH = int                  ( ITEM [ 2 ]                           )
        TITLE  = self . assureString  ( ITEM [ 3 ]                           )
        COMM   = self . assureString  ( ITEM [ 4 ]                           )
        EXTRA  = self . assureString  ( ITEM [ 5 ]                           )
        NOW . fromDateTime            ( ITEM [ 6 ]                           )
        ######################################################################
        J   =                         { "Id"      : NXID                   , \
                                        "Prefer"  : PREFER                 , \
                                        "Length"  : LENGTH                 , \
                                        "Name"    : KEY                    , \
                                        "Title"   : TITLE                  , \
                                        "Comment" : COMM                   , \
                                        "Extra"   : EXTRA                  , \
                                        "Lastest" : NOW . Stardate           }
        ITEMs . append                ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( ITEMs ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . emitAllNames  . emit    ( ITEMs                                )
    ##########################################################################
    return
  ############################################################################
  def AppendPrefer            ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    if                        ( len ( self . NOXTAB ) > 0                  ) :
      NOXTAB = self . NOXTAB
    ##########################################################################
    NOX    = Notes            (                                              )
    NOX    . Uuid  = self . Uuid
    NOX    . Name  = self . Key
    NOX    . Extra = self . Extra
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . appendNote       ( DB , NOXTAB                                  )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def AppendAndCopyPrefer     ( self , AT                                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    if                        ( len ( self . NOXTAB ) > 0                  ) :
      NOXTAB = self . NOXTAB
    ##########################################################################
    NOX    = Notes            (                                              )
    NOX    . Uuid  = self . Uuid
    NOX    . Name  = self . Key
    NOX    . Extra = self . Extra
    ##########################################################################
    NOX    . Obtains          ( DB , NOXTAB , AT                             )
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . appendNote       ( DB , NOXTAB                                  )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self    . setVacancy      (                                              )
    self    . GoRelax . emit  (                                              )
    DB      . Close           (                                              )
    ##########################################################################
    self    . loading         (                                              )
    ##########################################################################
    return
  ############################################################################
  def RemoveNotes             ( self , IDs                                 ) :
    ##########################################################################
    if                        ( len ( IDs ) <= 0                           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    IDZs   =                  [                                              ]
    ##########################################################################
    for ID in IDs                                                            :
      IDZs . append           ( str ( ID )                                   )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    if                        ( len ( self . NOXTAB ) > 0                  ) :
      NOXTAB = self . NOXTAB
    ##########################################################################
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    NOX    . RemovePrefers    ( DB , NOXTAB , IDZs                           )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def OrderingNumbers         ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    if                        ( len ( self . NOXTAB ) > 0                  ) :
      NOXTAB = self . NOXTAB
    ##########################################################################
    NOX    = Notes            (                                              )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    UUID          = self . Uuid
    KEY           = self . Key
    ##########################################################################
    IDs    = NOX . ObtainIDs  ( DB , NOXTAB , "prefer" , "asc"               )
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    ##########################################################################
    X      = 0
    for ID in IDs                                                            :
      ########################################################################
      QQ   = f"""update {NOXTAB}
                 set `prefer` = {X}
                 where ( `uuid` = {UUID} )
                   and ( `name` = '{KEY}' )
                   and ( `prefer` = {ID} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
      ########################################################################
      X    = X + 1
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
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
    pid    = self . itemUuid    ( item , 7                                   )
    item   . setText            ( column , msg                               )
    self   . removeParked       (                                            )
    ##########################################################################
    if                          ( column not in [ 3 , 4 , 5              ] ) :
      return
    ##########################################################################
    name   = ""
    if                          ( 3 == column                              ) :
      name = "title"
    elif                        ( 4 == column                              ) :
      name = "comment"
    elif                        ( 5 == column                              ) :
      name = "extra"
    ##########################################################################
    VAL    =                    ( item , pid , name , msg ,                  )
    self   . Go                 ( self . AssureItemContext , VAL             )
    ##########################################################################
    return
  ############################################################################
  def spinChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    sb     = self . CurrentItem [ "Widget"                                   ]
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      pid  = self . itemUuid    ( item , 7                                   )
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      self . Go                 ( self . UpdateItemPrefer                  , \
                                  ( item , pid , nv , )                      )
    ##########################################################################
    self . removeParked         (                                            )
    ##########################################################################
    return
  ############################################################################
  def AssureItemContext       ( self , item , pid , column , BLOB          ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    try                                                                      :
      BLOB = BLOB . encode    ( "utf-8"                                      )
    except                                                                   :
      return
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    QQ     = f"""update {NOXTAB}
                 set `{column}` = %s
                 where ( `id` = {pid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . QueryValues      ( QQ , ( BLOB , )                              )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemPrefer        ( self , item , pid , prefer                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    NOXTAB = self . Tables    [ "Notes"                                      ]
    ##########################################################################
    DB     . LockWrites       ( [ NOXTAB                                   ] )
    QQ     = f"""update {NOXTAB}
                 set `prefer` = {prefer}
                 where ( `id` = {pid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 , 100                                          )
    self . setColumnWidth ( 1 , 100                                          )
    self . setColumnWidth ( 2 , 120                                          )
    self . setColumnWidth ( 3 , 120                                          )
    self . setColumnWidth ( 4 , 120                                          )
    self . setColumnWidth ( 5 , 120                                          )
    self . setColumnWidth ( 6 , 200                                          )
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 7                              )
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
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      msg  = self . getMenuItem    ( "Edit"                                  )
      icon = QIcon                 ( ":/images/coding.png"                   )
      mm   . addActionWithIcon     ( 2001 , icon , msg                       )
      mm   . addSeparator          (                                         )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      msg  = self . getMenuItem    ( "CopyNote"                              )
      icon = QIcon                 ( ":/images/plus.png"                     )
      mm   . addActionWithIcon     ( 1102 , icon , msg                       )
      ########################################################################
      self . AppendDeleteAction    ( mm , 1103                               )
    ##########################################################################
    msg    = self . getMenuItem    ( "OrderingNumbers"                       )
    mm     . addAction             ( 1104 , msg                              )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
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
      self . restart               (                                         )
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
      self . CopyNote              ( uuid                                    )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1104                            ) :
      self . Go                    ( self . OrderingNumbers                  )
      return True
    ##########################################################################
    if                             ( at == 2001                            ) :
      ########################################################################
      TEXT = self . windowTitle    (                                         )
      UXID = str                   ( self . Uuid                             )
      KEY  = str                   ( self . Key                              )
      self . OpenSmartNote . emit  ( TEXT                                    ,
                                     self . NOXTAB                           ,
                                     UXID                                    ,
                                     KEY                                     ,
                                     int ( uuid )                            ,
                                     self . Extra                            )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

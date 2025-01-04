# -*- coding: utf-8 -*-
##############################################################################
## RaceListings
## 種族列表
##############################################################################
import os
import sys
import time
import requests
import threading
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
from   AITK    . People     . People   import People
##############################################################################
class RaceListings           ( TreeDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = Signal (                                               )
  emitAllNames      = Signal ( dict                                          )
  emitAssignAmounts = Signal ( str , int                                     )
  PeopleGroup       = Signal ( str , int , str                               )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "asc"
    self . Method             = "Original"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
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
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Insert"     , self . InsertItem        )
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    self . LinkAction              ( "Search"     , self . Search            )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Paste"      , self . Paste             )
    self . LinkAction              ( "Import"     , self . Import            )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkVoice               ( self . CommandParser                    )
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
  def twiceClicked            ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                column                                     , \
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
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
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
  def refresh                      ( self , JSON                           ) :
    ##########################################################################
    self    . clear                (                                         )
    ##########################################################################
    UUIDs   = JSON                 [ "UUIDs"                                 ]
    NAMEs   = JSON                 [ "NAMEs"                                 ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem   ( U , NAMEs [ U ]                         )
      self  . addTopLevelItem      ( IT                                      )
    ##########################################################################
    FMT     = self . getMenuItem   ( "DisplayTotal"                          )
    MSG     = FMT  . format        ( len ( UUIDs )                           )
    self    . setToolTip           ( MSG                                     )
    ##########################################################################
    if                             ( self . Method in [ "Searching" ]      ) :
      ########################################################################
      T     = self . Translations  [ "RaceListings" ] [ "Title"              ]
      K     = self . SearchKey
      T     = f"{T}:{K}"
      ########################################################################
      self  . setWindowTitle       ( T                                       )
    ##########################################################################
    self    . emitNamesShow . emit (                                         )
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
    time    . sleep                    ( 1.0                                 )
    ##########################################################################
    RELTAB  = self . Tables            [ "Relation"                          ]
    REL     = Relation                 (                                     )
    REL     . setT1                    ( "Race"                              )
    REL     . setT2                    ( "People"                            )
    REL     . setRelation              ( "Subordination"                     )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL   . set                      ( "first" , UUID                      )
      CNT   = REL . CountSecond        ( DB , RELTAB                         )
      ########################################################################
      self  . emitAssignAmounts . emit ( str ( UUID ) , CNT                  )
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT1 ( name , "Races" , "Names"                         )
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
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    if                                ( self . Method in [ "Original" ]    ) :
      self  . UUIDs =                 [                                      ]
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    else                                                                     :
      UUIDs = self . UUIDs
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
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
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids        ( self , DB                                    ) :
    ##########################################################################
    RACTAB = self . Tables  [ "Races"                                        ]
    ##########################################################################
    QQ     = f"""select `uuid` from {RACTAB}
                 where ( `used` = 1 )
                 order by `id` asc ;"""
    ##########################################################################
    QQ     = " " . join     ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Paste"      , self . Paste           , False   )
    self . LinkAction      ( "Import"     , self . Import          , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkVoice       ( None                                            )
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
    RACTAB = self . Tables [ "Races"                                         ]
    ##########################################################################
    QQ     = f"select count(*) from {RACTAB} where ( `used` = 1 ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( RR in [ False , None ] ) or ( len ( RR ) <= 0 )                     :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    RACTAB  = self . Tables          [ "Races"                               ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {RACTAB}
                  where ( `used` = 1 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "race/uuids"
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
    formats = "people/uuids"
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
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      FMT   = self . getMenuItem    ( "CopyFrom"                             )
      MSG   = FMT . format          ( title , CNT                            )
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget != self                      ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    if                         ( atItem is None                            ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    if                         ( "UUIDs" not in JSOX                       ) :
      return True
    ##########################################################################
    UUIDs  = JSOX              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    if                         ( atItem is None                            ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinRace                     , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinRace                ( self , UUID , UUIDs                  ) :
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    COUNT   = len                   ( UUIDs                                  )
    if                              ( COUNT <= 0                           ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden ( 1                                      )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem    ( "JoinPeople"                           )
    MSG     = FMT  . format         ( COUNT                                  )
    self    . ShowStatus            ( MSG                                    )
    self    . TtsTalk               ( MSG , 1002                             )
    ##########################################################################
    TYPE    = "Race"
    PER     = People                (                                        )
    RELTAB  = self . Tables         [ "RelationPeople"                       ]
    DB      . LockWrites            ( [ RELTAB ]                             )
    PER     . ConnectToPeople       ( DB , RELTAB , UUID , TYPE , UUIDs      )
    DB      . UnlockTables          (                                        )
    ##########################################################################
    if                              ( not Hide                             ) :
      TOTAL = PER . CountBelongs    ( DB , RELTAB , UUID , TYPE              )
    ##########################################################################
    DB      . Close                 (                                        )
    ##########################################################################
    self    . ShowStatus            ( ""                                     )
    self    . Notify                ( 5                                      )
    ##########################################################################
    if                              ( Hide                                 ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem     ( UUID , 0                               )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    self    . emitAssignAmounts . emit ( str ( UUID ) , int ( TOTAL )        )
    ##########################################################################
    return
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 2 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs = TRX              [ "RaceListings" ] [ "Labels"                  ]
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
    RACTAB  = self . Tables        [ "Races"                                 ]
    NAMTAB  = self . Tables        [ "NamesRaces"                            ]
    ##########################################################################
    DB      . LockWrites           ( [ RACTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . UnusedUuid      ( RACTAB                                  )
      DB    . UseUuid              ( RACTAB , uuid                           )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    ##########################################################################
    return
  ############################################################################
  def ImportFromText          ( self , text                                ) :
    ##########################################################################
    L      = text . split     ( "\n"                                         )
    if                        ( len ( L ) <= 0                             ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    RACTAB = self . Tables    [ "Races"                                      ]
    NAMTAB = self . Tables    [ "NamesRaces"                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ RACTAB , NAMTAB                          ] )
    ##########################################################################
    for N in L                                                               :
      ########################################################################
      name = N
      name = name .  strip    (                                              )
      name = name . rstrip    (                                              )
      ########################################################################
      if                      ( len ( name ) <= 0                          ) :
        continue
      ########################################################################
      uuid = DB . UnusedUuid  ( RACTAB                                       )
      DB   . UseUuid          ( RACTAB , uuid                                )
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def Paste             ( self                                             ) :
    ##########################################################################
    self . defaultPaste ( self . ImportFromText                              )
    ##########################################################################
    return
  ############################################################################
  def Import             ( self                                            ) :
    ##########################################################################
    self . defaultImport ( self . ImportFromText                             )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    return          { "Match" : False                                        }
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at == 9001 ) and ( hid )            ) :
        self . startup             (                                         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                   ( self , mm , item                      ) :
    ##########################################################################
    TRX    = self . Translations
    NAME   = item . text           ( 0                                       )
    FMT    = TRX                   [ "UI::Belongs"                           ]
    MSG    = FMT . format          ( NAME                                    )
    COL    = mm . addMenu          ( MSG                                     )
    ##########################################################################
    msg    = self . getMenuItem    ( "Crowds"                                )
    mm     . addActionFromMenu     ( COL , 1201 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , item                      ) :
    ##########################################################################
    if                             ( at == 1201                            ) :
      ########################################################################
      uuid = item . data           ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
      head = item . text           ( 0                                       )
      self . PeopleGroup   . emit  ( head , 34 , str ( uuid )                )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    if                              ( self . Method not in [ "Original" ]  ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Original"                             )
      mm   . addAction              ( 1002 , msg                             )
    ##########################################################################
    self   . AppendInsertAction     ( mm , 1101                              )
    self   . AppendRenameAction     ( mm , 1102                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      if                            ( self . EditAllNames != None          ) :
        ######################################################################
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      mm   = self . GroupsMenu      ( mm , atItem                            )
    ##########################################################################
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
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
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
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
    if                              ( self . RunGroupsMenu ( at , atItem ) ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . Method = "Original"
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
    if                              ( at == 1601                           ) :
      ########################################################################
      uuid = self . itemUuid        ( atItem , 0                             )
      NAM  = self . Tables          [ "NamesRaces"                           ]
      self . EditAllNames           ( self , "Races" , uuid , NAM            )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################

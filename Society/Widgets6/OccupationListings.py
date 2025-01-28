# -*- coding: utf-8 -*-
##############################################################################
## OccupationListings
## 職業列表
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import json
##############################################################################
from   PySide6                                          import QtCore
from   PySide6                                          import QtGui
from   PySide6                                          import QtWidgets
from   PySide6 . QtCore                                 import *
from   PySide6 . QtGui                                  import *
from   PySide6 . QtWidgets                              import *
from   AITK    . Qt6                                    import *
##############################################################################
from   AITK    . Essentials . Relation                  import Relation
from   AITK    . Calendars  . StarDate                  import StarDate
from   AITK    . Calendars  . Periode                   import Periode
from   AITK    . Society    . Occupations . Occupations import Occupations
##############################################################################
class OccupationListings     ( TreeDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = Signal (                                               )
  emitAllNames      = Signal ( dict                                          )
  emitAssignAmounts = Signal ( str , int , int                               )
  PeopleGroup       = Signal ( str , int , str                               )
  OpenLogHistory    = Signal ( str , str , str , str , str                   )
  emitLog           = Signal ( str                                           )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "OccupationListings"
    self . FetchTableKey      = "OccupationListings"
    self . GType              = 40
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 35
    self . SortOrder          = "asc"
    self . Method             = "Original"
    self . UsedOptions        = [ 1                                          ]
    ##########################################################################
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping = "Original"
    ## self . Grouping = "Subordination"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . OCCP               = Occupations (                                )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation         (                                     )
    self . Relation . setT1            ( "Occupation"                        )
    self . Relation . setT2            ( "Occupation"                        )
    self . Relation . setRelation      ( "Subordination"                     )
    ##########################################################################
    self . setColumnCount              ( 3                                   )
    self . setColumnHidden             ( 1 , True                            )
    self . setColumnHidden             ( 2 , True                            )
    ##########################################################################
    self . setRootIsDecorated          ( False                               )
    self . setAlternatingRowColors     ( True                                )
    ##########################################################################
    self . MountClicked                ( 1                                   )
    self . MountClicked                ( 2                                   )
    ##########################################################################
    self . assignSelectionMode         ( "ExtendedSelection"                 )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction                 ( self . FunctionDocking , True       )
    self . setFunction                 ( self . HavingMenu      , True       )
    ##########################################################################
    self . setAcceptDrops              ( True                                )
    self . setDragEnabled              ( True                                )
    self . setDragDropMode             ( QAbstractItemView . DragDrop        )
    ##########################################################################
    self . setMinimumSize              ( 80 , 80                             )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 280 , 640 )                       )
  ############################################################################
  def setGrouping ( self , group                                           ) :
    ##########################################################################
    self . Grouping = group
    ##########################################################################
    return self . Grouping
  ############################################################################
  def getGrouping ( self                                                   ) :
    return self . Grouping
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "Crowds"                             , \
                                      ":/images/viewpeople.png"            , \
                                      self . GotoItemCrowd                   )
    self . AppendToolNamingAction   (                                        )
    self . AppendSideActionWithIcon ( "Description"                        , \
                                      ":/images/documents.png"             , \
                                      self . GotoItemDescription             )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . Paste           , Enabled      )
    self . LinkAction ( "Import"     , self . Import          , Enabled      )
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
  def twiceClicked              ( self , item , column                     ) :
    ##########################################################################
    if                          ( column in [ 0 ]                          ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount          ( self , DB                          ) :
    return self . OCCP . CountOptions ( DB                                 , \
                                        self . Tables [ "Occupations" ]    , \
                                        self . UsedOptions                   )
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
    return self . OCCP . QuerySyntax ( self . Tables [ "Occupations"     ] , \
                                       self . UsedOptions                  , \
                                       self . getSortingOrder ( )          , \
                                       self . StartId                      , \
                                       self . Amount                         )
  ############################################################################
  def PrepareItem           ( self , UUID , NAME , BRUSH                   ) :
    ##########################################################################
    UXID = str              ( UUID                                           )
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , UXID                                       )
    IT   . setData          ( 0 , Qt . UserRole , UUID                       )
    ##########################################################################
    IT   . setTextAlignment ( 1 , Qt . AlignRight                            )
    IT   . setTextAlignment ( 2 , Qt . AlignRight                            )
    ##########################################################################
    for COL in              [ 0 , 1 , 2                                    ] :
      ########################################################################
      IT . setBackground    ( COL , BRUSH                                    )
    ##########################################################################
    return IT
  ############################################################################
  def InsertItem             ( self                                        ) :
    ##########################################################################
    self . defaultInsertItem ( 0 , "editingFinished" , self . nameChanged    )
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
  def SearchingTitle           ( self                                      ) :
    ##########################################################################
    if                         ( self . Method not in [ "Searching" ]      ) :
      return
    ##########################################################################
    T    = self . Translations [ self . ClassTag ] [ "Title"                 ]
    K    = self . SearchKey
    self . setWindowTitle      ( f"{T}:{K}"                                  )
    ##########################################################################
    return
  ############################################################################
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "DisplayTotal"                               )
    MSG  = FMT  . format      ( Total                                        )
    self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U                                      , \
                                    NAMEs [ U ]                            , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . SearchingTitle       (                                          )
    self   . RefreshToolTip       ( len ( UUIDs )                            )
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids ( self , DB                                         ) :
    ##########################################################################
    if                 ( self . Grouping == "Original"                     ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      TABLE = self . Tables   [ "Names"                                      ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def AssignAmounts        ( self , UUID , Amounts , COLUMN                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( COLUMN , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                 ( self , UUIDs                      ) :
    ##########################################################################
    time   . sleep                     ( 1.0                                 )
    ##########################################################################
    RELTAB = self . Tables             [ "RelationPeople"                    ]
    ##########################################################################
    DB     = self . ConnectDB          (                                     )
    ##########################################################################
    if                                 ( self . NotOkay ( DB )             ) :
      return
    ##########################################################################
    self   . OnBusy  . emit            (                                     )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      CNT  = self . OCCP . CountCrowds ( DB                                , \
                                         RELTAB                            , \
                                         "Subordination"                   , \
                                         UUID                                )
      self . emitAssignAmounts . emit  ( str ( UUID ) , CNT , 1              )
    ##########################################################################
    self   . GoRelax . emit            (                                     )
    DB     . Close                     (                                     )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT1 ( name , "Occupations" , "NamesEditing"            )
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
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
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
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self   . ReloadLocality           ( DB                                   )
    ##########################################################################
    self   . Total = 0
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
  def ObtainSubgroupUuids  ( self , DB                                     ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables [ "Relation"                                      ]
    ##########################################################################
    if                     ( self . isSubordination (                    ) ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                     ( self . isReverse       (                    ) ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                 [                                                 ]
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "occupation/uuids"
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
  def allowedMimeTypes     ( self , mime                                   ) :
    formats = "people/uuids"
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                            ( self                            , \
                                           sourceWidget                    , \
                                           mimeData                        , \
                                           mousePos                        ) :
    ##########################################################################
    if                                   ( self == sourceWidget            ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew      ( mimeData                          )
    if                                   ( not RDN                         ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON          [ "Mime"                            ]
    UUIDs   = self . DropInJSON          [ "UUIDs"                           ]
    ##########################################################################
    if                                   ( mtype in [ "people/uuids" ]     ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "CopyFrom"                        )
      MSG   = FMT  . format              ( title , CNT                       )
      self  . ShowStatus                 ( MSG                               )
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
    if                         ( atItem in [ False , None ]                ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinOccupation               , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinOccupation                ( self , UUID , UUIDs            ) :
    ##########################################################################
    if                                    ( UUID <= 0                      ) :
      return
    ##########################################################################
    COUNT   = len                         ( UUIDs                            )
    if                                    ( COUNT <= 0                     ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden       ( 1                                )
    ##########################################################################
    DB      = self . ConnectDB            (                                  )
    if                                    ( DB == None                     ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem          ( "JoinPeople"                     )
    MSG     = FMT  . format               ( COUNT                            )
    self    . ShowStatus                  ( MSG                              )
    self    . TtsTalk                     ( MSG , 1002                       )
    ##########################################################################
    RELTAB  = self . Tables               [ "RelationPeople"                 ]
    DB      . LockWrites                  ( [ RELTAB                       ] )
    self    . OCCP . PeopleJoinOccupation ( DB                             , \
                                            RELTAB                         , \
                                            "Subordination"                , \
                                            UUID                           , \
                                            UUIDs                            )
    DB      . UnlockTables                (                                  )
    ##########################################################################
    if                                    ( not Hide                       ) :
      TOTAL = self . OCCP . CountCrowds   ( DB                             , \
                                            RELTAB                         , \
                                            "Subordination"                , \
                                            UUID                             )
    ##########################################################################
    DB      . Close                       (                                  )
    ##########################################################################
    self    . ShowStatus                  ( ""                               )
    self    . Notify                      ( 5                                )
    ##########################################################################
    if                                    ( Hide                           ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem           ( UUID , 0                         )
    if                                    ( IT is None                     ) :
      return
    ##########################################################################
    self    . emitAssignAmounts . emit    ( str ( UUID ) , int ( TOTAL ) , 1 )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 2                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    OCPTAB = self . Tables    [ "Occupations"                                ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ OCPTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . UnusedUuid  ( OCPTAB                                       )
      DB   . UseUuid          ( OCPTAB , uuid                                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
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
    OCPTAB = self . Tables    [ "Occupations"                                ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ OCPTAB , NAMTAB                          ] )
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
      uuid = DB . UnusedUuid  ( OCPTAB                                       )
      DB   . UseUuid          ( OCPTAB , uuid                                )
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
  def UpdateLocalityUsage           ( self                                 ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subordination" , "Reverse"            ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return False
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return False
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    DB      . LockWrites            ( [ PAMTAB ]                             )
    ##########################################################################
    if                              ( SCOPE == "Subordination"             ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( SCOPE == "Reverse"                   ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    SCOPE   = f"Occupation-{SCOPE}"
    self    . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    DB      . UnlockTables          (                                        )
    DB      . Close                 (                                        )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality                ( self , DB                            ) :
    ##########################################################################
    SCOPE   = self . Grouping
    ALLOWED =                       [ "Subordination" , "Reverse"            ]
    ##########################################################################
    if                              ( SCOPE not in ALLOWED                 ) :
      return
    ##########################################################################
    PAMTAB  = self . Tables         [ "Parameters"                           ]
    ##########################################################################
    if                              ( SCOPE == "Subordination"             ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t1"                                   )
      UUID  = self . Relation . get ( "first"                                )
      ########################################################################
    elif                            ( SCOPE == "Reverse"                   ) :
      ########################################################################
      TYPE  = self . Relation . get ( "t2"                                   )
      UUID  = self . Relation . get ( "second"                               )
    ##########################################################################
    SCOPE   = f"Occupation-{SCOPE}"
    self    . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE      )
    ##########################################################################
    return
  ############################################################################
  def OpenItemCrowd           ( self , item                                ) :
    ##########################################################################
    uuid = item . data        ( 0 , Qt . UserRole                            )
    uuid = int                ( uuid                                         )
    xsid = str                ( uuid                                         )
    text = item . text        ( 0                                            )
    ##########################################################################
    self . PeopleGroup . emit ( text , self . GType , str ( uuid )           )
    ##########################################################################
    return
  ############################################################################
  def GotoItemCrowd             ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemCrowd      ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "Occupation"                       , \
                                        "NamesEditing"                       )
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
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9001 ) and ( hid )            ) :
        ######################################################################
        self . startup             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                     ( self , mm , item                    ) :
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text               ( 0                                     )
    FMT  = TRX                       [ "UI::Belongs"                         ]
    MSG  = FMT . format              ( NAME                                  )
    COL  = mm . addMenu              ( MSG                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Crowds"                              )
    ICON = QIcon                     ( ":/images/viewpeople.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 1201 , ICON , msg               )
    ##########################################################################
    msg  = self . getMenuItem        ( "Description"                         )
    ICON = QIcon                     ( ":/images/documents.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 1202 , ICON , msg               )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu             ( self , at , item                         ) :
    ##########################################################################
    if                          ( at == 1201                               ) :
      ########################################################################
      self . OpenItemCrowd      ( item                                       )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 1202                               ) :
      ########################################################################
      self . EmitOpenLogHistory ( item , 0                                   )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    if                                ( not self . isPrepared (          ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                    )
    if                                ( not doMenu                         ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu   ( mm , True                            )
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . AppendRefreshAction      ( mm , 1001                            )
    ##########################################################################
    if                                ( self . Method not in ["Original"]  ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Original"                           )
      mm   . addAction                ( 1002 , msg                           )
    ##########################################################################
    self   . AppendInsertAction       ( mm , 1101                            )
    self   . AppendRenameAction       ( mm , 1102                            )
    ##########################################################################
    if                                ( atItem not in self . EmptySet      ) :
      ########################################################################
      if                              ( self . EditAllNames != None        ) :
        ######################################################################
        mm . addAction                ( 1601 ,  TRX [ "UI::EditNames" ]      )
    ##########################################################################
    mm     . addSeparator             (                                      )
    ##########################################################################
    if                                ( atItem not in self . EmptySet      ) :
      ########################################################################
      mm   = self . GroupsMenu        ( mm , atItem                          )
    ##########################################################################
    mm     = self . ColumnsMenu       ( mm                                   )
    mm     = self . SortingMenu       ( mm                                   )
    mm     = self . LocalityMenu      ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                  ( self    . menuFont (               ) )
    aa     = mm . exec_               ( QCursor . pos      (               ) )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    ##########################################################################
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( self . RunDocking ( mm , aa )      ) :
      return True
    ##########################################################################
    if                                ( self . HandleLocalityMenu ( at )   ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( self . RunColumnsMenu     ( at )   ) :
      return True
    ##########################################################################
    if                                ( self . RunSortingMenu     ( at )   ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu     ( at , atItem                          )
    ##########################################################################
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1002                         ) :
      ########################################################################
      self . Method = "Original"
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1101                         ) :
      self . InsertItem               (                                      )
      return True
    ##########################################################################
    if                                ( at == 1102                         ) :
      self . RenameItem               (                                      )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor ( at , 1601 , atItem                   )
    ##########################################################################
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    return True
##############################################################################

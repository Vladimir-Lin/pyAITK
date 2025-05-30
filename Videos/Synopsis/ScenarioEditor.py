# -*- coding: utf-8 -*-
##############################################################################
## ScenarioEditor
## 影片場景
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
from           . Fragment              import Fragment    as FragmentItem
from           . Scenario              import Scenario    as ScenarioItem
from           . Descriptive           import Descriptive as DescriptiveItem
##############################################################################
class ScenarioEditor             ( TreeDock                                ) :
  ############################################################################
  HavingMenu            = 1371434312
  ############################################################################
  emitNamesShow         = Signal (                                           )
  emitAllNames          = Signal ( list                                      )
  emitDescriptives      = Signal ( QWidget , str , str , dict , QIcon        )
  ShowPeopleGroupRelate = Signal ( str , int , str , str                     )
  emitPlayer            = Signal ( QWidget                                   )
  emitLog               = Signal ( str                                       )
  ############################################################################
  def __init__                   ( self , parent = None , plan = None      ) :
    ##########################################################################
    super ( ) . __init__         (        parent        , plan               )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "ScenarioEditor"
    self . FetchTableKey      = self . ClassTag
    self . PlayerWidget       = None
    self . AlbumUuid          = 0
    self . FragmentUuid       = 0
    self . GType              = 212
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . JsonAt             = 10
    self . SortOrder          = "asc"
    self . UsedOptions        = [ 1 , 2 , 3                                  ]
    ##########################################################################
    self . Grouping           = "Subordination"
    ##########################################################################
    self . SCENE              = ScenarioItem (                               )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( "vFragment"                             )
    self . Relation . setT2        ( "Scenario"                              )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 11                                      )
    self . setColumnWidth          (  0 ,  48                                )
    self . setColumnWidth          (  1 , 400                                )
    self . setColumnHidden         (  2 , True                               )
    self . setColumnWidth          (  2 , 120                                )
    self . setColumnHidden         (  3 , True                               )
    self . setColumnWidth          (  3 , 120                                )
    self . setColumnHidden         (  4 , True                               )
    self . setColumnWidth          (  4 , 120                                )
    self . setColumnHidden         (  5 , True                               )
    self . setColumnWidth          (  5 , 120                                )
    self . setColumnHidden         (  7 , True                               )
    self . setColumnHidden         (  8 , True                               )
    self . setColumnHidden         ( 10 , True                               )
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
    self . setMinimumSize          ( 80 , 80                                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 600 , 200 )                       )
  ############################################################################
  def setAlbumUuid         ( self , UUID                                   ) :
    ##########################################################################
    self . AlbumUuid = int ( UUID                                            )
    ##########################################################################
    return
  ############################################################################
  def setFragmentUuid         ( self , UUID                                ) :
    ##########################################################################
    self . FragmentUuid = int ( UUID                                         )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendToolNamingAction   (                                        )
    self . AppendSideActionWithIcon ( "OpenDescriptives"                   , \
                                      ":/images/descriptions.png"          , \
                                      self . GotoItemDescriptive             )
    self . AppendSideActionWithIcon ( "ScenarioCrowds"                     , \
                                      ":/images/buddy.png"                 , \
                                      self . GotoItemCrowds                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . restart         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
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
  def AssignPlayer           ( self , widget                               ) :
    ##########################################################################
    self . PlayerWidget = widget
    ##########################################################################
    self . emitPlayer . emit (        widget                                 )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked                  ( self , item , column                 ) :
    ##########################################################################
    if                              ( column in [ 0 ]                      ) :
      ########################################################################
      ## 位序
      pass
    ##########################################################################
    if                              ( column in [ 1 , 3 , 4 , 5 ]          ) :
      ########################################################################
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    if                              ( column in [ 2 ]                      ) :
      ########################################################################
      ## 用途
      ########################################################################
      LL   = self . Translations    [ self . ClassTag ] [ "Usage"            ]
      val  = item . data            ( column , Qt . UserRole                 )
      val  = int                    ( val                                    )
      cb   = self . setComboBox     ( item                                 , \
                                      column                               , \
                                      "activated"                          , \
                                      self . usageChanged                    )
      cb   . addJson                ( LL , val                               )
      cb   . setMaxVisibleItems     ( 10                                     )
      cb   . showPopup              (                                        )
    ##########################################################################
    if                              ( column in [ 6 ]                      ) :
      ########################################################################
      slen = item . data            ( column , Qt . UserRole                 )
      xlen = self . SCENE . toFTime ( int ( slen                           ) )
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . blockSignals           ( True                                   )
      line . setText                ( xlen                                   )
      line . blockSignals           ( False                                  )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                    ( self , POS , BT , JSON , BRUSH      ) :
    ##########################################################################
    USAGE   = self . Translations    [ self . ClassTag ] [ "Usage"           ]
    UUID    = JSON                   [ "Uuid"                                ]
    NAME    = JSON                   [ "Name"                                ]
    STYPE   = JSON                   [ "Type"                                ]
    SCOPE   = JSON                   [ "Scope"                               ]
    USED    = int                    ( JSON [ "Used"                       ] )
    STATEs  = int                    ( JSON [ "States"                     ] )
    SLEN    = int                    ( JSON [ "Duration"                   ] )
    CPEO    = int                    ( JSON [ "People"                     ] )
    ELEN    = int                    ( SLEN + BT                             )
    ##########################################################################
    DTIME   = self . SCENE . toLTime ( SLEN                                  )
    STIME   = self . SCENE . toLTime ( BT                                    )
    ETIME   = self . SCENE . toLTime ( ELEN                                  )
    ##########################################################################
    UNAME   = ""
    ##########################################################################
    if                               ( str ( USED ) in USAGE               ) :
      ########################################################################
      UNAME = USAGE                  [ str ( USED )                          ]
    ##########################################################################
    IT      = QTreeWidgetItem        (                                       )
    IT      . setData                ( 0 , Qt . UserRole , str ( UUID )      )
    IT      . setText                ( 0 , str ( POS )                       )
    IT      . setTextAlignment       ( 0 , Qt . AlignRight                   )
    IT      . setText                ( 1 , NAME                              )
    IT      . setToolTip             ( 1 , str ( UUID )                      )
    IT      . setData                ( 1 , Qt . UserRole , str ( UUID )      )
    IT      . setText                ( 2 , UNAME                             )
    IT      . setData                ( 2 , Qt . UserRole , USED              )
    IT      . setTextAlignment       ( 2 , Qt . AlignCenter                  )
    IT      . setText                ( 3 , str ( STYPE )                     )
    IT      . setTextAlignment       ( 3 , Qt . AlignRight                   )
    IT      . setData                ( 3 , Qt . UserRole , STYPE             )
    IT      . setText                ( 4 , SCOPE                             )
    IT      . setText                ( 5 , str ( STATEs )                    )
    IT      . setTextAlignment       ( 5 , Qt . AlignRight                   )
    IT      . setData                ( 5 , Qt . UserRole , STATEs            )
    IT      . setText                ( 6 , DTIME                             )
    IT      . setTextAlignment       ( 6 , Qt . AlignRight                   )
    IT      . setData                ( 6 , Qt . UserRole , str ( SLEN )      )
    IT      . setText                ( 7 , STIME                             )
    IT      . setTextAlignment       ( 7 , Qt . AlignRight                   )
    IT      . setData                ( 7 , Qt . UserRole , str ( BT   )      )
    IT      . setText                ( 8 , ETIME                             )
    IT      . setTextAlignment       ( 8 , Qt . AlignRight                   )
    IT      . setText                ( 9 , str ( CPEO )                      )
    IT      . setData                ( 9 , Qt . UserRole , CPEO              )
    IT      . setTextAlignment       ( 9 , Qt . AlignRight                   )
    ##########################################################################
    IT      . setData                ( self . JsonAt , Qt . UserRole , JSON  )
    ##########################################################################
    COLs    =                        [  0 ,  1 ,  2 ,  3 ,  4 ,              \
                                        5 ,  6 ,  7 ,  8 ,  9 ,              \
                                       10                                    ]
    ##########################################################################
    for COL in COLs                                                          :
      ########################################################################
      IT    . setBackground          ( COL , BRUSH                           )
    ##########################################################################
    return IT
  ############################################################################
  def ObtainsInformation      ( self , DB                                  ) :
    ##########################################################################
    self     . ReloadLocality (        DB                                    )
    ##########################################################################
    RELTAB   = self . Tables  [ "Relation"                                   ]
    SCNTAB   = self . Tables  [ "Scenarios"                                  ]
    ##########################################################################
    if                        ( self . isSubordination (                 ) ) :
      ########################################################################
      self   . Total = self . SCENE . CountSecondTotal                     ( \
                                DB                                         , \
                                self . Relation                            , \
                                SCNTAB                                     , \
                                RELTAB                                     , \
                                self . UsedOptions                           )
      ########################################################################
    elif                      ( self . isReverse       (                 ) ) :
      ########################################################################
      self   . Total = self . SCENE . CountFirstTotal                      ( \
                                DB                                         , \
                                self . Relation                            , \
                                SCNTAB                                     , \
                                RELTAB                                     , \
                                self . UsedOptions                           )
      ########################################################################
    else                                                                     :
      ########################################################################
      self   . Total = self . SCENE . CountTotal                           ( \
                                DB                                         , \
                                SCNTAB                                     , \
                                self . UsedOptions                           )
    ##########################################################################
    return
  ############################################################################
  def LoadScenarios                          ( self , DB                   ) :
    ##########################################################################
    SCENARIOs   =                            [                               ]
    LISTs       =                            [                               ]
    UUIDs       =                            [                               ]
    ##########################################################################
    RELTAB      = self . Tables              [ "Relation"                    ]
    PEOREL      = self . Tables              [ "RelationPeople"              ]
    SCNTAB      = self . Tables              [ "Scenarios"                   ]
    ##########################################################################
    if                                       ( self . isSubordination (  ) ) :
      ########################################################################
      LISTs     = self . SCENE . FetchListsByFirst                         ( \
                                               DB                          , \
                                               SCNTAB                      , \
                                               RELTAB                      , \
                                               self . Relation             , \
                                               self . UsedOptions          , \
                                               self . StartId              , \
                                               self . Amount               , \
                                               self . SortOrder              )
      ########################################################################
    elif                                     ( self . isReverse       (  ) ) :
      ########################################################################
      LISTs     = self . SCENE . FetchListsBySecond                        ( \
                                               DB                          , \
                                               SCNTAB                      , \
                                               RELTAB                      , \
                                               self . Relation             , \
                                               self . UsedOptions          , \
                                               self . StartId              , \
                                               self . Amount               , \
                                               self . SortOrder              )
      ########################################################################
    else                                                                     :
      ########################################################################
      LISTs     = self . SCENE . FetchLists  ( DB                          , \
                                               SCNTAB                      , \
                                               self . UsedOptions          , \
                                               self . StartId              , \
                                               self . Amount               , \
                                               self . SortOrder              )
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      UUIDs     . append                     ( L [ "Uuid"                  ] )
    ##########################################################################
    NAMEs       = self . ObtainsUuidNames    ( DB , UUIDs                    )
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      UUID      = L                          [ "Uuid"                        ]
      ########################################################################
      if                                     ( UUID in NAMEs               ) :
        ######################################################################
        L [ "Name" ] = NAMEs                 [ UUID                          ]
      ########################################################################
      PCNT      = self . SCENE . CountPeople ( DB , PEOREL , UUID            )
      L [ "People" ] = PCNT
      ########################################################################
      SCENARIOs . append                     ( L                             )
    ##########################################################################
    return SCENARIOs
  ############################################################################
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "DisplayTotal"                               )
    MSG  = FMT  . format      ( Total , self . Total                         )
    self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , LISTs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    POS    = 0
    BT     = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      POS  = int                  ( POS + 1                                  )
      ########################################################################
      IT   = self . PrepareItem   ( POS                                    , \
                                    BT                                     , \
                                    JSON                                   , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      DURT = int                  ( JSON [ "Duration"                      ] )
      BT   = int                  ( BT + DURT                                )
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . RefreshToolTip       ( len ( LISTs )                            )
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                     ( self                                   ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( DB                  ) ) :
      ########################################################################
      self . emitNamesShow . emit (                                          )
      ########################################################################
      return
    ##########################################################################
    self   . Notify               ( 3                                        )
    self   . OnBusy  . emit       (                                          )
    self   . setBustle            (                                          )
    ##########################################################################
    FMT    = self . Translations  [ "UI::StartLoading"                       ]
    MSG    = FMT . format         ( self . windowTitle (                   ) )
    self   . ShowStatus           ( MSG                                      )
    ##########################################################################
    self   . ObtainsInformation   ( DB                                       )
    L      = self . LoadScenarios ( DB                                       )
    ##########################################################################
    self   . setVacancy           (                                          )
    self   . GoRelax . emit       (                                          )
    self   . ShowStatus           ( ""                                       )
    DB     . Close                (                                          )
    ##########################################################################
    if                            ( len ( L ) <= 0                         ) :
      ########################################################################
      self . emitNamesShow . emit (                                          )
      ########################################################################
      return
    ##########################################################################
    self   . emitAllNames  . emit ( L                                        )
    self   . Notify               ( 5                                        )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "scenario/uuids"
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
    FMTs =                 [ "scenario/uuids"                              , \
                             "people/uuids"                                  ]
    return self . MimeType ( mime , ";" . join ( FMTs  )                     )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    if                               ( self == source                      ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( mtype in [ "people/uuids"         ] ) :
      ########################################################################
      if                             ( atItem not in self . EmptySet       ) :
        ######################################################################
        TXT  = atItem . text         ( 0                                     )
        UID  = atItem . data         ( 0 , Qt . UserRole                     )
        FMT  = self   . getMenuItem  ( "PeopleFrom"                          )
        MSG  = FMT    . format       ( title , CNT , TXT , UID               )
        self . ShowStatus            ( MSG                                   )
      ########################################################################
      return True
    ##########################################################################
    if                               ( mtype not in [ "scenario/uuids" ]  ) :
      return False
    ##########################################################################
    if                               ( not self . isGrouping (           ) ) :
      return False
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving                  ( self , source , mimeData , mousePos    ) :
    ##########################################################################
    if                            ( self . droppingAction                  ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON  [ "Mime"                                   ]
    UUIDs  = self   . DropInJSON  [ "UUIDs"                                  ]
    atItem = self   . itemAt      ( mousePos                                 )
    title  = source . windowTitle (                                          )
    CNT    = len                  ( UUIDs                                    )
    ##########################################################################
    if                            ( mtype in [ "people/uuids"            ] ) :
      ########################################################################
      if                          ( atItem in self . EmptySet              ) :
        return False
      ########################################################################
      TXT  = atItem . text        ( 0                                        )
      UID  = atItem . data        ( 0 , Qt . UserRole                        )
      FMT  = self   . getMenuItem ( "PeopleFrom"                             )
      MSG  = FMT    . format      ( title , CNT , TXT , UID                  )
      self . ShowStatus           ( MSG                                      )
      ########################################################################
      return True
    ##########################################################################
    if                            ( mtype not in [ "scenario/uuids" ]      ) :
      return False
    ##########################################################################
    if                            ( source == self                         ) :
      ########################################################################
      FMT  = self   . getMenuItem ( "MoveScenarios"                          )
      MSG  = FMT    . format      ( title , CNT                              )
      self . ShowStatus           ( MSG                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      FMT  = self   . getMenuItem ( "CopyScenarios"                          )
      MSG  = FMT    . format      ( title , CNT                              )
      self . ShowStatus           ( MSG                                      )
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop ( self                                              ) :
    return True
  ############################################################################
  def dropPeople           ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem in self . EmptySet                     ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    VAL    =               ( UUID , UUIDs ,                                  )
    self   . Go            ( self . AppendingCrowds , VAL                    )
    ##########################################################################
    return True
  ############################################################################
  def AppendingCrowds           ( self , UUID , UUIDs                      ) :
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    ##########################################################################
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    FMT    = self . getMenuItem ( "JoinCrowds"                               )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationPeople"                           ]
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "Scenario"                                 )
    REL    . setT2              ( "People"                                   )
    REL    . setRelation        ( "Contains"                                 )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    REL    . Joins              ( DB , RELTAB , UUIDs                        )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    self   . loading            (                                            )
    ##########################################################################
    return
  ############################################################################
  def acceptScenariosDrop ( self                                           ) :
    return True
  ############################################################################
  def dropScenarios        ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem in self . EmptySet                     ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    VAL    =               ( UUID , UUIDs ,                                  )
    ##########################################################################
    if                     ( source == self                                ) :
      ########################################################################
      self . Go            ( self . MovingScenarios    , VAL                 )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Go            ( self . AppendingScenarios , VAL                 )
    ##########################################################################
    return True
  ############################################################################
  def MovingScenarios           ( self , UUID , UUIDs                      ) :
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    ##########################################################################
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    self   . Notify             ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def AppendingScenarios        ( self , UUID , UUIDs                      ) :
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    ##########################################################################
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    FMT    = self . getMenuItem ( "JoinScenarios"                            )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationVideos"                           ]
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination (               ) ) :
      ########################################################################
      self . Relation . Joins   ( DB , RELTAB , UUIDs                        )
      ########################################################################
    elif                        ( self . isReverse       (               ) ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        self . Relation . Join  ( DB      , RELTAB                           )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    self   . Notify             ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    item . setData            ( 1 , Qt . UserRole , 0                        )
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                1                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
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
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 1                                                  )
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
    self   . removeParked       (                                            )
    ##########################################################################
    if                          ( 1 == column                              ) :
      ########################################################################
      if                        ( len ( msg ) <= 0                         ) :
        ######################################################################
        if                      ( uuid <= 0                                ) :
          ####################################################################
          self . removeTopLevelItem ( item                                   )
          ####################################################################
          return
      ########################################################################
      item . setText            ( column , msg                               )
      VAL  =                    ( item , uuid , msg ,                        )
      self . Go                 ( self . AssureUuidItem , VAL                )
      ########################################################################
    elif                        ( 3 == column                              ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        stype = int             ( msg                                        )
        item  . setText         ( column , msg                               )
        VAL   =                 ( item , uuid , stype ,                      )
        self  . Go              ( self . AssureItemType , VAL                )
        ######################################################################
      except                                                                 :
        pass
      ########################################################################
    elif                        ( 4 == column                              ) :
      ########################################################################
      item . setText            ( column , msg                               )
      VAL  =                    ( item , uuid , msg ,                        )
      self . Go                 ( self . AssureItemName , VAL                )
      ########################################################################
    elif                        ( 5 == column                              ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        states = int            ( msg                                        )
        item   . setText        ( column , msg                               )
        VAL    =                ( item , uuid , states ,                     )
        self   . Go             ( self . AssureItemStates , VAL              )
        ######################################################################
      except                                                                 :
        pass
      ########################################################################
    elif                        ( 6 == column                              ) :
      ########################################################################
      VAL  =                    ( item , uuid , msg ,                        )
      self . Go                 ( self . UpdateItemDuration , VAL            )
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
      uuid = int                 ( item . data ( 0 , Qt . UserRole )         )
      LL   = self . Translations [ self . ClassTag ] [ "Usage"               ]
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
  def RemoveItems                       ( self , UUIDs                     ) :
    ##########################################################################
    if                                  ( len ( UUIDs ) <= 0               ) :
      self . Notify                     ( 1                                  )
      return
    ##########################################################################
    if                                  ( not self . isGrouping (        ) ) :
      self . Notify                     ( 1                                  )
      return
    ##########################################################################
    RELTAB = self . Tables              [ "Relation"                         ]
    SQLs   =                            [                                    ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                                ( self . isSubordination (       ) ) :
        self . Relation . set           ( "second" , UUID                    )
      elif                              ( self . isReverse       (       ) ) :
        self . Relation . set           ( "second" , UUID                    )
      ########################################################################
      QQ     = self . Relation . Delete ( RELTAB                             )
      SQLs   . append                   ( QQ                                 )
    ##########################################################################
    DB       = self . ConnectDB         (                                    )
    if                                  ( DB == None                       ) :
      return
    ##########################################################################
    self     . OnBusy  . emit           (                                    )
    self     . setBustle                (                                    )
    DB       . LockWrites               ( [ RELTAB                         ] )
    ##########################################################################
    TITLE    = "RemoveScenarioItems"
    self     . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100            )
    ##########################################################################
    DB       . UnlockTables             (                                    )
    self     . setVacancy               (                                    )
    self     . GoRelax . emit           (                                    )
    DB       . Close                    (                                    )
    self     . loading                  (                                    )
    ##########################################################################
    return
  ############################################################################
  def DoExportASS                        ( self , filename                 ) :
    ##########################################################################
    FMT       = "Dialogue: 0,$(START),$(END),Default,,0,0,0,,$(MESSAGE)"
    ROWS      = [ "[Events]" ,
                  "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text" ]
    ##########################################################################
    LOC       = self . getLocality       (                                   )
    TOTAL     = self . topLevelItemCount (                                   )
    ##########################################################################
    for id in range                      ( 0 , TOTAL                       ) :
      ########################################################################
      item    = self . topLevelItem      ( id                                )
      BTS     = item . data              ( 7             , Qt . UserRole     )
      JSOZ    = item . data              ( self . JsonAt , Qt . UserRole     )
      DESC    = DescriptiveItem          (                                   )
      DESC    . setJson                  ( JSOZ [ "Description" ]            )
      DESC    . Locality = LOC
      BT      = int                      ( BTS                               )
      ########################################################################
      for T in DESC . TIMESTAMPs                                             :
        ######################################################################
        OK , JJ = DESC . itemJson        ( T                                 )
        ######################################################################
        if                               ( not OK                          ) :
          continue
        ######################################################################
        JOPTs = JJ                       [ "Options"                         ]
        ######################################################################
        if                               ( "Subtitle" not in JOPTs         ) :
          continue
        ######################################################################
        SOPT  = JOPTs                    [ "Subtitle"                        ]
        if                               ( not SOPT                        ) :
          continue
        ######################################################################
        DT    = 0
        if                               ( "Duration" in JOPTs             ) :
          DT  = JOPTs                    [ "Duration"                        ]
        ######################################################################
        ST    = int                      ( T  + BT                           )
        ET    = int                      ( ST + DT                           )
        NAME  = JJ                       [ "Name"                            ]
        ######################################################################
        SS    = self . SCENE . toCTime   ( ST                                )
        ES    = self . SCENE . toCTime   ( ET                                )
        MSG   = FMT
        MSG   = MSG  . replace           ( "$(START)"   , SS                 )
        MSG   = MSG  . replace           ( "$(END)"     , ES                 )
        MSG   = MSG  . replace           ( "$(MESSAGE)" , NAME               )
        ROWS  . append                   ( MSG                               )
    ##########################################################################
    TEXT      = "\n" . join              ( ROWS                              )
    ##########################################################################
    with open ( filename , "w" , encoding="utf-8" ) as f                     :
      f       . write                    ( TEXT                              )
    ##########################################################################
    self      . Notify                   ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def ExportASS                  ( self                                    ) :
    ##########################################################################
    Title   = self . getMenuItem ( "ExportASS"                               )
    Filters = self . getMenuItem ( "AssFilters"                              )
    ASSFILE = "subtitle.ass"
    ##########################################################################
    ( ASS , filter ) = QFileDialog . getSaveFileName                         (
                         self                                              , \
                         Title                                             , \
                         ASSFILE                                           , \
                         Filters                                             )
    ##########################################################################
    if                           ( len ( ASS ) <= 0                        ) :
      self  . Notify             ( 1                                         )
      return
    ##########################################################################
    self    . Go                 ( self . DoExportASS , ( ASS , )            )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    ##########################################################################
    if                        ( self . NotOkay ( DB )                      ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    SCNTAB = self . Tables    [ "Scenarios"                                  ]
    RELTAB = self . Tables    [ "RelationVideos"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ SCNTAB , RELTAB , NAMTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( SCNTAB , "uuid" , 2800008000000000000        )
      DB   . AppendUuid       ( SCNTAB , uuid                                )
      ########################################################################
      JJ   =                  { "Id"          : -1                         , \
                                "Uuid"        : uuid                       , \
                                "Name"        : name                       , \
                                "Used"        :  1                         , \
                                "States"      :  0                         , \
                                "Type"        :  0                         , \
                                "Scope"       : ""                         , \
                                "Duration"    :  0                         , \
                                "Description" : {                          } }
      ########################################################################
    else                                                                     :
      ########################################################################
      JJ   = item . data      ( self . JsonAt , Qt . UserRole                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      self . Relation . set   ( "second" , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
      ########################################################################
    elif                      ( self . isReverse       ( )                 ) :
      ########################################################################
      self . Relation . set   ( "first"  , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def AssureItemType          ( self , item , uuid , stype                 ) :
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    ##########################################################################
    if                        ( self . NotOkay ( DB )                      ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    SCNTAB = self . Tables    [ "Scenarios"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ SCNTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {SCNTAB}
                 set `type` = {stype}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AssureItemName          ( self , item , uuid , name                  ) :
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    ##########################################################################
    if                        ( self . NotOkay ( DB )                      ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    try                                                                      :
      ########################################################################
      BB   = name . encode    ( "utf-8"                                      )
      ########################################################################
    except                                                                   :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    SCNTAB = self . Tables    [ "Scenarios"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ SCNTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {SCNTAB}
                 set `name` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . QueryValues      ( QQ ,       ( BB ,                          ) )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AssureItemStates        ( self , item , uuid , states                ) :
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    ##########################################################################
    if                        ( self . NotOkay ( DB )                      ) :
      ########################################################################
      self . Notify           ( 1                                            )
      ########################################################################
      return
    ##########################################################################
    SCNTAB = self . Tables    [ "Scenarios"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ SCNTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {SCNTAB}
                 set `states` = {states}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemDuration                   ( self , item , uuid , name     ) :
    ##########################################################################
    uuid        = int                      ( uuid                            )
    ##########################################################################
    if                                     ( uuid <= 0                     ) :
      ########################################################################
      self      . Notify                   ( 1                               )
      ########################################################################
      return
    ##########################################################################
    OKAY , SLEN = self . SCENE . FromFTime ( name                            )
    ##########################################################################
    if                                     ( not OKAY                      ) :
      ########################################################################
      self      . Notify                   ( 1                               )
      ########################################################################
      return
    ##########################################################################
    DB          = self . ConnectDB         (                                 )
    ##########################################################################
    if                                     ( self . NotOkay ( DB )         ) :
      ########################################################################
      self      . Notify                   ( 1                               )
      ########################################################################
      return
    ##########################################################################
    SCNTAB      = self . Tables            [ "Scenarios"                     ]
    ##########################################################################
    DB          . LockWrites               ( [ SCNTAB                      ] )
    ##########################################################################
    QQ          = f"""update {SCNTAB}
                      set `duration` = {SLEN}
                      where ( `uuid` = {uuid} ) ;"""
    DB          . Query                    ( " " . join ( QQ . split (   ) ) )
    ##########################################################################
    DB          . Close                    (                                 )
    self        . loading                  (                                 )
    ##########################################################################
    return
  ############################################################################
  def UpdateUsage             ( self , item , uuid , usage                 ) :
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    SCNTAB = self . Tables    [ "Scenarios"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ SCNTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {SCNTAB}
                 set `used` = {usage}
                 where ( `uuid` = {uuid} ) ;"""
    DB     . Query            ( " " . join ( QQ . split (                ) ) )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 10                             )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def OpenItemDescriptive          ( self , item                           ) :
    ##########################################################################
    uuid = item . data             ( 0             , Qt . UserRole           )
    dlen = item . data             ( 6             , Qt . UserRole           )
    slen = item . data             ( 7             , Qt . UserRole           )
    jsoz = item . data             ( self . JsonAt , Qt . UserRole           )
    uuid = int                     ( uuid                                    )
    uxid = str                     ( uuid                                    )
    head = item . text             ( 1                                       )
    icon = self . windowIcon       (                                         )
    JJ   =                         { "Uuid"        : uuid                  , \
                                     "Album"       : self . AlbumUuid      , \
                                     "Fragment"    : self . FragmentUuid   , \
                                     "Name"        : head                  , \
                                     "BaseTime"    : int  ( slen         ) , \
                                     "Duration"    : int  ( dlen         ) , \
                                     "Description" : jsoz [ "Description"  ] }
    ##########################################################################
    self . emitDescriptives . emit ( self                                  , \
                                     head                                  , \
                                     uxid                                  , \
                                     JJ                                    , \
                                     icon                                    )
    ##########################################################################
    return
  ############################################################################
  def GotoItemDescriptive        ( self                                    ) :
    ##########################################################################
    atItem = self . currentItem  (                                           )
    if                           ( self . NotOkay ( atItem )               ) :
      return
    ##########################################################################
    self   . OpenItemDescriptive ( atItem                                    )
    ##########################################################################
    return
  ############################################################################
  def OpenItemCrowds                    ( self , item                      ) :
    ##########################################################################
    uuid = item . data                  ( 0 , Qt . UserRole                  )
    uuid = int                          ( uuid                               )
    xsid = str                          ( uuid                               )
    text = item . text                  ( 1                                  )
    relz = "Contains"
    ##########################################################################
    self . ShowPeopleGroupRelate . emit ( text , self . GType , xsid , relz  )
    ##########################################################################
    return
  ############################################################################
  def GotoItemCrowds            ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemCrowds     ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "Scenario"                         , \
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage       ( self                                     ) :
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return False
    ##########################################################################
    PAMTAB = self . Tables      [ "Parameters"                               ]
    DB     . LockWrites         ( [ PAMTAB                                 ] )
    ##########################################################################
    self   . SetLocalityByUuid  ( DB                                       , \
                                  PAMTAB                                   , \
                                  0                                        , \
                                  self . GType                             , \
                                  self . ClassTag                            )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    DB     . Close              (                                            )
    self   . emitRestart . emit (                                            )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality           ( self , DB                                 ) :
    ##########################################################################
    PAMTAB = self . Tables     [ "Parameters"                                ]
    self   . GetLocalityByUuid ( DB                                        , \
                                 PAMTAB                                    , \
                                 0                                         , \
                                 self . GType                              , \
                                 self . ClassTag                             )
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
  def ColumnsMenu                   ( self , mm                           ) :
    ##########################################################################
    TRX     = self . Translations
    head    = self . headerItem     (                                        )
    COL     = mm   . addMenu        ( TRX [ "UI::Columns" ]                  )
    ##########################################################################
    msg     = self . getMenuItem    ( "ShowAllColumns"                       )
    mm      . addActionFromMenu     ( COL , 9501 , msg                       )
    ##########################################################################
    mm      . addSeparatorFromMenu  ( COL                                    )
    ##########################################################################
    for i in range                  ( 2 , self . columnCount ( )           ) :
      ########################################################################
      msg   = head . text           ( i                                      )
      if                            ( len ( msg ) <= 0                     ) :
        msg = TRX                   [ "UI::Whitespace"                       ]
      ########################################################################
      hid   = self . isColumnHidden ( i                                      )
      mm    . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid  )
    ##########################################################################
    return mm
  ############################################################################
  def RunColumnsMenu                 ( self , at                           ) :
    ##########################################################################
    if                               ( 9501 == at                          ) :
      ########################################################################
      for i in range                 ( 2 , self . columnCount (          ) ) :
        ######################################################################
        self . setColumnHidden       ( i , False                             )
      ########################################################################
      return
    ##########################################################################
    DCOLs    = self . columnCount    (                                       )
    MCOLs    = int                   ( 9000 + DCOLs                          )
    ##########################################################################
    if                               ( ( at >= 9002 ) and ( at <= MCOLs )  ) :
      ########################################################################
      col    = at - 9000
      hid    = self . isColumnHidden ( col                                   )
      self   . setColumnHidden       ( col , not hid                         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                     ( self , mm , item                    ) :
    ##########################################################################
    if                               ( self . NotOkay ( item )             ) :
      return mm
    ##########################################################################
    msg  = self . getMenuItem        ( "GroupFunctions"                      )
    COL  = mm . addMenu              ( msg                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "CopyScenarioUuid"                    )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "OpenDescriptives"                    )
    icon = QIcon                     ( ":/images/descriptions.png"           )
    mm   . addActionFromMenuWithIcon ( COL , 38522001 , icon , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "ScenarioCrowds"                      )
    icon = QIcon                     ( ":/images/buddy.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 38522002 , icon , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , item                     ) :
    ##########################################################################
    if                              ( at == 38521001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522001                       ) :
      ########################################################################
      self . OpenItemDescriptive    ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522002                       ) :
      ########################################################################
      self . OpenItemCrowds         ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared (         ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items  , atItem , uuid = self . GetMenuDetails ( 0                       )
    mm     = MenuManager               ( self                                )
    ##########################################################################
    mm     = self . AmountIndexMenu    ( mm , True                           )
    mm     . addSeparator              (                                     )
    ##########################################################################
    msg    = self . getMenuItem        ( "ExportASS"                         )
    icon   = QIcon                     ( ":/images/saveall.png"              )
    mm     . addActionWithIcon         ( 3501 , icon , msg                   )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1102                           )
    self   . AppendRenameAction        ( mm , 1103                           )
    self   . AppendDeleteAction        ( mm , 1104                           )
    self   . TryAppendEditNamesAction  ( atItem , mm , 1601                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . GroupsMenu                ( mm ,        atItem                  )
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont (              ) )
    aa     = mm . exec_                ( QCursor . pos      (              ) )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu      ( at , atItem                         )
    ##########################################################################
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      self . InsertItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1103                        ) :
      self . RenameItem                (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1104                        ) :
      self . DeleteItems               (                                     )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    ##########################################################################
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( 3501 == at                        ) :
      self . ExportASS                 (                                     )
      return True
    ##########################################################################
    return True
##############################################################################

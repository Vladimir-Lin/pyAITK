# -*- coding: utf-8 -*-
##############################################################################
## FragmentEditor
## 影片段落
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
from           . Fragment              import Fragment as FragmentItem
from           . Scenario              import Scenario as ScenarioItem
##############################################################################
class FragmentEditor          ( TreeDock                                   ) :
  ############################################################################
  HavingMenu         = 1371434312
  ############################################################################
  emitNamesShow      = Signal (                                              )
  emitAllNames       = Signal ( list                                         )
  emitScenarios      = Signal ( QWidget                                    , \
                                str                                        , \
                                str                                        , \
                                str                                        , \
                                int                                        , \
                                str                                        , \
                                str                                        , \
                                QIcon                                        )
  emitOpenVideoGroup = Signal ( str ,       int , str , str , QIcon          )
  emitPlayer         = Signal ( QWidget                                      )
  emitLog            = Signal ( str                                          )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "FragmentEditor"
    self . FetchTableKey      = self . ClassTag
    self . PlayerWidget       = None
    self . AlbumUuid          = 0
    self . GType              = 213
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . JsonAt             = 4
    self . SortOrder          = "asc"
    self . UsedOptions        = [ 1 , 2 , 3                                  ]
    ##########################################################################
    self . Grouping           = "Subordination"
    ##########################################################################
    self . FRAG               = FragmentItem (                               )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( "Album"                                 )
    self . Relation . setT2        ( "vFragment"                             )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 5                                       )
    self . setColumnWidth          ( 0 , 400                                 )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 4 , True                                )
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
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendToolNamingAction   (                                        )
    self . AppendSideActionWithIcon ( "OpenScenarios"                      , \
                                      ":/images/scenarios.png"             , \
                                      self . GotoItemScenario                )
    self . AppendSideActionWithIcon ( "BelongVideos"                       , \
                                      ":/images/videoclip.png"             , \
                                      self . GotoItemVideos                  )
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
  def twiceClicked               ( self , item , column                    ) :
    ##########################################################################
    if                           ( column in [ 0 , 2 ]                     ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    if                           ( column in [ 1 ]                         ) :
      ########################################################################
      LL   = self . Translations [ self . ClassTag ] [ "Usage"               ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                    , \
                                   column                                  , \
                                   "activated"                             , \
                                   self . usageChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 10                                        )
      cb   . showPopup           (                                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                    ( self , JSON , BRUSH                 ) :
    ##########################################################################
    USAGE   = self . Translations    [ self . ClassTag ] [ "Usage"           ]
    UUID    = JSON                   [ "Uuid"                                ]
    NAME    = JSON                   [ "Name"                                ]
    USED    = int                    ( JSON [ "Used"                       ] )
    STATEs  = int                    ( JSON [ "States"                     ] )
    VIDEOs  = int                    ( JSON [ "Videos"                     ] )
    UNAME   = ""
    ##########################################################################
    if                               ( str ( USED ) in USAGE               ) :
      ########################################################################
      UNAME = USAGE                  [ str ( USED )                          ]
    ##########################################################################
    IT      = self . PrepareUuidItem ( 0 , UUID , NAME                       )
    ##########################################################################
    IT      . setText                ( 1 , UNAME                             )
    IT      . setTextAlignment       ( 1 , Qt . AlignCenter                  )
    IT      . setData                ( 1 , Qt . UserRole , USED              )
    IT      . setText                ( 2 , str ( STATEs )                    )
    IT      . setTextAlignment       ( 2 , Qt . AlignRight                   )
    IT      . setData                ( 2 , Qt . UserRole , STATEs            )
    IT      . setText                ( 3 , str ( VIDEOs )                    )
    IT      . setTextAlignment       ( 3 , Qt . AlignRight                   )
    IT      . setData                ( 3 , Qt . UserRole , VIDEOs            )
    ##########################################################################
    IT      . setData                ( self . JsonAt , Qt . UserRole , JSON  )
    ##########################################################################
    for COL in                       [ 0 , 1 , 2 , 3 , 4                   ] :
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
    FRGTAB   = self . Tables  [ "Fragments"                                  ]
    ##########################################################################
    if                        ( self . isSubordination (                 ) ) :
      ########################################################################
      self   . Total = self . FRAG . CountSecondTotal                      ( \
                                DB                                         , \
                                self . Relation                            , \
                                FRGTAB                                     , \
                                RELTAB                                     , \
                                self . UsedOptions                           )
      ########################################################################
    elif                      ( self . isReverse       (                 ) ) :
      ########################################################################
      self   . Total = self . FRAG . CountFirstTotal                       ( \
                                DB                                         , \
                                self . Relation                            , \
                                FRGTAB                                     , \
                                RELTAB                                     , \
                                self . UsedOptions                           )
      ########################################################################
    else                                                                     :
      ########################################################################
      self   . Total = self . FRAG . CountTotal                            ( \
                                DB                                         , \
                                FRGTAB                                     , \
                                self . UsedOptions                           )
    ##########################################################################
    return
  ############################################################################
  def LoadFragments                        ( self , DB                     ) :
    ##########################################################################
    FRAGMENTs   =                          [                                 ]
    LISTs       =                          [                                 ]
    UUIDs       =                          [                                 ]
    ##########################################################################
    RELTAB      = self . Tables            [ "Relation"                      ]
    FRGTAB      = self . Tables            [ "Fragments"                     ]
    VIDREL      = self . Tables            [ "RelationVideos"                ]
    ##########################################################################
    if                                     ( self . isSubordination (    ) ) :
      ########################################################################
      LISTs     = self . FRAG . FetchListsByFirst                          ( \
                                             DB                            , \
                                             FRGTAB                        , \
                                             RELTAB                        , \
                                             self . Relation               , \
                                             self . UsedOptions            , \
                                             self . StartId                , \
                                             self . Amount                 , \
                                             self . SortOrder                )
      ########################################################################
    elif                                   ( self . isReverse       (    ) ) :
      ########################################################################
      LISTs     = self . FRAG . FetchListsBySecond                         ( \
                                             DB                            , \
                                             FRGTAB                        , \
                                             RELTAB                        , \
                                             self . Relation               , \
                                             self . UsedOptions            , \
                                             self . StartId                , \
                                             self . Amount                 , \
                                             self . SortOrder                )
      ########################################################################
    else                                                                     :
      ########################################################################
      LISTs     = self . FRAG . FetchLists ( DB                            , \
                                             FRGTAB                        , \
                                             self . UsedOptions            , \
                                             self . StartId                , \
                                             self . Amount                 , \
                                             self . SortOrder                )
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      UUIDs     . append                   ( L [ "Uuid"                    ] )
    ##########################################################################
    NAMEs       = self . ObtainsUuidNames  ( DB , UUIDs                      )
    ##########################################################################
    REX         = Relation                 (                                 )
    REX         . setT1                    ( "vFragment"                     )
    REX         . setT2                    ( "Video"                         )
    REX         . setRelation              ( "Contains"                      )
    ##########################################################################
    for L in LISTs                                                           :
      ########################################################################
      UUID      = L                        [ "Uuid"                          ]
      ########################################################################
      if                                   ( UUID in NAMEs                 ) :
        ######################################################################
        L [ "Name" ] = NAMEs               [ UUID                            ]
      ########################################################################
      REX       . set                      ( "first" , UUID                  )
      ########################################################################
      L   [ "Videos" ] = REX . CountSecond ( DB , VIDREL                     )
      ########################################################################
      FRAGMENTs . append                   ( L                               )
    ##########################################################################
    return FRAGMENTs
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
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON , self . TreeBrushes [ CNT ]        )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
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
    L      = self . LoadFragments ( DB                                       )
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
    mtype   = "vfragment/uuids"
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
    FMTs =                 [ "vfragment/uuids"                             , \
                             "scenario/uuids"                              , \
                             "video/uuids"                                   ]
    return self . MimeType ( mime , ";" . join ( FMTs  )                     )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self , source , mimeData , mousePos ) :
    ##########################################################################
    if                               ( self == source                      ) :
      return False
    ##########################################################################
    RDN      = self . RegularDropNew ( mimeData                              )
    ##########################################################################
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype    = self   . DropInJSON   [ "Mime"                                ]
    UUIDs    = self   . DropInJSON   [ "UUIDs"                               ]
    atItem   = self   . itemAt       ( mousePos                              )
    title    = source . windowTitle  (                                       )
    CNT      = len                   ( UUIDs                                 )
    ##########################################################################
    if                               ( mtype in [ "video/uuids"          ] ) :
      ########################################################################
      if                             ( atItem not in self . EmptySet       ) :
        ######################################################################
        TXT  = atItem . text         ( 0                                     )
        UID  = atItem . data         ( 0 , Qt . UserRole                     )
        FMT  = self   . getMenuItem  ( "VideosFrom"                          )
        MSG  = FMT    . format       ( title , CNT , TXT , UID               )
        self . ShowStatus            ( MSG                                   )
    ##########################################################################
    if                               ( mtype in [ "scenario/uuids"       ] ) :
      ########################################################################
      if                             ( atItem not in self . EmptySet       ) :
        ######################################################################
        TXT  = atItem . text         ( 0                                     )
        UID  = atItem . data         ( 0 , Qt . UserRole                     )
        FMT  = self   . getMenuItem  ( "ScenariosFrom"                       )
        MSG  = FMT    . format       ( title , CNT , TXT , UID               )
        self . ShowStatus            ( MSG                                   )
    ##########################################################################
    if                               ( mtype not in [ "vfragment/uuids" ]  ) :
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
    if                            ( mtype in [ "video/uuids"             ] ) :
      ########################################################################
      if                          ( atItem in self . EmptySet              ) :
        return False
      ########################################################################
      TXT  = atItem . text        ( 0                                        )
      UID  = atItem . data        ( 0 , Qt . UserRole                        )
      FMT  = self   . getMenuItem ( "VideosFrom"                             )
      MSG  = FMT    . format      ( title , CNT , TXT , UID                  )
      self . ShowStatus           ( MSG                                      )
    ##########################################################################
    if                            ( mtype in [ "scenario/uuids"          ] ) :
      ########################################################################
      if                          ( atItem not in self . EmptySet          ) :
        return False
      ########################################################################
      TXT  = atItem . text        ( 0                                        )
      UID  = atItem . data        ( 0 , Qt . UserRole                        )
      FMT  = self   . getMenuItem ( "ScenariosFrom"                          )
      MSG  = FMT    . format      ( title , CNT , TXT , UID                  )
      self . ShowStatus           ( MSG                                      )
    ##########################################################################
    if                            ( mtype not in [ "vfragment/uuids" ]     ) :
      return False
    ##########################################################################
    if                            ( source == self                         ) :
      ########################################################################
      FMT  = self   . getMenuItem ( "MoveFragments"                          )
      MSG  = FMT    . format      ( title , CNT                              )
      self . ShowStatus           ( MSG                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      FMT  = self   . getMenuItem ( "CopyFragments"                          )
      MSG  = FMT    . format      ( title , CNT                              )
      self . ShowStatus           ( MSG                                      )
    ##########################################################################
    return True
  ############################################################################
  def acceptVideoDrop ( self                                               ) :
    return True
  ############################################################################
  def dropVideos           ( self , source , pos , JSOX                    ) :
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
    self   . Go            ( self . AppendingVideos , VAL                    )
    ##########################################################################
    return True
  ############################################################################
  def AppendingVideos           ( self , UUID , UUIDs                      ) :
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
    FMT    = self . getMenuItem ( "JoinVideos"                               )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationVideos"                           ]
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "vFragment"                                )
    REL    . setT2              ( "Video"                                    )
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
    self   . Go            ( self . AppendingScenarios , VAL                 )
    ##########################################################################
    return True
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
    REL    = Relation           (                                            )
    REL    . set                ( "first" , UUID                             )
    REL    . setT1              ( "vFragment"                                )
    REL    . setT2              ( "Scenario"                                 )
    REL    . setRelation        ( "Subordination"                            )
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
    self   . Notify             ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def acceptVFragmentsDrop ( self                                          ) :
    return True
  ############################################################################
  def dropVFragments       ( self , source , pos , JSOX                    ) :
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
      self . Go            ( self . MovingVFragments    , VAL                )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Go            ( self . AppendingVFragments , VAL                )
    ##########################################################################
    return True
  ############################################################################
  def MovingVFragments          ( self , UUID , UUIDs                      ) :
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
  def AppendingVFragments       ( self , UUID , UUIDs                      ) :
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
    FMT    = self . getMenuItem ( "JoinFragments"                            )
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
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
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
    self . goRenameItem ( 0                                                  )
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
    self   . removeParked       (                                            )
    ##########################################################################
    if                          ( 0 == column                              ) :
      ########################################################################
      item . setText            ( column , msg                               )
      VAL  =                    ( item , uuid , msg ,                        )
      self . Go                 ( self . AssureUuidItem , VAL                )
    ##########################################################################
    elif                        ( 2 == column                              ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        ss = int                ( msg                                        )
        item . setText          ( column , msg                               )
        VAL  =                  ( item , uuid , ss ,                         )
        self . Go               ( self . UpdateStates , VAL                  )
        ######################################################################
      except                                                                 :
        pass
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
    TITLE    = "RemoveFragmentItems"
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
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      self . Notify           ( 1                                            )
      return
    ##########################################################################
    FRGTAB = self . Tables    [ "Fragments"                                  ]
    RELTAB = self . Tables    [ "RelationVideos"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ FRGTAB , RELTAB , NAMTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( FRGTAB , "uuid" , 2800009000000000000        )
      DB   . AppendUuid       ( FRGTAB , uuid                                )
      ########################################################################
      JJ   =                  { "Id"          : -1                         , \
                                "Uuid"        : uuid                       , \
                                "Name"        : name                       , \
                                "Used"        :  1                         , \
                                "States"      :  0                         , \
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
    ##########################################################################
    item   . setData          ( 0             , Qt . UserRole , str ( uuid ) )
    item   . setData          ( self . JsonAt , Qt . UserRole , JJ           )
    ##########################################################################
    self   . Notify           ( 5                                            )
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
    FRGTAB = self . Tables    [ "Fragments"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ FRGTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {FRGTAB}
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
  def UpdateStates            ( self , item , uuid , states                ) :
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    FRGTAB = self . Tables    [ "Fragments"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ FRGTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {FRGTAB}
                 set `states` = {states}
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
    self . defaultPrepare ( self . ClassTag , 4                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def OpenItemScenario          ( self , item                              ) :
    ##########################################################################
    uuid = item . data          ( 0 , Qt . UserRole                          )
    uuid = int                  ( uuid                                       )
    uxid = str                  ( uuid                                       )
    azid = str                  ( self . AlbumUuid                           )
    head = item . text          ( 0                                          )
    icon = self . windowIcon    (                                            )
    relz = "Subordination"
    ##########################################################################
    self . emitScenarios . emit ( self                                     , \
                                  head                                     , \
                                  azid                                     , \
                                  uxid                                     , \
                                  self . GType                             , \
                                  uxid                                     , \
                                  relz                                     , \
                                  icon                                       )
    ##########################################################################
    return
  ############################################################################
  def GotoItemScenario          ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemScenario   ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemVideos                 ( self , item                         ) :
    ##########################################################################
    uuid = item . data               ( 0 , Qt . UserRole                     )
    uuid = int                       ( uuid                                  )
    uxid = str                       ( uuid                                  )
    head = item . text               ( 0                                     )
    icon = self . windowIcon         (                                       )
    relz = "Contains"
    ##########################################################################
    self . emitOpenVideoGroup . emit ( head                                , \
                                       self . GType                        , \
                                       uxid                                , \
                                       relz                                , \
                                       icon                                  )
    ##########################################################################
    return
  ############################################################################
  def GotoItemVideos            ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemVideos     ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "vFragment"                        , \
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
    for i in range                  ( 1 , self . columnCount ( )           ) :
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
      for i in range                 ( 1 , self . columnCount (          ) ) :
        ######################################################################
        self . setColumnHidden       ( i , False                             )
      ########################################################################
      return
    ##########################################################################
    if                               ( at >= 9001 ) and ( at <= 9004 )       :
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
    msg  = self . getMenuItem        ( "CopyFragmentUuid"                    )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "OpenScenarios"                       )
    icon = QIcon                     ( ":/images/scenarios.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 38522001 , icon , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "BelongVideos"                        )
    icon = QIcon                     ( ":/images/videoclip.png"              )
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
      self . OpenItemScenario       ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522002                       ) :
      ########################################################################
      self . OpenItemVideos         ( item                                   )
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
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    return True
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
## NodeDependencies
## 節點相依性
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
from   PyQt5 . QtCore                 import QDateTime
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDateTimeEdit
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
from   AITK  . Scheduler  . Event     import Event       as Event
from   AITK  . Scheduler  . Events    import Events      as Events
##############################################################################
class NodeDependencies             ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  updateTitle   = pyqtSignal       (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "NodeDependencies"
    self . AssignedTitle      = ""
    self . NodeTypes          =        {                                     }
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Prerequisite = Relation     (                                     )
    self . Prerequisite . setRelation  ( "Prerequisite"                      )
    ##########################################################################
    self . Successor    = Relation     (                                     )
    self . Successor    . setRelation  ( "Successor"                         )
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 7 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    self . updateTitle   . connect ( self . changeWindowTitle                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 400 )                       )
  ############################################################################
  def asPrerequisite                  ( self                               ) :
    ##########################################################################
    self . Prerequisite . setRelation ( "Prerequisite"                       )
    self . Successor    . setRelation ( "Successor"                          )
    ##########################################################################
    return
  ############################################################################
  def asSuccessor                     ( self                               ) :
    ##########################################################################
    self . Prerequisite . setRelation ( "Successor"                          )
    self . Successor    . setRelation ( "Prerequisite"                       )
    ##########################################################################
    return
  ############################################################################
  def setRequirement        ( self , require                               ) :
    ##########################################################################
    if                      ( require == 31                                ) :
      self . asPrerequisite (                                                )
    elif                    ( require == 32                                ) :
      self . asSuccessor    (                                                )
    ##########################################################################
    return
  ############################################################################
  def setOwner                ( self     , TypeId , Uuid                   ) :
    ##########################################################################
    self . Prerequisite . set ( "t1"     , TypeId                            )
    self . Prerequisite . set ( "first"  , Uuid                              )
    ##########################################################################
    self . Successor    . set ( "t2"     , TypeId                            )
    self . Successor    . set ( "second" , Uuid                              )
    ##########################################################################
    return
  ############################################################################
  def assignWindowTitle      ( self , Title                                ) :
    ##########################################################################
    self . AssignedTitle = Title
    self . changeWindowTitle (                                               )
    ##########################################################################
    return
  ############################################################################
  def changeWindowTitle                 ( self                             ) :
    ##########################################################################
    REL     = self . Prerequisite . get ( "relation"                         )
    REL     = int                       ( REL                                )
    TFMT    = self . getMenuItem        ( "TitleFormat"                      )
    ##########################################################################
    if                                  ( REL == 31                        ) :
      MSG   = self . getMenuItem        ( "Prerequisite"                     )
      title = TFMT . format             ( self . AssignedTitle , MSG         )
    elif                                ( REL == 32                        ) :
      MSG   = self . getMenuItem        ( "Successor"                        )
      title = TFMT . format             ( self . AssignedTitle , MSG         )
    else                                                                     :
      title = self . AssignedTitle
    ##########################################################################
    self    . setWindowTitle            ( title                              )
    ##########################################################################
    return
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup                   )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    self     . Notify         ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    return
  ############################################################################
  def DurationSTR              ( self , START , FINISH                     ) :
    ##########################################################################
    TRX  = self . Translations [ self . ClassTag ] [ "Units"                 ]
    SFMT = TRX                 [ "Second"                                    ]
    MFMT = TRX                 [ "Minute"                                    ]
    HFMT = TRX                 [ "Hour"                                      ]
    DFMT = TRX                 [ "Day"                                       ]
    ##########################################################################
    DT   = int                 ( FINISH - START                              )
    RR   = int                 ( DT % 60                                     )
    DT   = int                 ( DT / 60                                     )
    SS   = SFMT . format       ( RR                                          )
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    RR   = int                 ( DT % 60                                     )
    DT   = int                 ( DT / 60                                     )
    MM   = MFMT . format       ( RR                                          )
    SS   = f"{MM}{SS}"
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    RR   = int                 ( DT % 24                                     )
    DT   = int                 ( DT / 24                                     )
    HH   = HFMT . format       ( RR                                          )
    SS   = f"{HH}{SS}"
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    DD   = DFMT . format       ( RR                                          )
    SS   = f"{DD}{SS}"
    ##########################################################################
    return SS
  ############################################################################
  def getItemJson    ( self , IT                                           ) :
    return IT . data ( 7    , Qt . UserRole                                  )
  ############################################################################
  def PrepareItemContent           ( self , IT , JSON                      ) :
    ##########################################################################
    TZ       = "Asia/Taipei"
    TRX      = self . Translations [ self . ClassTag                         ]
    NOW      = StarDate            (                                         )
    ##########################################################################
    UUID     = int                 ( JSON [ "Uuid" ]                         )
    Id       = int                 ( UUID % 100000000                        )
    UXID     = str                 ( UUID                                    )
    Name     = JSON                [ "Name"                                  ]
    TYPE     = JSON                [ "Type"                                  ]
    PERIOD   = JSON                [ "Period"                                ]
    ##########################################################################
    START    = PERIOD . Start
    ENDT     = PERIOD . End
    STATES   = PERIOD . States
    ##########################################################################
    J        =                     { "Uuid"   : UUID                       , \
                                     "Name"   : Name                       , \
                                     "Type"   : TYPE                       , \
                                     "States" : STATES                     , \
                                     "Start"  : START                      , \
                                     "Finish" : ENDT                         }
    ##########################################################################
    TName    = TRX                 [ "ObjectTypes" ] [ str ( TYPE )          ]
    DURATION = self . DurationSTR  ( START , ENDT                            )
    ##########################################################################
    IT       . setText             ( 0 , TName                               )
    IT       . setToolTip          ( 0 , UXID                                )
    IT       . setData             ( 0 , Qt . UserRole , UXID                )
    ##########################################################################
    IT       . setText             ( 1 , str ( Id )                          )
    IT       . setTextAlignment    ( 1 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 2 , Name                                )
    ##########################################################################
    DTS      = ""
    if                             ( START    > 0                          ) :
      NOW    . Stardate = START
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 3 , DTS                                 )
    ##########################################################################
    DTS      = ""
    if                             ( ENDT     > 0                          ) :
      NOW    . Stardate = ENDT
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 4 , DTS                                 )
    ##########################################################################
    IT       . setText             ( 5 , DURATION                            )
    ##########################################################################
    TRXS     = TRX                 [ "States"                                ]
    IT       . setText             ( 6 , TRXS [ str ( STATES ) ]             )
    ##########################################################################
    IT       . setData             ( 7 , Qt . UserRole , J                   )
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
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , ITEMs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for T in ITEMs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( T                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def LoadProjects            ( self , DB , LISTS                          ) :
    ##########################################################################
    NAMTAB   = self . Tables  [ "NamesParent"                                ]
    RELTAB   = self . Tables  [ "RelationDepends"                            ]
    ##########################################################################
    self            . Prerequisite . set           ( "t2" , 71               )
    PROJECTS = self . Prerequisite . Subordination ( DB   , RELTAB           )
    ##########################################################################
    for UUID in PROJECTS                                                     :
      ########################################################################
      self   . NodeTypes [ UUID ] = 71
      ########################################################################
      PRJ    = Project        (                                              )
      PRJ    . Tables = self . Tables
      PRJ    . Uuid   = UUID
      PRJ    . LoadBriefs     ( DB                                           )
      ########################################################################
      NAME   = self . GetName ( DB , NAMTAB , UUID                           )
      ########################################################################
      J      =                { "Uuid"    : UUID                           , \
                                "Type"    : 71                             , \
                                "Name"    : NAME                           , \
                                "Period"  : PRJ . Period                   , \
                                "Project" : PRJ                              }
      LISTS  . append         ( J                                            )
    ##########################################################################
    return LISTS
  ############################################################################
  def LoadTasks               ( self , DB , LISTS                          ) :
    ##########################################################################
    NAMTAB   = self . Tables  [ "NamesParent"                                ]
    RELTAB   = self . Tables  [ "RelationDepends"                            ]
    ##########################################################################
    self     .        Prerequisite . set           ( "t2" , 16               )
    TASKS    = self . Prerequisite . Subordination ( DB   , RELTAB           )
    ##########################################################################
    for UUID in TASKS                                                        :
      ########################################################################
      self   . NodeTypes [ UUID ] = 16
      ########################################################################
      TASK   = Task           (                                              )
      TASK   . Tables = self . Tables
      TASK   . Uuid   = UUID
      TASK   . LoadBriefs     ( DB                                           )
      ########################################################################
      NAME   = self . GetName ( DB , NAMTAB , UUID                           )
      ########################################################################
      J      =                { "Uuid"   : UUID                            , \
                                "Type"   : 16                              , \
                                "Name"   : NAME                            , \
                                "Period" : TASK . Period                   , \
                                "Task"   : TASK                              }
      LISTS  . append         ( J                                            )
    ##########################################################################
    return LISTS
  ############################################################################
  def LoadEvents              ( self , DB , LISTS                          ) :
    ##########################################################################
    NAMTAB   = self . Tables  [ "NamesParent"                                ]
    RELTAB   = self . Tables  [ "RelationDepends"                            ]
    ##########################################################################
    self            . Prerequisite . set           ( "t2" , 15               )
    EVENTS   = self . Prerequisite . Subordination ( DB   , RELTAB           )
    ##########################################################################
    for UUID in EVENTS                                                       :
      ########################################################################
      self   . NodeTypes [ UUID ] = 15
      ########################################################################
      EVENT  = Event          (                                              )
      EVENT  . Tables = self . Tables
      EVENT  . Uuid   = UUID
      EVENT  . LoadBriefs     ( DB                                           )
      ########################################################################
      NAME   = self . GetName ( DB , NAMTAB , UUID                           )
      ########################################################################
      J      =                { "Uuid"   : UUID                            , \
                                "Type"   : 15                              , \
                                "Name"   : NAME                            , \
                                "Period" : EVENT . Period                  , \
                                "Event"  : EVENT                             }
      LISTS  . append         ( J                                            )
    ##########################################################################
    return LISTS
  ############################################################################
  def LoadPeriods             ( self , DB , LISTS                          ) :
    ##########################################################################
    PRDTAB   = self . Tables  [ "Periods"                                    ]
    NAMTAB   = self . Tables  [ "NamesLocal"                                 ]
    RELTAB   = self . Tables  [ "RelationDepends"                            ]
    ##########################################################################
    self     . Prerequisite . set                  ( "t2" , 92               )
    PERIODS  = self . Prerequisite . Subordination ( DB   , RELTAB           )
    ##########################################################################
    for UUID in PERIODS                                                      :
      ########################################################################
      self   . NodeTypes [ UUID ] = 92
      ########################################################################
      PERIOD = Periode        (                                              )
      PERIOD . Uuid   = UUID
      PERIOD . ObtainsByUuid  ( DB , PRDTAB                                  )
      ########################################################################
      NAME   = self . GetName ( DB , NAMTAB , UUID                           )
      ########################################################################
      J      =                { "Uuid"   : UUID                            , \
                                "Type"   : 92                              , \
                                "Name"   : NAME                            , \
                                "Period" : PERIOD                            }
      LISTS  . append         ( J                                            )
    ##########################################################################
    return LISTS
  ############################################################################
  def loading                     ( self                                   ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    if                            ( DB == None                             ) :
      self . emitNamesShow . emit (                                          )
      return
    ##########################################################################
    self   . Notify               ( 3                                        )
    ##########################################################################
    FMT    = self . Translations  [ "UI::StartLoading"                       ]
    MSG    = FMT . format         ( self . windowTitle ( )                   )
    self   . ShowStatus           ( MSG                                      )
    self   . OnBusy  . emit       (                                          )
    self   . setBustle            (                                          )
    ##########################################################################
    ITEMs  =                      [                                          ]
    ITEMs  = self . LoadProjects  ( DB , ITEMs                               )
    ITEMs  = self . LoadTasks     ( DB , ITEMs                               )
    ITEMs  = self . LoadEvents    ( DB , ITEMs                               )
    ITEMs  = self . LoadPeriods   ( DB , ITEMs                               )
    ##########################################################################
    self   . setVacancy           (                                          )
    self   . GoRelax . emit       (                                          )
    self   . ShowStatus           ( ""                                       )
    DB     . Close                (                                          )
    ##########################################################################
    if                            ( len ( ITEMs ) <= 0                     ) :
      self . emitNamesShow . emit (                                          )
      return
    ##########################################################################
    self   . emitAllNames  . emit ( ITEMs                                    )
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
  def allowedMimeTypes     ( self , mime                                   ) :
    FMTs    =              [ "project/uuids"                               , \
                             "task/uuids"                                  , \
                             "event/uuids"                                 , \
                             "period/uuids"                                  ]
    formats = ";" . join   ( FMTs                                            )
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def acceptProjectsDrop ( self                                            ) :
    return True
  ############################################################################
  def acceptTasksDrop    ( self                                            ) :
    return True
  ############################################################################
  def acceptEventsDrop   ( self                                            ) :
    return True
  ############################################################################
  def acceptPeriodsDrop  ( self                                            ) :
    return True
  ############################################################################
  def dropNew                           ( self                             , \
                                          sourceWidget                     , \
                                          mimeData                         , \
                                          mousePos                         ) :
    ##########################################################################
    if                                  ( self == sourceWidget             ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew      ( mimeData                           )
    if                                  ( not RDN                          ) :
      return False
    ##########################################################################
    mtype  = self . DropInJSON          [ "Mime"                             ]
    LISTS  =                            [ "project/uuids"                  , \
                                          "task/uuids"                     , \
                                          "event/uuids"                    , \
                                          "period/uuids"                     ]
    ##########################################################################
    if                                  ( mtype not in LISTS               ) :
      return False
    ##########################################################################
    title  = sourceWidget . windowTitle (                                    )
    UUIDs  = self . DropInJSON          [ "UUIDs"                            ]
    CNT    = len                        ( UUIDs                              )
    self   . ShowMenuItemTitleStatus    ( "JoinNodes" , title , CNT          )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving              ( self , sourceWidget , mimeData , mousePos  ) :
    ##########################################################################
    if                        ( self . droppingAction                      ) :
      return False
    ##########################################################################
    if                        ( sourceWidget == self                       ) :
      return False
    ##########################################################################
    mtype = self . DropInJSON [ "Mime"                                       ]
    LISTS =                   [ "project/uuids"                            , \
                                "task/uuids"                               , \
                                "event/uuids"                              , \
                                "period/uuids"                               ]
    ##########################################################################
    if                        ( mtype not in LISTS                         ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def dropProjects                  ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . ProjectsJoinCondition
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def dropTasks                     ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . TasksJoinCondition
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def dropEvents                    ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . EventsJoinCondition
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def dropPeriods                   ( self , source , pos , JSON           ) :
    ##########################################################################
    FUNC = self . PeriodsJoinCondition
    ##########################################################################
    return self . defaultDropInside ( self , source , JSON , FUNC            )
  ############################################################################
  def ProjectsJoinCondition   ( self , UUIDs                               ) :
    ##########################################################################
    self . NodesJoinCondition ( 71   , UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def TasksJoinCondition      ( self , UUIDs                               ) :
    ##########################################################################
    self . NodesJoinCondition ( 16   , UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def EventsJoinCondition     ( self , UUIDs                               ) :
    ##########################################################################
    self . NodesJoinCondition ( 15   , UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def PeriodsJoinCondition    ( self , UUIDs                               ) :
    ##########################################################################
    self . NodesJoinCondition ( 92   , UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def NodesJoinCondition         ( self , TypeId , UUIDs                   ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB in [ False , None ]                  ) :
      return
    ##########################################################################
    RELTAB = self . Tables       [ "RelationDepends"                         ]
    ##########################################################################
    self   . Prerequisite . set  ( "t2" , TypeId                             )
    self   . Successor    . set  ( "t1" , TypeId                             )
    ##########################################################################
    DB     . LockWrites          ( [ RELTAB                                ] )
    ##########################################################################
    for TUID in UUIDs                                                        :
      ########################################################################
      self . Prerequisite . set  ( "second" , TUID                           )
      self . Prerequisite . Join ( DB       , RELTAB                         )
      ########################################################################
      self . Successor    . set  ( "first"  , TUID                           )
      self . Successor    . Join ( DB       , RELTAB                         )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    DB     . Close               (                                           )
    ##########################################################################
    self   . Notify              ( 5                                         )
    self   . loading             (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . DetachConditions                  )
    ##########################################################################
    return
  ############################################################################
  def DetachConditions           ( self , UUIDs                            ) :
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB in [ False , None ]                  ) :
      return
    ##########################################################################
    RELTAB = self . Tables       [ "RelationDepends"                         ]
    ##########################################################################
    self   . Prerequisite . set  ( "t2" , TypeId                             )
    self   . Successor    . set  ( "t1" , TypeId                             )
    ##########################################################################
    DB     . LockWrites          ( [ RELTAB                                ] )
    ##########################################################################
    for TUID in UUIDs                                                        :
      ########################################################################
      self . Prerequisite . set  ( "second" , TUID                           )
      QQ   = self . Prerequisite . Delete ( RELTAB                           )
      DB   . Query               ( QQ                                        )
      ########################################################################
      self . Successor    . set  ( "first"  , TUID                           )
      QQ   = self . Successor    . Delete ( RELTAB                           )
      DB   . Query               ( QQ                                        )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    DB     . Close               (                                           )
    ##########################################################################
    self   . Notify              ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth (  0 ,  80                                         )
    self . setColumnWidth (  1 , 120                                         )
    self . setColumnWidth (  2 , 280                                         )
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
  def GroupsMenu              ( self , mm                                  ) :
    ##########################################################################
    msg  = self . getMenuItem ( "Details"                                    )
    LOM  = mm . addMenu       ( msg                                          )
    ##########################################################################
    msg  = self . getMenuItem ( "Project"                                    )
    mm   . addActionFromMenu  ( LOM , 2001 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Task"                                       )
    mm   . addActionFromMenu  ( LOM , 2002 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Event"                                      )
    mm   . addActionFromMenu  ( LOM , 2003 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Editor"                                     )
    mm   . addActionFromMenu  ( LOM , 2004 , msg                             )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu               ( self , at , item                       ) :
    ##########################################################################
    if                            ( at == 2001                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenProjects , ( uuid , )         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2002                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenTasks , ( uuid , )            )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2003                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenEvents , ( uuid , )           )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2004                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      name = item . text          ( 1                                        )
      self . PeriodDetails . emit ( name , str ( uuid )                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    ##########################################################################
    return self . DefaultColumnsMenu (        mm , 0                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9007 )         :
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
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    ## if                              ( atItem not in [ False , None ]       ) :
    ##   mm   = self . GroupsMenu      ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunGroupsMenu ( at , atItem ) ) :
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################

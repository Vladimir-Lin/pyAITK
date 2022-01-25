# -*- coding: utf-8 -*-
##############################################################################
## PeriodEditor
## 時段列表
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
from   PyQt5                               import QtCore
from   PyQt5                               import QtGui
from   PyQt5                               import QtWidgets
##############################################################################
from   PyQt5 . QtCore                      import QObject
from   PyQt5 . QtCore                      import pyqtSignal
from   PyQt5 . QtCore                      import pyqtSlot
from   PyQt5 . QtCore                      import Qt
from   PyQt5 . QtCore                      import QPoint
from   PyQt5 . QtCore                      import QPointF
from   PyQt5 . QtCore                      import QSize
from   PyQt5 . QtCore                      import QDateTime
##############################################################################
from   PyQt5 . QtGui                       import QIcon
from   PyQt5 . QtGui                       import QCursor
from   PyQt5 . QtGui                       import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                   import QApplication
from   PyQt5 . QtWidgets                   import QWidget
from   PyQt5 . QtWidgets                   import qApp
from   PyQt5 . QtWidgets                   import QMenu
from   PyQt5 . QtWidgets                   import QAction
from   PyQt5 . QtWidgets                   import QShortcut
from   PyQt5 . QtWidgets                   import QAbstractItemView
from   PyQt5 . QtWidgets                   import QTreeWidget
from   PyQt5 . QtWidgets                   import QTreeWidgetItem
from   PyQt5 . QtWidgets                   import QLineEdit
from   PyQt5 . QtWidgets                   import QComboBox
from   PyQt5 . QtWidgets                   import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager            import MenuManager    as MenuManager
from   AITK  . Qt . Widget                 import Widget         as Widget
##############################################################################
from   AITK  . Essentials . Relation       import Relation       as Relation
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
from   AITK  . Documents  . Notes          import Notes          as Notes
from   AITK  . Documents  . Variables      import Variables      as Variables
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK  . Scheduler  . Project        import Project        as Project
from   AITK  . Scheduler  . Projects       import Projects       as Projects
from   AITK  . Scheduler  . Event          import Event          as Event
from   AITK  . Scheduler  . Events         import Events         as Events
from   AITK  . Scheduler  . Task           import Task           as Task
from   AITK  . Scheduler  . Tasks          import Tasks          as Tasks
##############################################################################
from         . AppendPeriod                import Ui_AppendPeriod
##############################################################################
class PeriodAppend                  ( Widget                               ) :
  ############################################################################
  emitProjects = pyqtSignal         ( dict                                   )
  emitTasks    = pyqtSignal         ( dict                                   )
  emitEvents   = pyqtSignal         ( dict                                   )
  CloseMyself  = pyqtSignal         ( QWidget                                )
  OpenEditor   = pyqtSignal         ( str , str                              )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    self . ui = Ui_AppendPeriod     (                                        )
    self . ui . setupUi             ( self                                   )
    ##########################################################################
    self . ClassTag     = "PeriodAppend"
    self . VoiceJSON    =           {                                        }
    self . Period       = Periode   (                                        )
    self . Now          = StarDate  (                                        )
    self . DefaultType  = 196833
    ##########################################################################
    self . emitProjects . connect   ( self . ListingProjects                 )
    self . emitTasks    . connect   ( self . ListingTasks                    )
    self . emitEvents   . connect   ( self . ListingEvents                   )
    ##########################################################################
    self . ui . Append . setEnabled ( False                                  )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def Relocation                            ( self                         ) :
    ##########################################################################
    R    = self . ui . Append    . geometry (                                )
    N    = self . ui . Note      . geometry (                                )
    T    = self . ui . StartTime . geometry (                                )
    W    = self . width                     (                                )
    H    = self . height                    (                                )
    B    = R    . height                    (                                )
    L    = T    . left                      (                                )
    A    = N  . top                         (                                )
    D    = W    - 20
    Z    = W    - L - 10
    X    = H    - A - 10
    ##########################################################################
    self . ui . Append     . resize         ( D , B                          )
    self . ui . Projects   . resize         ( D , B                          )
    self . ui . Tasks      . resize         ( D , B                          )
    self . ui . Events     . resize         ( D , B                          )
    self . ui . Name       . resize         ( D , B                          )
    ##########################################################################
    self . ui . StartTime  . resize         ( Z , B                          )
    self . ui . FinishTime . resize         ( Z , B                          )
    ##########################################################################
    self . ui . Note       . resize         ( D , X                          )
    ##########################################################################
    return
  ############################################################################
  def GetEventUUID                            ( self                       ) :
    ##########################################################################
    INDEX = self . ui . Events . currentIndex (                              )
    if                                        ( INDEX < 0                  ) :
      return 0
    ##########################################################################
    WID   = self . ui . Events . itemData     ( INDEX                        )
    WID   = int                               ( WID                          )
    if                                        ( WID <= 0                   ) :
       return 0
    ##########################################################################
    return WID
  ############################################################################
  def DetectValidPeriod                           ( self                   ) :
    ##########################################################################
    ENABLED   = True
    ##########################################################################
    Name      = self . ui . Name . text           (                          )
    if                                            ( len ( Name ) <= 0      ) :
      ENABLED = False
    ##########################################################################
    SDT       = self . ui . StartTime  . dateTime (                          )
    EDT       = self . ui . FinishTime . dateTime (                          )
    ##########################################################################
    if                                            ( SDT >= EDT             ) :
      ENABLED = False
    ##########################################################################
    EUID      = self . GetEventUUID               (                          )
    INDEX     = self . ui . Events . currentIndex (                          )
    if                                            ( EUID <= 0              ) :
      ENABLED = False
    ##########################################################################
    self . ui . Append . setEnabled               ( ENABLED                  )
    ##########################################################################
    return
  ############################################################################
  def ListingProjects                     ( self , JSON                    ) :
    ##########################################################################
    UUIDs  = JSON                         [ "UUIDs"                          ]
    NAMEs  = JSON                         [ "NAMEs"                          ]
    msg    = self . getMenuItem           ( "Useless"                        )
    ##########################################################################
    self   . ui . Projects . blockSignals ( True                             )
    self   . ui . Projects . clear        (                                  )
    self   . ui . Projects . addItem      ( msg , "0"                        )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . ui . Projects . addItem      ( NAMEs [ UUID ] , f"{UUID}"       )
    ##########################################################################
    self   . ui . Projects . blockSignals ( False                            )
    self   . setEnabled                   ( True                             )
    self   . ui . Append . setEnabled     ( False                            )
    self   . Notify                       ( 0                                )
    ##########################################################################
    return
  ############################################################################
  def ListingTasks                      ( self , JSON                      ) :
    ##########################################################################
    UUIDs  = JSON                       [ "UUIDs"                            ]
    NAMEs  = JSON                       [ "NAMEs"                            ]
    msg    = self . getMenuItem         ( "Useless"                          )
    ##########################################################################
    self   . ui . Tasks  . blockSignals ( True                               )
    self   . ui . Events . blockSignals ( True                               )
    self   . ui . Events . clear        (                                    )
    self   . ui . Tasks  . addItem      ( msg , "0"                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . ui . Tasks  . addItem      ( NAMEs [ UUID ] , f"{UUID}"         )
    ##########################################################################
    self   . ui . Events . blockSignals ( False                              )
    self   . ui . Tasks  . blockSignals ( False                              )
    self   . setEnabled                 ( True                               )
    self   . Notify                     ( 0                                  )
    ##########################################################################
    return
  ############################################################################
  def ListingEvents                     ( self , JSON                      ) :
    ##########################################################################
    UUIDs  = JSON                       [ "UUIDs"                            ]
    NAMEs  = JSON                       [ "NAMEs"                            ]
    msg    = self . getMenuItem         ( "Useless"                          )
    ##########################################################################
    self   . ui . Events . blockSignals ( True                               )
    self   . ui . Events . clear        (                                    )
    self   . ui . Events . addItem      ( msg , "0"                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . ui . Events . addItem      ( NAMEs [ UUID ] , f"{UUID}"         )
    ##########################################################################
    self   . ui . Events . blockSignals ( False                              )
    self   . setEnabled                 ( True                               )
    self   . Notify                     ( 0                                  )
    ##########################################################################
    return
  ############################################################################
  def ProjectsChanged                        ( self , index                ) :
    ##########################################################################
    UUID   = self . ui . Projects . itemData (        index                  )
    UUID   = int                             ( UUID                          )
    ##########################################################################
    self   . setEnabled                      ( False                         )
    self   . ui . Append . setEnabled        ( False                         )
    self   . ui . Tasks  . blockSignals      ( True                          )
    self   . ui . Events . blockSignals      ( True                          )
    self   . ui . Tasks  . clear             (                               )
    self   . ui . Events . clear             (                               )
    self   . ui . Events . blockSignals      ( False                         )
    self   . ui . Tasks  . blockSignals      ( False                         )
    ##########################################################################
    if                                       ( UUID > 0                    ) :
      VAL  =                                 ( UUID ,                        )
      self . Go                              ( self . LoadTasks , VAL        )
    ##########################################################################
    return
  ############################################################################
  def TasksChanged                           ( self , index                ) :
    ##########################################################################
    UUID   = self . ui . Tasks    . itemData (        index                  )
    UUID   = int                             ( UUID                          )
    ##########################################################################
    self   . setEnabled                      ( False                         )
    self   . ui . Append . setEnabled        ( False                         )
    self   . ui . Events . blockSignals      ( True                          )
    self   . ui . Events . clear             (                               )
    self   . ui . Events . blockSignals      ( False                         )
    ##########################################################################
    if                                       ( UUID > 0                    ) :
      VAL  =                                 ( UUID ,                        )
      self . Go                              ( self . LoadEvents , VAL       )
    ##########################################################################
    return
  ############################################################################
  def EventsChanged                        ( self , index                  ) :
    ##########################################################################
    UUID   = self . ui . Events . itemData ( index                           )
    UUID   = int                           ( UUID                            )
    ##########################################################################
    if                                     ( UUID <= 0                     ) :
      self . ui . Append . setEnabled      ( False                           )
      return
    ##########################################################################
    self   . DetectValidPeriod             (                                 )
    ##########################################################################
    return
  ############################################################################
  def NameChanged            ( self                                        ) :
    ##########################################################################
    self . DetectValidPeriod (                                               )
    ##########################################################################
    return
  ############################################################################
  def StartTimeChanged       ( self , dt                                   ) :
    ##########################################################################
    self . DetectValidPeriod (                                               )
    ##########################################################################
    return
  ############################################################################
  def FinishTimeChanged      ( self , dt                                   ) :
    ##########################################################################
    self . DetectValidPeriod (                                               )
    ##########################################################################
    return
  ############################################################################
  def NoteChanged                  ( self                                  ) :
    return
  ############################################################################
  def AppendPeriod                             ( self                      ) :
    ##########################################################################
    EUID   = self . GetEventUUID               (                             )
    if                                         ( EUID <= 0                 ) :
      self . Notify                            ( 4                           )
      return
    ##########################################################################
    NAME   = self . ui . Name . text           (                             )
    if                                         ( len ( NAME ) <= 0         ) :
      self . Notify                            ( 4                           )
      return
    ##########################################################################
    SDT    = self . ui . StartTime  . dateTime (                             )
    EDT    = self . ui . FinishTime . dateTime (                             )
    ##########################################################################
    if                                         ( SDT >= EDT                ) :
      self . Notify                            ( 4                           )
      return
    ##########################################################################
    NOTE   = self . ui . Note . toPlainText    (                             )
    OPEN   = ( self . ui . OpenEditor . checkState ( ) == Qt . Checked       )
    ##########################################################################
    self   . Now . setTime                     ( SDT . toSecsSinceEpoch ( )  )
    SDTX   = self . Now . Stardate
    self   . Now . setTime                     ( EDT . toSecsSinceEpoch ( )  )
    EDTX   = self . Now . Stardate
    ##########################################################################
    self   . ui . Append . setEnabled        ( False                         )
    ##########################################################################
    JSON   = { "Event"  : EUID                                             , \
               "Name"   : NAME                                             , \
               "Note"   : NOTE                                             , \
               "Start"  : SDTX                                             , \
               "Finish" : EDTX                                             , \
               "Open"   : OPEN                                               }
    ##########################################################################
    self   . Go ( self . AppendingPeriod , ( JSON , )                        )
    ##########################################################################
    return
  ############################################################################
  def AppendingPeriod             ( self , JSON                            ) :
    ##########################################################################
    self     . Now  . Now         (                                          )
    NOW      = self . Now . Stardate
    ##########################################################################
    EUID     = JSON               [ "Event"                                  ]
    NAME     = JSON               [ "Name"                                   ]
    NOTE     = JSON               [ "Note"                                   ]
    START    = JSON               [ "Start"                                  ]
    FINISH   = JSON               [ "Finish"                                 ]
    OPEN     = JSON               [ "Open"                                   ]
    STATES   = 1
    ##########################################################################
    if                            ( START  > NOW                           ) :
      STATES = 3
    elif                          ( FINISH < NOW                           ) :
      STATES = 4
    else                                                                     :
      STATES = 5
    ##########################################################################
    DB       = self . ConnectDB   ( UsePure = True                           )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    self     . LoopRunning = False
    ##########################################################################
    self     . Notify             ( 3                                        )
    ##########################################################################
    MSG      = self . getMenuItem ( "Appending"                              )
    self     . ShowStatus         ( MSG                                      )
    ##########################################################################
    PRDTAB   = self . Tables      [ "Periods"                                ]
    RELTAB   = self . Tables      [ "RelationPeriods"                        ]
    NAMTAB   = self . Tables      [ "NamesLocal"                             ]
    GNATAB   = self . Tables      [ "NamesPrivate"                           ]
    TYPTAB   = self . Tables      [ "Types"                                  ]
    TABLES   =                    [ PRDTAB                                 , \
                                    NAMTAB                                 , \
                                    RELTAB                                 , \
                                    GNATAB                                 , \
                                    TYPTAB                                   ]
    ##########################################################################
    DB       . LockWrites         ( TABLES                                   )
    ##########################################################################
    EVTS     = Events             (                                          )
    EVTS     . Tables      = self . Tables
    EVTS     . DefaultType = self . DefaultType
    uuid     = EVTS . NewPeriod   ( DB , 4 , START , FINISH , STATES         )
    ##########################################################################
    EVT      = Event              (                                          )
    EVT      . Tables = self . Tables
    EVT      . Uuid   = EUID
    EVT      . JoinPeriods        ( DB , RELTAB , [ uuid ]                   )
    ##########################################################################
    self     . AssureUuidName     ( DB , NAMTAB , uuid , NAME                )
    ##########################################################################
    self     . ShowStatus         ( ""                                       )
    self     . LoopRunning = True
    ##########################################################################
    DB       . UnlockTables       (                                          )
    DB       . Close              (                                          )
    ##########################################################################
    self     . Notify             ( 0                                        )
    ##########################################################################
    if                            ( OPEN                                   ) :
      self  . OpenEditor  . emit  ( Name , str ( uuid )                      )
      time  . sleep               ( 1.0                                      )
    ##########################################################################
    self    . CloseMyself . emit  ( self                                     )
    ##########################################################################
    return
  ############################################################################
  def LoadEvents                  ( self , TASK                            ) :
    ##########################################################################
    DB      = self . ConnectDB    ( UsePure = True                           )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    self    . LoopRunning = False
    ##########################################################################
    self    . Notify              ( 3                                        )
    ##########################################################################
    FMT     = self . Translations [ "UI::StartLoading"                       ]
    MSG     = FMT . format        ( self . windowTitle ( )                   )
    self    . ShowStatus          ( MSG                                      )
    ##########################################################################
    NAMTAB  = self . Tables       [ "Names"                                  ]
    ##########################################################################
    TSK     = Task                (                                          )
    TSK     . Tables = self . Tables
    TSK     . Uuid   = TASK
    UUIDs   = TSK . GetEvents     ( DB                                       )
    ##########################################################################
    NAMEs   =                     {                                          }
    if                            ( len ( UUIDs ) > 0                      ) :
      NAMEs = self . GetNames     ( DB , NAMTAB , UUIDs                      )
    ##########################################################################
    self    . ShowStatus          ( ""                                       )
    self    . LoopRunning = True
    ##########################################################################
    DB      . Close               (                                          )
    ##########################################################################
    JSON             =            {                                          }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self    . Notify              ( 0                                        )
    self    . emitEvents . emit   ( JSON                                     )
    ##########################################################################
    return
  ############################################################################
  def LoadTasks                    ( self , PROJECT                        ) :
    ##########################################################################
    DB      = self . ConnectDB    ( UsePure = True                           )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    self    . LoopRunning = False
    ##########################################################################
    self    . Notify              ( 3                                        )
    ##########################################################################
    FMT     = self . Translations [ "UI::StartLoading"                       ]
    MSG     = FMT . format        ( self . windowTitle ( )                   )
    self    . ShowStatus          ( MSG                                      )
    ##########################################################################
    NAMTAB  = self . Tables       [ "Names"                                  ]
    ##########################################################################
    PRJ     = Project             (                                          )
    PRJ     . Tables = self . Tables
    PRJ     . Uuid   = PROJECT
    UUIDs   = PRJ . GetTasks      ( DB                                       )
    ##########################################################################
    NAMEs   =                     {                                          }
    if                            ( len ( UUIDs ) > 0                      ) :
      NAMEs = self . GetNames     ( DB , NAMTAB , UUIDs                      )
    ##########################################################################
    self    . ShowStatus          ( ""                                       )
    self    . LoopRunning = True
    ##########################################################################
    DB      . Close               (                                          )
    ##########################################################################
    JSON             =            {                                          }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self    . Notify              ( 0                                        )
    self    . emitTasks . emit    ( JSON                                     )
    ##########################################################################
    return
  ############################################################################
  def LoadProjects                ( self                                   ) :
    ##########################################################################
    DB      = self . ConnectDB    ( UsePure = True                           )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    self    . LoopRunning = False
    ##########################################################################
    self    . Notify              ( 3                                        )
    ##########################################################################
    FMT     = self . Translations [ "UI::StartLoading"                       ]
    MSG     = FMT . format        ( self . windowTitle ( )                   )
    self    . ShowStatus          ( MSG                                      )
    ##########################################################################
    PRJTAB  = self . Tables       [ "Projects"                               ]
    NAMTAB  = self . Tables       [ "Names"                                  ]
    ##########################################################################
    QQ      = f"""select `uuid` from {PRJTAB}
                 where ( `used` = 1 )
                 order by `id` asc ;"""
    QQ      = " " . join          ( QQ . split ( )                           )
    UUIDs   = DB   . ObtainUuids  ( QQ                                       )
    NAMEs   =                     {                                          }
    if                            ( len ( UUIDs ) > 0                      ) :
      NAMEs = self . GetNames     ( DB , NAMTAB , UUIDs                      )
    ##########################################################################
    self    . ShowStatus          ( ""                                       )
    self    . LoopRunning = True
    ##########################################################################
    DB      . Close               (                                          )
    ##########################################################################
    JSON             =            {                                          }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self    . Notify              ( 0                                        )
    self    . emitProjects . emit ( JSON                                     )
    ##########################################################################
    return
  ############################################################################
  def startup                             ( self                           ) :
    ##########################################################################
    self . setEnabled                     ( False                            )
    self . ui . Projects . clear          (                                  )
    self . ui . Tasks    . clear          (                                  )
    self . ui . Events   . clear          (                                  )
    ##########################################################################
    self . Now . Now                      (                                  )
    TS   = self . Now . Timestamp         (                                  )
    DT   = QDateTime . fromSecsSinceEpoch ( TS                               )
    self . ui . StartTime  . setDateTime  ( DT                               )
    self . ui . FinishTime . setDateTime  ( DT                               )
    ##########################################################################
    self . Go                             ( self . LoadProjects              )
    ##########################################################################
    return
##############################################################################

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
from   AITK  . Calendars  . Apple          import Apple          as DAV
##############################################################################
from         . PeriodEditorUI              import Ui_PeriodEditorUI
##############################################################################
class PeriodEditor                ( Widget                                 ) :
  ############################################################################
  emitShow   = pyqtSignal         (                                          )
  emitApple  = pyqtSignal         (                                          )
  emitUpdate = pyqtSignal         (                                          )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . ui = Ui_PeriodEditorUI (                                          )
    self . ui . setupUi           ( self                                     )
    ##########################################################################
    self . ClassTag  = "PeriodEditor"
    self . VoiceJSON =            {                                          }
    self . Period    = Periode    (                                          )
    self . Now       = StarDate   (                                          )
    ##########################################################################
    self . Calendars =            [                                          ]
    ##########################################################################
    self . emitShow   . connect   ( self . show                              )
    self . emitApple  . connect   ( self . ShowAppleCalendars                )
    self . emitUpdate . connect   ( self . UpdatePeriodValues                )
    ##########################################################################
    return
  ############################################################################
  def PrepareComboBox               ( self , combo , JSON                  ) :
    ##########################################################################
    combo . blockSignals            ( True                                   )
    ##########################################################################
    for key , value in JSON . items (                                      ) :
      ########################################################################
      combo . addItem               ( value , int ( key )                    )
    ##########################################################################
    combo . blockSignals            ( False                                  )
    ##########################################################################
    return
  ############################################################################
  def PrepareDefaultValues          ( self                                 ) :
    ##########################################################################
    TRX    = self . Translations    [ self . ClassTag                        ]
    TRT    = TRX                    [ "Type"                                 ]
    TRU    = TRX                    [ "Used"                                 ]
    TRS    = TRX                    [ "States"                               ]
    ##########################################################################
    self   . Now  . Now             (                                        )
    TS     = self . Now . Timestamp (                                        )
    DT     = QDateTime . fromSecsSinceEpoch ( TS                             )
    ##########################################################################
    TSON   =                        { "0" : "Asia/Taipei" , "1" : "UTC"      }
    ##########################################################################
    self   . PrepareComboBox        ( self . ui . TypeBox     , TRT          )
    self   . PrepareComboBox        ( self . ui . UsageBox    , TRU          )
    self   . PrepareComboBox        ( self . ui . StatesBox   , TRS          )
    self   . PrepareComboBox        ( self . ui . TimeZoneBox , TSON         )
    ##########################################################################
    self   . ui . StartTime  . setDateTime ( DT                              )
    self   . ui . FinishTime . setDateTime ( DT                              )
    ##########################################################################
    if                              ( self . Period . Uuid > 0             ) :
      self . ui . Append . hide     (                                        )
    ##########################################################################
    return
  ############################################################################
  def NameChanged                         ( self                           ) :
    ##########################################################################
    oname = self . Period . getProperty   ( "Name"                           )
    name  = self . ui . NameEditor . text (                                  )
    ##########################################################################
    if                                    ( oname == name                  ) :
      return
    ##########################################################################
    self  . AssurePeriodName              ( name                             )
    ##########################################################################
    return
  ############################################################################
  def TypeChanged                ( self   , typeIndex                      ) :
    ##########################################################################
    TYPE = int                   ( typeIndex                                 )
    if                           ( TYPE == self . Period . Type            ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue ( "type" , TYPE                             )
    ##########################################################################
    return
  ############################################################################
  def UsageChanged                ( self   , usageIndex                    ) :
    ##########################################################################
    Usage = int                   ( usageIndex                               )
    if                            ( Usage == self . Period . Used          ) :
      return
    ##########################################################################
    self  . UpdatePeriodItemValue ( "used" , Usage                           )
    ##########################################################################
    return
  ############################################################################
  def TimeZoneChanged      ( self , tzIndex                                ) :
    ##########################################################################
    print("TimeZoneChanged",tzIndex)
    ##########################################################################
    return
  ############################################################################
  def StartTimeChanged           ( self                                    ) :
    ##########################################################################
    TS   = self . ui . StartTime . toSecsSinceEpoch (                        )
    self . Now . setTime         ( TS                                        )
    SDT  = self . Now . Stardate
    ##########################################################################
    if                           ( SDT == self . Period . Start            ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue ( "start" , SDT                             )
    ##########################################################################
    return
  ############################################################################
  def FinishTimeChanged          ( self                                    ) :
    ##########################################################################
    TS   = self . ui . FinishTime . toSecsSinceEpoch (                       )
    self . Now . setTime         ( TS                                        )
    SDT  = self . Now . Stardate
    ##########################################################################
    if                           ( SDT == self . Period . End              ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue ( "end"   , SDT                             )
    ##########################################################################
    return
  ############################################################################
  def ItemChanged                       ( self                             ) :
    ##########################################################################
    Item = self . ui . ItemSpin . value (                                    )
    if                                  ( Item == self . Period . Item     ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue        ( "item" , Item                      )
    ##########################################################################
    return
  ############################################################################
  def StatesChanged                ( self     , statesIndex                ) :
    ##########################################################################
    States = int                   ( statesIndex                             )
    if                             ( States == self . Period . States      ) :
      return
    ##########################################################################
    self   . UpdatePeriodItemValue ( "states" , statesIndex                  )
    ##########################################################################
    return
  ############################################################################
  def NoteChanged                              ( self                      ) :
    ##########################################################################
    onote = self . Period . getProperty        ( "Description"               )
    note  = self . ui . NoteEdit . toPlainText (                             )
    ##########################################################################
    if                                         ( onote == note             ) :
      return
    ##########################################################################
    self . AssurePeriodNote                    ( note                        )
    ##########################################################################
    return
  ############################################################################
  def AppendPeriod         ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AppleCalendarChanged ( self , calendarIndex                          ) :
    ##########################################################################
    print("AppleCalendarChanged",calendarIndex)
    ##########################################################################
    return
  ############################################################################
  def AppleEventCidChanged ( self                                          ) :
    ##########################################################################
    print("AppleEventCidChanged")
    ##########################################################################
    return
  ############################################################################
  def SyncToApple          ( self                                          ) :
    ##########################################################################
    print("SyncToApple")
    ##########################################################################
    return
  ############################################################################
  def SyncFromApple        ( self                                          ) :
    ##########################################################################
    print("SyncFromApple")
    ##########################################################################
    return
  ############################################################################
  def AssignAppleEvent     ( self , index                                  ) :
    ##########################################################################
    print("AssignAppleEvent:",index)
    ##########################################################################
    return
  ############################################################################
  def PullAppleEvents      ( self                                          ) :
    ##########################################################################
    print("PullAppleEvents")
    ##########################################################################
    return
  ############################################################################
  def AssurePeriodName              ( self , name                          ) :
    ##########################################################################
    if                              ( self . Period . Uuid <= 0            ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       ( UsePure = True                         )
    if                              ( DB in [ False , None ]               ) :
      return
    ##########################################################################
    NAMTAB = self . Tables          [ "NamesLocal"                           ]
    DB     . LockWrites             ( [ NAMTAB                             ] )
    ##########################################################################
    UUID   = self . Period . Uuid
    self   . AssureUuidName         ( DB , NAMTAB , UUID , name              )
    self   . Period . setProperties ( "Name"        , name                   )
    ##########################################################################
    DB     . UnlockTables           (                                        )
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def AssurePeriodNote              ( self , note                          ) :
    ##########################################################################
    if                              ( self . Period . Uuid <= 0            ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       ( UsePure = True                         )
    if                              ( DB in [ False , None ]               ) :
      return
    ##########################################################################
    NOXTAB = self . Tables          [ "Notes"                                ]
    ##########################################################################
    NOTE   = Notes                  (                                        )
    NOTE   . Uuid   = self . Period . Uuid
    NOTE   . Name   = "Description"
    NOTE   . Prefer = 0
    NOTE   . Note   = note
    ##########################################################################
    DB     . LockWrites             ( [ NOXTAB                             ] )
    NOTE   . assureNote             ( DB , NOXTAB                            )
    self   . Period . setProperties ( "Description" , note                   )
    DB     . UnlockTables           (                                        )
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdatePeriodItemValue   ( self , item , value                        ) :
    ##########################################################################
    if                        ( self . Period . Uuid <= 0                  ) :
      return
    ##########################################################################
    DB     = self . ConnectDB ( UsePure = True                               )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    PRDTAB = self . Tables    [ "Periods"                                    ]
    DB     . LockWrites       ( [ PRDTAB                                   ] )
    ##########################################################################
    UUID   = self . Period . Uuid
    QQ     = f"""update {PRDTAB}
                 set `{item}` = {value}
                 where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def ShowAppleCalendars                             ( self                ) :
    ##########################################################################
    CID    = self . Period . getProperty             ( "Calendar" , ""       )
    ##########################################################################
    self   . ui . AppleCalendarBox . blockSignals    ( True                  )
    self   . ui . AppleEventEdit   . blockSignals    ( True                  )
    ##########################################################################
    self   . ui . AppleCalendarBox . clear           (                       )
    ##########################################################################
    self   . ui . AppleCalendarBox . addItem         ( "沒有使用" , "" )
    AT     = 0
    POS    = 1
    ##########################################################################
    for calendar in self . Calendars                                         :
      ########################################################################
      cid  = calendar                                [ "Id"                  ]
      name = calendar                                [ "Name"                ]
      ########################################################################
      if                                             ( cid == CID          ) :
        AT = POS
      ########################################################################
      self . ui . AppleCalendarBox . addItem         ( name , cid            )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    self   . ui . AppleCalendarBox . setCurrentIndex ( AT                    )
    self   . ui . AppleEventEdit   . setText         ( CID                   )
    ##########################################################################
    self   . ui . AppleEventEdit   . blockSignals    ( False                 )
    self   . ui . AppleCalendarBox . blockSignals    ( False                 )
    ##########################################################################
    return
  ############################################################################
  def UpdatePeriodValues      ( self                                       ) :
    ##########################################################################
    if                        ( self . Period . Uuid <= 0                  ) :
      return
    ##########################################################################
    self . ui . NameEditor . blockSignals    ( True                          )
    self . ui . TypeBox    . blockSignals    ( True                          )
    self . ui . UsageBox   . blockSignals    ( True                          )
    self . ui . StartTime  . blockSignals    ( True                          )
    self . ui . FinishTime . blockSignals    ( True                          )
    self . ui . ItemSpin   . blockSignals    ( True                          )
    self . ui . StatesBox  . blockSignals    ( True                          )
    self . ui . NoteEdit   . blockSignals    ( True                          )
    ##########################################################################
    Name = self . Period . getProperty       ( "Name"        , ""            )
    DESC = self . Period . getProperty       ( "Description" , ""            )
    ##########################################################################
    self . ui . NameEditor . setText         ( Name                          )
    self . ui . NoteEdit   . setText         ( DESC                          )
    ##########################################################################
    self . ui . TypeBox    . setCurrentIndex ( self . Period . Type          )
    self . ui . UsageBox   . setCurrentIndex ( self . Period . Used          )
    self . ui . StatesBox  . setCurrentIndex ( self . Period . States        )
    ##########################################################################
    self . ui . ItemSpin   . setValue        ( self . Period . Item          )
    ##########################################################################
    if ( self . Period . Start > 0 )                                         :
      ########################################################################
      self . Now . Stardate = self . Period . Start
      TS = self . Now . Timestamp            (                               )
      DT = QDateTime . fromSecsSinceEpoch    ( TS                            )
      self . ui . StartTime  . setDateTime   ( DT                            )
    ##########################################################################
    if ( self . Period . End > 0 )                                         :
      ########################################################################
      self . Now . Stardate = self . Period . End
      TS = self . Now . Timestamp            (                               )
      DT = QDateTime . fromSecsSinceEpoch    ( TS                            )
      self . ui . FinishTime . setDateTime   ( DT                            )
    ##########################################################################
    self . ui . NoteEdit   . blockSignals    ( False                         )
    self . ui . StatesBox  . blockSignals    ( False                         )
    self . ui . ItemSpin   . blockSignals    ( False                         )
    self . ui . FinishTime . blockSignals    ( False                         )
    self . ui . StartTime  . blockSignals    ( False                         )
    self . ui . UsageBox   . blockSignals    ( False                         )
    self . ui . TypeBox    . blockSignals    ( False                         )
    self . ui . NameEditor . blockSignals    ( False                         )
    ##########################################################################
    return
  ############################################################################
  def GetAppleCalendars            ( self                                  ) :
    ##########################################################################
    URL   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"        ]
    DSID  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"       ]
    USER  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"   ]
    PASS  = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"   ]
    ##########################################################################
    APPLE = DAV                    ( URL , DSID , USER , PASS                )
    OKAY  = APPLE . FetchCalendars (                                         )
    ##########################################################################
    self  . Calendars =            [                                         ]
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      return
    ##########################################################################
    for calendar in APPLE . Calendars                                        :
      ########################################################################
      CID   = APPLE . CalendarId   ( calendar                                )
      NAME  = calendar.name
      ########################################################################
      J     =                      { "Id"      : CID                       , \
                                     "Name"    : NAME                        }
      self  . Calendars . append   ( J                                       )
    ##########################################################################
    return
  ############################################################################
  def FetchPeriodDetails              ( self                               ) :
    ##########################################################################
    if                                ( self . Period . Uuid <= 0          ) :
      return
    ##########################################################################
    DB       = self . ConnectDB       ( UsePure = True                       )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    VITEM    = Variables              (                                      )
    NITEM    = Notes                  (                                      )
    ##########################################################################
    VITEM    . Uuid = self . Period . Uuid
    VITEM    . Type = 196833
    ##########################################################################
    NITEM    . Uuid = self . Period . Uuid
    NITEM    . Name = "Description"
    ##########################################################################
    PRDTAB   = self . Tables          [ "Periods"                            ]
    NOXTAB   = self . Tables          [ "Notes"                              ]
    PAMTAB   = self . Tables          [ "Parameters"                         ]
    VARTAB   = self . Tables          [ "Variables"                          ]
    NAMTAB   = self . Tables          [ "NamesLocal"                         ]
    ##########################################################################
    self     . Period . ObtainsByUuid ( DB , PRDTAB                          )
    ##########################################################################
    Name     = self . GetName         ( DB , NAMTAB , self . Period . Uuid   )
    self     . Period . setProperties ( "Name"        , Name                 )
    ##########################################################################
    VITEM    . Name = "AppleCalendar"
    CID      = VITEM . GetValue       ( DB , VARTAB                          )
    if                                ( CID in [ False , None ]            ) :
      CID    = ""
    else                                                                     :
      CID    = self . assureString    ( CID                                  )
    self     . Period . setProperties ( "Calendar"    , CID                  )
    ##########################################################################
    VITEM    . Name = "AppleEvent"
    EID      = VITEM . GetValue       ( DB , VARTAB                          )
    if                                ( EID in [ False , None ]            ) :
      EID    = ""
    else                                                                     :
      EID    = self . assureString    ( EID                                  )
    self     . Period . setProperties ( "Event"       , EID                  )
    ##########################################################################
    NITEM    . ObtainsAll             ( DB , NOXTAB                          )
    DESC     = self . assureString    ( NITEM . Note                         )
    self     . Period . setProperties ( "Description" , DESC                 )
    ##########################################################################
    DB       . Close                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def loading                 ( self                                       ) :
    ##########################################################################
    self . GetAppleCalendars  (                                              )
    self . FetchPeriodDetails (                                              )
    ##########################################################################
    self . emitUpdate . emit  (                                              )
    self . emitApple  . emit  (                                              )
    self . emitShow   . emit  (                                              )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def startup                   ( self , Uuid                              ) :
    ##########################################################################
    self . Period . Uuid = int  ( Uuid                                       )
    self . PrepareDefaultValues (                                            )
    ##########################################################################
    self . Go                   ( self . loading                             )
    ##########################################################################
    return
##############################################################################

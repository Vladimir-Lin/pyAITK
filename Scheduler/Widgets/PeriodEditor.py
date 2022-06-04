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
from   PyQt5 . QtWidgets                   import QMessageBox
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
import icalendar
from   AITK  . Calendars  . Apple          import Apple          as DAV
##############################################################################
from         . PeriodEditorUI              import Ui_PeriodEditorUI
##############################################################################
class PeriodEditor                 ( Widget                                ) :
  ############################################################################
  emitShow            = pyqtSignal (                                         )
  emitApple           = pyqtSignal (                                         )
  emitEventId         = pyqtSignal (                                         )
  emitUpdate          = pyqtSignal (                                         )
  emitAskClose        = pyqtSignal (                                         )
  emitShowAppleEvents = pyqtSignal ( list                                    )
  emitOpenSmartNote   = pyqtSignal ( str                                     )
  emitAssignAppleBtn  = pyqtSignal ( bool                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ui = Ui_PeriodEditorUI  (                                         )
    self . ui . setupUi            ( self                                    )
    ##########################################################################
    self . ClassTag  = "PeriodEditor"
    self . VoiceJSON =             {                                         }
    self . Period    = Periode     (                                         )
    self . Now       = StarDate    (                                         )
    self . ContentChanged = False
    ##########################################################################
    self . Calendars =             [                                         ]
    ##########################################################################
    self . emitShow     . connect  ( self . show                             )
    self . emitApple    . connect  ( self . ShowAppleCalendars               )
    self . emitEventId  . connect  ( self . ShowAppleEventId                 )
    self . emitUpdate   . connect  ( self . UpdatePeriodValues               )
    self . emitAskClose . connect  ( self . AskToClose                       )
    self . emitShowAppleEvents . connect ( self . ShowAppleEvents            )
    self . emitAssignAppleBtn  . connect ( self . AssignAppleButton          )
    ##########################################################################
    self . ui . SaveNote . blockSignals  ( True                              )
    self . ui . SaveNote . setEnabled    ( False                             )
    self . ui . SaveNote . blockSignals  ( False                             )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                    ( self , event                         ) :
    ##########################################################################
    if                              ( self . ContentChanged                ) :
      ########################################################################
      event   . ignore              (                                        )
      self    . emitAskClose . emit (                                        )
      ########################################################################
      return
    ##########################################################################
    super ( ) . closeEvent          ( event                                  )
    ##########################################################################
    return
  ############################################################################
  def AssignAppleButton                ( self , enable                     ) :
    ##########################################################################
    self . ui . SyncApple . setEnabled (        enable                       )
    ##########################################################################
    return
  ############################################################################
  def AskToClose                  ( self                                   ) :
    ##########################################################################
    MSG  = self . getMenuItem     ( "ReallyQuit"                             )
    OKAY = QMessageBox . question ( self , self . windowTitle ( ) , MSG      )
    ##########################################################################
    if                            ( OKAY != QMessageBox . Yes              ) :
      return
    ##########################################################################
    self . ContentChanged = False
    self . close                  (                                          )
    ## self . close 這一行有問題
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
      ## self . ui . Append . hide     (                                        )
      pass
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
    self . Period . Type = TYPE
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
    self  . Period . Used = Usage
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
    TS   = self . ui . StartTime  . dateTime ( ) . toSecsSinceEpoch (        )
    self . Now . setTime         ( TS                                        )
    SDT  = self . Now . Stardate
    ##########################################################################
    if                           ( SDT == self . Period . Start            ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue ( "start" , SDT                             )
    self . Period . Start = SDT
    ##########################################################################
    return
  ############################################################################
  def FinishTimeChanged          ( self                                    ) :
    ##########################################################################
    TS   = self . ui . FinishTime . dateTime ( ) . toSecsSinceEpoch (        )
    self . Now . setTime         ( TS                                        )
    SDT  = self . Now . Stardate
    ##########################################################################
    if                           ( SDT == self . Period . End              ) :
      return
    ##########################################################################
    self . UpdatePeriodItemValue ( "end"   , SDT                             )
    self . Period . End = SDT
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
    self . Period . Item = Item
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
    self   . Period . States = States
    ##########################################################################
    return
  ############################################################################
  def NoteModified                    ( self                               ) :
    ##########################################################################
    self . ContentChanged = True
    self . ui . SaveNote . blockSignals  ( True                              )
    self . ui . SaveNote . setEnabled    ( True                              )
    self . ui . SaveNote . blockSignals  ( False                             )
    ##########################################################################
    return
  ############################################################################
  def NoteChanged                              ( self                      ) :
    ##########################################################################
    onote = self . Period . getProperty        ( "Description"               )
    note  = self . ui . NoteEdit . toPlainText (                             )
    ##########################################################################
    self  . ContentChanged = False
    ##########################################################################
    self  . ui . SaveNote . blockSignals       ( True                        )
    self  . ui . SaveNote . setEnabled         ( False                       )
    self  . ui . SaveNote . blockSignals       ( False                       )
    ##########################################################################
    if                                         ( onote == note             ) :
      return
    ##########################################################################
    self  . Go ( self . AssurePeriodNote , ( note , )                        )
    ##########################################################################
    return
  ############################################################################
  def AppendPeriod                           ( self                        ) :
    ##########################################################################
    CID  = self . GetCurrentCalendarId       (                               )
    if                                       ( len ( CID ) <= 0            ) :
      return
    ##########################################################################
    EID  = self . ui . AppleEventEdit . text (                               )
    if                                       ( len ( EID ) <= 0            ) :
      return
    ##########################################################################
    VAL  =                                   ( CID , EID ,                   )
    FUNC = self . ReportEventDetails
    self . Go                                ( FUNC , VAL                    )
    ##########################################################################
    return
  ############################################################################
  def ReportAll                              ( self                        ) :
    ##########################################################################
    CID  = self . GetCurrentCalendarId       (                               )
    if                                       ( len ( CID ) <= 0            ) :
      return
    ##########################################################################
    VAL  =                                   ( CID ,                         )
    FUNC = self . ReportCalendarDetails
    self . Go                                ( FUNC , VAL                    )
    ##########################################################################
    return
  ############################################################################
  def GetCurrentCalendarId ( self                                          ) :
    ##########################################################################
    calendarIndex = self . ui . AppleCalendarBox . currentIndex (            )
    if                     ( calendarIndex <= 0                            ) :
      self . Notify        ( 1                                               )
      return ""
    ##########################################################################
    CID           = self . ui . AppleCalendarBox . itemData ( calendarIndex  )
    if                     ( len ( CID ) <= 0                              ) :
      self . Notify        ( 1                                               )
      return ""
    ##########################################################################
    return str             ( CID                                             )
  ############################################################################
  def AppleCalendarChanged ( self , calendarIndex                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AppleEventCidChanged ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AssignStartTimeNow                  ( self                           ) :
    ##########################################################################
    self . Now  . Now                     (                                  )
    TS   = self . Now . Timestamp         (                                  )
    DT   = QDateTime . fromSecsSinceEpoch ( TS                               )
    self . ui . StartTime  . setDateTime  ( DT                               )
    self . StartTimeChanged               (                                  )
    ##########################################################################
    return
  ############################################################################
  def AssignFinishTimeNow                 ( self                           ) :
    ##########################################################################
    self . Now  . Now                     (                                  )
    TS   = self . Now . Timestamp         (                                  )
    DT   = QDateTime . fromSecsSinceEpoch ( TS                               )
    self . ui . FinishTime . setDateTime  ( DT                               )
    self . FinishTimeChanged              (                                  )
    ##########################################################################
    return
  ############################################################################
  def SyncToApple                              ( self                      ) :
    ##########################################################################
    CID    = self . GetCurrentCalendarId       (                             )
    if                                         ( len ( CID ) <= 0          ) :
      return
    ##########################################################################
    EID    = self . ui . AppleEventEdit . text (                             )
    if                                         ( len ( EID ) <= 0          ) :
      EID  = ""
    ##########################################################################
    NOTICE = self . ui . AlarmBox . value      (                             )
    ##########################################################################
    self   . emitAssignAppleBtn . emit         ( False                       )
    ##########################################################################
    VAL    =                                   ( CID , EID , - NOTICE        )
    FUNC   = self . SyncToAppleCalendar
    self   . Go                                ( FUNC , VAL                  )
    ##########################################################################
    return
  ############################################################################
  def SyncFromApple                          ( self                        ) :
    ##########################################################################
    CID  = self . GetCurrentCalendarId       (                               )
    if                                       ( len ( CID ) <= 0            ) :
      return
    ##########################################################################
    EID  = self . ui . AppleEventEdit . text (                               )
    if                                       ( len ( EID ) <= 0            ) :
      return
    ##########################################################################
    VAL  =                                   ( CID , EID ,                   )
    FUNC = self . SyncEventFromApple
    self . Go                                ( FUNC , VAL                    )
    ##########################################################################
    return
  ############################################################################
  def AssignAppleEvent                          ( self , index             ) :
    ##########################################################################
    EID  = self . ui . AppleEventBox . itemData ( index                      )
    EID  = str                                  ( EID                        )
    ##########################################################################
    self . ui . AppleEventEdit . blockSignals   ( True                       )
    self . ui . AppleEventEdit . setText        ( EID                        )
    self . ui . AppleEventEdit . blockSignals   ( False                      )
    ##########################################################################
    return
  ############################################################################
  def PullAppleEvents                  ( self                              ) :
    ##########################################################################
    CID  = self . GetCurrentCalendarId (                                     )
    if                                 ( len ( CID ) <= 0                  ) :
      return
    ##########################################################################
    self . ui . AppleEventBox . blockSignals ( True                          )
    self . ui . AppleEventBox . clear        (                               )
    self . ui . AppleEventBox . blockSignals ( False                         )
    self . Go                          ( self . GetAppleEvents , ( CID , )   )
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
    NOTE   . ObtainsLastest         ( DB , NOXTAB                            )
    NOTE   . Note   = note
    ##########################################################################
    DB     . LockWrites             ( [ NOXTAB                             ] )
    NOTE   . Editing                ( DB , NOXTAB                            )
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
  def ReportEventDetails             ( self , CalendarId , EventId         ) :
    ##########################################################################
    EVENT = self . GetEventFromApple (        CalendarId , EventId           )
    if ( type ( EVENT ) is not icalendar . cal . Calendar                  ) :
      self . Notify                  ( 1                                     )
      return
    ##########################################################################
    BODY  = self . assureString      ( EVENT . to_ical ( )                   )
    TEXT  = f"{CalendarId} {EventId}\n{BODY}"
    ##########################################################################
    self  . emitOpenSmartNote . emit ( TEXT                                  )
    ##########################################################################
    return
  ############################################################################
  def ReportCalendarDetails          ( self , CalendarId                   ) :
    ##########################################################################
    URL    = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"       ]
    DSID   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"      ]
    USER   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"  ]
    PASS   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"  ]
    ##########################################################################
    APPLE  = DAV                    ( URL , DSID , USER , PASS               )
    OKAY   = APPLE . FetchCalendars (                                        )
    ##########################################################################
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      return
    ##########################################################################
    CAL    = APPLE . FindCalendar   ( CalendarId                             )
    if                              ( CAL in [ False , None ]              ) :
      return
    ##########################################################################
    LISTS  =                        [                                        ]
    ##########################################################################
    for event in CAL . events              (                               ) :
      ########################################################################
      evt      = APPLE . EventFromICalData ( event . data                    )
      J        = APPLE . GetEventBrief     ( evt                             )
      ########################################################################
      if                                   ( J not in [ False , None ]     ) :
        ######################################################################
        PUID   = J                         [ "Period"                        ]
        ######################################################################
        if                                 ( len ( PUID ) <= 0             ) :
          ####################################################################
          L    = json . dumps              ( J                               )
          B    = self . assureString       ( event . data                    )
          LISTS . append                   ( f"{L}\n{B}\n"                   )
    ##########################################################################
    self  . emitOpenSmartNote . emit       ( "\n" . join ( LISTS )           )
    ##########################################################################
    return
  ############################################################################
  def SyncToAppleCalendar           ( self , CalendarId , EventId , NOTICE ) :
    ##########################################################################
    self   . Period . setProperties ( "Calendar" , CalendarId                )
    self   . Period . setProperties ( "Event"    , EventId                   )
    ##########################################################################
    URL    = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"       ]
    DSID   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"      ]
    USER   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"  ]
    PASS   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"  ]
    ##########################################################################
    APPLE  = DAV                    ( URL , DSID , USER , PASS               )
    OKAY   = APPLE . FetchCalendars (                                        )
    ##########################################################################
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      self . emitAssignAppleBtn . emit ( True                                )
      ########################################################################
      return
    ##########################################################################
    CAL    = APPLE . FindCalendar   ( CalendarId                             )
    if                              ( CAL in [ False , None ]              ) :
      self . emitAssignAppleBtn . emit ( True                                )
      ########################################################################
      return
    ##########################################################################
    if                              ( len ( EventId ) <= 0                 ) :
      ########################################################################
      E    = APPLE . iCalFromPeriod ( self . Period , NOTICE                 )
      try                                                                    :
        R  = CAL . add_event        ( ical = E . to_ical ( )                 )
      except                                                                 :
        self . Notify               ( 1                                      )
        self . emitAssignAppleBtn . emit ( True                              )
        return
      ########################################################################
      evt  = APPLE . EventFromICalData ( R . data                            )
      J    = APPLE . GetEventBrief  ( evt                                    )
      EID  = J                      [ "Id"                                   ]
      ########################################################################
      self . AssignAppleCalendarId  ( CalendarId , EID                       )
      self . emitEventId . emit     (                                        )
      self . Notify                 ( 5                                      )
      self . emitAssignAppleBtn . emit ( True                                )
      ########################################################################
      return
    ##########################################################################
    ## 更新舊事件資料
    ##########################################################################
    R      = APPLE . LocateEvent    ( CAL , EventId                          )
    ##########################################################################
    if                              ( R in [ False , None ]                ) :
      self . Notify                 ( 1                                      )
      self . emitAssignAppleBtn . emit ( True                                )
      return
    ##########################################################################
    evt    = APPLE . EventFromICalData    ( R . data                         )
    evt    = APPLE . iCalUpdateFromPeriod ( evt , self . Period , NOTICE     )
    R      . data = evt . to_ical   (                                        )
    R      . save                   (                                        )
    ##########################################################################
    self   . Notify                 ( 5                                      )
    self   . emitAssignAppleBtn . emit ( True                                )
    ##########################################################################
    return
  ############################################################################
  def ShowAppleEvents                          ( self , EVENTs             ) :
    ##########################################################################
    self   . ui . AppleEventBox . blockSignals ( True                        )
    self   . ui . AppleEventBox . clear        (                             )
    ##########################################################################
    msg    = self . getMenuItem                ( "Useless"                   )
    self   . ui . AppleEventBox . addItem      ( msg , ""                    )
    ##########################################################################
    for E in EVENTs                                                          :
      ########################################################################
      Id   = E                                 [ "Id"                        ]
      Name = E                                 [ "Name"                      ]
      self . ui . AppleEventBox . addItem      ( Name , Id                   )
    ##########################################################################
    self   . ui . AppleEventBox . blockSignals ( False                       )
    self   . Notify                            ( 5                           )
    ##########################################################################
    return
  ############################################################################
  def ShowAppleCalendars                             ( self                ) :
    ##########################################################################
    CID    = self . Period . getProperty             ( "Calendar" , ""       )
    EID    = self . Period . getProperty             ( "Event"    , ""       )
    ##########################################################################
    self   . ui . AppleCalendarBox . blockSignals    ( True                  )
    self   . ui . AppleEventEdit   . blockSignals    ( True                  )
    ##########################################################################
    self   . ui . AppleCalendarBox . clear           (                       )
    ##########################################################################
    msg    = self . getMenuItem                      ( "Useless"             )
    self   . ui . AppleCalendarBox . addItem         ( msg , ""              )
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
    self   . ui . AppleEventEdit   . setText         ( EID                   )
    ##########################################################################
    self   . ui . AppleEventEdit   . blockSignals    ( False                 )
    self   . ui . AppleCalendarBox . blockSignals    ( False                 )
    ##########################################################################
    return
  ############################################################################
  def ShowAppleEventId                        ( self                       ) :
    ##########################################################################
    EID  = self . Period . getProperty        ( "Event" , ""                 )
    ##########################################################################
    self . ui . AppleEventEdit . blockSignals ( True                         )
    self . ui . AppleEventEdit . setText      ( EID                          )
    self . ui . AppleEventEdit . blockSignals ( False                        )
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
  def GetEventFromApple             ( self , CalendarId , EventId          ) :
    ##########################################################################
    URL    = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"       ]
    DSID   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"      ]
    USER   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"  ]
    PASS   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"  ]
    ##########################################################################
    APPLE  = DAV                    ( URL , DSID , USER , PASS               )
    OKAY   = APPLE . FetchCalendars (                                        )
    ##########################################################################
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      return None
    ##########################################################################
    CAL    = APPLE . FindCalendar   ( CalendarId                             )
    if                              ( CAL in [ False , None ]              ) :
      return None
    ##########################################################################
    return APPLE . FindEvent        ( CAL , EventId                          )
  ############################################################################
  def InvestigateEvent                 ( self , PERIOD , EVENT             ) :
    ##########################################################################
    Changed = False
    BEGIN   = False
    ##########################################################################
    for key , value in EVENT . property_items (                            ) :
      ########################################################################
      K         = key . lower          (                                     )
      if                               ( BEGIN                             ) :
        ######################################################################
        if                             ( K in [ "end" ]                    ) :
          V     = self . assureString  ( value                               )
          V     = V . lower            (                                     )
          ####################################################################
          if                           ( V in [ "vevent" ]                 ) :
            BEGIN = False
        ######################################################################
        elif                           ( K in [ "summary" ]                ) :
          ####################################################################
          V     = self . assureString  ( str ( value )                       )
          N     = PERIOD . getProperty ( "Name"                              )
          if                           ( V != N                            ) :
            ##################################################################
            PERIOD . setProperties     ( "Name"        , V                   )
            Changed = True
        ######################################################################
        elif                           ( K in [ "description" ]            ) :
          ####################################################################
          V     = self . assureString  ( str ( value )                       )
          N     = PERIOD . getProperty ( "Description"                       )
          if                           ( V != N                            ) :
            ##################################################################
            PERIOD . setProperties     ( "Description" , V                   )
            Changed = True
        ######################################################################
        elif                           ( K in [ "dtstart" ]                ) :
          ####################################################################
          self . Now . fromDateTime    ( value . dt                          )
          SDT  = int                   ( self . Now . Stardate               )
          if                           ( PERIOD . Start != SDT             ) :
            PERIOD . Start = SDT
            Changed = True
        ######################################################################
        elif                           ( K in [ "dtend"   ]                ) :
          ####################################################################
          self . Now . fromDateTime    ( value . dt                          )
          SDT  = int                   ( self . Now . Stardate               )
          if                           ( PERIOD . End != SDT               ) :
            PERIOD . End = SDT
            Changed = True
        ######################################################################
      else                                                                   :
        ######################################################################
        if                             ( K in [ "begin" ]                  ) :
          ####################################################################
          V     = self . assureString  ( value                               )
          V     = V . lower            (                                     )
          ####################################################################
          if                           ( V in [ "vevent" ]                 ) :
            BEGIN = True
    ##########################################################################
    if                                 ( Changed                           ) :
      ########################################################################
      if                               ( PERIOD . Start < PERIOD . End     ) :
        ######################################################################
        PERIOD . Type = 4
      ########################################################################
      self . Now . Now                 (                                     )
      CDT  = int                       ( self . Now . Stardate               )
      ########################################################################
      if                               ( PERIOD . Start > CDT              ) :
        PERIOD . States = 3
      elif                             ( PERIOD . End   < CDT              ) :
        PERIOD . States = 4
      else                                                                   :
        PERIOD . States = 5
    ##########################################################################
    return Changed
  ############################################################################
  def SyncEventFromApple              ( self , CalendarId , EventId        ) :
    ##########################################################################
    EVENT  = self . GetEventFromApple (        CalendarId , EventId          )
    if ( type ( EVENT ) is not icalendar . cal . Calendar                  ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    CHANGED = self . InvestigateEvent ( self . Period , EVENT                )
    ##########################################################################
    if                                ( not CHANGED                        ) :
      self . Notify                   ( 5                                    )
      return
    ##########################################################################
    self . Period . setProperties     ( "Calendar" , CalendarId              )
    self . Period . setProperties     ( "Event"    , EventId                 )
    ##########################################################################
    self . UpdatePeriodDetails        (                                      )
    ##########################################################################
    self . emitUpdate . emit          (                                      )
    self . Notify                     ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def GetAppleEvents                ( self , CalendarId                    ) :
    ##########################################################################
    URL    = self . Settings        [ "Apple" ] [ "Calendar" ] [ "URL"       ]
    DSID   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "DSID"      ]
    USER   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Username"  ]
    PASS   = self . Settings        [ "Apple" ] [ "Calendar" ] [ "Password"  ]
    ##########################################################################
    APPLE  = DAV                    ( URL , DSID , USER , PASS               )
    OKAY   = APPLE . FetchCalendars (                                        )
    ##########################################################################
    if ( not OKAY ) or ( len ( APPLE . Calendars ) <= 0 )                    :
      ########################################################################
      return
    ##########################################################################
    CAL    = APPLE . FindCalendar   ( CalendarId                             )
    if                              ( CAL in [ False , None ]              ) :
      return
    ##########################################################################
    EVENTs = APPLE . GetEvents      ( CAL                                    )
    if                              ( len ( EVENTs ) <= 0                  ) :
      return
    ##########################################################################
    self . emitShowAppleEvents . emit ( EVENTs                               )
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
  def AssignAppleCalendarId           ( self , CalendarId , EventId        ) :
    ##########################################################################
    if                                ( self . Period . Uuid <= 0          ) :
      return
    ##########################################################################
    DB       = self . ConnectDB       ( UsePure = True                       )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    UUID     = int                    ( self . Period . Uuid                 )
    ##########################################################################
    VITEM    = Variables              (                                      )
    VITEM    . Uuid   = UUID
    VITEM    . Type   = 196833
    ##########################################################################
    VARTAB   = self . Tables          [ "Variables"                          ]
    ##########################################################################
    DB       . LockWrites             ( [ VARTAB                           ] )
    ##########################################################################
    VITEM    . Name  = "AppleCalendar"
    VITEM    . Value = CalendarId
    VITEM    . AssureValue            ( DB , VARTAB                          )
    ##########################################################################
    VITEM    . Name  = "AppleEvent"
    VITEM    . Value = EventId
    VITEM    . AssureValue            ( DB , VARTAB                          )
    ##########################################################################
    DB       . UnlockTables           (                                      )
    DB       . Close                  (                                      )
    ##########################################################################
    self     . Period . setProperties ( "Calendar" , CalendarId              )
    self     . Period . setProperties ( "Event"    , EventId                 )
    ##########################################################################
    return
  ############################################################################
  def UpdatePeriodDetails             ( self                               ) :
    ##########################################################################
    if                                ( self . Period . Uuid <= 0          ) :
      return
    ##########################################################################
    DB       = self . ConnectDB       ( UsePure = True                       )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    UUID     = int                    ( self . Period . Uuid                 )
    ##########################################################################
    VITEM    = Variables              (                                      )
    VITEM    . Uuid   = UUID
    VITEM    . Type   = 196833
    ##########################################################################
    NOTE     = Notes                  (                                      )
    NOTE     . Uuid   = UUID
    NOTE     . Name   = "Description"
    NOTE     . ObtainsLastest         ( DB , NOXTAB                          )
    ##########################################################################
    NOTE     . Note   = self . Period . getProperty ( "Description"          )
    ##########################################################################
    PRDTAB   = self . Tables          [ "Periods"                            ]
    NOXTAB   = self . Tables          [ "Notes"                              ]
    PAMTAB   = self . Tables          [ "Parameters"                         ]
    VARTAB   = self . Tables          [ "Variables"                          ]
    NAMTAB   = self . Tables          [ "NamesLocal"                         ]
    ##########################################################################
    DB       . LockWrites             ( [ PRDTAB                           , \
                                          NOXTAB                           , \
                                          PAMTAB                           , \
                                          VARTAB                           , \
                                          NAMTAB                           ] )
    ##########################################################################
    ITEMs    =                        [ "type" , "states" , "start" , "end"  ]
    self     . Period . UpdateItems   ( DB , PRDTAB , ITEMs                  )
    ##########################################################################
    Name     = self . Period . getProperty ( "Name"                          )
    self     . AssureUuidName         ( DB , NAMTAB , UUID , Name            )
    ##########################################################################
    NOTE     . Editing                ( DB , NOXTAB                          )
    ##########################################################################
    VITEM    . Name  = "AppleCalendar"
    VITEM    . Value = self . Period . getProperty ( "Calendar"              )
    VITEM    . AssureValue            ( DB , VARTAB                          )
    ##########################################################################
    VITEM    . Name  = "AppleEvent"
    VITEM    . Value = self . Period . getProperty ( "Event"                 )
    VITEM    . AssureValue            ( DB , VARTAB                          )
    ##########################################################################
    DB       . UnlockTables           (                                      )
    DB       . Close                  (                                      )
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
    DESC     = f"{DESC}"
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
